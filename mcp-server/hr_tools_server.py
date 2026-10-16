"""Demo read-only HR tools as an MCP server.

Data: bundled CSVs in ./data (fake people). Every tool takes a `role` and an
optional `branches` scope; scope is enforced here, in the tool, not in the prompt.

Run:  python hr_tools_server.py           (stdio transport, for Claude Code / Desktop)
"""
from __future__ import annotations

import csv
from datetime import date
from pathlib import Path

try:  # mcp >= 2
    from mcp.server.mcpserver import MCPServer as FastMCP
except ImportError:  # mcp 1.x
    from mcp.server.fastmcp import FastMCP

DATA = Path(__file__).parent / "data"
ROLES = {"guest": 0, "employee": 1, "manager": 2, "hr_head": 3, "owner": 4}
PAYROLL_ROLES = {"hr_head", "owner"}

mcp = FastMCP("hr-tools-demo")


def _load(name: str) -> list[dict]:
    with open(DATA / f"{name}.csv", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def _require(role: str, minimum: str) -> None:
    if ROLES.get(role, 0) < ROLES[minimum]:
        raise PermissionError(f"role '{role}' is below '{minimum}'")


def _scope(rows: list[dict], role: str, branches: str | None) -> list[dict]:
    """Managers must pass their branches; hr_head/owner see all unless they narrow it."""
    allowed = {b.strip() for b in branches.split(",")} if branches else None
    if role == "manager" and not allowed:
        raise PermissionError("manager needs a branch scope")
    return [r for r in rows if allowed is None or r["branch"] in allowed]


def _employees(role: str, branches: str | None) -> list[dict]:
    return _scope(_load("employees"), role, branches)


def _norm(s: str) -> str:
    return s.lower().replace("x", "h").replace("'", "")


@mcp.tool()
def search_employee(query: str, role: str, branches: str | None = None) -> list[dict]:
    """Find employees by name or position (max 8). Role: manager+."""
    _require(role, "manager")
    q = _norm(query)
    hits = [e for e in _employees(role, branches)
            if q in _norm(e["name"]) or q in _norm(e["position"])]
    fields = ("id", "name", "position", "branch", "region", "hire_date", "status")
    return [{k: e[k] for k in fields} for e in hits[:8]]


@mcp.tool()
def attendance_today(role: str, branches: str | None = None, day: str | None = None) -> dict:
    """Attendance for a day by branch. 'not_checked_in' is NOT 'absent'. Role: manager+."""
    _require(role, "manager")
    emps = {e["id"]: e for e in _employees(role, branches) if e["status"] != "dismissed"}
    rows = _load("attendance")
    day = day or max(r["date"] for r in rows)
    events = {r["employee_id"]: r for r in rows if r["date"] == day}
    by_branch: dict[str, dict] = {}
    for eid, e in emps.items():
        b = by_branch.setdefault(e["branch"], {"total": 0, "present": 0, "late": 0,
                                               "absent": 0, "not_checked_in": 0, "conflicts": 0})
        b["total"] += 1
        ev = events.get(eid, {})
        lead = ev.get("lead_report", "")
        checked_in = bool(ev.get("check_in"))
        if lead == "absent":
            b["absent"] += 1
            if checked_in:
                b["conflicts"] += 1
        elif lead.startswith("present") or checked_in:
            b["present"] += 1
            if checked_in and ev["check_in"] > "09:00" and not lead:
                b["late"] += 1
        else:
            b["not_checked_in"] += 1
    return {"date": day, "branches": by_branch,
            "note": "not_checked_in does not mean absent"}


@mcp.tool()
def turnover(role: str, months: int = 3, branches: str | None = None,
             as_of: str = "2026-10-17") -> dict:
    """Leavers in the last N months with base. Small groups return counts only. Role: manager+."""
    _require(role, "manager")
    end = date.fromisoformat(as_of)
    y, m = divmod(end.year * 12 + end.month - 1 - months, 12)
    start = date(y, m + 1, min(end.day, 28))
    out = {}
    for e in _employees(role, branches):
        b = out.setdefault(e["branch"], {"base": 0, "left": 0, "left_within_30d": 0})
        hired = date.fromisoformat(e["hire_date"])
        gone = date.fromisoformat(e["dismiss_date"]) if e["dismiss_date"] else None
        if hired <= end and (gone is None or gone >= start):
            b["base"] += 1
        if gone and start <= gone <= end:
            b["left"] += 1
            if (gone - hired).days <= 30:
                b["left_within_30d"] += 1
    for b in out.values():
        if b["base"] >= 10:
            b["pct"] = round(100 * b["left"] / b["base"], 1)
        else:
            b["pct"] = None
            b["note"] = "fewer than 10 people: counts only" + (
                "; a percentage would be unreliable" if b["base"] <= 3 else "")
    return {"period": f"{start}..{end}", "by_branch": out}


@mcp.tool()
def payroll_precheck(role: str, month: str = "2026-09", branches: str | None = None,
                     overtime_limit: float = 40) -> dict:
    """Pre-payout issues with amount at risk. Unknown = None, never 0. Role: hr_head+."""
    if role not in PAYROLL_ROLES:
        return {"error": "Payroll data is outside your permissions. Please contact the HR lead."}
    emps = {e["id"]: e for e in _employees(role, branches)}
    issues = []
    for p in _load("payroll"):
        e = emps.get(p["employee_id"])
        if not e or p["month"] != month:
            continue
        base = float(e["base_salary"]) if e["base_salary"] else None
        norm = float(p["norm_hours"])
        rate = base / norm if base else None

        def add(code: str, risk: float | None, detail: str):
            issues.append({"employee": e["name"], "branch": e["branch"], "code": code,
                           "amount_at_risk": round(risk) if risk is not None else None,
                           "detail": detail})

        if not p["worked_hours"]:
            add("NO_HOURS", None, "contract exists but no attendance data")
            continue
        if int(p["missing_checkouts"]):
            add("MISSING_CHECKOUT", rate * 8 * int(p["missing_checkouts"]) if rate else None,
                f"{p['missing_checkouts']} day(s) need review")
        if int(p["missed_shifts"]):
            add("MISSED_SHIFT", rate * 12 * int(p["missed_shifts"]) if rate else None,
                f"{p['missed_shifts']} scheduled shift(s) without attendance or leave")
        if float(p["manual_bonus"] or 0) > 0 and not p["bonus_reason"]:
            add("BONUS_NO_BASIS", float(p["manual_bonus"]), "manual bonus without a reason")
        ot = float(p["overtime_hours"] or 0)
        if ot > overtime_limit:
            add("OVERTIME_LIMIT", rate * (ot - overtime_limit) if rate else None,
                f"{ot:g} h > limit {overtime_limit:g} h (check limit for 24h schedules)")
    known = [i["amount_at_risk"] for i in issues if i["amount_at_risk"] is not None]
    return {"month": month, "status": "calculated, not approved", "issues": issues,
            "total_at_risk": sum(known),
            "unknown_amounts": sum(1 for i in issues if i["amount_at_risk"] is None),
            "note": "Read-only check. Approval is a human decision."}


if __name__ == "__main__":
    mcp.run()

# hr-tools-demo MCP server

A small MCP server that exposes read-only HR tools over bundled CSV demo data. All people in it are fake. It shows the two rules every HR tool should follow:

- **Scope is enforced inside the tool.** A `manager` must pass `branches`, and the tool filters rows. `payroll_precheck` refuses anyone below `hr_head`.
- **Unknown is not zero.** Missing amounts come back as `null`. "Not checked in" is reported separately from "absent".

| Tool | Min role | Returns |
|---|---|---|
| `search_employee(query, role, branches?)` | manager | up to 8 matches |
| `attendance_today(role, branches?, day?)` | manager | present / late / absent / not checked in / conflicts per branch |
| `turnover(role, months=3, branches?, as_of?)` | manager | base, leavers, early leavers; `pct` only for groups ≥ 10 |
| `payroll_precheck(role, month, branches?, overtime_limit=40)` | hr_head | issues with amount at risk |

## Run

```bash
python -m venv .venv
.venv/Scripts/pip install -r requirements.txt   # Windows (macOS/Linux: .venv/bin/pip)
.venv/Scripts/python smoke_test.py
```

Add it to Claude Code:

```bash
claude mcp add hr-tools-demo -- /abs/path/mcp-server/.venv/Scripts/python /abs/path/mcp-server/hr_tools_server.py
```

> In production the role comes from the authenticated user (e.g. a verified Telegram ID), not from a tool argument. Here it's an argument only to keep the demo simple.

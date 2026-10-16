"""Smoke test: import the server and call each tool directly."""
import json

import hr_tools_server as s

print(json.dumps(s.search_employee("pharm", role="manager", branches="Branch-01"), indent=1))
print(json.dumps(s.attendance_today(role="hr_head"), indent=1))
print(json.dumps(s.turnover(role="owner", months=3), indent=1))
print(json.dumps(s.payroll_precheck(role="hr_head"), indent=1))
assert "error" in s.payroll_precheck(role="manager", branches="Branch-01")
try:
    s.search_employee("a", role="manager")
    raise SystemExit("FAIL: manager without scope must be refused")
except PermissionError:
    pass
try:
    s.attendance_today(role="employee")
    raise SystemExit("FAIL: employee must be refused")
except PermissionError:
    pass
print("SMOKE OK")

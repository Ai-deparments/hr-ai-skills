---
name: payroll-precheck
description: Check a month's payroll before payout and report problems with the amount that could be paid incorrectly. Use for "payroll check", "проверь зарплату", "перед выплатой", "oylik tekshir", "oylikni tekshirib ber", overtime limits, missed shifts, bonuses without a basis. Read-only — never calculates the final payroll, approves, pays, or edits attendance.
---

# Payroll pre-check

The HR panel calculates payroll: attendance → timesheet → formula → **a human approves**. This skill checks that chain and lists what could be paid wrong.

## Reference formula (what you check against)

```
accrued     = base_salary × (worked_hours + paid_absence_hours) / norm_hours
kpi_bonus   = base_salary × kpi_score / 100      # kpi factor 0 … 1.2
manual      = manual bonus (reason required)
penalties   = late penalty + other penalties (reason required)
to_pay      = accrued + kpi_bonus + manual + allowances − advances − penalties − deductions
```

- `norm_hours` comes only from the working calendar or the shift schedule.
- Taxes are not calculated unless the company config says so. The amount is "net to hand".
- Every amount keeps its formula and inputs, so you can always say where a number came from.

## Checks

| Code | Issue | Amount at risk |
|---|---|---|
| `NO_CONTRACT` | Employee has hours but no contract / base salary | — (cannot calculate) |
| `NO_HOURS` | Employee has a contract but no attendance data | — |
| `NO_POSITION` | Not in the staffing table | — |
| `MISSING_CHECKOUT` | Day with check-in but no check-out | hours × hourly rate |
| `MISSED_SHIFT` | Scheduled shift with no attendance and no leave | hourly rate × shift hours |
| `BONUS_NO_BASIS` | Manual bonus or % of sales without a source or reason | full bonus |
| `OVERTIME_LIMIT` | Overtime > limit for the period (default 40 h; set separately for 24h schedules) | overtime × rate |
| `DOUBLE_PENALTY` | Manual late penalty on a day that already has an automatic one | penalty |
| `CHANGED_AFTER_CALC` | Data edited after calculation, so it can't be approved | — |

## Rules

- **Unknown is `—`, never 0.** A day with no data is "unknown". A missing check-out is "needs review". Never fill in 8 hours.
- Don't mark an absence as "unexcused" yourself. Only the team lead confirms that.
- Never approve, deduct, change a contract or pay. If asked, create an approval request (see `human-in-the-loop-guard`).
- Salary data only for roles with `payroll.read`. Everyone else gets one line: *"Payroll data is outside your permissions. Please contact the HR lead."*
- Amounts in UZS (or the configured currency), times in the company time zone.

## Output

```
💰 Payroll pre-check — 2026-09 (calculated, not approved)
Employees checked: 142 · Issues: 7 · At risk: 3,420,000 UZS

🔴 MISSED_SHIFT  · Branch #4 · 2 people · 1,150,000 UZS
🔴 BONUS_NO_BASIS · Branch #9 · 1 person · 1,500,000 UZS
🟡 MISSING_CHECKOUT · 3 days · 770,000 UZS
⚪ NO_CONTRACT · 1 person · —

Next: HR fixes the source data → recalc → human approves.
```

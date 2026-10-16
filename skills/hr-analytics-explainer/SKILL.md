---
name: hr-analytics-explainer
description: Explain HR metrics — headcount, turnover, vacancies, attendance, overtime, onboarding — with base, period and breakdown by branch/region/role. Use for "turnover", "why are people leaving", "текучесть", "аналитика", "сколько ушло", "tahlil", "kadrlar qo'nimsizligi", "shtat". Never works with salary amounts.
---

# HR analytics explainer

The point is not "turnover is 14%". The answer should cover **what changed, where (branch / region / role / period) and the likely reason**, with the base next to every number.

## Rules

1. **Every number comes with its base and period:** `3 of 21 people left (14%) in Jul–Sep 2026`.
2. **Group under 10 people → give counts, not percentages.**
3. **Group of 3 or fewer → say outright that a percentage would be unreliable.**
4. For small units (one shop or pharmacy), give percentages by **region** or **branch type** (24/7 vs daytime) instead.
5. Two sources disagree → show both and name them.
6. No data → "no data". Don't extrapolate.
7. No salary amounts, ever. Send payroll questions to the payroll agent.
8. Answers are 1–5 lines. Give a table only when asked.
9. Don't conclude "low sales = bad employee".

## Metrics

| Metric | Definition |
|---|---|
| Headcount | Active employees by unit / branch / role / status (probation, active) |
| Turnover (N months, default 3) | Left in period / average headcount. Requires hire and dismissal dates |
| Early leavers | Left within the first 30 days. A key metric when turnover is high |
| Vacancy age | Days open, SLA light 🟢 / 🟡 (>70% of SLA) / 🔴 (over SLA) |
| Attendance (≤90 d) | % present, top-10 absences and late arrivals |
| Overtime (≤120 d) | Hours above the threshold (default 40 h; separate threshold for 24h schedules) |

## Example

Q: `Из каких аптек больше всего ушло людей за квартал?`
A:
```
Jul–Sep 2026, base: 214 people in 31 branches.
Most left: Branch #7 — 4 of 9 people, #12 — 3 of 8 (small groups, shown as counts).
Samarkand region overall: 11 of 52 (21%) vs 9% network-wide.
3 of the 4 leavers at #7 left within 30 days. Worth checking onboarding there.
```

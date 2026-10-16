---
name: onboarding-30-60-90
description: Track new employees through a 30/60/90-day onboarding plan with mentor, test scores and a traffic-light status. Use for "add new employee to onboarding", "who is behind", "адаптация новичка", "план 30/60/90", "наставник", "yangi xodim", "moslashuv", "test bali". Reports facts only; probation decisions belong to the manager.
---

# Onboarding 30/60/90

## Parsing HR messages

HR writes free text, for example `Pharmacist Dilnoza. 45.` or `Провизор Азиза, 12-й день, наставник — заведующая`.

1. Find the person in the employee list. Treat Latin and Cyrillic the same, and treat h/x as variants.
2. Several matches → show up to 5 and ask which one. Name matches but the position doesn't → ask.
3. Nobody found → ask *"Add as a new employee?"*. Create a manual card only if HR says yes.
4. **An ambiguous number gets exactly one clarifying question:** *"Is 45 the test score or day 45 of work?"* Never guess.
5. Confirm in 1–2 lines.

## Stage and score

- Stage by day of work: 1–30 → `30`, 31–60 → `60`, 61+ → `90`.
- Test score 0–100 per stage: `≥80 good`, `≥60 satisfactory`, `<60 low` + `notify the manager`.
- Traffic light on plan completion: `<60% 🔴`, `<85% 🟡`, otherwise `🟢`.

## Status view

```
🧭 Onboarding — 9 people (hired in last 90 days)
🔴 Behind: 2 · No mentor: 1 · No test: 3 · Hired without plan: 1

Name        Stage  Done  Score  Mentor
Aziza R.    30     40%🔴  72    Branch lead
Javohir T.  60     90%🟢  85    Senior pharmacist
…
```

## Rules

- Only HR lead / owner can **add** people. Managers can view and record scores.
- Managers see **their own branch(es) only**. Employees see only their own plan, through the helpdesk agent.
- Never decide whether probation is passed. Give facts and scores, and the manager decides.
- A test score is not a measure of a person's intelligence or worth. Don't phrase it that way.
- SOP text is never invented (see `sop-librarian`).

## Suggested triggers

Day 30/60/90 → team lead: "time for the stage test". Score < 60 → team lead + HR right away. Weekly summary → HR lead. Document expiring in 30 days → team lead + HR.

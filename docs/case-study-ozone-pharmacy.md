# Case study: Ozone (pharmacy chain), adapting the system

Moving the factory system to a pharmacy chain showed which parts were generic and which were built only for the factory.

| Factory assumption | Pharmacy reality | Adaptation |
|---|---|---|
| Department / crew | **Pharmacy = branch**, pharmacy head = team lead, region = group of pharmacies | Branch scope for regional managers |
| Turnstiles, face terminals | Usually none | `ATTENDANCE_SOURCE=telegram`: Mini App check-in, checked against the pharmacy head's report |
| 09:00–18:00, six-day week | **24/48, 24/72, 2/2**, pharmacies open 24/7 | Shift schedules, overnight shift counted on the start day, norm per schedule, separate overtime limit |
| Base + KPI | **Base + % of sales** / plan bonus | Manual bonus with a reason first, then a feed from the POS/ERP |
| Factory SOPs | Dispensing, cold chain, cash discipline, pharmacovigilance | One SOP library with upload from file |
| — | **Diplomas, pharmacist certificates, medical books, check-ups** expire | New module for documents and expiry reminders |
| "Mark everyone present" button | In 24/7 pharmacies only one shift is on duty | Hide the button for shift-based branches |
| Lookup "department → name" | Many pharmacies | Lookup "pharmacy → name" |

## Security checklist used before a pilot

General patterns worth checking in any multi-branch HR agent system:

1. **Scope every summary, not just search.** Branch restrictions must apply to aggregates (attendance, onboarding, analytics) too.
2. **Self-service tools take no "person" argument.** "My plan" must resolve the user from their identity, not from a name in the prompt.
3. **Account linking needs proof.** Never link a chat to an employee ID that was simply typed in. Require a phone match or HR confirmation.
4. **Every web surface needs auth.** Internal dashboards go behind login, a proxy password or an IP allow-list.
5. **One token per agent with least privilege.** Shared tokens hide permission bugs and make audits useless.

## Pilot design

- 2–3 pharmacies, one of them open 24/7.
- Two weeks of attendance, helpdesk and onboarding.
- One month of payroll in parallel with the old sheet.
- 1–2 pharmacist vacancies, with the ads agent in manual mode.
- 20–30 real analytics questions, with the answers checked by hand.

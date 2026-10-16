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

## Security holes found in the review

These must be closed before the pilot.

1. Pharmacy heads saw network-wide attendance and onboarding summaries in the bots. Scope was applied only to employee search.
2. The helpdesk could return a colleague's onboarding plan by name. Only the prompt forbade it.
3. A simplified panel bot linked a chat to any employee number someone typed in, without checking it.
4. The recruiter's web dashboard had no authentication of its own. It has to sit behind a password or an IP allow-list.
5. The payroll agent used another agent's panel token without `payroll.read`, so it only ever saw demo data.

## Pilot design

- 2–3 pharmacies, one of them open 24/7.
- Two weeks of attendance, helpdesk and onboarding.
- One month of payroll in parallel with the old sheet.
- 1–2 pharmacist vacancies, with the ads agent in manual mode.
- 20–30 real analytics questions, with the answers checked by hand.

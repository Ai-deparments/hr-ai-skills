---
name: hr-rollout-playbook
description: Plan and run the rollout of the multi-agent HR system to a new company (white-label) — phases 0–6, client data checklist, adaptation checklist, pilot design. Use for "deploy HR agents for a new client", "адаптация под компанию", "план запуска", "pilot", "yangi kompaniyaga moslash", "ishga tushirish rejasi".
---

# HR rollout playbook

## Phases

| Phase | Goal | Exit criteria |
|---|---|---|
| 0. Data & decisions | Client answers the questionnaire, sends reference data, bot tokens, server + domain | Checklist below is ≥90% done |
| 1. Separate install | Own DB, panel, agents, bots on a 24/7 server, client brand, demo data removed | Health check is green, no other client's data |
| 2. Reference data | Branches, regions, employees, positions, team leads by phone, roles, schedules, calendar | Import report has no unmatched rows |
| 3. Pre-pilot gaps | Overnight shifts, branch scope in bots, real payroll data, approval screen, self-only checks | Golden-question evals pass |
| 4. Pilot | 2–3 branches (include one 24/7), 2 weeks of attendance; 1 month of payroll run in parallel with the old process | Numbers reconcile with the old process |
| 5. Full network | Remaining branches, `/id` linking, short guides for team leads and the accountant | ≥95% of employees linked |
| 6. On request | % of sales from POS/ERP, documents & training, geolocation, night rates, more languages | — |

## White-label adaptation checklist

- [ ] **Branding in config**, not code: company name, description, slogan, logo, colors, HR phone, form URL, bot names
- [ ] **Branch = site** (pharmacy / store / plant). Team lead = head of that branch. Region = group of branches
- [ ] **Attendance source:** turnstile / face terminal / `telegram` (Mini App + team-lead report)
- [ ] **Shifts:** 5/2, 2/2, 24/48, 24/72, overnight; norm hours **per schedule**; overtime threshold per schedule
- [ ] **Pay scheme:** base, hourly, daily; KPI; % of sales (manual bonus with reason → later POS/ERP feed); late-penalty rule or none; night/holiday rates
- [ ] **Roles:** owner, hr_head, payroll, manager (regional), team_lead, recruiter, employee; who must not see salaries
- [ ] **Branch scope** enforced in every agent tool, not only in the panel
- [ ] **Remove the previous client's rules:** working-week changes, special pay days, turnstile assumptions, crews
- [ ] **Language:** UI, reports, voice
- [ ] **Documents with expiry** (diplomas, certificates, medical book) and mandatory training, if the industry needs them
- [ ] **Consent:** voice and CVs sent to external cloud services; data-retention rules from the client's lawyer

## Client questionnaire (condensed)

**Sites & people:** list of branches (code, address, city, region, 24/7 or day), regional managers, employee list (name, phone, position, branch, hire date, status, manager, pay type), one job-title dictionary, staffing table, 12–24 months of dismissals, current HR system and whether it can export.
**Schedules:** schedule types per branch, shift start/end, breaks, norm hours, production calendar, late threshold and penalties, smartphone/Telegram coverage, report recipients and times.
**Payroll:** contracts and allowances, bonus scheme, POS/ERP API, penalties, night/holiday/overtime rules, advance and payday dates, taxes or net only, 1–2 past payroll sheets for reconciliation, who approves.
**Onboarding:** SOPs per role, 30/60/90 plans, tests and pass mark, mentors, mandatory training, document expiries, leave balances, who approves requests.
**Hiring:** open vacancies, requirements per role, SLA per role, job boards and keys, own channels, ad budget, who approves > threshold, brand assets, candidate data retention.
**Tech:** existing bots, new bot tokens (created by the owner), Telegram IDs per role, panel users, server + permanent HTTPS domain, voice keys.

## Pilot design

- 2–3 branches, at least one running 24/7.
- Attendance + team-lead report + helpdesk + onboarding: 2 weeks.
- Payroll: one full month in parallel with the old sheet, reconciled line by line.
- Recruiting & ads: 1–2 vacancies in 1–2 cities, auto mode **off**.
- Analytics: 20–30 real questions from the HR director, numbers checked by hand → turn them into golden evals.

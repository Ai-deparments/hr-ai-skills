# Architecture

## Components

| Component | Users | Purpose |
|---|---|---|
| **Hamza** (HR lead + attendance) | Owner, HR director, team leads, regional managers | One HR entry point for management. 09:00 / 18:30 attendance reports, monthly timesheet Excel. Hosts the check-in Mini App |
| **Ozoda** (onboarding) | HR lead, team leads | 30/60/90 plans, mentor, test scores, SOPs, who is behind |
| **Bexruz** (payroll pre-check) | Owner, HR lead, accountant | Finds missed shifts, bonuses without a basis, overtime, and the amount at risk. Never approves |
| **Husayn** (analytics) | Owner, HR lead, managers; Hamza | Explains turnover, vacancies and attendance by branch / region / role, with base and period |
| **Suhayl** (employee helpdesk) | Every employee | My shift, leave balance, request status, rules, my plan. Files requests. Understands voice |
| **Rauf** (recruiter) | Candidates; HR | Vacancy drafts, job-board publishing, Telegram interview, 4-criteria scoring, shortlist, SLA |
| **Rauf recruiter panel** (`/rauf`) | Recruiters, HR | Rauf's own web panel: funnel and KPI (open vacancies, avg score, days to close, SLA lights), kanban pipeline, vacancies and candidates, CV archive, channel-ad deals, integration status. Cut by branch scope |
| **Rauf HR Mini App** (`/m/rauf`) | HR (owner / HR-head Telegram IDs only) | Candidates with scores and Shortlist / Hired / Reject buttons inside Rauf's bot; a person makes every decision |
| **Ads agent** | HR director, recruiters | Finds job channels, negotiates within budget, collects payment details. A human pays |
| **Web HR panel** | HR, accountant, management, regional managers, recruiter | Employees, attendance, timesheet, payroll, requests, candidates, agent conversations, branch access |
| **Team-lead cabinet** (Mini App) | Branch heads, regional managers, HR | Present/absent + hours (up to 24 h), month view, advance / penalty / bonus / warning with a reason |

## Data flow

```
Ads agent ──(channel posts)──┐
                             ▼
HR opens vacancy ──► Rauf: publish, interview, score, shortlist
                             │  "hired" is a human decision
                             ▼
                HR panel: employee card (branch, position)
                             ▼
                Ozoda: 30/60/90 plan, mentor, tests
                             │
Suhayl ◄── employee asks about plan, shift, leave, rules; files request
                             ▼
Daily: employee "Check in / Check out" (Mini App) + team lead "Present / Absent" + hours
                             ▼
HR panel: attendance → timesheet (HR closes the month)
Hamza: 09:00 + 18:30 reports, timesheet Excel at month end
                             ▼
HR panel: payroll is calculated, a human approves
Bexruz: pre-payout check
                             ▼
Husayn: turnover, vacancies, attendance by branch / region
                             ▼
Hamza: management summary (asks up to 3 agents)
```

**Day source priority:** HR edit > HR leave / sick leave > team-lead report > self check-in / turnstile.

## Runtime

- The model is Claude. The agent loop only gets **the tools allowed for the caller's role**.
- Tools call the HR panel's agent API with a **per-agent token**. Tokens are read-only, and only the payroll agent has payroll scope.
- A local SQLite / Postgres DB stores conversations (last 10–12 turns), the audit log and agent-specific tables.
- Scheduled reports are rendered by code, with no model, so they look the same every day.
- Roles: `owner > hr_head > manager > employee > guest`. A role is resolved from the Telegram ID plus job-title keywords. A dismissed employee becomes a guest.

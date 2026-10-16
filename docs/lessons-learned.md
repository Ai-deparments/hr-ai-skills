# Lessons learned and what the next generation does differently

1. **One company config instead of hard-coded branding.** `company.yaml` holds the name, description, branches, regions, positions, schedules, pay rules, contacts and colors. A new client is a config change, not a fork.
2. **One database instead of an hourly copy.** Syncing the employee list between the panel and the agents lost hire dates, branches, leave balances and managers. When every agent reads the same DB through a scoped service layer, that whole class of bugs goes away.
3. **Scope enforced in tools, not prompts.** Every tool gets the caller's identity and filters by branch. A prompt can be talked around. Code can't.
4. **One token per agent, least privilege.** Only the payroll agent has payroll scope. No agent token can perform any of the 7 human-only decisions.
5. **An approval queue built in from the start.** Leave, payroll approval, broadcasts and hires all become an `ApprovalRequest` with Telegram buttons, a dashboard inbox, a required reason and an audit entry. Approved leave goes into the timesheet automatically.
6. **A notification scheduler.** Payday in 2 days, overtime over the limit, 3 missed shifts in a row, day 30/60/90, test score under 60, a document expiring in 30 days. Triggers are code, not prompts.
7. **Golden-question evals.** The 20–30 pilot questions become a regression suite for each agent and run in CI.
8. **One SOP library**, with file upload, versions, and a notice to the affected roles when something changes.
9. **The shift engine comes first.** Overnight shifts, 24-hour shifts and norm hours per schedule are the hardest part of attendance, so test them before anything else.
10. **One bot can host many agents.** A router in front of the personas means fewer bot tokens for the client to create and one place for authentication.

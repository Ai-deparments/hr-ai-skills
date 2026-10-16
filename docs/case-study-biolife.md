# Case study: BioLife (drinking-water factory)

The system first ran in production at BioLife under the name **NOVA-KIT**.

**Context:** a factory with production crews, a warehouse, sales reps and branches. Many line workers have no smartphone.

## What was built

- Turnstiles and face-recognition terminals as the main attendance source. Agents can only read them.
- The **team-lead cabinet**, because many workers had no phone. Crew leaders mark "present / absent" and hours for their people.
- A fixed-format 09:00 / 18:30 attendance report with Excel and the line "not checked in ≠ absent".
- A payroll engine in the panel: base × (worked + paid absence) / norm, KPI 0–1.2, manual entries with a reason. Statuses go draft → calculated → approved → paid → closed.
- 7 agents on Claude, each with its own Telegram bot and role-filtered tools, plus a full audit log.

## What worked

- Reports built by code. Management trusts numbers that can't be hallucinated.
- "Unknown = —, not 0" and "missing check-out = needs review" stopped silent 8-hour fills.
- A safety rule for syncing: if more than 20% of employees disappear in one sync, nobody is marked as dismissed and a warning goes out.

## What hurt

These are fixed in the next generation, see [lessons-learned](lessons-learned.md).

- The company name was hard-coded in personas, templates and banners (~15 files).
- The employee list was copied every hour between two databases, and some fields got lost on the way.
- Several agents shared one panel token.
- Branch scope existed in the panel but not in the bots.

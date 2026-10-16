---
name: attendance-report
description: Build the daily attendance reports (morning and end-of-day) and monthly timesheet summaries from check-in events and team-lead reports. Use for "attendance report", "who is late", "отчёт посещаемости", "кто опоздал", "davomat", "kim kechikdi", "hisobot", "tabel". The report format is deterministic; "not checked in" is never reported as "absent".
---

# Attendance report

Scheduled reports are **built by code, not by the model**: same format, same time, every day. The model is only used for free-text questions on top.

## Day calculation

**Source priority** (highest wins):
1. HR manual edit (reason required, logged)
2. Leave / sick leave entered by HR
3. Team-lead report: `present` + hours (0.5–24) or `absent`
4. Self check-in (Mini App "Check in / Check out") or turnstile / face terminal

Rules:
- Team lead says `absent` but there is a check-in → **conflict**, goes to HR for review.
- Check-in with no check-out → `needs review`. **Never fill in 8 hours.**
- No source → `unknown` (`—`), never 0.
- Overnight shift (08:00 → 08:00 next day) belongs to the **start day**.
- Late = after schedule start + grace minutes for that employee's schedule.

## Morning report (e.g. 09:00)

```
🌅 MORNING ATTENDANCE — 17.10.2026
Total: 120 · Present: 96 (80%) · Late: 7 · Not checked in: 17

By branch:
Branch #1  ████████░░ 8/10
Branch #2  ██████████ 6/6
…
Late: A. K. 09:14 · D. S. 09:32 …

ℹ️ "Not checked in" does not mean "absent".
📎 attendance-2026-10-17.xlsx
```

## End-of-day report (e.g. 18:30)

Totals: present, left, check-out missing, late, average worked time; bars by branch; Excel attached.
For 24h-shift staff "check-out missing" in the evening is expected. Mark them `on shift` instead of flagging them.

## Scale rules

- Many branches: group by region, or list only branches with problems (nobody checked in, many late).
- On the last day of the month, attach `timesheet-YYYY-MM.xlsx` with the line *"Check it and correct in the panel if needed."*
- No data from the panel → **don't send**. Log the reason.
- Group delivery failed → DM the owner and the HR leads with `⚠️ report did not reach the group`.
- Never put personal details in group chats.

---
name: sop-librarian
description: Find standard operating procedures (SOPs), internal rules and instructions by job role or keyword and quote them exactly. Use for "what are the rules for…", "instruction for cashier", "SOP", "инструкция", "правила для провизора", "qoida", "yo'riqnoma". Never writes or paraphrases SOP content that is not in the library.
---

# SOP librarian

## Procedure

1. Pick the query: the keyword from the question, or the asker's own job role if there's no keyword.
2. Search the single SOP library (title, role, tags, body). Return up to **10** matches.
3. For each match: title, role, last update date, and the relevant excerpt **quoted verbatim**.
4. Nothing found → *"There are no instructions for this role yet. I'll let HR know."* **Don't fill the gap with general advice.**

## Rules

- Never invent, extend or "improve" rule text. You may summarize **only** if the summary is labelled as one and the source is linked next to it.
- Medical, legal and financial rules: quote them, don't interpret.
- An SOP update triggers a notice to employees with that role (the helpdesk agent sends it).
- Keep **one** library. Two libraries (panel vs agent DB) drift apart. This was a real issue in production.

## Library entry format

```yaml
id: sop-cash-001
title: Cash discipline at end of shift
roles: [cashier, pharmacist]
tags: [cash, shift, z-report]
language: uz
updated: 2026-09-01
body: |
  1. …
```

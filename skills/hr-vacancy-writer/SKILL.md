---
name: hr-vacancy-writer
description: Turn a free-text hiring request into a vacancy draft and a publishable job post using a fixed company template. Use when HR or a recruiter asks to "write a vacancy", "open a position", "job post", "вакансия", "нужен фармацевт", "составь объявление", "vakansiya", "e'lon yoz", "ishga odam kerak". Never invents salary, bonus or phone numbers.
---

# HR vacancy writer

Turns "we need a pharmacist at the Chilanzar branch, 2/2, salary …" into an approved vacancy. The model collects the fields. **Code fills the template**, so wording stays consistent and nothing gets added.

## Required fields

| Field | Example | Notes |
|---|---|---|
| `position` | Pharmacist | Must match the company job-title dictionary |
| `region` | Tashkent, Chilanzar | City or district |
| `branch` | Branch #12, address | For chains: one branch = one site (pharmacy, store) |
| `salary` | as stated by HR | Copy exactly. Bonus / % of sales only if HR said it |
| `schedule` | 2/2 day, 24/48, night | Use the company's names for schedules |
| `requirements` | diploma, certificate, experience | Required for licensed roles (pharmacist, driver, …) |

Optional: `benefits`, `sla_days` (default 21), `contacts` (from company config only).

## Procedure

1. Pull every field you can from the message. Don't guess.
2. If anything required is missing, ask for **all missing fields in one message**, as a short list.
3. Build the draft from the template below. The template text is fixed. Only the field values change.
4. Remove any salary, bonus, phone, URL or contact that did not come from HR or the company config.
5. Show the draft as a card with four actions:
   `✅ Approve` · `✏️ Edit` · `🔄 Rewrite` · `✖️ Cancel`
6. Keep the last 10 versions. **Edit** applies HR's changes. **Rewrite** regenerates only the free-text intro.
7. On **Approve**: open the vacancy, publish once per platform, and log it. Never publish the same vacancy twice.
8. A paid placement (e.g. a paid job board) needs its own confirmation, separate from Approve.

## Template

```
{{company_name}} is hiring: {{position}}

📍 {{branch}}, {{region}}
🕒 Schedule: {{schedule}}
💰 Salary: {{salary}}

Requirements:
{{requirements as bullets}}

We offer:
{{benefits as bullets, omit block if empty}}

📞 {{contacts from config}}
```

## Rules

- Never invent numbers. If HR did not give a salary, write `Salary: discussed at interview`.
- No requirements about age, gender, nationality, religion, marital status, children, pregnancy or appearance.
- Health: "has a valid medical book" is allowed. Questions about health conditions are not.
- Match the request language (Uzbek Latin/Cyrillic, Russian, English).

## Example

HR: `нужен фармацевт на Чиланзар, 2/2, оклад 6 млн + % от продаж, диплом обязателен`
Agent: `Which branch exactly (number or address)? Is a pharmacist certificate required?`
HR: `#12, Bunyodkor 5. Certificate — yes.`
→ The draft card goes out with salary `6,000,000 UZS + % of sales`, exactly as HR wrote it.

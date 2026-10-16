---
name: tsenzura-censor
description: Filter profanity and mask personal data (phones, card numbers, passport numbers, emails) in Uzbek and Russian free text before it is stored, shown in dashboards or forwarded by HR agents. Use for "цензура", "tsenzura", "mask PII", "убери мат", "so'kinishni olib tashla", or when adding a free-text field to an HR bot.
---

# Tsenzura (censor)

A shared filter used by every agent's free-text path: dashboard previews, forwarded messages, reports.

## What it does

1. **Profanity:** replace whole-word matches (uz Latin, uz Cyrillic, ru, en) with `***`. Handle character tricks: `@→a`, `0→o`, `3→e/з`, repeated letters, `x/h` and `ё/е` variants.
2. **PII masking:**
   - Phone `+998 90 123 45 67` → `+998 90 *** ** 67`
   - Card `8600 1234 5678 9012` → `8600 **** **** 9012`
   - Passport `AA1234567` → `AA*****67`
   - Email `name@mail.uz` → `n***@mail.uz`
3. **Return** `{clean_text, flags: [profanity|pii_phone|pii_card|…], severity}` so the bot can decide whether to warn, escalate or simply store.

## Rules

- Never alter the meaning of the message. Mask, don't rewrite.
- Keep the raw text only where the law and the client allow it (e.g. an encrypted audit log). Show the clean text everywhere else.
- Abuse aimed at a person, or threats → `severity=high` → escalate to HR. Don't argue with the user.
- Wordlists live in config (`censor/words_uz.txt`, `words_ru.txt`) so clients can extend them without code changes.

## Reference regexes

```python
PHONE = r"(?:\+?998[\s-]?)?\(?\d{2}\)?[\s-]?\d{3}[\s-]?\d{2}[\s-]?\d{2}"
CARD  = r"\b(?:\d{4}[\s-]?){3}\d{4}\b"
PASSPORT_UZ = r"\b[A-Z]{2}\d{7}\b"
EMAIL = r"[\w.+-]+@[\w-]+\.[\w.]+"
```

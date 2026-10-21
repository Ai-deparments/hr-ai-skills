---
name: telegram-rich-format
description: Write beautiful Telegram messages, channel posts, reports and alerts with Bot API HTML formatting — bold/italic/underline/strike, spoilers, links, code blocks with syntax highlighting, block and expandable quotes, live date-time (tg-time) and PREMIUM (custom) emoji via :shortcodes:, plus an Article mode for long structured Telegram articles (headings, lists, quotes, tables, links). Includes a validator/renderer (tgfmt.py) for tags, nesting, escaping and length limits. Use whenever a message, report, post, notification or digest is sent to Telegram (Bot API, Composio TELEGRAM_SEND_MESSAGE, Hermes/Atlas replies), or the user asks for "красивое оформление", "премиум эмодзи", "chiroyli xabar".
version: 1.0.0
license: MIT
---

# Telegram rich format

Always format with **HTML** (`parse_mode=HTML`). It is the most predictable mode:
only `<`, `>` and `&` need escaping. MarkdownV2 requires escaping 18 characters and
breaks on every unescaped `.` or `-`.

## Tag reference (Bot API HTML)

| Effect | HTML |
|---|---|
| Bold | `<b>text</b>` |
| Italic | `<i>text</i>` |
| Underline | `<u>text</u>` |
| Strikethrough | `<s>text</s>` |
| Spoiler (hidden) | `<tg-spoiler>text</tg-spoiler>` |
| Link | `<a href="https://…">text</a>` |
| User mention | `<a href="tg://user?id=123">name</a>` (only works in links/buttons) |
| Inline code | `<code>text</code>` |
| Code block | `<pre>text</pre>` |
| Code block + highlight | `<pre><code class="language-python">…</code></pre>` |
| Quote | `<blockquote>text</blockquote>` |
| Collapsible quote | `<blockquote expandable>long text</blockquote>` |
| Premium emoji | `<tg-emoji emoji-id="5368324170671202286">👍</tg-emoji>` |
| Live date/time | `<tg-time unix="1791306000" format="wDT">tue 20:00</tg-time>` — `r` relative ("in 2 hours"), `w` weekday, `d`/`D` short/long date, `t`/`T` short/long time |

`sendMessage` has no headings, tables or lists — for those use a **rich message** (below).

## Rich messages: real tables, headings, lists (Bot API 10.1+)

`sendRichMessage` (`chat_id`, `message_thread_id`, `rich_message`) renders like the app's
article editor. `rich_message` = JSON `{"markdown": "..."}` (or `"html"`, or `"blocks"`).
Rich Markdown: `#`–`######` headings, `**bold**`, `*italic*`, `==marked==`, `||spoiler||`,
`` `code` ``, lists, `- [x]` tasks, `>` quotes, `---` divider, footnotes, `$math$`,
`<details><summary>…</summary>…</details>`, `<tg-button …>` buttons, and tables:

```
| № | Время | Урок |
|:-:|:-----:|:-----|
| 1 | `10:40–11:25` | ![🧪](tg://emoji?id=5…) **Химия** |
```

- Premium emoji in rich Markdown: `![fallback](tg://emoji?id=ID)` — ids from `emoji.json`
  (`:shortcodes:` are NOT expanded here). Works inside headings and table cells.
- Limits: 32768 chars, 500 blocks (table rows count), 20 columns.
- Use it for schedules, plans, price lists, comparisons, metrics. Keep a plain
  `sendMessage` HTML fallback if the call fails. Edit with `editMessageText(rich_message=…)`.
- Atlas example: `~/.atlas-home/atlas/reminders/school_morning.py`.

### Reports: heading size = importance

Every report is a rich message. The more important the block, the bigger its heading:

| Level | Use for |
|---|---|
| `#` | the one main or urgent thing (alert, blocker) — at most one per report |
| `##` | important blocks: today's plan, priorities, results |
| `###` | normal blocks: details, next step, risks |
| `####` | minor notes: system line, sources |

Times, schedules, numbers and multi-field records go in tables; one premium emoji per
heading or cell; `---` between big blocks; *italic* for conclusions.

**Atlas / Hermes:** start the reply (or cron output) with `<!--tg-rich-->` and write rich
Markdown after it — the gateway sends it with `sendRichMessage` (streaming edits too),
turns `:shortcodes:` into premium emoji and falls back to HTML if Telegram rejects it.
Cron jobs with this skill are sent as rich messages even without the marker.

## Rules

1. Escape text: `&` → `&amp;`, `<` → `&lt;`, `>` → `&gt;` everywhere outside tags
   (user names, captions, code samples, error messages).
2. Nesting: b/i/u/s/spoiler can wrap anything except code/pre; blockquotes cannot nest;
   nothing goes inside `<code>`; only `<code class="language-…">` inside `<pre>`.
3. Limits: message **4096** characters, media caption **1024** (counted without tags).
   Split long reports at paragraph boundaries, never inside an open tag.
4. Links: real `https://` URLs only; turn link previews off for reports.
5. Style: one idea per line, blank line between blocks, bold for the headline and key
   numbers, emoji as bullets (not more than one per line), collapsible quote for details,
   spoiler only for a reveal/answer, no walls of bold.

## Premium (custom) emoji

Write shortcodes from `emoji.json`: `:fire:`, `:rocket:`, `:chart_up:`, `:robot:`, `:check:`…
`tgfmt.py render` turns them into `<tg-emoji>` with a normal emoji fallback inside.

- They render only when the **bot owner has Telegram Premium** (private chats, groups,
  supergroups) or the bot has a **Fragment-purchased username**. In channels without a
  Fragment username, and for non-premium readers of forwards, the fallback emoji shows.
  So posts always look fine — premium is an upgrade, never a dependency.
- For channel posts without a Fragment username use `--no-premium`.
- Ids: forward the emoji to @idstickerbot (or similar), or list a whole pack with
  `tgfmt.py pack <sticker_set_name>`; put ids into `emoji.json`. Never invent ids.
- **Only names that exist in `emoji.json`** (`tgfmt.py list`). An unknown `:name:` is sent
  as literal text (`:test_tube:`), so for anything missing write the plain emoji (🧪).

### Reports always use premium emoji

Every report, brief, digest, reminder list or status message (Atlas cron output, daily
metrics, alerts) is formatted with premium emoji — no plain-emoji-only reports:

- Headline: `<b>:shortcode: Title</b>` with one premium emoji that matches the report
  (`:sparkles:`/`:rocket:` morning, `:moon:` evening, `:chart_up:`/`:chart_down:` metrics,
  `:siren:` alert, `:check:` done, `:cross:` failed, `:gear:` system, `:wallet:` money).
- One premium emoji as the bullet of each section or key line; plain emoji only where
  the registry has no fitting name.
- Keep the other rules: at most one emoji per line, bold for key numbers, details in
  `<blockquote expandable>`.

## Article mode

Use when asked for an article, long post, guide or explainer ("статья", "лонгрид",
"maqola"). Act as a professional Telegram article editor: structured, readable, in the
reader's language (Russian by default).

**Structure:** catchy title → short intro → sections with subheadings → lists, tables or
examples where they help → short conclusion.

**Style rules**
1. Big headings for the main sections; **key words in bold**; *italic* for side info.
2. Quotes for important thoughts; numbered and bulleted lists.
3. Tables only to compare data; links placed inside the text.
4. Blank line between blocks; few emoji; correct, professional, clear language.
5. No invented facts or sources, no filler, no explanation of the formatting — return
   only the finished article.

**Output by destination**
- Text the user pastes into the Telegram app editor, telegra.ph or a doc → **Markdown**:
  `#` title, `##` section, `**bold**`, `*italic*`, `> quote`, `-` / `1.` lists,
  `[name](URL)`, `| … |` tables. No HTML unless asked.
- Sent by a bot (Bot API, Atlas) → send the Markdown as a **rich message**
  (`sendRichMessage`, up to 32768 chars): headings and tables render natively. Only where
  rich messages can't be used (Composio send, captions) convert to plain HTML: `#` →
  `<b>` line, `>` → `<blockquote>`, lists → `1.`/`•` lines, table → `<pre>` columns.

## Workflow

The script sits next to this file: `scripts/tgfmt.py` (Claude Code:
`~/.claude/skills/telegram-rich-format`, Atlas: `~/.atlas-home/skills/telegram-rich-format`;
run it with a Python that exists, e.g. `python3`).

```bash
S=~/.claude/skills/telegram-rich-format/scripts/tgfmt.py   # Atlas: ~/.atlas-home/skills/…
python $S list                         # available :shortcodes:
python $S render draft.html            # → final HTML on stdout, problems on stderr
python $S check  final.html --caption  # validate a caption (1024 limit)
TELEGRAM_BOT_TOKEN=… python $S send draft.html --chat 123456   # manual test send
```
Exit code 1 = problems found; fix them before sending.

Templates in `templates/`: `report.html` (daily metrics), `post.html` (channel post),
`alert.html` (decision request with `<tg-time>`).

## Sending

- **Bot API / Composio** (`TELEGRAM_SEND_MESSAGE`): pass the rendered HTML as `text`
  with `parse_mode: "HTML"`; photo captions ≤1024.
- **Hermes / Atlas agent replies and cron deliveries:** the Telegram gateway converts
  replies to MarkdownV2 by default. Start the reply with the marker
  `<!--tg-html-->` and write Telegram HTML after it — the gateway then sends it as HTML
  as-is (premium emoji, quotes, spoilers, tg-time), escapes any text before the marker,
  splits long messages safely and falls back to plain text if Telegram rejects the markup.
  The gateway expands `:shortcodes:` from `emoji.json` (also in streamed replies), so
  write shortcodes; close every tag, or the message arrives as plain text.

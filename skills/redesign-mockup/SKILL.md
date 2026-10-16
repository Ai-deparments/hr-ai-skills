---
name: redesign-mockup
description: Turn a reference UI image (Pinterest, Dribbble, screenshot) into a full redesign mockup of the user's app — every screen, as ONE grid PNG — next to an overview grid of the current design, plus a before/after image. Images only; the project code is not touched until the user approves. Use when the user attaches a design reference and asks for a "redesign", "yangi dizayn", "shunaqa qilib ber", "new design vs old design", "redesign overview", or "before/after" of their app.
---

# Redesign mockup (old vs new grids)

Deliverables, all on the Desktop (or where the user asks):
1. `<app>_overview.png`: current UI, every screen in a grid
2. `<app>_redesign.png`: the same screens redesigned in the reference's style, same grid
3. `<app>_before_after.png`: both grids side by side

**Images only.** Never edit the user's project in this skill. Build the mockup in the scratchpad. Implementing the design in code is a separate step, and only after the user approves the image.

## Steps

### 1. Read the reference
Look at the attached image(s). Write down, briefly, before building:
- **Tokens:** background, surface(s), hairline, primary/secondary text, accent, success/danger, corner radii, font feel (geometric sans, rounded, mono for codes).
- **Patterns:** hero (avatar + big number? card?), action buttons (circle icon + label?), list style (dividers, grouped), grids/tiles, tab bar (icons only?), primary CTA style.
- **What to keep from the product:** brand color, logo/mascot, real assets. A reference's accent should not overwrite a color that is part of the product (e.g. a currency's gold). Use it as the accent and let the reference drive everything else.

### 2. Gather the project's real content
- Routes/screens from the router (skip notfound/debug). URL shape: hash (`#/x`) or path (`/x`).
- Real copy in the app's default language (i18n dictionaries), real prices, labels, statuses, demo data.
- Asset folder (`public/`, `src/assets`): images, emoji posters, logo. Copy it into the scratchpad mockup folder.
Mockups must use the real content. Never put lorem ipsum or invented features in them.

### 3. Old overview grid
Start the dev server (mock/demo mode if available, in the background), then run the bundled `scripts/shots.mjs` from the scratchpad (setup: `npm init -y && npm i playwright sharp && npx playwright install chromium`):
```bash
node shots.mjs http://localhost:5173 old.png home,stars,profile "#/{r}" 4
```
If the `screens-overview` skill exists, this step is exactly that skill.

### 4. Build the redesign mockup (scratchpad)
- Copy `templates/example.html` into `<scratchpad>/mock/index.html`. It is a full worked example: a 12-screen fintech Telegram Mini App in Phantom-wallet style. It shows the structure (`:root` tokens, component classes, inline SVG icon set `I`, `S = { route: () => html }`, hash switching) and the quality bar.
- Replace the `:root` tokens with the reference's tokens from step 1. Then rewrite **one render function per route** in `S` with that screen's real content. Keep the same route names as the real app.
- 390×844 body. Status bar on top, home indicator at the bottom, tab bar on top-level screens, back button + title on inner screens, primary CTA pinned at the bottom where the real screen has one.
- Spend the boldness in one signature element (e.g. the brand avatar/hero). Keep everything else quiet.

### 5. Shoot the mockup
```bash
node shots.mjs "file:///<scratchpad>/mock" new.png home,stars,profile "index.html#{r}" 4
```
Use the same route list and order as the old grid, so screen N in the old grid matches screen N in the new one. Run it with `run_in_background` and wait with an until-loop on `done`.

### 6. Review and fix
Open `shots/<route>.png` with Read and check every screen:
- content cut by the tab bar or CTA, text touching the edges, rows that wrap or overflow
- broken images, missing fonts, an empty screen
- contrast: secondary text must still read on its background
Fix in `index.html`, re-shoot, and repeat until clean. Don't report a grid you haven't looked at.

### 7. Compare and deliver
```bash
node compare.mjs old.png new.png before_after.png "Eski dizayn" "Yangi dizayn"
```
Copy all three PNGs to the Desktop. Report the paths, then in a few bullets say what came from the reference and what you kept or added from the product. Ask whether to iterate on the image or implement it in code 1:1.

## Notes
- Language: reply in the user's language. Labels in compare.mjs can be localized.
- Fonts: the template loads Inter + JetBrains Mono from Google Fonts. Without internet, switch to system fonts.
- If a screen needs auth/initData and has no mock mode, mark it in the old grid instead of faking it, and still design it in the new grid from the source code.
- Implementation later: port tokens to the app's CSS variables first, then screen by screen, and verify on localhost with the same shots.mjs to compare against the mockup.

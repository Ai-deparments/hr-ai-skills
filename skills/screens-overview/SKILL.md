---
name: screens-overview
description: Capture every screen/page of a web or mobile-web app (Telegram Mini App, SPA, dashboard) at phone size and compose them into ONE grid image, so the whole UI can be seen at a glance. Use when the user asks to "show all pages in one screenshot", "hamma pageni 1ta rasmga", "grid of all screens", "UI overview", "app showcase grid", or wants to compare the current UI against Pinterest/Dribbble references before a redesign.
---

# Screens overview grid

Output: one PNG, phone-sized screenshots (390×844) in a grid with route labels, rounded corners, dark background. Default 4 columns.

## Steps

1. **Find the routes.** Read the project's router (e.g. `src/router.js`, `app/` dir in Next.js, `react-router` config). List every user-facing screen; skip `notfound`/error/debug routes. Note the URL shape: hash routing (`#/attendance`) or path routing (`/attendance`).
2. **Start the dev server** in the background (`npm run dev`), wait for it, confirm HTTP 200. Prefer a mode that runs on mocks/demo data so screens render without auth (check README). If screens need auth or Telegram initData, say so instead of faking it.
3. **Set up tools in the scratchpad**, not in the user's project:
   ```bash
   cd <scratchpad> && npm init -y && npm i playwright sharp && npx playwright install chromium
   ```
4. **Run the bundled script** (copy `scripts/shots.mjs` from this skill's directory into the scratchpad):
   ```bash
   node shots.mjs http://localhost:5173 overview.png home,attendance,requests,profile "#/{r}" 4
   ```
   Args: base URL, output file, comma-separated routes, URL pattern (`{r}` = route; use `/{r}` for path routing), columns. It is slow (~2s per screen), so run it with `run_in_background` and wait with an until-loop on `done` in the output.
5. **Look at the result** with Read before reporting. Check for blank/loading screens, error states, or screens that redirected. If a screen needs a longer wait or a click to open (sheets, modals), extend the script for that case.
6. **Copy the PNG to the Desktop** (or where the user wants) and report the path, size, and which screens are included. Mention that data shown is demo/mock data if so.

## Notes

- Screens that are modals/sheets over another screen (e.g. a payment sheet) render as-is; that is fine.
- Long screens are cropped to the viewport height. If the user wants full-height, switch `page.screenshot` to `fullPage: true` and drop the fixed-height mask.
- Tested on: a Telegram Mini App (Vite, vanilla JS, hash routing, 12 screens).

// Usage: node shots.mjs <baseUrl> <out.png> <route1,route2,...> [urlPattern] [cols]
// urlPattern: how a route becomes a URL, {r} is replaced. Default "#/{r}" (hash routing).
import { chromium } from 'playwright';
import sharp from 'sharp';
import { mkdirSync } from 'fs';

const [base, out = 'overview.png', list, pattern = '#/{r}', colsArg] = process.argv.slice(2);
if (!base || !list) {
  console.error('usage: node shots.mjs <baseUrl> <out.png> <routes,comma,separated> [urlPattern] [cols]');
  process.exit(1);
}
const ROUTES = list.split(',').map(s => s.trim()).filter(Boolean);
const W = 390, H = 844, GAP = 40, LABEL = 56, PAD = 60;
const COLS = Number(colsArg) || Math.min(4, ROUTES.length);
const url = r => base.replace(/\/$/, '') + '/' + pattern.replace('{r}', r).replace(/^\//, '');
mkdirSync('shots', { recursive: true });

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
await page.goto(url(ROUTES[0]));
await page.waitForTimeout(2500);

const files = [];
for (const r of ROUTES) {
  await page.goto(url(r));
  await page.waitForTimeout(1800);
  const f = `shots/${r.replace(/[^\w-]/g, '_')}.png`;
  await page.screenshot({ path: f });
  files.push({ r, f });
  console.log('shot', r);
}
await browser.close();

const esc = s => s.replace(/[&<>]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]));
const rows = Math.ceil(files.length / COLS);
const cw = PAD * 2 + COLS * W + (COLS - 1) * GAP;
const ch = PAD * 2 + rows * (H + LABEL) + (rows - 1) * GAP;
const mask = Buffer.from(`<svg width="${W}" height="${H}"><rect width="${W}" height="${H}" rx="36" ry="36"/></svg>`);
const composites = [];
for (const [i, { r, f }] of files.entries()) {
  const x = PAD + (i % COLS) * (W + GAP);
  const y = PAD + Math.floor(i / COLS) * (H + LABEL + GAP);
  const label = Buffer.from(`<svg width="${W}" height="${LABEL}"><text x="0" y="36" font-family="Segoe UI, Arial" font-size="28" font-weight="600" fill="#e5e5e5">${esc(r)}</text></svg>`);
  composites.push({ input: label, left: x, top: y });
  const rounded = await sharp(f).composite([{ input: mask, blend: 'dest-in' }]).png().toBuffer();
  composites.push({ input: rounded, left: x, top: y + LABEL });
}
await sharp({ create: { width: cw, height: ch, channels: 4, background: '#111214' } })
  .composite(composites).png().toFile(out);
console.log('done', out, cw, ch);

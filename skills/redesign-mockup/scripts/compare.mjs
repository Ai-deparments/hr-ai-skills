// Usage: node compare.mjs <old.png> <new.png> <out.png> [oldLabel] [newLabel]
import sharp from 'sharp';

const [oldF, newF, out = 'before_after.png', oldL = 'OLD', newL = 'NEW'] = process.argv.slice(2);
if (!oldF || !newF) {
  console.error('usage: node compare.mjs <old.png> <new.png> <out.png> [oldLabel] [newLabel]');
  process.exit(1);
}
const PAD = 60, GAP = 80, HEAD = 110;
const a = await sharp(oldF).metadata();
const b = await sharp(newF).metadata();
const h = Math.max(a.height, b.height);
const resize = async (f, m) => m.height === h ? sharp(f).toBuffer() : sharp(f).resize({ height: h }).toBuffer();
const A = await resize(oldF, a), B = await resize(newF, b);
const aw = (await sharp(A).metadata()).width, bw = (await sharp(B).metadata()).width;
const W = PAD * 2 + aw + GAP + bw, H = PAD + HEAD + h + PAD;
const esc = s => s.replace(/[&<>]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]));
const label = (t, w, color) => Buffer.from(`<svg width="${w}" height="${HEAD}"><text x="60" y="70" font-family="Segoe UI, Arial" font-size="56" font-weight="700" fill="${color}">${esc(t)}</text></svg>`);
await sharp({ create: { width: W, height: H, channels: 4, background: '#0B0B0C' } })
  .composite([
    { input: label(oldL, aw, '#8E8E93'), left: PAD, top: PAD },
    { input: A, left: PAD, top: PAD + HEAD },
    { input: Buffer.from(`<svg width="4" height="${h}"><rect width="4" height="${h}" fill="#2A2A2C"/></svg>`), left: PAD + aw + GAP / 2 - 2, top: PAD + HEAD },
    { input: label(newL, bw, '#FFFFFF'), left: PAD + aw + GAP, top: PAD },
    { input: B, left: PAD + aw + GAP, top: PAD + HEAD },
  ])
  .png().toFile(out);
console.log('done', out, W, H);

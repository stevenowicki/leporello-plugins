#!/usr/bin/env node
/**
 * dls_check.mjs — automated DLS-conformance gate for a Leporello bundle.
 *
 * Renders a bundle and checks the DLS rules that a static lint can't see —
 * the ones the first unsupervised skill output got wrong:
 *   1. FONT          — text must actually render in Libre Franklin (not a
 *                      system/Inter/Roboto stack). Catches "vendored the lib but
 *                      didn't apply it" and "authored fresh HTML, forgot the font".
 *   2. PRESENTER COL — critical content (prominent text/numbers) must stay left of
 *                      x=1574 (the right ~18% is the presenter + nav rail). §4 / §5.3.
 *   3. ATTRIBUTION   — no on-frame source/attribution strip. §5.14 (metadata only).
 *   4. HEADLINE SCALE— the headline must be broadcast-big (≥ ~64px @1080). §2.
 *
 * This is the MECHANICAL half of supervision; the vision critique (references/
 * dls-rubric.md) is the perceptual backstop. Run BOTH before publishing.
 *
 * Usage:  node scripts/dls_check.mjs <bundle-dir | index.html | http://url>
 * Exit 0 = clean, 1 = violations (printed as JSON). Headed (live maps need a GPU
 * context to composite; headless renders maps black). Playwright must be installed
 * (npx playwright install chromium).
 */
import { chromium } from 'playwright';
import path from 'node:path';
import fs from 'node:fs';

const PRES = 1574; // presenter-safe boundary (right ~18% of 1920)
const arg = process.argv[2];
if (!arg) { console.error('usage: node dls_check.mjs <bundle-dir|index.html|url>'); process.exit(2); }

let url = arg;
if (!/^https?:\/\//.test(arg)) {
  let f = path.resolve(arg);
  if (fs.existsSync(f) && fs.statSync(f).isDirectory()) f = path.join(f, 'index.html');
  url = 'file://' + f;
}

const browser = await chromium.launch({ headless: false });
const page = await (await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 })).newPage();
await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 }).catch(() => {});
await page.waitForTimeout(4500); // let fonts + any map settle

const result = await page.evaluate((PRES) => {
  const viol = [];
  const headline =
    document.querySelector('.lep-headline, .lep-headline--map, h1, [class*="headline"]') || document.body;
  const headFam = getComputedStyle(headline).fontFamily;
  const headPx = Math.round(parseFloat(getComputedStyle(headline).fontSize) || 0);

  // 1. FONT — Libre Franklin must actually be the rendered family.
  if (!/libre franklin/i.test(headFam)) {
    viol.push({ rule: 'font', severity: 'critical',
      detail: `Headline renders in "${headFam}" — not Libre Franklin (the DLS primary). Vendor libre-franklin-latin-var.woff2, @font-face it, and resolve type through var(--lep-font-sans) / the DLS lib.` });
  }

  // gather visible elements that directly contain text
  const hasText = (el) => [...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim().length > 1);
  const els = [...document.querySelectorAll('body *')].filter((el) => {
    const cs = getComputedStyle(el);
    if (cs.visibility === 'hidden' || cs.display === 'none' || parseFloat(cs.opacity) === 0) return false;
    return hasText(el);
  });

  // 2. PRESENTER COLUMN — prominent text past x=1574.
  const offenders = [];
  for (const el of els) {
    const r = el.getBoundingClientRect();
    const fs = parseFloat(getComputedStyle(el).fontSize) || 0;
    if (r.width > 0 && r.top < 1080 && r.bottom > 0 && fs >= 26 && r.right > PRES + 2) {
      offenders.push(`"${el.textContent.trim().slice(0, 28)}" (${Math.round(fs)}px → x${Math.round(r.right)})`);
    }
  }
  if (offenders.length) {
    viol.push({ rule: 'presenter-column', severity: 'critical',
      detail: `Critical content crosses the x=${PRES} presenter-safe boundary (right ~18% is the presenter + nav rail): ${offenders.slice(0, 6).join('; ')}. Pull it left of ${PRES}.` });
  }

  // 3. ATTRIBUTION on-frame (bottom strip / source-y text).
  const attrib = els.find((el) => {
    const t = (el.textContent || '').trim();
    const r = el.getBoundingClientRect();
    return t.length < 160 && r.top > 900 && /(^|\b)(source|projection|credit|attribution|courtesy|not final)\b/i.test(t);
  });
  if (attrib) {
    viol.push({ rule: 'attribution', severity: 'warn',
      detail: `On-frame attribution/source detected ("${attrib.textContent.trim().slice(0, 50)}") — §5.14: capture source as manifest metadata, do NOT draw it on the frame.` });
  }

  // 4. HEADLINE SCALE
  if (headPx && headPx < 64) {
    viol.push({ rule: 'headline-scale', severity: 'warn',
      detail: `Headline is ${headPx}px — below the broadcast floor (headline tier is 84px @1080).` });
  }

  // 5. BREVITY — the graphic is the presenter's backdrop, not the script. The presenter
  //    explains; the graphic gives them something to point at.
  const headWords = (headline.textContent || '').trim().split(/\s+/).filter(Boolean).length;
  if (headline !== document.body && headWords > 9) {
    viol.push({ rule: 'verbose-headline', severity: 'warn',
      detail: `Headline is a ${headWords}-word sentence ("${(headline.textContent || '').trim().slice(0, 60)}…"). A broadcast headline is a few words — let the presenter say the rest.` });
  }
  // "Prose" = elements whose OWN text is a phrase/sentence (≥6 words): headlines,
  // subheads, captions, explanatory annotations. Short data labels ("PA 19",
  // "BLUE PARTY", axis ticks) are NOT prose and don't count — so a dense cartogram
  // or chart isn't penalized; only the presenter's-job explanatory copy is.
  let proseWords = 0;
  for (const el of els) {
    const own = [...el.childNodes].filter((n) => n.nodeType === 3).map((n) => n.textContent).join(' ').trim();
    const w = own ? own.split(/\s+/).filter(Boolean).length : 0;
    if (w >= 6) proseWords += w;
  }
  if (proseWords > 28) {
    viol.push({ rule: 'too-much-text', severity: 'warn',
      detail: `~${proseWords} words of explanatory copy on the frame (headline + subhead + captions/annotations). The graphic is doing the presenter's explaining — cut to a short headline + the data + ≤1–2 markers; strip the "here's what happened" labels.` });
  }

  return { ok: viol.length === 0, font: headFam, headlinePx: headPx, proseWords, violations: viol };
}, PRES);

await browser.close();
console.log(JSON.stringify(result, null, 2));
process.exit(result.ok ? 0 : 1);

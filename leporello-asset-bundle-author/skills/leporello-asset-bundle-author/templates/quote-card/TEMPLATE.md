# `quote-card` template

A single pull-quote with speaker attribution, restyled to the **v1 Leporello DLS**. Large quote type at the headline tier, a left accent rule, a broadcast lower-third attribution block, and a full-bleed ambient background with a mandatory legibility scrim. Broadcast-safe.

**Anchored on:** the broadcast convention of "let the words speak for themselves." No single canonical Leporello asset because the shape is so generic, but every newsroom ships a version of it.

> This file is template documentation — it is **NOT** copied into authored bundles. The skill fills `content.json`, `manifest.json`, `brief.md`, `README.md`, and `CLAUDE.md` from the skeletons in this directory.

## When to use

- **The quote IS the story.** A statement, a denial, a commitment, a slip-of-the-tongue.
- The viewer needs to read the words directly (not paraphrased).
- The speaker's identity and the circumstance of the quote matter.

**Don't use when:**
- You have multiple short quotes to compare (a wall of quotes is fine in `generic`; this template is for one).
- The "quote" is paraphrased speech reported by a journalist (treat as `narrative-flow` or `generic` with proper attribution).
- The quote is so short it functions as a `stat-callout` ("$2.4 million" said by the CEO → just use stat-callout).

## What's in it

```
templates/quote-card/
├── TEMPLATE.md          this file (template docs — NOT copied into bundles)
├── README.md            per-bundle producer-ops skeleton ([CLAUDE-PLACEHOLDER:*])
├── CLAUDE.md            per-bundle AI-resume skeleton ([CLAUDE-PLACEHOLDER:*])
├── manifest.json        skeleton with [CLAUDE-PLACEHOLDER:*] markers (technical fields pre-filled)
├── brief.md             editorial brief skeleton with quote-specific framing
├── index.html           renders kicker + quote body (headline tier, accent rule) + speaker block + ambient background
├── content.json         eyebrow / quote / speaker / speakerTitle / context / source (+ optional background* / sourceRefs)
└── lib/                 vendored DLS tokens, base CSS, helpers, and the self-hosted Libre Franklin woff2
```

## DLS conformance (v1)

This template is built to the v1 DLS direction. The load-bearing rules it follows:

- **Primary typeface is Libre Franklin** (SIL OFL 1.1), self-hosted as `lib/libre-franklin-latin-var.woff2` and declared via `@font-face` in `lib/tokens.css`. No CDN font load — the bundle ships the face. Body type is sans-serif at all times.
- **Type ramp (px @1080).** The quote runs at the **headline tier** (84px) and auto-shrinks one notch to 68px (long) or 58px (very long) by character count so multi-sentence pulls still fit the composition zone. The kicker is the **kicker tier** (34px); the speaker name a heavy secondary tier; the role at the **subhead tier**; the context line at the **source tier** (22px).
- **Named regions.** Layout uses the regions defined in `lib/base.css`: a `lockup` (kicker), a centered quote stage held inside the **composition zone** (x0–1574), a bottom-left attribution block, and an optional corner source strip. Everything critical stays **left of x1574** — the right ~18% is the presenter column; the background runs full-bleed behind the presenter.
- **Background-media layer + scrim (§5.4).** A full-bleed ambient background is mounted by `leporello.mountBackgroundMedia()` so a lone quote never leaves a dead dark field. The default is a self-contained inline-SVG radial gradient (ships no external image); a producer can override via `content.backgroundImage`. The **mandatory scrim** (left-weighted by default) keeps the quote and attribution legible.
- **Attribution is OFF (§5.14).** No attribution footer band, no `[src-N]` markers, no bottom source list. The speaker / role / context block IS the editorial citation surface for this template (who said it, where, when) — keep it; don't turn it into footnote machinery. Machine-readable sources stay in `manifest.sources[]`.
- **The accent rule is the only ornament.** A single `--lep-data-accent` `border-left` on the quote block reads as editorial blockquote grammar. Zero decoration budget otherwise.
- **Telestration is the default raster telestrator.** This is a non-map template (`telestrator: "default"` in the manifest), so the stage is scaled with `leporello.fitStage('.lep-stage')` to the 1920×1080 canvas — the standard for every non-map template.

## Content shape

`content.json` for this template:

```json
{
  "eyebrow": "string — kicker, e.g. 'IN THEIR OWN WORDS', 'ON THE RECORD', 'TESTIMONY'",
  "quote": "string — the full quote, no leading/trailing quotes (template adds smart-quotes)",
  "speaker": "string — speaker's name",
  "speakerTitle": "string — role/title at time of quote",
  "context": "string — when/where the quote was made, e.g. 'Press conference · May 14, 2026'",
  "source": "string — short provenance line for the producer (not rendered on the lower-third)",
  "backgroundImage": "optional string — any URL; overrides the default inline-SVG ambient field",
  "backgroundScrim": "optional 'left' | 'bottom' | ... — scrim weighting passed to mountBackgroundMedia",
  "sourceRefs": ["src-N", ...]
}
```

`index.html` keeps an inline `<script type="application/json">` mirror of `content.json` (and a small `manifest.json` mirror) as a render-time fallback for `file://` previews where `fetch` is blocked. **Keep the inline mirror in sync with `content.json`** when you author a bundle — `content.json` remains the editable source of truth; the inline copy is a convenience only.

### Notes for other catalog templates

The map / iran-alignment templates in this catalog carry richer content shapes the quote-card does not use, but which the skill should recognize when working across the catalog:

- **Geo-anchored labels** — map templates place labels by `lngLat: [lng, lat]` so MapLibre owns re-projection through pan/zoom; they render **full-bleed** (no `fitStage`, no `transform: scale` on a live map), expose `window.leporelloMap`, and embed the `lepo-tele` postMessage receiver for cross-origin geo-anchored telestration.
- **Roster metric encoding (§5.13)** — where a template lists people/units, the encoding carries the metric (e.g. color/order maps to the value), never a bare unsorted roster.

Neither applies to the quote-card itself, but the same `lib/` and DLS tokens back all of them.

## Source rigor

Quotes are the highest-scrutiny content type. Bare minimum:
- **Primary source preferred.** Direct transcript, court filing, official statement, video timestamp. If you only have a secondary report ("the AP says X said Y"), that's a flag the bundle should disclose — note in the `context` field or `brief.md` source decisions.
- **Verify the exact wording.** Misquotes propagate fast. If you have access to the recording, quote against it.
- **Note ellipses.** If the quote is excerpted, use `...` (or `…`) where text is omitted. The brief's "Content decisions" section should justify the cut.

## Quote length

The template auto-sizes by character count, but density still matters:
- **Up to ~30 words** sits comfortably at the headline tier (84px) in a single stage.
- **30–60 words** drops to 68px (`data-long="true"`) — legible but denser.
- **60+ words** drops to 58px (`data-long="very"`). Past that, trim the quote or use `narrative-flow` with the quote as a step. A 100-word quote on broadcast is unreadable.

## On sources, footnotes, and attribution

Unlike the other templates, **the speaker block on a quote-card IS a citation surface** — `Director of Operations, Port Authority · September 12` is where/when the quote was made, which is editorial context the viewer needs (not academic-paper machinery). Keep it.

What's NOT here (per §5.14, attribution off):
- No `[src-X]` superscript after the context line.
- No source list at the bottom.
- No attribution footer band.

Sources stay in `manifest.sources[]` (the primary-transcript link, for example) for the producer to verify against and for the admin source-review UI to surface. The on-screen surface stays clean.

## Things not to change

- The body type is sans-serif (Libre Franklin). No serif body.
- The accent rule is the only ornament.
- The speaker / title / context block — that IS the citation, editorially.
- The full-bleed background + mandatory scrim.
- The `data-version` / `data-updated` plumbing.
- The manifest schema shape and the pre-filled technical fields (`dlsVersion`, `telestrator`, `dimensions`).
- The vendored `lib/` (including the woff2).

## Density check

The quote-card is the easiest template to "just throw a long quote at and hope." Resist. The presenter can read aloud what's on the screen; if it's too long for the broadcast viewer to read in 15 seconds, it's too long.

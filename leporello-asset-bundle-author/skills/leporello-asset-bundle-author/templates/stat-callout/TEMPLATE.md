# `stat-callout` template

One number, dominant. Per broadcast-standards: "A hero figure with one line of context is the most efficient slide format that exists."

**Anchored on:** the hero-number shape used across many Leporello assets. No single canonical example because it's the workhorse — almost every broadcast graphic touches this shape at some point.

## When to use

- **One number is the entire story.** Revenue, casualties, polling margin, market cap, response rate.
- The viewer should walk away knowing one figure.
- The presenter fills in the surrounding context.

**Don't use when:**
- You're tempted to put two numbers side-by-side. Either pick one and reference the other in `comparison`, or split into two assets — two hero numbers on one slide both lose.
- The number is a percentage that only makes sense with the base it's drawn from. Use `generic` and write the relationship explicitly.
- The story is about a relationship between numbers (use a chart in `generic` or wait for a future chart template).

## What's in it

```
templates/stat-callout/
├── TEMPLATE.md          this file (template docs — NOT copied into bundles)
├── README.md           per-bundle producer-ops skeleton ([CLAUDE-PLACEHOLDER:*])
├── CLAUDE.md           per-bundle AI-resume skeleton ([CLAUDE-PLACEHOLDER:*])
├── manifest.json       skeleton with [CLAUDE-PLACEHOLDER:*] markers
├── brief.md            editorial brief skeleton with stat-callout framing
├── index.html          kicker + headline in the top-left lockup, a 270px hero number as the star, optional trend delta on its shoulder, hero label beneath, one context line bottom-left, over an ambient background-media layer + scrim
├── content.json        eyebrow / headline / stat (value + label) / comparison / context / background / source / sourceRefs
└── lib/                vendored DLS tokens, base CSS, helpers, Libre Franklin woff2, bg-relief.svg
```

> **This template is restyled to the v1 DLS** (`docs/prelim/dls/m1/direction/direction.md`,
> `dlsVersion` 1.5). Primary typeface **Libre Franklin** (self-hosted woff2 in `lib/`);
> the broadcast type ramp, palette, and named regions come from `lib/tokens.css` +
> `lib/base.css` so the ramp can't drift. Critical content stays inside the
> **composition zone** (x < 1574 — left of the ~18% presenter column); the
> background-media layer runs **full-bleed** behind a **mandatory scrim**.
> **Attribution does not render** (direction §5.14) — sources live in the manifest.

## Content shape

```json
{
  "eyebrow": "string — the kicker eyebrow (top-left lockup)",
  "headline": "string — the slide's point, what this number means",
  "stat": {
    "value": "string — the formatted hero number, e.g. '$2.4M', '34%', '1,247'",
    "label": "string — one-line description of what the number represents"
  },
  "comparison": {
    "value": "string — e.g. '+18%', '−$340K', '2.3x' — the trend delta",
    "label": "string — what it's compared to, e.g. 'vs Q3', 'vs target'"
  },
  "context": "string — one or two sentences of context, max",
  "background": {
    "image": "string — path to a full-bleed ambient layer (default './lib/bg-relief.svg')",
    "scrim": "'left' | 'center' | 'heavy' — mandatory legibility scrim variant (default 'left')"
  },
  "source": "string — provenance line (NOT rendered on air; see §5.14)",
  "sourceRefs": ["src-N", ...]
}
```

### The `background` block (background-media + scrim)

The frame mounts a **full-bleed ambient background-media layer** behind all
content (direction §5.4) so the right field — which the composition zone
intentionally leaves clear of data — never reads as a dead empty third.

- `background.image` — a self-contained, low-contrast, low-motion image or SVG.
  The vendored `lib/bg-relief.svg` (an abstract recessed-column "data relief",
  no text/logos) is the default and a safe fallback. It is **ambient texture**,
  not a depiction of anything real — never put a chart, logo, or data into it.
- `background.scrim` — picks the **mandatory** legibility scrim. `'left'`
  darkens behind the top-left lockup while keeping the center bright (the
  default, matches the hormuz-map pattern); `'heavy'` for busy imagery;
  `'center'` for an even wash. Scrim opacity stays inside the §5.4 0.55–0.78
  mandate — set by the helper, don't hand-roll a lighter one.
- Mounted in JS via `leporello.mountBackgroundMedia({ stage, image, scrim })`
  as the first child of `.lep-stage` so it sits behind everything.

### Geo-anchored labels (`map` / `iran-alignment` templates only)

`stat-callout` is **not** a map template, so it has no `lngLat` labels and no
MapLibre dependency. For the map-bearing templates, label entries in
`content.json` carry geographic anchors — `{ "text": "...", "lngLat": [lng, lat],
"tier": "featured" | "orientation" }` — and the renderer projects them onto the
live full-bleed map (direction §6, two-tier map labels). Those templates set
`telestrator: "map"`, declare `maplibre` + `pmtiles` in
`manifest.externalDependencies`, expose `window.leporelloMap`, and embed the
`lepo-tele` postMessage receiver. **None of that applies here** — flagged only so
the field shapes don't surprise anyone cross-referencing templates.

### Rounding precision

**Round aggressively.** Per broadcast-standards:
- `$2.4M`, not `$2,387,491`.
- `34%`, not `34.27%`.
- `1.2 billion`, not `1,234,567,890`.

The full precision goes in the source documentation, not the hero number. If precision genuinely matters to the story (election margin, drug-trial significance level), that's a flag the wrong template is in play — consider `narrative-flow` to surface the precision-with-context relationship.

### The comparison block

Optional, but powerful when used. The comparison renders in the broadcast-safe orange and frames the hero number relative to something. Two valid framings:

1. **vs. previous** — "+18% vs Q3"
2. **vs. expected** — "−$340K vs target"

Avoid:
- More than one comparison. Pick the one that matters.
- Comparisons that confuse direction. Use `+` and `−` (or `↑` / `↓`) explicitly, and make sure the sign reads as "good" or "bad" in the way the story wants.

If there's no comparison, omit the field or set it to `null`. The block hides.

## Layout (v1 DLS)

Everything critical lives inside the **composition zone** (x < 1574, left of the
presenter column) on the 1920×1080 `.lep-stage`, over the ambient background layer:

1. **Lockup** (top-left, title-safe inset): `.lep-kicker` eyebrow + `.lep-headline`
   headline, from the DLS type roles (kicker 34px, headline 84px @1080).
2. **Hero number** — the star. Base role is 150px / weight 900; a lone short figure
   is pushed to **270px** (direction §2 allows up to 200px and "bigger is usually
   fine") so it reads as ~3× the headline. Auto-scaled down by character length via
   `[data-len]` so a wide value never crosses x1574:
   - up to 5 chars (e.g., `$2.4M`, `34%`): **270px**
   - 6–7 chars: **224px** (`data-len="medium"`)
   - 8–9 chars: **168px** (`data-len="long"`)
   - 10+ chars: **128px** (`data-len="xlong"`)
3. **Trend delta** (optional) — rides the hero's top-right shoulder like a ticker
   delta, colored `--lep-data-accent`, capped at the data-label tier so it never
   competes with the hero number.
4. **Hero label** — subhead tier (40px), tight under the number, says what the
   number measures. Structurally always smaller than the value.
5. **Context line** (optional) — one muted sentence bottom-left with a thin
   `--lep-data-primary` accent rule (no decorative container).

The hero number stays dominant by a wide ratio (270px vs an 84px headline ≈ 3.2×),
so the "one slide, one point" effect holds. Tabular figures throughout (the stage
sets `font-feature-settings: 'tnum'`).

**No attribution / source strip renders** (direction §5.14). The `source` line in
`content.json` and `manifest.sources[]` are provenance for the producer / admin /
future-Claude only — the on-air shell renders attribution from the admin layer
outside the iframe.

## Common customizations

- **Number-only (no comparison or context):** omit `comparison` (set to `null`) and `context`. The trend delta and context line both hide; the hero + label stand alone.
- **Multiple stats in a grid:** that's a dashboard. Use multiple `stat-callout` assets in one package, or build a custom layout with `generic`. Don't extend this template.
- **Different sign/direction accent on the trend delta:** the delta uses `--lep-data-accent` (the one story color). For "bad news up is bad" cases (casualties, costs) you can point it at a muted-red token, but keep it one token — don't reintroduce a pill container.
- **Swap the background:** point `background.image` at a different self-contained ambient image/SVG, or bump `background.scrim` to `'heavy'` for busy imagery. Keep it ambient and inside the §5.4 scrim mandate — never let it carry data.
- **Override hero auto-scaling:** if the JS-set `data-len` band makes your hero too small, set `font-size` inline on the `.lep-hero-number` element after content load — but keep the whole figure left of x1574.

## On sources, footnotes, and attribution

The template does **not** render a visible source list, inline `[src-X]` footnotes, or an attribution footer. The hero number is the whole composition; cluttering it with citation machinery loses the entire point. Sources live in `manifest.sources[]` for producer / admin / future-Claude use. See the same section in the `timeline` template README for the full reasoning.

The `sourceRefs` field on `content.json` stays in the schema for parity with other templates and so future tooling (presenter notes, admin source-review UI) can consume it — it just isn't rendered.

## Things not to change

- The composition discipline: critical content left of x1574, lockup top-left, hero number dominant. Background-media runs full-bleed; data never does.
- The hero number's default weight (900) and the 270px size (auto-scaled down by JS for long values). It's the entire reason for the template.
- The **mandatory scrim** over the background-media layer — never drop it or push it below the §5.4 0.55 floor; the lockup must stay legible.
- The `data-version` / `data-updated` plumbing.
- The manifest schema shape and the synced technical fields (`dlsVersion`, `telestrator`, `dimensions`).
- The vendored `lib/` — including the Libre Franklin woff2 and the base.css region-helper specificity (a zero-specificity `:where()` rule keeps `.lep-lockup` / `.lep-source` absolutely positioned; don't reintroduce a `>`-combinator `position: relative` that collapses them into flow).
- The "sources / attribution stay invisible" rule (§5.14).

## Density check

Per `references/broadcast-standards.md`: rounded to broadcast precision, no decorative noise. If your slide has the hero number plus more than ~30 words of supporting text total (label + comparison label + context), trim. The presenter's words carry the rest.

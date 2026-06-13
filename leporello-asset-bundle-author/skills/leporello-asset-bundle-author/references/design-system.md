# Design System (DLS) — Token Usage

The Leporello Design Language System (DLS) defines the visual vocabulary every
bundle inherits: typeface, the broadcast type ramp, palette, named on-screen
regions, telestration, radii, motion. The authoritative direction is
`docs/prelim/dls/m1/direction/direction.md` in the main Leporello repo; the
canonical tokens live at `dls/tokens.json` (+ `dls/tokens.css`). This skill
ships a snapshot of the v1 tokens at `lib/tokens.css`, and every template
vendors that same snapshot into its own `lib/`.

**The one rule that governs this whole document: everything sizes, colors, and
spaces from `var(--lep-*)`. Never invent a value that already has a token.**
There is no escape hatch. The old guidance that said "size headlines / hero
numbers / labels in pt or px to match broadcast minimums" is **deleted** — that
freelancing of raw values is the exact failure the v1 DLS was built to stop. The
ramp is now a set of tokens; author against the tokens.

---

## The reference canvas

All authoring is on a **1920 × 1080** stage, and **every size in the token set is
px on that reference**. `leporello.fitStage()` scales the whole stage to the
viewport, so the ratios hold on any wall. **Never author in `rem`** (the old
split-brain failure) and **never author in `pt`** (the deleted escape hatch).

> **Maps are the exception to fitStage.** A live MapLibre map renders FULL-BLEED
> at true viewport size — never wrap a MapLibre map in `.lep-stage` /
> `transform: scale()`. The map template's DLS chrome (lockup, legend, stepper,
> labels) sits on a separate non-scaled overlay. See `template-catalog.md`.

---

## Why tokens, not raw values

Tokens are the brand. Hardcoding `#0a0e14` where `--lep-surface-0` belongs, or
`font-size: 80px` where `--lep-size-headline` belongs, makes the bundle drift
from the rest of the broadcast surface and from sibling bundles — and, worse, it
lets each frame re-decide the type scale, which is precisely how `lepo-1` ended
up with ~45px headlines and same-size map labels.

**Any hardcoded value that already has a token is a pushback** (see
`editorial-standards.md` on UI-chrome DLS overrides). The token-lint gate
enforces this mechanically where wired.

---

## Token reference

The full set lives in `lib/tokens.css` (mirror of `dls/tokens.json`). Highlights
below. Token names are part of the public API — the `--lep-*` prefixes are stable.

### Typeface — Libre Franklin

The primary face is **Libre Franklin** (SIL OFL 1.1), self-hosted as a variable
`.woff2` (weights 400–900) vendored in every bundle's `lib/`. It is Franklin
Gothic's open revival — the iconic American news-graphic vernacular. **Not
Inter** (brief-banned). The `@font-face` declarations live in `tokens.css`; the
woff2 ships beside it.

```css
font-family: var(--lep-font-sans);
/* 'Libre Franklin', 'Lep Primary', 'Helvetica Neue', Helvetica, Arial, sans-serif */
```

The system fallbacks are a no-FOIT safety net only — the woff2 is always
vendored so the rendered result is deterministic across machines and headless
capture.

**Numerals:** for every numeric tier (hero-number, data-label, any aligned
column) enable tabular figures — `font-variant-numeric: tabular-nums;` /
`font-feature-settings: "tnum" 1;` — so stacked / right-aligned values lock to a
grid. The `.lep-tabular` / `[data-lep-tabular]` utility in `tokens.css` does
this.

### Type ramp (the headline fix)

Named tiers, px @ the 1080 reference. **Size from the token, never a literal.**
Casing and tracking are rules per element class, not suggestions.

| Token | px@1080 | Weight | Casing | Tracking token | Usage |
|---|---|---|---|---|---|
| `--lep-size-hero-number` | 150 | 900 (black) | as-data | `--lep-tracking-hero` (-0.02em) | THE single figure on a stat/big-bars frame. One per asset. Tabular. May go to 200px for a lone number. ~3–4× the next-largest text. |
| `--lep-size-headline` | 84 | 800 | Title Case **or** ALL CAPS | `--lep-tracking-headline` (-0.01em) | The slide's one-sentence point. The #1 `lepo-1` fix (it ran ~45px). |
| `--lep-size-headline-map` | 72 | 800 | Title Case | `--lep-tracking-headline` | Headline variant for full-bleed map frames. |
| `--lep-size-data-label` | 64 | 700–800 | as-data | `--lep-tracking-headline` | Values annotated directly on bars/segments. Must be **≥** the label it annotates. Tabular. |
| `--lep-size-subhead` | 40 | 400–500 | Sentence case | 0 | One line of context under the headline. Optional. |
| `--lep-size-kicker` | 34 | 700 | ALL CAPS | `--lep-tracking-kicker` (0.1em) | Eyebrow/category above the headline. |
| `--lep-size-legend` | 34 | 600 | Title/Sentence | `--lep-tracking-legend` (0.01em) | Legend rows — a first-class storytelling tier, never fine print. Floor 30px. |
| `--lep-size-label-featured` | 40 | 700 | Title Case | 0 | Featured (story) map place-labels. ≤3–5 per asset. Strong white halo. |
| `--lep-size-label-orientation` | 22 | 400 | as-basemap | 0 | Recessed orientation/basemap labels at ~0.7 opacity. |
| `--lep-size-source` | 22 | 400–500 | Sentence/UPPER tag | `--lep-tracking-source` (0.04em) | Source/caption — **absolute floor, 22px**. Corner only (and OFF by default on-frame; see below). |

**Weights** (`--lep-weight-*`): regular 400 / medium 500 / semibold 600 / bold
700 / extrabold 800 / black 900. **No Light/Thin anywhere** — camera
re-compression eats hairlines. Nothing below 400 at any storytelling tier.

**Line heights**: `--lep-leading-tight` 0.95 (hero/one-line headline),
`--lep-leading-snug` 1.08 (multi-line headline), `--lep-leading-normal` 1.3
(subhead/body).

**Composite typography tokens** are also exported in `dls/tokens.json` under
`typography.*` (family + size + weight + line-height + tracking bundled per
tier) for tooling that consumes DTCG.

#### Hard ratios (enforce, don't drift)

- One element per asset is dramatically largest — that's the asset's point. The
  hero-number is typically **3–4×** the next-largest text.
- In any roster/bar, the **value ≥ its label** (the Bloomberg/FT inversion that
  makes the number the star).
- Parallel list items share one size/weight/casing. One casing rule per element
  class. No footnotes, no asterisks.

### Palette (semantic roles)

Rule: **max 2 categorical story colors OR one ≤5-stop sequential ramp +
neutrals. Decoration color budget = 0.** Test in grayscale.

| Token | Hex | Use |
|---|---|---|
| `--lep-surface-0` | `#0a0e14` | Deepest broadcast canvas / hero field. |
| `--lep-surface-1` | `#141820` | Card / panel surface. |
| `--lep-surface-2` | `#181e28` | Elevated / hover surface. |
| `--lep-border` | `#1e2530` | Divider on dark. |
| `--lep-ink-100` | `#f9fafb` | Headlines, hero numbers on dark. |
| `--lep-ink-200` | `#e0e0e0` | Subhead / body on dark. |
| `--lep-ink-muted` | `#9ca3af` | Orientation / recessed labels (the "orientation" semantic). |
| `--lep-ink-source` | `#666666` | Source / caption corner text. |
| `--lep-data-primary` | `#4fb3ff` | **THE** single-series data color. Default for one-metric bars / choropleth base. |
| `--lep-data-accent` | `#ffb23f` | The one bar / point / region that tells the story. TV-safe orange. |
| `--lep-accent-interactive` | `#3b82f6` | Hover / focus / active chrome. |
| `--lep-live-fresh` | `#22c55e` | Live-data fresh pill. |
| `--lep-live-stale` | `#f87171` | Live-data stale pill. |
| `--lep-alert` | `#ef4444` | Alert / error. |
| `--lep-tele-default` | `#ff3b30` | Default telestration stroke (TV-safe red, not pure `#FF0000`). |
| `--lep-tele-halo` | `rgba(0,0,0,0.45)` | Soft dark halo behind a telestration stroke. |
| `--lep-halo-white` | `#ffffff` | Universal label halo. |

Legacy aliases (`--lep-broadcast-0..3`, `--lep-ink-300/400`, `--lep-accent`)
still resolve, so older recipes don't break — but new bundles use the semantic
names above.

**Sequential ramp** (`--lep-ramp-1..5`, choropleths ≤5 classes, colorblind-safe,
dark = more): `#deebf7 → #9ecae1 → #6baed6 → #3182bd → #08519c`.

**Categorical pair** (when color encodes a 2-way category): `--lep-data-primary`
+ `--lep-data-accent`. Avoid red/green together (colorblind).

### Label halos

| Token | Use |
|---|---|
| `--lep-halo-featured` | Strong, low-blur shadow stack for featured (story) map labels. |
| `--lep-halo-orientation` | Thin halo for recessed orientation labels. |
| `--lep-halo-white` | The white halo color itself. |

Dark-text + white-halo is the only label treatment that survives an arbitrary
choropleth color + codec re-compression. See `direction.md` §6 for the two-tier
map-label grammar.

### Translucent overlays

`--lep-overlay-legend` (legend chip backgrounds), `--lep-overlay-pill` (LIVE /
status pills, marquee-label backdrops), `--lep-overlay-card` (floating cards over
imagery / maps).

### Named on-screen regions + safe area

The DLS encodes the on-screen geography as tokens (direction §4). Critical
content (text, data, foreground panels) lives in the **composition zone**; ambient
layers (basemaps, background media, choropleths) run **full-bleed** through the
presenter column.

| Token | Value | Meaning |
|---|---|---|
| `--lep-stage-w` / `--lep-stage-h` | 1920 / 1080 | Authoring canvas. |
| `--lep-comp-zone-w` | 1574px | x0 → 1574. Critical-content region. |
| `--lep-presenter-col` / `--lep-presenter-col-x` | 18% / 1574px | Right ~18% presenter column (body + nav rail). No critical content; ambient layers pass through. |
| `--lep-title-safe-inset` / `--lep-title-safe-inset-y` | 90px / 54px | Title-safe insets, computed against the comp zone. |
| `--lep-scrim-min` / `--lep-scrim-max` | rgba(10,14,20,0.55) / 0.78 | Background-media scrim opacity floor/ceiling (§5.4). |

Spacing scale (`--lep-space-1..6`: 8 / 16 / 24 / 36 / 54 / 90 px) for stacks and
gaps. **Presenter-operated controls** (steppers, toggles) go top-right near the
nav (direction §5.15) — never center/bottom.

### Telestration

`--lep-tele-width-default: 8px` (@1080 default stroke; producer-editable, min
4px / max 16px), `--lep-tele-default` (color), `--lep-tele-halo` (dark halo).
Map bundles set `telestrator: "map"` for geo-anchored strokes; non-map bundles
use the default raster (PixiJS) telestrator.

### Radii, shadow, motion

`--lep-radius-xs/sm/md/lg/full` (4 / 6 / 8 / 14 / 999 px). `--lep-shadow-sm/md/lg`.
`--lep-duration-fast/med/slow` (120 / 240 / 560 ms) + `--lep-ease-out` /
`--lep-ease-inout`.

---

## Helpers baked into the lib

`lib/helpers.js` exposes the global `leporello`:

- `fitStage(selector?)` — scale a 1920×1080 `.lep-stage` to the viewport. **Not
  for maps** (full-bleed).
- `mountBackgroundMedia(opts)` — full-bleed ambient image **or** video layer +
  the mandatory legibility scrim (direction §5.4). Use it to kill dead right-field
  space rather than leaving an empty dark panel.
- `renderRoster(container, rows, opts?)` — proportional roster bars, leader
  longest, value as the hero, on-bar labels carrying the `.lep-on-bar` halo
  (direction §5.13 — "rosters encode their metric").
- `loadContent()` / `loadManifest()` / `applyVersionStamp()` — content + version
  plumbing.

`tokens.css` also ships `.lep-tabular` (tabular figures) and the
`@keyframes lep-live-pulse` live-dot (static under `prefers-reduced-motion`).

---

## DLS overrides — the sliding scale

From SKILL.md:

- **UI chrome colors** (frame, headers, navigation, base typography) — strong
  pushback. The DLS is the brand; chrome is where it lives.
- **Data-viz colors** (chart palettes, choropleth fills, status indicators) — DLS
  guidance is the default, but well-justified deviations are OK when the data
  demands it.
- **Asset-bundle chrome** (the bundle's own frame, headers within the iframe) —
  light pushback. The bundle has more flexibility here than the surrounding admin
  UI.

The type ramp and named regions are **not** on the sliding scale — those are the
structural fix the v1 DLS exists to lock in. Don't shrink a headline below the
token or move critical content into the presenter column.

---

## DLS version pinning

The skill ships a snapshot of the v1 DLS tokens at its release version (`lib/`),
and every template vendors that snapshot into its own `lib/`. So:

- Bundles are self-contained and don't depend on the live DLS at runtime.
- A token rename upstream does not break old bundles — they reference their own
  snapshot.
- Bundles authored under skill v1.5 carry v1.5's Libre Franklin + ramp; both
  render correctly forever.

This is why every template includes `lib/tokens.css` (and the woff2) directly —
it is the bundle's tokens, not a reference to a remote source of truth.

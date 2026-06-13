# Broadcast Standards

*Typography, layout, and data-viz guidelines for content destined for on-air, recorded video, or other broadcast contexts.*

This is a snapshot of the Leporello v1 broadcast design spec, embedded with the skill at release time. The authoritative direction is `docs/prelim/dls/m1/direction/direction.md` in the main Leporello repo; the numbers below are reconciled to it. **All sizes are px on the 1920 × 1080 reference, and every one of them has a token** (`--lep-size-*`). Author against the tokens, not raw values — see `design-system.md`. The old pt-based scale that lived here has been removed; it was the freelancing-of-values escape hatch the v1 DLS exists to close.

---

## Why broadcast is different

Leporello content is often built and reviewed on monitors at desk-viewing distance, but the audience experiences it on a TV from across the room, on a streaming feed compressed for bandwidth, or on a phone held at arm's length. Each of those contexts is more punishing than the design surface.

Three constraints from broadcast practice drive everything in this spec:

- **Distance.** The viewer is roughly 10 feet from a TV, or holding a phone with a 6-inch screen. The same text size that feels generous on a 27-inch monitor at two feet is small in both contexts.
- **Time.** The presenter spends 10–30 seconds with each slide. The viewer absorbs whatever is on screen in that window or not at all.
- **Cropping and compression.** Most TVs still overscan by default. Streaming compresses fine lines into mush. Anything near the edges or built from hairline strokes is lost.

> *If you would not put it on a CNN Magic Wall or MSNBC Big Board, do not put it in a Leporello broadcast slide.*

---

## Layout and named regions

Leporello slides are designed on a **1920 × 1080** canvas, scaled to the wall by
`leporello.fitStage()`. The right ~18% is the **presenter column** — the
presenter's body plus the asset-nav rail. The v1 direction (REV validated against
the demo video) draws a sharper distinction than "everything left of the nav":

- **Ambient layers** — basemaps, **background media**, choropleths — run
  **full-bleed, edge-to-edge (x 0–1920)**. The presenter stands *in front* of
  them; that's how every pro frame works. **Live MapLibre maps render full-bleed
  and are NEVER wrapped in fitStage / `transform: scale()`.**
- **Critical content** — headline, hero number, legend, data labels, foreground
  panels — stays inside the **composition zone** (x 0 → 1574) and out of the
  presenter column.

### Region dimensions (direction §4)

| Region | x | w | Token | Note |
|---|---|---|---|---|
| **Full canvas** | 0 | 1920 | `--lep-stage-w` / `-h` | 1080 tall. |
| **Composition zone** | 0 | 1574 | `--lep-comp-zone-w` | Critical-content region, left of the presenter column. |
| **Presenter column** | 1574 | ~18% | `--lep-presenter-col(-x)` | Body + nav rail. Ambient layers pass through; NO critical content. |
| **Background-media layer** | 0 | 1920 | — | Optional full-bleed image/video behind content. MUST carry a scrim (see §5.4 below). |
| **Presenter-controls zone** | top-right | — | — | Presenter-OPERATED controls (steppers, toggles) go here, near the nav — never center/bottom. |
| **Title-safe inset** | — | — | `--lep-title-safe-inset` (90px L/R), `-y` (54px T/B) | Computed against the composition zone, not the full canvas. |

### Title-safe is for everything readable

Headlines, numbers, axis labels, legends, captions — anything the viewer has to
read — must sit inside title-safe **of the composition zone**: a **90 px L/R
inset and 54 px T/B inset** against the x 0–1574 region. Use the
`--lep-title-safe-inset*` tokens.

### Critical content is left-weighted, but fills the width

Don't strand the headline/legend/hero-number at ~50–60% — critical content uses
the composition-zone width (up to x 1574), then stops. When it can't naturally
fill the primary stage, add a **background-media layer** rather than leaving a
dead dark right-third (the R1 `big-bars` / `people-panel` miss).

### Bleed is for ambient layers only

Background fills, gradients, basemaps, and the background-media layer run all the
way to the canvas edge (full 1920). They are not readable content, so overscan
doesn't matter. Decorative photo/media may reach action-safe and beyond — but no
*critical-only* content past the composition zone.

### Presenter column is exempt

The right ~18% (x 1574–1920) is the presenter's space — body + the asset-nav
rail. It does not follow the safe-area or typography rules here. **Nothing
critical in the composition zone should sit in it**; ambient layers pass through
it freely.

> *Quick check: imagine a vertical line at x = 1574. Everything left of it is the
> composition zone — critical content follows this spec. Everything right of it is
> the presenter column. Ambient layers (maps, background media) ignore the line
> and run full-bleed; critical content respects it.*

---

## Typography

### Typeface — Libre Franklin

The v1 DLS primary face is **Libre Franklin** (SIL OFL 1.1) — Franklin Gothic's
open revival, the iconic American news-graphic vernacular. It is self-hosted as a
variable `.woff2` (weights 400–900) vendored in every bundle's `lib/`, and wired
up by `var(--lep-font-sans)`. **Inter is banned** (per the brief); **Helvetica /
Roboto are fallback-only**, not a default. Avoid:

- Serif faces with thin strokes (Bodoni, Didot, Times). Hairlines disappear under
  broadcast compression.
- Display faces with eccentric letterforms or extreme weight contrast. Illegible
  at distance.
- Anything below Regular (400). Light and Thin weights are too fragile — the
  camera eats hairlines.

Enable **tabular figures** on every numeric tier (`.lep-tabular` / `tabular-nums`)
so stacked / right-aligned values lock to a grid.

### Type scale — the v1 ramp (px @ 1080, every size a token)

These are the measured v1 ramp sizes, px on the 1920 × 1080 reference. **Size from
the `--lep-size-*` token — never a literal, never pt.** They are **floors**: bigger
is usually fine, smaller almost never is. (Full table + casing/tracking in
`design-system.md`.)

| Role | Token | px@1080 | Weight | Use for |
|---|---|---|---|---|
| **Hero number** | `--lep-size-hero-number` | 150 (→200 for a lone number) | 900 | The single most important figure ($2.4M, 34%, 1,247). One per asset. |
| **Headline** | `--lep-size-headline` | 84 | 800 | The slide's one-sentence point. (`lepo-1` ran ~45px — the #1 fix.) |
| **Headline (map)** | `--lep-size-headline-map` | 72 | 800 | Headline on a full-bleed map frame. |
| **Data label** | `--lep-size-data-label` | 64 | 700–800 | Values annotated directly on bars/segments. Must be **≥** its label. |
| **Subhead** | `--lep-size-subhead` | 40 | 400–500 | One line of context under the headline. Optional. |
| **Kicker / eyebrow** | `--lep-size-kicker` | 34 | 700 | ALL-CAPS category label above the headline. |
| **Legend** | `--lep-size-legend` | 34 | 600 | Legend rows — a first-class storytelling tier, never fine print. |
| **Featured map label** | `--lep-size-label-featured` | 40 | 700 | Marquee place-labels (≤3–5 per asset, strong white halo). |
| **Orientation label** | `--lep-size-label-orientation` | 22 | 400 | Recessed basemap labels at ~0.7 opacity. |
| **Source / caption** | `--lep-size-source` | 22 | 400–500 | **Absolute floor, 22px.** Captured as metadata; OFF the frame by default (see "Sources don't render" below). |

> *Rule of thumb: if a viewer 10 feet from a 50-inch TV cannot read it without
> effort, it is too small. When in doubt, test on an actual television.*

### Hierarchy

Each slide has **one element dramatically larger than everything else** — the
slide's point. If the headline number is only slightly larger than the labels, the
slide has no center of gravity. In practice the hero number is **3–4× the
next-largest text**: a 150px (`--lep-size-hero-number`) figure against an 84px
(`--lep-size-headline`) headline lands in that range. And in any roster/bar, the
**value ≥ its label** — numbers are the star.

---

## Color

### Default palette

**Dark background, light foreground.** This is the broadcast-news convention for a reason: light-on-dark survives variation in viewer monitor calibration and ambient room light better than dark-on-light, and is more legible at distance. **Every role below is a token — use the token, not the hex** (`design-system.md` has the full set).

| Role | Token | Hex | Use |
|---|---|---|---|
| **Background** | `--lep-surface-0` | `#0a0e14` | Slide background / hero field. |
| **Foreground (primary)** | `--lep-ink-100` | `#f9fafb` | Headlines, hero numbers. |
| **Foreground (muted)** | `--lep-ink-muted` | `#9ca3af` | Subheads, orientation labels, secondary info. |
| **Data (primary)** | `--lep-data-primary` | `#4fb3ff` | Default data color. Stop here for single-series charts. |
| **Data (accent)** | `--lep-data-accent` | `#ffb23f` | The one bar / point that tells the story. |
| **Divider** | `--lep-border` | `#1e2530` | Separators. Never use for data. |

For 2-way categorical encoding use the `--lep-data-primary` + `--lep-data-accent`
pair; for choropleths use the `--lep-ramp-1..5` sequential ramp (≤5 classes,
colorblind-safe). **Max 2 categorical story colors OR one ramp + neutrals;
decoration color budget = 0.**

### Color rules for data

- **Use one color for data by default.** Add a second only when one data point needs to be called out — the story bar, the outlier, the projection.
- **Never encode meaning in color alone.** The accent color tells the viewer where to look; the chart's labels and the presenter's words tell them what it means.
- **Avoid rainbow palettes for sequential data.** They are not perceptually uniform and they exclude colorblind viewers, who are roughly 8% of any audience.
- **Avoid fully saturated red (`#FF0000`) and orange.** They can bloom and vibrate on consumer TVs and through some encoding chains. The accent orange in the default palette (`#FFB23F`) is desaturated enough to be safe.
- **Test in grayscale.** If the chart still encodes its meaning when desaturated, the color is doing visual work, not semantic work.

---

## Data visualization

### One slide, one point

This is the single biggest shift from screen-oriented Leporello content. On a dashboard, packing several related metrics into one view rewards the user, who can dwell on it. On broadcast, the viewer has 10–30 seconds and is not in control of pacing. **A slide with three charts and four bullets transmits zero of them.**

Pick the one thing the slide is for. Everything else either supports that one thing or moves to a different slide.

### Density rules

- **Headline copy:** one short sentence or a 3–5 word phrase. Anything longer is what the presenter is for.
- **Bullets**, if used at all: maximum three, each one short. Do not write paragraphs in bullets.
- **Chart labels:** annotate directly on the chart. A bar with its value sitting on top of it is read instantly; a bar with a legend swatch elsewhere is not.
- **Round numbers.** "$2.4M" reads in a second. "$2,387,491" does not. Save precision for the script or the printed brief.
- **Strip what isn't doing work.** Axis lines, tick marks, redundant legends, decorative gridlines — if removing it does not change what the viewer understands, remove it.

### Charts scale-to-fill — both axes (direction §5.7)

Bars/columns derive their **thickness + label size** from
`stage-height / series-count` (fewer series → thicker bars, bigger labels) AND the
**longest bar scales to ~75–80% of the composition-zone width**, value label just
past the bar end but still inside x 1574. Never let the max bar strand at ~50% (the
R1 `big-bars` bug). Direct-label every bar, delete axis/ticks/gridlines, sort
descending, one color unless color encodes a category. Cap ~6–7 series; pre-filter
to top-N beyond that. Use `leporello.renderRoster()` for the proportional-bar
mechanics.

### Rosters encode their metric (direction §5.13)

A people/candidate roster with a comparable value (support %, votes, count)
reinforces the ranking with **geometry** — an inline proportional bar per row,
leader longest — so the eye gets the order before reading a digit. Equal-width rows
that merely print the number waste the format. The number stays the hero (largest,
tabular); the bar is the supporting encoding. On-bar labels MUST carry a
halo/outline (`.lep-on-bar`) so the name stays legible when the bar is short and
overflows onto the dark track.

### Chart types that work on air

- **Bar charts.** Comparison is instant, no axis math required.
- **Big single numbers.** A hero figure with one line of context is the most efficient slide format that exists.
- **Simple line charts.** Two or three series maximum, with directly labeled endpoints rather than a legend.
- **Maps with one or two data layers.**

### Chart types to avoid

- **Pie charts — at all.** Sourced anti-pattern (Cleveland & McGill: length is ~1.96× more accurate to read than angle). Replace with sorted bars or a ranked stat-list. Not "≤4 slices is fine" — none.
- **Scatter plots.** They reward dwell time and have too many encoding dimensions for 15-second comprehension.
- **Stacked bars with more than three segments.** Viewers cannot estimate non-baseline segment sizes by eye.
- **Anything with two y-axes.** Always misread.
- **Sankey diagrams, treemaps, parallel coordinates,** anything else built for exploration.

> *Designer Kent Kerr's rule, originally for weather graphics, applies to all broadcast data viz: good design is not when there is nothing left to add, but when there is nothing left to remove.*

---

## Sources don't render visibly — attribution is OFF by default (direction §5.14)

The v1 direction makes this a hard default: **attribution/source is captured as
METADATA (the `.lepo` manifest + the sourcing discipline in
`editorial-standards.md` are unchanged — sourcing rigor still matters) but is NOT
drawn on the broadcast frame.** Do not render a source strip or attribution chip.
On-frame attribution covers content and reads off-brand at this scale; the
presenter cites sources verbally. It is a producer-optional element (to be
redesigned), not a default.

A broadcast graphic is not an academic paper. The viewer cannot click a footnote, will not read a numbered citation list, and is not in the room to be persuaded by transparent sourcing — they are 10 feet from a TV, watching for 15 seconds, listening to the presenter, not auditing the bundle's references.

Therefore:

- **No inline `[src-X]` superscripts** in the rendered content. Per-fact `sourceRefs` arrays stay in `content.json` (and the underlying `manifest.sources[]`) for the producer, the admin source-review UI, and the eventual presenter-notes second screen. They never render in the broadcast frame.
- **No numbered source list at the bottom of the slide.** Same reasoning. The list is metadata, not on-air content.
- **No attribution footer band inside the bundle.** The on-air shell already surfaces the asset's attribution from the admin layer outside the iframe. Repeating it inside the bundle just clutters the frame.

What sources are for:

- **Validation** — the upload pipeline requires `manifest.sources[]` to be present (may be empty for a bundle with no factual claims, like a pure-design quote card with attribution carried in the speaker block).
- **The producer** — sources are how the producer knows the bundle is defensible. They live in the manifest where the producer can audit them before broadcast.
- **The presenter** — the presenter-notes second-screen experience (when it ships; see `docs/prelim/presenter-notes.md`) will surface sources to the presenter so they can speak to them.
- **Admin review** — the admin UI shows sources alongside the asset metadata, so a reviewing producer or editor can validate sourcing before adding the bundle to a package.
- **Future iteration** — when Claude is asked to update the bundle, the existing `sources[]` and `sourceRefs` tell it what's claimed and where each claim comes from.

What sources are NOT for: the broadcast audience. The audience trusts the news organization, not its bibliography.

### The one place a citation surface IS appropriate on screen

Quote-card templates render the speaker / title / context block on screen — that is editorial framing (who said it, where, when), not a citation. It's the on-air convention for quoted speech and predates Leporello by decades. Keep it.

Other templates can carry equivalent editorial framing in the headline or subhead ("Source: NASA, May 2026" is fine as a subhead when the subhead's job is exactly that). What's never appropriate is a separate numbered citation list, inline `[src-X]` markers, or an attribution strip that duplicates the admin-level attribution.

---

## Pre-broadcast checklist

Before declaring a bundle done, the skill verifies:

1. **All readable content is inside title-safe of the composition zone** (90 px L/R, 54 px T/B against x 0–1574). Maps render full-bleed; their DLS chrome respects this.
2. **No critical content sits in the presenter column** (x ≥ 1574). Ambient layers (maps, background media) may pass through it; nothing readable.
3. **Every size, color, and inset is a `var(--lep-*)` token** — no freelanced px/pt/hex that already has a token. (The headline is `--lep-size-headline`, not a literal.)
4. **The largest element on screen is the slide's main point**, ~**3–4× the next-largest text** (at minimum 2×).
5. **No text below the ramp floor for its role**, and no weight below 400.
6. **Charts are directly annotated**; the longest bar scales to ~75–80% of the comp zone; legends removed unless they carry story (legend tier).
7. **Presenter-operated controls are top-right near the nav**, not center/bottom.
8. **No source strip / attribution chip on the frame** (§5.14) — sourcing lives in the manifest.
9. **Color is doing semantic work, not decoration.** The chart still reads in grayscale.
10. **Numbers are rounded to broadcast precision** (two significant figures for most contexts) and use tabular figures.
11. **The slide has been previewed full-screen at typical viewing distance** (or at least at full window size in `scripts/preview.sh`).

---

## A note on web accessibility

Traditional web a11y (screen readers, keyboard nav, ARIA) is **not** the primary concern for asset bundles, because they are rendered in front of a camera and consumed via video, not directly by end users. Broadcast standards above are the operative standard. ARIA / focus-management / semantic-HTML hygiene are nice-to-haves; the floor is "viewer-from-across-the-room can read it without effort."

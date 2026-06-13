# `photo-collection` template

A **candidate-roster** panel — a vertical stack of a few LARGE rows, each a
portrait tile + a proportional metric block carrying a big name and a hero value.
The "who's who" of a story on one screen, ranked by a comparable metric.

**Restyled for the v1 DLS (dlsVersion 1.5).** Primary typeface **Libre Franklin**
(SIL OFL 1.1), self-hosted as a variable woff2 in `lib/`. Authored on the
1920×1080 `.lep-stage` and scaled by `leporello.fitStage()` (this is NOT a map
template, so fitStage is correct here). Default raster (PixiJS) telestrator.

**Anchored on:** the Kornacki candidate-panel shape (see
`docs/prelim/dls/examples/img/kornacki-1`) — a vertical roster of a few large
rows, leader-first, NOT a grid of small clickable cards.

## When to use

- The story has a **cast** (people / organizations / objects) the audience should
  put faces to, AND each carries a **comparable metric** that ranks them
  (approval, vote share, capacity, etc.).
- **~4–5 of them.** A wall of faces transmits nothing on air. The render JS caps
  at 5; pick the handful that matter or split into segments.

**Don't use when:**
- It's really one person (use `stat-callout` or `quote-card`).
- There's no comparable metric to rank by — a flat "who's who" with no number is
  weaker here; consider a simpler grid or the `generic` template.
- The relationship *between* people is the point (use a diagram, not a roster).

## What's in it

```
templates/photo-collection/
├── TEMPLATE.md          this file (template docs — NOT copied into bundles)
├── README.md            per-bundle producer-ops skeleton
├── CLAUDE.md            per-bundle AI-resume skeleton
├── manifest.json        skeleton ([CLAUDE-PLACEHOLDER:*]); telestrator "default"
├── brief.md             editorial brief skeleton
├── index.html           lockup (kicker + headline) + vertical metric roster
├── content.json         kicker / headline / metricLabel / metricMax / people[] / source
│                        (ships a CONCRETE sample — replace it when authoring)
├── static/images/       placeholder-portrait.svg (UNUSED at runtime — portraits
│                        are generated in JS; kept only as a real-headshot starting point)
└── lib/                 vendored DLS: tokens.css, base.css, helpers.js,
                         libre-franklin-latin-var.woff2 (don't edit)
```

> `content.json` here is a **filled sample** ("Who's Running Northport"), matching
> the map / iran-alignment templates' convention — it's a working EXAMPLE, not a
> `[CLAUDE-PLACEHOLDER]` skeleton. Replace its values when authoring a bundle.

## Content shape

```json
{
  "kicker": "string — small uppercase eyebrow",
  "headline": "string — the panel headline",
  "metricLabel": "string — what the metric measures (e.g. 'Approval'); appended to each role line",
  "metricMax": 100,
  "people": [
    {
      "id": "string",
      "name": "string",
      "role": "string — short title/role line",
      "metric": 61,
      "metricDisplay": "61%"
    }
  ],
  "source": "string — provenance (METADATA only; never drawn on the frame)"
}
```

- **`metric`** is the comparable value each row encodes as **block width**
  (direction §5.13 — rosters encode their metric). The roster is sorted
  descending so it reads leader-first top-to-bottom and rank chips run 1..N.
- **`metricMax`** is the metric's true axis (default 100 if omitted → scales
  against the leader's value). Bar width = `metric / metricMax`, honest — a 61
  bar against a max of 100 is ~61% full, with a 38% floor so the shortest row
  still reads as a filled block carrying its name.
- **`metricDisplay`** is the preformatted hero value (the largest text in the
  row, tabular). Falls back to `metric` if omitted.
- **`source`** is provenance metadata. Per direction §5.14 attribution is **OFF**
  — it is NEVER rendered on the frame; the presenter cites it verbally.

### Portraits

Portraits are **generated in JS** (`duotonePortrait()`) — deterministic duotone
monogram tiles from each person's initials, leader keyed to `data-accent` (amber),
others to `data-primary` (blue). They are **never fabricated photos**.
`static/images/placeholder-portrait.svg` is unused at runtime. To use **real
headshots**, credit each in `manifest.sources[]` and swap the `duotonePortrait()`
call for an `<img>` from a relative `static/images/` path (background-removed
cutouts à la Kornacki read best).

### Inline content mirror

`index.html` carries an `#lep-content-inline`
`<script type="application/json">` block mirroring `content.json`. It is used
**only** when `fetch()` is blocked (the `file://` render harness, sandboxed
iframes). In production the bundle is hosted over HTTP and `content.json` loads
normally. **Keep the two in sync** when editing the cast.

## Layout (DLS rules this template follows)

- **Lockup zone** (top-left): a single "Sample · Illustrative" tag (sample
  content only), `kicker` (34px), then `headline` (84px). No filter chips, no
  per-card badges — viewers can't click; the presenter navigates via Leporello
  assets, so interactive/chrome affordances are clutter on a wall.
- **The roster** fills the **composition zone** (left of x1574), left-weighted, so
  it clears the ~18% presenter column on the right. Names read at the data-label
  tier (64px); the metric value is a true hero (96px tabular).
- **Background-media layer + scrim** (direction §4 / §5.4): a quiet low-contrast
  vignette mounted via `leporello.mountBackgroundMedia({ image, scrim: 'left' })`
  seats the lockup and kills the dead field. The mandatory scrim is added by the
  helper.
- **On-bar text halo** (direction §5.13): text riding inside the proportional bar
  uses a white glyph + dark stroke + dark shadow ring so it stays legible whether
  it sits over the bright fill OR overflows onto the dark track. Mirrors the
  vendored lib's `.lep-on-bar`.
- **Attribution OFF** (direction §5.14): `source` is metadata, never drawn.
- **Telestration:** default raster telestrator, 8px stroke (direction §7),
  overlaid by the on-air app.

> `base.css`'s generic rule `.lep-stage > :not(.lep-bg-media)` forces
> `position: relative` on every direct stage child, which clobbers the absolute
> placement of the predefined regions. `index.html` re-asserts `position:
> absolute` on `.lep-lockup` / `.lep-source` / `.pc-roster` with `.lep-stage`-
> scoped selectors (matching specificity, later in cascade). If you move those
> regions, keep the override.

## Common customizations

- **Different cast / metric:** edit `content.json` `people[]` + `metricLabel` +
  `metricMax`; mirror into the inline block. Keep ~4–5 people.
- **Real headshots:** see "Portraits" above — credit in `manifest.sources[]`.
- **Objects, not people:** the template doesn't care — `name` / `role` / `metric`
  work for ships, weapons systems, programs, etc.

## Things not to change

- The ~4–5 density (the JS caps at 5) — it's the whole point of the format
  reading on air.
- The metric-encoding (block width) + single hero value as the dominant read.
- The vendored `lib/` (incl. the Libre Franklin woff2) and the version plumbing.

## Sourcing

Any metric (and any real headshot) is factual content: keep `source` accurate in
`content.json` and credit photos in `manifest.sources[]` (`sourceRefs` per
person). Sources travel as data for editorial review; they are **not** drawn on
the frame (§5.14).

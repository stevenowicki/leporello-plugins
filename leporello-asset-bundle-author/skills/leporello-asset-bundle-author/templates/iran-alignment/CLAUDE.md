# CLAUDE.md — [CLAUDE-PLACEHOLDER:title]

Context for an AI assistant resuming work on this bundle with no prior session
memory. Read `brief.md` first for editorial intent; this holds the
implementation context that isn't obvious from the source. Also see `TEMPLATE.md`
for the full `iran-alignment` template contract + DLS rules.

## What this bundle is

[CLAUDE-PLACEHOLDER: one-paragraph orientation — that this is an `iran-alignment`
template bundle (a full-bleed alignment choropleth styled to the v1 DLS), what
region + blocs it shows, and whether it's a single static map or a multi-snapshot
stepper.]

## Where the data lives

- Content: **`content.json`** — `groups` (id/label/color), `snapshots`
  (`members`: groupId → [ISO3], plus `label` + `caption`), `bounds` (the camera
  frame), and the two-tier map labels `featuredLabels` / `orientationLabels`.
  Country geometry is NOT here.
- Geometry (live): the shared geo layer's **admin0** PMTiles, pulled at runtime
  from `<interactives-base>/geo/admin0.pmtiles` (base derived from `location`),
  keyed by `shapeGroup` (ISO-3166 alpha-3). See the geo `catalog.json`.
- Geometry (offline): a stylized regional SVG baked into `index.html`
  (`#static-map`); each path carries `data-iso` matching the live `shapeGroup`,
  so the stepper recolors it offline exactly like the live `match` expression.
- Sources: `manifest.sources[]` + `sourceRefs`. [CLAUDE-PLACEHOLDER: which source
  backs which placement.]

## Non-obvious decisions (DLS + template invariants)

- **NO `fitStage()` on the map.** The map renders full-bleed at true viewport size
  with **no transformed ancestor**. A CSS `transform: scale()` (what
  `leporello.fitStage()` applies) breaks MapLibre's pixel↔lng/lat math:
  geo-anchored markers stop tracking pan/zoom and telestration jumps on commit.
  So this bundle does NOT use `.lep-stage` / `fitStage` at all.
- **Chrome is scaled by a length unit, not a transform.** The DLS chrome (lockup,
  legend, stepper, static-label harness) lives on a separate non-scaled
  `.lep-chrome` overlay; its children are authored in DLS reference-px ×
  `var(--u)` (`--u = min(vw/1920, vh/1080)`), keeping DLS proportions on any wall
  while the map's coordinate math stays exact.
- **Map labels are geo-anchored markers.** Featured + orientation labels are
  `maplibregl.Marker`s placed by `lngLat` (in `content.json`) so they track the
  map natively. The `x`/`y` fields are ONLY used by the offline static-SVG harness.
- **Stepper is top-right (§5.15); legend bottom-left; attribution OFF (§5.14).**
  The presenter-operated snapshot stepper lives in the top-right presenter-controls
  zone (prev/next + label + dots + a caption card in that column, not over the
  focal map). There is no on-frame attribution/source strip.
- **Map is CONSTRUCTED at the story bounds (blob-flash fix).** `new
  maplibregl.Map({...})` passes `bounds: content.bounds` + `fitBoundsOptions:
  { animate: false }` so the first painted frame is already the story view. Don't
  revert to constructing at `center`/`zoom` then calling `fitBounds` in `onLoad`.
- **Gated reveal + real-feature static hand-off.** The composition is hidden
  (`body:not([data-ready])`) until the live choropleth paints; the static SVG
  fallback only shows if MapLibre / the geo tiles never load.
- Fill color is a MapLibre `match` on `shapeGroup` rebuilt per snapshot via
  `setPaintProperty` — not feature-state. `paintStatic()` mirrors the same logic
  onto the SVG paths so the stepper works offline.
- The bundle derives the interactives base by splitting its own URL on `/orgs/`.
- Colors are the DLS budget: two categoricals (`--lep-data-primary` +
  `--lep-data-accent`) + a neutral. No red/green pairing (colorblind-safe).
- [CLAUDE-PLACEHOLDER: anything bundle-specific — basemap choice, why a country
  is/ isn't colored, contested placements. Remove if nothing.]

## How to change it safely

- Edit `content.json` for groups / snapshots / membership / labels / `bounds`;
  `index.html` only for layout, the static-fallback geometry, or render tweaks.
- ISO3 codes must match the geo layer's `shapeGroup` (check the catalog if a
  country doesn't color). To make a country appear offline too, add a `data-iso`
  path to `#static-map`. Give every featured/orientation label a `lngLat` so it
  geo-anchors on the live map (and an `x`/`y` if it should also show offline).
- **Do NOT wrap the map in `.lep-stage` / `leporello.fitStage()`** — the map must
  render natively, not CSS-scaled, or markers + telestration break. Size chrome
  with `var(--u)`, never a transform on a map ancestor.
- Don't rename `window.leporelloMap` or drop `telestrator: "map"`; keep the
  `lepo-tele` postMessage receiver. Don't touch the `data-version` plumbing or
  vendored `lib/` (DLS tokens / base / helpers / Libre Franklin woff2).
- Reference DLS tokens (`var(--lep-*)`), not literals; author chrome in
  reference-px × `var(--u)`. Never author in rem or pt.
- Loop: edit → `scripts/validate.sh <dir>` → `scripts/package.sh <dir>` → upload
  (needs a Range-supporting host for the PMTiles — Leporello's bucket is fine).

## Open threads

[CLAUDE-PLACEHOLDER: deferred ideas (admin1 drill, animated stepper, contested
borders). Remove if none.]

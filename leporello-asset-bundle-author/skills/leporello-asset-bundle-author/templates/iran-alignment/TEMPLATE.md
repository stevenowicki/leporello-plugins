# `iran-alignment` template

A regional **alignment map**, restyled to the **v1 DLS** (direction 1.5): real
countries colored by which bloc / alignment they belong to, with an optional
snapshot stepper to show how alignment shifts. No inline geometry — countries
come from the shared geo layer (admin0 PMTiles), colored by ISO code. The map
renders **full-bleed** (a live MapLibre map at true viewport size); DLS chrome
(lockup, legend, stepper, geo-anchored labels) sits on a non-scaled overlay.
Telestrate on any step (manifest `telestrator: "map"`).

**Anchored on:** the "Iran Regional Alignment" wall-map — two illustrative blocs
plus a non-aligned middle, narrated and drawn on live.

## When to use

- The story is **who's aligned with whom**: blocs, axes, coalitions, sanctions
  regimes, recognition, membership.
- A handful of alignment **groups**, each a color, applied to whole countries.
- Optionally: how that alignment **changed** over time (snapshot stepper).

**Don't use when:**
- You're showing data *within* one country (use the `map` template with regions,
  or a future admin1 choropleth).
- The unit isn't a country (use `map` with custom GeoJSON).
- It's a single location/event (use `map` with markers).

## How it works

Countries are drawn from the shared geo layer's **admin0** PMTiles
(`<interactives>/geo/admin0.pmtiles`, keyed by `shapeGroup` = ISO-3166 alpha-3).
The bundle derives the interactives base from its own URL, reads
`/geo/catalog.json`, adds a `pmtiles://` vector source, and colors the fill with
a MapLibre `match` expression on `shapeGroup` built from the active snapshot's
group membership. No country geometry ships in the bundle.

A baked-in **static SVG fallback** (`#static-map` in `index.html`) mirrors the
live choropleth for offline capture (the M1 harness shot, served over `file://`
with no network). On the normal on-air path it stays hidden and the live map
wins; it only appears if MapLibre or the geo tiles never load. Each fallback
path carries `data-iso` so the stepper recolors it offline exactly like the live
`match`.

## DLS rules this template follows (direction 1.5)

- **Map is FULL-BLEED — never wrapped in `leporello.fitStage()` / `.lep-stage`.**
  A CSS `transform: scale()` on a MapLibre ancestor breaks the renderer's
  pixel↔lng/lat math: geo-anchored markers stop tracking pan/zoom and
  telestration jumps on commit. The map gets **no transformed ancestor**.
- **Chrome is scaled by a length unit, not a transform.** Lockup, legend,
  stepper, and the static-label harness live on a separate non-scaled
  `.lep-chrome` overlay whose children are authored in DLS reference-px ×
  `var(--u)` (`--u = min(vw/1920, vh/1080)`). This keeps DLS proportions on any
  wall while leaving the map's coordinate math exact.
- **Type ramp (px @1080):** kicker 34 / headline-map 72 / legend 34 /
  label-featured 40 / label-orientation 22. All authored as `calc(<px> * var(--u))`.
- **Primary typeface: Libre Franklin** (self-hosted woff2 in `lib/`, SIL OFL 1.1),
  referenced via `var(--lep-font-sans)` — never a literal font stack.
- **Two-tier map labels (§6).** *Featured* labels (Tehran, Strait of Hormuz)
  dominate at 40px-equiv with the featured halo; *orientation* labels (country /
  sea names) recede at 22px-equiv, 0.7 opacity, with the orientation halo.
- **First-class legend (bottom-left).** One row per alignment group; color carries
  meaning together with the label, never color alone.
- **Presenter controls top-right (§5.15).** The snapshot stepper lives in the
  top-right presenter-controls zone (compact prev/next + label + dots + a caption
  card in that column) — never center/bottom, so it stays clear of the focal map.
- **Attribution OFF the frame (§5.14).** No on-frame source/attribution strip;
  sources travel as data (`manifest.sources[]` + `sourceRefs`) and the presenter
  + caption carry the meaning.
- **Telestration 8px (§7).** The default geo telestrator stroke width.
- **Left-weighted legibility scrim (§5.4).** `.align-scrim` keeps the lockup +
  legend readable while the map center stays bright.
- **Colorblind-safe palette.** Two categoricals (`--lep-data-primary` +
  `--lep-data-accent`) + a neutral; no red/green pairing.

## Content shape

```json
{
  "eyebrow": "string (kicker)",
  "headline": "string (headline-map tier)",

  "basemap": { "styleUrl": "https://… (default: Carto Dark Matter, no key)" },
  "camera":  { "center": [lng, lat], "zoom": 3.7, "pitch": 0, "bearing": 0 },
  "bounds":  [[w, s], [e, n]],

  "groups": [
    { "id": "string", "label": "string (legend)", "color": "#hex" }
  ],
  "snapshots": [
    { "id": "string", "label": "string (stepper)", "caption": "string",
      "members": { "<groupId>": ["ISO3", "ISO3", ...] } }
  ],

  "featuredLabels": [
    { "text": "Strait of Hormuz", "lngLat": [lng, lat],
      "x": 1206, "y": 560, "pill": true, "kind": "primary|dot" }
  ],
  "orientationLabels": [
    { "text": "IRAN", "lngLat": [lng, lat], "x": 760, "y": 360, "sea": false }
  ],

  "unassignedColor": "rgba(...)  (countries in no group)",
  "sourceRefs": ["src-N", ...]
}
```

- **`groups`** = the alignment categories → legend + colors.
- **`snapshots`** = one or more. Each assigns countries (ISO-3166 **alpha-3**) to
  groups and carries a `label` (stepper) + `caption`. **One snapshot = a static
  alignment map; two or more = a stepper** (‹ / ›) that recolors countries and
  swaps the caption.
- **`bounds`** = the `[[w,s],[e,n]]` camera frame. The live map is **constructed
  at these bounds** (`fitBoundsOptions: { animate: false }`) so the very first
  painted frame is already the story view — this is the blob-flash fix; don't
  remove it. `camera.center`/`zoom` are the fallback only when `bounds` is absent.
- **`featuredLabels` / `orientationLabels`** = the two-tier map labels. Give every
  label a **`lngLat`** so it geo-anchors as a `maplibregl.Marker` on the live map
  (tracks pan/zoom natively — the geo-anchoring fix). The **`x`/`y`** fields are
  used ONLY by the offline static-SVG harness path; a label needs them only if it
  should also appear in an offline capture. `featuredLabels` extras: `pill` (pill
  background), `kind: "primary" | "dot"` (a colored marker dot). `orientationLabels`
  extra: `sea: true` (italic, letter-spaced, dimmer — for water bodies).
- ISO3 codes must match the geo layer's `shapeGroup`. Use the catalog's `keyFields`
  if unsure. A country not listed in any group gets `unassignedColor`.

Clicking a country (live map) shows its name + current group.

## Common customizations

- **Static map (no stepping):** ship a single `snapshot`. The prev/next bar hides;
  its caption still shows in the top-right column.
- **More blocs:** add `groups` — the legend and the color `match` grow with them.
- **Different region:** set `bounds` (and `camera` as a fallback); the geo layer is
  global, so any region works. To make countries appear in the *offline* capture
  too, add matching `data-iso` paths to `#static-map` in `index.html`.
- **Re-anchor a label:** edit its `lngLat` (live) and, if it must show offline,
  its `x`/`y` against the static map's 1920×1080 viewBox.
- **Admin1 (states/provinces):** swap the source to the catalog's `admin1` layer
  (promoteId `shapeID`) and key membership by `shapeID` instead of ISO3.

## Things not to change

- **Do NOT wrap the map in `leporello.fitStage()` / `.lep-stage`.** The map must
  render at native viewport size with no transformed ancestor, or markers +
  telestration break. Size chrome with `var(--u)`, never a transform on a map
  ancestor.
- `window.leporelloMap = map` and `telestrator: "map"` (the telestrator contract),
  plus the `lepo-tele` postMessage receiver (the cross-origin telestration bridge).
- The map-construction-at-`bounds` blob-flash fix and the gated reveal
  (`body[data-ready]`) — both prevent load-flash on asset switch.
- The shared-geo source pattern (derive base from `location`, read the catalog) —
  it keeps the bundle portable across dev / prod without hardcoded URLs.
- The `data-version` / `data-updated` plumbing and the vendored `lib/`
  (DLS tokens / base / helpers + the Libre Franklin woff2).

## Sourcing

Alignment is an **editorial claim** — who is "aligned" with whom is a judgment.
Source it (`manifest.sources[]` + `sourceRefs`) and keep the caption honest about
what the coloring asserts. Per §5.14 the bundle renders **no visible source list**
(sources travel as data); the presenter and caption carry the meaning.

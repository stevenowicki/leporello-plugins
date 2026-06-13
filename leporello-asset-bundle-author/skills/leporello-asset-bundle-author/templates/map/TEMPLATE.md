# `map` template (v1 DLS)

A MapLibre-driven custom map — full-bleed live basemap + GeoJSON regions + a **two-tier, geo-anchored label system** — that the presenter can pan, zoom, and **telestrate in geographic space**. Strokes anchor to lng/lat and re-project through pan/zoom because the manifest sets `telestrator: "map"`.

This template is restyled to the **v1 DLS** (`dlsVersion: "1.5"`): Libre Franklin type ramp, the named composition zones, attribution off-frame. The authoritative DLS spec is `docs/prelim/dls/m1/direction/direction.md`.

**Anchored on:** the "Iran Regional Alignment"-style explainer map — a basemap with a few colored regions and labeled places, narrated live — re-cast as an *ambient* full-bleed layer with a dominant featured-label tier on top.

## When to use

- The story is **geographic**: who controls what, where events happened, alignment/territory, routes, ranges.
- The presenter wants to pan/zoom and draw on the map on air.
- A handful of regions (choropleth-style fills) and/or labeled places tells the story.

**Don't use when:**
- The "map" is really a static image with pins — use `generic` with an image and absolute-positioned markers (no MapLibre overhead).
- You need a full election choropleth with drill-down, balance-of-power, year switching — that's the built-in `election-map` asset type, not a bundle.
- There's no geography — pick a non-map template.

## What's in it

```
templates/map/
├── TEMPLATE.md          this file (template docs — NOT copied into bundles)
├── README.md            per-bundle producer-ops skeleton ([CLAUDE-PLACEHOLDER:*])
├── CLAUDE.md            per-bundle AI-resume skeleton ([CLAUDE-PLACEHOLDER:*])
├── manifest.json        skeleton; telestrator: "map", externalDependencies pre-filled, dlsVersion 1.5
├── brief.md             editorial brief skeleton with map framing
├── index.html           full-bleed live MapLibre map + DLS chrome overlay + two-tier geo-anchored labels + window.leporelloMap + lepo-tele receiver
├── content.json         eyebrow / headline / subhead / basemap / camera / featuredLabels[] / orientationLabels[] / regions[] / legend
└── lib/                 vendored v1 DLS tokens, base CSS, helpers, + Libre Franklin woff2
```

The shipped `content.json` is a **worked EXAMPLE** filled with clearly-illustrative "demo geography" (an abstract strait). When authoring a real bundle, replace every value with real content — it is not a placeholder skeleton, it's a reference of the shape.

## Content shape

```json
{
  "eyebrow": "string — kicker (34px@1080)",
  "headline": "string — the map's point (headline-map tier, 72px@1080)",
  "subhead": "string — optional one-line support (40px@1080)",

  "basemap": { "styleUrl": "https://… MapLibre-compatible style.json (dark dataviz preferred)" },

  "camera": {
    "bounds": [[west, south], [east, north]],
    "fitPadding": 80,
    "center": [lng, lat], "zoom": 6.4, "pitch": 0, "bearing": 0
  },

  "featuredLabels": [
    { "text": "string", "lngLat": [lng, lat], "x": 1080, "y": 548, "pill": true, "primary": true },
    { "text": "string", "lngLat": [lng, lat], "x": 1030, "y": 430, "dot": true }
  ],

  "orientationLabels": [
    { "text": "REGION", "lngLat": [lng, lat], "x": 660, "y": 250 },
    { "text": "Sea name", "lngLat": [lng, lat], "x": 380, "y": 560, "sea": true },
    { "text": "Place", "lngLat": [lng, lat], "x": 470, "y": 470, "dot": true }
  ],

  "regions": [
    { "id": "string", "label": "string", "color": "#hex",
      "geometry": { "type": "Polygon" | "MultiPolygon", "coordinates": [...] } }
  ],

  "legend": { "rows": [ { "label": "string", "color": "#hex | rgba()" } ] },

  "source": "metadata only — NOT drawn (direction §5.14)",
  "sourceRefs": ["src-N", ...]
}
```

### The two-tier label system (direction §6)

Map labels are split into two tiers and the design depends on the contrast between them — do not flatten them to the same size (that was the original failure this restyle fixes):

- **`featuredLabels[]`** — the story labels. Rendered at the **`label-featured`** tier (40px@1080 / weight 700 / heavy halo). Keep to **2–3**. `pill: true` gives the marquee label a pill backdrop; `primary: true` enlarges/accents its dot. These dominate the basemap and carry the point in under 3 seconds.
- **`orientationLabels[]`** — recessed basemap labels at the **`label-orientation`** tier (22px@1080 / weight 400 / ~0.7 opacity). They only orient; they must never compete with the featured tier. `sea: true` renders italic small-caps for water bodies; `dot: true` adds a small place dot.

**Both tiers are geo-anchored.** Each label is a `maplibregl.Marker` placed by its `lngLat` `[lng, lat]`, so it pans/zooms WITH the live map (mirrors `iran-alignment`). Place the `lngLat` on the real basemap feature.

**`x`/`y` are the offline fallback.** Each label also takes `x`/`y` in the **1920×1080 reference field** that position the SAME label over the static SVG fallback, so the offline render (and the headless validation harness, which can't composite live WebGL) is never blank. Set both `lngLat` (live) and `x`/`y` (static).

### Camera

Prefer **`bounds`** (`[[west,south],[east,north]]`) + `fitPadding` so the frame fits the area of interest on any wall size; `center`/`zoom` are the fallback when no bounds are given. The frame is held hidden (chrome only) until the post-`fitBounds` `idle` fires, then revealed (no load flash).

### Regions + legend

- **`regions[]`** render as semi-transparent fills + a matching outline, colored by `color` (plain GeoJSON, `[lng, lat]` order). The skill generates these — from natural-language descriptions, a GeoJSON the producer supplies, or by tracing known boundaries. Keep vertex counts modest; broadcast maps don't need survey precision.
- **`legend.rows[]`** — one `{ label, color }` per row, rendered bottom-left at the `legend` tier (34px@1080). Color meaning is **never carried by color alone** — the legend + the presenter's words carry it.

## DLS rules this template follows

- **Maps render FULL-BLEED — never scaled.** The live MapLibre map (`#map`) renders at **native viewport px with no `transform: scale()` ancestor**. A CSS scale breaks MapLibre's pixel↔lng/lat math: markers stop tracking the map on pan/zoom and telestration strokes jump on commit. Only the **chrome overlay** (`.lep-chrome-stage` — lockup + legend + scrims) is `leporello.fitStage()`-scaled, on a separate layer that does NOT contain the map. A `ResizeObserver` calls `map.resize()` on frame resize.
- **Composition zone (x < 1574).** The lockup (top-left) and legend (bottom-left) stay inside the composition zone so the presenter owns the right ~18% column. The scrim only darkens behind chrome, never the whole frame.
- **Attribution is OFF-frame (§5.14).** No on-frame source strip. `source` in content.json is metadata only — it is NOT drawn. Sources live in `manifest.sources[]`, joined to claims via `sourceRefs`. (The basemap provider's own attribution control stays on the map — legally required for real tiles — as the compact control bottom-right.)
- **Telestration is 8px (§7)** and geo-anchored — see the handshake below.
- **Type ramp** comes entirely from the vendored `lib/tokens.css` + `lib/base.css` (kicker 34 / headline-map 72 / subhead 40 / data-label 64 / legend 34 / label-featured 40 / label-orientation 22 / source 22, all px@1080). No invented hex/px at storytelling tiers. The primary typeface is **Libre Franklin** (self-hosted `lib/libre-franklin-latin-var.woff2`, SIL OFL 1.1).

> Note: `rosters-encode-metric` (§5.13) and the `background-media` layer/scrim are general DLS rules that apply to *roster*/*media* templates; the `map` template's "media layer" is the live basemap itself and it has no roster, so those fields don't appear in this template's `content.json`.

## Telestrator handshake

The manifest sets `telestrator: "map"`. On air, Leporello mounts the map telestrator (not the default raster one) over the iframe.

- **In-document case:** the on-air `MapTelestrator` reads `iframe.contentWindow.leporelloMap` to project strokes through the map.
- **Cross-origin case:** because the bundle iframe is served from `interactives.*` (a different origin than `live.*`), the parent can't read `contentWindow` — so `index.html` also embeds the **`lepo-tele` postMessage receiver**: the parent overlay forwards pointer events over the `lepo-tele` channel, the bundle owns the MapLibre projection and renders strokes (canvas-hybrid live draw → GL line layer on pointer-up, 8px) in lng/lat, and the parent owns per-asset persistence.

**Don't rename or remove `window.leporelloMap = map`** or the `lepo-tele` receiver — they're the contract.

## Common customizations

- **No regions, labels only:** leave `regions` empty; the fills/outlines auto-skip.
- **Start at a bbox:** set `camera.bounds` to the area of interest (preferred over center/zoom).
- **Different region opacity / outline weight:** edit the `lep-regions-fill` / `lep-regions-outline` paint in `index.html`.
- **Globe projection:** add `projection: { type: 'globe' }` to the `new maplibregl.Map({...})` options (MapLibre 5.x).
- **Richer basemap:** swap `basemap.styleUrl` for an origin-restricted MapTiler dark style with an inlined key.

## Things not to change

- `window.leporelloMap = map` and the `lepo-tele` postMessage receiver (the telestrator contract).
- `telestrator: "map"` in the manifest.
- The **full-bleed map + scaled-chrome-only model** — never wrap `#map` in `.lep-stage` / `leporello.fitStage()` / any `transform: scale()` ancestor.
- The static-SVG fallback under `#map` (keeps the frame non-blank offline / pre-tiles).
- The `data-version` / `data-updated` plumbing and the vendored `lib/`.

## Basemap

Default in the example is a **dark, low-label dataviz** style — it reads best behind colored regions and the featured-label tier; a busy street basemap fights the choropleth. For broadcast, set `basemap.styleUrl` to a MapTiler style with an **inlined** key (bundles are self-contained — no env var to read) and **origin-restrict the key** in the MapTiler dashboard to the live + admin subdomains. Any MapLibre-compatible `style.json` works (Carto, Stadia, self-hosted).

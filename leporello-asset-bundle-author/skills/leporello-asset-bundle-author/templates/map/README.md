# [CLAUDE-PLACEHOLDER:title]

[CLAUDE-PLACEHOLDER: one sentence — what this map shows on air.]

Built from the `map` template, restyled to the **v1 DLS** (Libre Franklin type ramp, composition-zone lockup + legend, presenter-safe right column, attribution off-frame). A full-bleed live MapLibre basemap with a dominant two-tier geo-anchored label system. Editorial intent lives in `brief.md`; AI-resumption context in `CLAUDE.md`.

## Data sources

[CLAUDE-PLACEHOLDER: where the boundaries / marker positions / territorial claims come from, in plain language — this mirrors `manifest.sources[]`. Note anything that goes stale (e.g. shifting front lines) and when it was last verified.]

## Preview locally

```bash
npx serve .          # or, from the skill:  scripts/preview.sh <this-dir>
```

Open the served URL. The map fills the frame (16:9) and is pannable/zoomable.

## Update this bundle

- Map chrome + labels live in **`content.json`**: `eyebrow`/`headline`/`subhead` (the top-left lockup), `featuredLabels[]` + `orientationLabels[]` (the two geo-anchored label tiers — see `TEMPLATE.md`), `legend.rows[]`, plus live-map `regions[]` (GeoJSON + color + label), `camera`, `basemap.styleUrl`. Edit there, not in `index.html`.
- To re-aim the opening view, change `camera.bounds` (preferred) or `camera.center` / `camera.zoom`.
- To change the basemap, set `basemap.styleUrl` (a MapTiler style needs an inlined, origin-restricted key — see `TEMPLATE.md`).
- The live MapLibre map renders **full-bleed at native viewport px** — never wrap `#map` in `leporello.fitStage()` / a `transform: scale()` ancestor. Only the lockup/legend chrome overlay is scaled.
- `source` in `content.json` is metadata only — it is NOT drawn on the frame (direction §5.14).
- After editing, re-validate and re-package (run from the asset-bundle-author skill):
  ```bash
  scripts/validate.sh <this-dir>     # expect 0 errors
  scripts/package.sh  <this-dir>     # writes <slug>.lepo
  ```
- Re-upload the `.lepo` in the Leporello admin (or via the MCP `publish_bundle` flow). Each upload is a new immutable version.

## Files

- `index.html` — entry point; renders the full-bleed MapLibre map + DLS chrome overlay + geo-anchored labels from `content.json`; exposes `window.leporelloMap` and the `lepo-tele` postMessage receiver for on-air telestration
- `content.json` — the editable chrome, labels, legend, and live-map content
- `manifest.json` — bundle metadata + `sources[]`; `telestrator: "map"`, `dlsVersion: "1.5"`
- `brief.md` — editorial intent · `CLAUDE.md` — AI-resumption context
- `lib/` — vendored v1 DLS tokens + base + helpers + Libre Franklin woff2 (snapshot at authoring time; don't edit)

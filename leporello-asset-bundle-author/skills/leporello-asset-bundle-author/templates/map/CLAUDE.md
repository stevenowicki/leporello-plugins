# CLAUDE.md — [CLAUDE-PLACEHOLDER:title]

Context for an AI assistant resuming work on this bundle with no prior session memory. Read `brief.md` first for editorial intent; this file holds the implementation context that isn't obvious from the source.

## What this bundle is

A `map`-template bundle restyled to the **v1 DLS** (`dlsVersion: "1.5"`): a full-bleed live MapLibre map (ambient layer) with a Libre Franklin lockup top-left, a dominant pair of geo-anchored featured place-labels over recessed orientation labels, and a first-class legend bottom-left — lockup + legend kept inside the composition zone (x < 1574) so the presenter owns the right ~18% column. No on-frame source strip (direction §5.14 — attribution is metadata only). [CLAUDE-PLACEHOLDER: which area this depicts, which regions/featured labels, what they represent.]

## Where the data lives

- Content: **`content.json`** — `eyebrow`/`headline`/`subhead` (lockup), `featuredLabels[]` + `orientationLabels[]` (the two map label tiers, **geo-anchored by `lngLat`**, with `x`/`y` static-SVG fallback positions), `legend.rows[]`, `source` (metadata only — not drawn), plus live-map `regions[]` (GeoJSON geometry + color + label) / `camera` (`bounds` preferred, `center`/`zoom` fallback) / `basemap.styleUrl`.
- Sources: `manifest.sources[]`, joined to claims via `sourceRefs`. [CLAUDE-PLACEHOLDER: annotate which source backs which boundary/position, with `accessedAt` notes for anything that can shift.]

## Non-obvious decisions

[CLAUDE-PLACEHOLDER: choices that would otherwise live only in the original conversation — where the GeoJSON came from and how it was simplified, the color encoding's meaning, basemap choice, any inlined MapTiler key (and that it's origin-restricted), camera framing rationale. Remove this section if nothing's non-obvious.]

## How to change it safely

- Edit `content.json` for chrome / labels / legend / live-map content; edit `index.html` / CSS only for layout/paint changes.
- **Do not rename or remove `window.leporelloMap = map`** or the `lepo-tele` postMessage receiver — the on-air `MapTelestrator` reads `leporelloMap` (same-origin) and parity-drives the `lepo-tele` receiver (cross-origin) to anchor strokes in lng/lat. Keep `telestrator: "map"` in the manifest.
- **Never wrap `#map` in `.lep-stage` / `leporello.fitStage()` or any `transform: scale()` ancestor** — the map MUST render full-bleed at native viewport px (a scale breaks MapLibre's coordinate math: markers stop tracking, strokes jump). Only the chrome overlay (`.lep-chrome-stage`) is scaled.
- Place featured/orientation labels with `lngLat` (NOT stage px) so they track the live map; also give each an `x`/`y` (1920×1080 reference field) for the static SVG fallback. Re-fit `camera.bounds` to the real area of interest when swapping geography.
- Don't touch the `data-version` / `data-updated` plumbing or the vendored `lib/` (v1 DLS tokens + base + helpers + Libre Franklin woff2).
- Loop: edit → `scripts/validate.sh <dir>` → `scripts/package.sh <dir>` → re-upload.

## Open threads

[CLAUDE-PLACEHOLDER: known TODOs, deferred ideas, things the producer wanted but punted (e.g. globe projection, fitBounds to a bbox, animated camera). Remove this section if none.]

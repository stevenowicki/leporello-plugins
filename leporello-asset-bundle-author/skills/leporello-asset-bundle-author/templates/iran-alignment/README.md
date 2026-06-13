# [CLAUDE-PLACEHOLDER:title]

[CLAUDE-PLACEHOLDER: one sentence — what alignment this map shows on air.]

Built from the `iran-alignment` template, styled to the Leporello v1 DLS
(Libre Franklin type, two-tier map labels, first-class legend, top-right
presenter stepper, attribution off the frame). The map renders full-bleed.
Editorial intent lives in `brief.md`; AI-resumption context in `CLAUDE.md`.

## Data sources

[CLAUDE-PLACEHOLDER: where each country's alignment comes from, in plain language
(mirrors `manifest.sources[]`). Alignment is a judgment — say what framework /
reporting backs it, and note anything contested or time-sensitive.]

Country shapes come from Leporello's shared geo layer (geoBoundaries CGAZ, CC BY
4.0) — not from this bundle.

## Preview locally

```bash
npx serve .          # or, from the skill:  scripts/preview.sh <this-dir>
```

Note: previewing needs the shared geo layer reachable at `<host>/geo/` and a
server that supports HTTP Range requests (`npx serve` does; Python's
`http.server` does not). Uploaded to Leporello it just works.

## Update this bundle

- Alignment lives in **`content.json`**: `groups` (colors + legend), `snapshots`
  (which countries — ISO-3166 alpha-3 — are in each group, + a label + caption),
  `bounds` (the camera frame), and the two-tier map labels (`featuredLabels` /
  `orientationLabels`, each geo-anchored by `lngLat`). Edit there, not `index.html`.
- One snapshot = static map; add more to create a time stepper.
- After editing: `scripts/validate.sh <dir>` then `scripts/package.sh <dir>`,
  and re-upload (or MCP `publish_bundle`). Each upload is a new version.

## Files

- `index.html` — entry point; renders countries from the shared geo layer,
  colored by `content.json`; exposes `window.leporelloMap` for telestration
- `content.json` — the editable alignment content
- `manifest.json` — bundle metadata + `sources[]`; `telestrator: "map"`
- `brief.md` — editorial intent · `CLAUDE.md` — AI-resumption context
- `lib/` — vendored DLS tokens + base + helpers + the Libre Franklin woff2 (don't edit)

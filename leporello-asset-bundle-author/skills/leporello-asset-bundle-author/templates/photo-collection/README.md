# [CLAUDE-PLACEHOLDER:title]

[CLAUDE-PLACEHOLDER: one sentence — whose faces this ranks on air, and by what metric.]

Built from the `photo-collection` template (candidate-roster) on the v1 DLS
(Libre Franklin, named regions, attribution-off). Editorial intent lives in
`brief.md`; AI-resumption context in `CLAUDE.md`.

## Data sources

[CLAUDE-PLACEHOLDER: where the ranking metric comes from + its credit/license,
and (if real headshots are used) where each comes from. Sources are metadata —
the presenter cites them verbally; they are NOT drawn on the frame (§5.14).]

## Preview locally

```bash
npx serve .          # or, from the skill:  scripts/preview.sh <this-dir>
```

Open the served URL. Renders at 16:9 (1920×1080).

## Update this bundle

- The cast lives in **`content.json`** (`people[]`: name / role / metric /
  metricDisplay, plus `metricLabel` / `metricMax` / `kicker` / `headline` /
  `source`). Edit there, not `index.html`.
- `index.html` mirrors `content.json` in an inline `#lep-content-inline` block
  for the offline render harness — **keep the two in sync**.
- Portraits are generated in JS (duotone monogram placeholders). For real,
  sourced headshots, drop them in **`static/images/`**, credit each in
  `manifest.sources[]`, and swap the `duotonePortrait()` call for an `<img>`.
- Keep it to ~4–5 people (the render caps at 5). After editing:
  `scripts/validate.sh <dir>` then `scripts/package.sh <dir>`, and re-upload
  (each upload is a new version).

## Files

- `index.html` — entry point; renders the metric roster from `content.json`
- `content.json` — the editable cast + metric (ships a sample to replace)
- `manifest.json` — bundle metadata + `sources[]`
- `static/images/` — placeholder (unused at runtime; for optional real headshots)
- `brief.md` — editorial intent · `CLAUDE.md` — AI-resumption context
- `lib/` — vendored DLS tokens + base CSS + helpers + Libre Franklin woff2 (don't edit)

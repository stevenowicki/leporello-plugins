# CLAUDE.md — [CLAUDE-PLACEHOLDER:title]

Context for an AI assistant resuming work on this bundle with no prior session
memory. Read `brief.md` first for editorial intent; this holds the
implementation context that isn't obvious from the source.

## What this bundle is

[CLAUDE-PLACEHOLDER: one-paragraph orientation — that this is a `photo-collection`
(candidate-roster) bundle: a vertical stack of a few LARGE rows, sorted
leader-first, each a portrait tile + a proportional metric block carrying the
name and a hero value. Say whose cast it shows and what metric ranks them.]

Built on the v1 DLS: Libre Franklin (self-hosted woff2 in `lib/`), the named
regions (lockup top-left, roster filling the composition zone left of the ~18%
presenter column), background-media + scrim, and attribution OFF (§5.14 — the
`source` is metadata, never drawn). Rows ENCODE their metric as block width
(§5.13). NOT a grid of clickable cards — no filters, no per-card badges.

## Where the data lives

- Content: **`content.json`** — `people[]` (id / name / role / metric /
  metricDisplay), `metricLabel`, `metricMax`, plus `kicker` / `headline` /
  `source`.
- Inline fallback: an `#lep-content-inline` `<script type="application/json">`
  block in `index.html` mirrors `content.json` — used ONLY when `fetch()` is
  blocked (file:// harness / sandboxed iframes). **Keep it in sync.**
- Portraits: **generated in JS** (`duotonePortrait()`), not files.
  `static/images/placeholder-portrait.svg` is unused at runtime.
- Sources: `manifest.sources[]` ( + `sourceRefs` if you add real headshots).

## Non-obvious decisions

[CLAUDE-PLACEHOLDER: density choices, who's included/excluded, metricMax rationale.
Remove if nothing non-obvious.] Standing implementation notes:
- Bars scale against `metricMax` (the metric's true axis), NOT the leader's
  value — a 61 bar against max 100 is ~61% full, honest; a 38% min-width floor
  keeps the shortest row's name legible inside its block.
- `base.css`'s `.lep-stage > :not(.lep-bg-media)` forces `position: relative` on
  stage children; `index.html` re-asserts `position: absolute` on `.lep-lockup` /
  `.lep-source` / `.pc-roster`. Keep that override if you move regions.
- The render caps the cast at 5 and sorts descending so rank chips run 1..N.

## How to change it safely

- Edit `content.json` for the cast + metric; mirror any change into the inline
  `#lep-content-inline` block in `index.html`.
- Keep ~4–5 people (broadcast density). Don't touch the vendored `lib/`.
- For real headshots, credit them in `manifest.sources[]` and replace the
  `duotonePortrait()` call with an `<img>` from a relative `static/images/` path.
- Loop: edit → `scripts/validate.sh <dir>` → `scripts/package.sh <dir>` → upload.

## Open threads

[CLAUDE-PLACEHOLDER: deferred ideas (real-headshot cutout path, a secondary
per-person stat). Remove if none.]

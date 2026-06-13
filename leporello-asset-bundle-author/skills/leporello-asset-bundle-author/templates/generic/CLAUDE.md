# CLAUDE.md — [CLAUDE-PLACEHOLDER:title]

Context for an AI assistant resuming work on this bundle with no prior session memory. Read `brief.md` first for editorial intent; this file holds the implementation context that isn't obvious from the source.

## What this bundle is

[CLAUDE-PLACEHOLDER: one-paragraph orientation — that this is a `generic`-template bundle, and what it renders on air.]

## Where the data lives

- Content: **`content.json`** — free-form JSON; `index.html` reads a fixed set of keys. [CLAUDE-PLACEHOLDER: list the keys this bundle's index.html reads.]
- Sources: `manifest.sources[]`, joined to claims via `sourceRefs`. [CLAUDE-PLACEHOLDER: annotate which source backs which claim, with `accessedAt` notes for anything that can change.]

## Non-obvious decisions

Built on the v1 DLS (`docs/prelim/dls/m1/direction/direction.md`): styling resolves
to `--lep-*` tokens from `lib/tokens.css` + `lib/base.css`; type, the named regions
(lockup / hero / roster / presenter column), the roster's metric encoding (§5.13),
and the background-media + scrim machinery all live in the shared `base.css`. The
template `<style>` does layout only — don't hardcode hex/px a token already covers,
and keep critical content inside the composition zone (x < 1574). Attribution is off
inside the frame (§5.14). [CLAUDE-PLACEHOLDER: choices specific to THIS bundle —
the accent choice, any DLS deviation and why, layout adjustments, anything
surprising. Remove this section if there's nothing non-obvious.]

## How to change it safely

- Edit `content.json` for facts; edit `index.html` / CSS for layout.
- Don't touch the `data-version` / `data-updated` plumbing on the root element, or the vendored `lib/`.
- Generic has no fixed schema — if you add a content key, wire it into `index.html` too.
- Keep critical content left of x1574 (composition zone) and out of the title-safe
  edges; ambient layers (background) may run full-bleed. Don't edit the vendored
  `lib/` (incl. the Libre Franklin woff2).
- Loop: edit → `scripts/validate.sh <dir>` → `scripts/package.sh <dir>` → re-upload.

## Open threads

[CLAUDE-PLACEHOLDER: known TODOs, deferred ideas, things the producer wanted but punted. Remove this section if none.]

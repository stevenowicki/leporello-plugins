# CLAUDE.md — [CLAUDE-PLACEHOLDER:title]

Context for an AI assistant resuming work on this bundle with no prior session memory. Read `brief.md` first for editorial intent; this file holds the implementation context that isn't obvious from the source.

## What this bundle is

[CLAUDE-PLACEHOLDER: one-paragraph orientation — that this is a `timeline`-template bundle restyled to the v1 DLS, and what it renders on air: a top-left lockup over up to five full-width beat bands reading top-to-bottom (compact date meta line + a 56px title hero each), atop an ambient full-bleed background-media layer with a left scrim.]

## Where the data lives

- Content: **`content.json`** — `events[]` (`date` / `title` / `accent` / `sourceRefs`)
  + `dateRange` + `dateMode` (`"month"` | `"day"`) + `eyebrow` / `headline` / `subhead`
  + optional `source` (string, metadata only — NOT drawn) + `background.image`.
  (The original swim-lane mechanic — `lanes[]`, per-lane color, `description` — is not in
  the v1 render path.)
- Sources: `manifest.sources[]`, optionally joined per-event via `sourceRefs`. Per DLS
  §5.14 these are metadata only — never drawn on frame; the presenter cites verbally.
  [CLAUDE-PLACEHOLDER: annotate which source backs which date/fact, with `accessedAt`
  notes for anything that can change.]

## Non-obvious decisions

[CLAUDE-PLACEHOLDER: choices that would otherwise live only in the original conversation — hardcoded values, DLS deviations and why, layout adjustments, the accent choice, anything surprising. Remove this section if there's nothing non-obvious.]

## How to change it safely

- Edit `content.json` for facts; edit `index.html` / CSS for layout.
- Don't touch the `data-version` / `data-updated` plumbing on the root element, or the vendored `lib/`.
- Keep 3–5 beats; at most one `accent: true`. Don't fix crowding with positioning hacks — cut beats. (No swim-lanes in this template.)
- Loop: edit → `scripts/validate.sh <dir>` → `scripts/package.sh <dir>` → re-upload.

## Open threads

[CLAUDE-PLACEHOLDER: known TODOs, deferred ideas, things the producer wanted but punted. Remove this section if none.]

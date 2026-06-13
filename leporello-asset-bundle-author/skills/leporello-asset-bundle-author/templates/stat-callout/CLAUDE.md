# CLAUDE.md — [CLAUDE-PLACEHOLDER:title]

Context for an AI assistant resuming work on this bundle with no prior session memory. Read `brief.md` first for editorial intent; this file holds the implementation context that isn't obvious from the source.

## What this bundle is

A `stat-callout`-template bundle restyled to the **v1 DLS** (Libre Franklin, broadcast type ramp, composition zone, ambient background-media + mandatory scrim; attribution does not render on air, §5.14). On air it renders one giant hero number as the visual center of gravity, with a kicker + headline lockup top-left, an optional trend delta on the number's shoulder, a hero label beneath, and one muted context line at the bottom. [CLAUDE-PLACEHOLDER: name the specific number + what story this instance tells.]

## Where the data lives

- Content: **`content.json`** — `eyebrow`, `headline`, `stat.value` / `stat.label`, optional `comparison.value` / `comparison.label`, `context`, `background.{image,scrim}`, `source`, `sourceRefs`.
- The same content is **mirrored** into an inline `<script type="application/json" id="inline-content">` in `index.html` — the `file://` fallback (browsers block `fetch` of sibling files over `file://`). Keep the two in sync when hand-editing facts.
- Sources: `manifest.sources[]`, joined to claims via `sourceRefs`. [CLAUDE-PLACEHOLDER: annotate which source backs which claim, with `accessedAt` notes for anything that can change.]

## Non-obvious decisions

[CLAUDE-PLACEHOLDER: choices that would otherwise live only in the original conversation — hardcoded values, DLS deviations and why, layout adjustments, the accent choice, anything surprising. Remove this section if there's nothing non-obvious.]

## How to change it safely

- Edit `content.json` for facts; mirror into the inline `#inline-content` block in `index.html`. Edit `index.html` / CSS for layout.
- Don't touch the `data-version` / `data-updated` plumbing, the vendored `lib/` (incl. the Libre Franklin woff2 and the base.css region-helper specificity fix), or the mandatory background scrim.
- Keep critical content inside the composition zone (x < 1574); only the background-media layer runs full-bleed.
- One stat, one point. If a second number is creeping in, it's probably a second asset.
- Loop: edit → `scripts/validate.sh <dir>` → `scripts/package.sh <dir>` → re-upload.

## Open threads

[CLAUDE-PLACEHOLDER: known TODOs, deferred ideas, things the producer wanted but punted. Remove this section if none.]

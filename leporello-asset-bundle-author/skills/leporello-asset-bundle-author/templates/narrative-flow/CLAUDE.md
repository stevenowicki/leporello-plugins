# CLAUDE.md — [CLAUDE-PLACEHOLDER:title]

Context for an AI assistant resuming work on this bundle with no prior session memory. Read `brief.md` first for editorial intent; this file holds the implementation context that isn't obvious from the source. Also see `TEMPLATE.md` for the full `narrative-flow` template contract + DLS rules.

## What this bundle is

[CLAUDE-PLACEHOLDER: one-paragraph orientation — that this is a `narrative-flow`-template bundle restyled to the v1 DLS, which renders ONE step at a time as a full broadcast frame (giant hero step number + headline-tier title + one line of context) with a progress rail bottom-left, and what sequence of steps it walks through.]

## Where the data lives

- Content: **`content.json`** — `eyebrow` (kicker) / `headline` (rail header) / `subhead` (carried, not rendered on-frame) / `source` (optional bottom-right strip) / `steps[]`. Each step: `number?` / `title` / `railLabel?` (short rail label, falls back to `title`) / `description` (one tight sentence) / `accent` / `sourceRefs`.
- Sources: `manifest.sources[]`, joined to step claims via `sourceRefs`. [CLAUDE-PLACEHOLDER: annotate which source backs which step, with `accessedAt` notes for anything that can change. If the bundle is illustrative, say so and leave `sources` empty.]

## Non-obvious decisions (DLS + template invariants)

- **One step per frame, not all-at-once.** Each step is its own clean broadcast frame; the presenter taps the stage to advance (loops) or taps a rail pip to jump. This is the v1-DLS / LEPO-38 staging — do not revert to a row of small cards.
- **The hero number is the focal figure.** A lone step number per frame earns the hero-number tier (≥150px); it tints `data-accent` orange on the accented step, `data-primary` blue otherwise.
- **`fitStage` is correct here.** No live map → the 1920×1080 canvas is scaled via `leporello.fitStage('.lep-stage')`. (Only map templates must avoid `fitStage`.)
- **Background-media + mandatory left scrim (§5.4).** `static/backdrop.svg` is mounted via `helpers.mountBackgroundMedia({ scrim: 'left' })` to fill the dead right field. Swap the image to a producer asset by changing that call.
- **Attribution OFF (§5.14).** No on-frame credit strip; the optional `source` line is content provenance only.
- **Accent is a string attribute.** The number/rail color switches on `.flow-frame[data-accent='true']`, so the JS sets `setAttribute('data-accent','true')` (not `toggleAttribute`).
- [CLAUDE-PLACEHOLDER: anything bundle-specific — hardcoded values, the accent choice, any DLS deviation and why. Remove this section if there's nothing non-obvious.]

## How to change it safely

- Edit `content.json` for facts; edit `index.html` / CSS for layout.
- Keep **3–6 steps**; at most one `accent: true`. Each `description` is ONE tight sentence — two start to crowd the frame.
- Give long-titled steps a short `railLabel` so the bottom rail stays compact.
- Reference DLS tokens (`var(--lep-*)`), not literal px. Keep the self-hosted Libre Franklin woff2 in `lib/` — don't substitute a system/webfont.
- Don't touch the `data-version` / `data-updated` plumbing, the manifest's pre-filled technical fields (`dlsVersion: "1.5"`, `telestrator: "default"`), or the vendored `lib/`.
- Loop: edit → `scripts/validate.sh <dir>` → `scripts/package.sh <dir>` → re-upload.

## Open threads

[CLAUDE-PLACEHOLDER: known TODOs, deferred ideas, things the producer wanted but punted. Remove this section if none.]

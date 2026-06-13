# CLAUDE.md — [CLAUDE-PLACEHOLDER:title]

Context for an AI assistant resuming work on this bundle with no prior session memory. Read `brief.md` first for editorial intent; this file holds the implementation context that isn't obvious from the source.

## What this bundle is

A `quote-card`-template bundle on the **v1 Leporello DLS**. On air it renders a single large pull-quote at the headline tier with a left accent rule, a broadcast lower-third attribution block (speaker / role / context), and a full-bleed ambient background with a mandatory legibility scrim. Everything critical sits left of the presenter column (x1574). [CLAUDE-PLACEHOLDER: one-paragraph orientation — what THIS bundle's quote is and what segment it serves.]

## Where the data lives

- Content: **`content.json`** — `eyebrow`, `quote`, `speaker`, `speakerTitle`, `context`, `source` (+ optional `backgroundImage` / `backgroundScrim`, + `sourceRefs`). `index.html` also keeps an inline JSON mirror of `content.json` for `file://` previews — keep the two in sync.
- Sources: `manifest.sources[]`, joined to claims via `sourceRefs`. [CLAUDE-PLACEHOLDER: annotate which source backs the quote — primary transcript/filing preferred — with `accessedAt` notes for anything that can change.]

## Non-obvious decisions

[CLAUDE-PLACEHOLDER: choices that would otherwise live only in the original conversation — hardcoded values, DLS deviations and why, layout adjustments, the accent choice, anything surprising. Remove this section if there's nothing non-obvious.]

## How to change it safely

- Edit `content.json` for facts; edit `index.html` / CSS for layout.
- Don't touch the `data-version` / `data-updated` plumbing on the root element, or the vendored `lib/`.
- The speaker block is editorial framing, not a citation — don't add visible `[src-N]` markers.
- Loop: edit → `scripts/validate.sh <dir>` → `scripts/package.sh <dir>` → re-upload.

## Open threads

[CLAUDE-PLACEHOLDER: known TODOs, deferred ideas, things the producer wanted but punted. Remove this section if none.]

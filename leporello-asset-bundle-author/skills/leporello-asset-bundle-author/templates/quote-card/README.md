# [CLAUDE-PLACEHOLDER:title]

[CLAUDE-PLACEHOLDER: one sentence — what this bundle shows on air.]

Built from the `quote-card` template. Editorial intent lives in `brief.md`; AI-resumption context in `CLAUDE.md`.

## Data sources

[CLAUDE-PLACEHOLDER: where the facts/numbers come from, in plain language — this mirrors `manifest.sources[]`. Note anything that goes stale and when it was last verified. If the bundle makes no factual claims, say so.]

## Preview locally

```bash
npx serve .          # or, from the skill:  scripts/preview.sh <this-dir>
```

Open the served URL. The bundle renders at 16:9 (1920×1080).

## Update this bundle

- Text and numbers live in **`content.json`** — edit there, not in `index.html`.
- The quote, speaker, and context live in `content.json` — keep the quote short enough to read in one breath on air.
- After editing, re-validate and re-package (run from the asset-bundle-author skill):
  ```bash
  scripts/validate.sh <this-dir>     # expect 0 errors
  scripts/package.sh  <this-dir>     # writes <slug>.lepo
  ```
- Re-upload the `.lepo` in the Leporello admin (or via the MCP `publish_bundle` flow). Each upload is a new immutable version.

## Files

- `index.html` — entry point; renders `content.json`
- `content.json` — the editable content
- `manifest.json` — bundle metadata + `sources[]`
- `brief.md` — editorial intent · `CLAUDE.md` — AI-resumption context
- `lib/` — vendored v1 DLS tokens + helpers + self-hosted Libre Franklin woff2 (snapshot at authoring time; don't edit)

Styled to the v1 Leporello DLS — Libre Franklin, the named composition regions (quote held left of the presenter column), and a full-bleed ambient background with the mandatory scrim. On-screen attribution is off; the speaker / role / context block carries the editorial framing.

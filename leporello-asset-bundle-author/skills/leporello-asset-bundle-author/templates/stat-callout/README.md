# [CLAUDE-PLACEHOLDER:title]

[CLAUDE-PLACEHOLDER: one sentence — what this bundle shows on air.]

Built from the `stat-callout` template. Editorial intent lives in `brief.md`; AI-resumption context in `CLAUDE.md`.

## Data sources

[CLAUDE-PLACEHOLDER: where the facts/numbers come from, in plain language — this mirrors `manifest.sources[]`. Note anything that goes stale and when it was last verified. If the bundle makes no factual claims, say so.]

## Preview locally

```bash
npx serve .          # or, from the skill:  scripts/preview.sh <this-dir>
```

Open the served URL. The bundle renders at 16:9 (1920×1080).

Built to the v1 DLS direction (Libre Franklin, the broadcast type ramp, the composition zone with a clear presenter column, a full-bleed ambient background layer + mandatory scrim; attribution does not render on air).

## Update this bundle

- Text and numbers live in **`content.json`** — edit there, not in `index.html`. If you hand-edit `content.json`, mirror the change into the inline `#inline-content` block in `index.html` so the `file://` fallback stays in sync.
- The headline number and its label live in `content.json` — one number is the point; resist adding a second.
- After editing, re-validate and re-package (run from the asset-bundle-author skill):
  ```bash
  scripts/validate.sh <this-dir>     # expect 0 errors
  scripts/package.sh  <this-dir>     # writes <slug>.lepo
  ```
- Re-upload the `.lepo` in the Leporello admin (or via the MCP `publish_bundle` flow). Each upload is a new immutable version.

## Files

- `index.html` — entry point; renders `content.json` (with an inline `file://` fallback)
- `content.json` — the editable content (hero stat, headline, context, background, source)
- `manifest.json` — bundle metadata + `sources[]`
- `brief.md` — editorial intent · `CLAUDE.md` — AI-resumption context
- `lib/` — vendored v1 DLS tokens + base CSS + helpers + Libre Franklin woff2 + `bg-relief.svg` (snapshot at authoring time; don't edit)

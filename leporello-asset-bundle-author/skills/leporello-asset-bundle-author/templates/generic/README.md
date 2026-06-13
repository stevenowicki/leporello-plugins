# [CLAUDE-PLACEHOLDER:title]

[CLAUDE-PLACEHOLDER: one sentence — what this bundle shows on air.]

Built from the `generic` template. Editorial intent lives in `brief.md`; AI-resumption context in `CLAUDE.md`.

## Data sources

[CLAUDE-PLACEHOLDER: where the facts/numbers come from, in plain language — this mirrors `manifest.sources[]`. Note anything that goes stale and when it was last verified. If the bundle makes no factual claims, say so.]

## Preview locally

```bash
npx serve .          # or, from the skill:  scripts/preview.sh <this-dir>
```

Open the served URL. The bundle renders at 16:9 (1920×1080), styled to the v1
Leporello DLS (Libre Franklin, the broadcast type ramp, the named on-screen
regions). Per DLS §5.14, no attribution renders inside the frame — the on-air shell
surfaces `manifest.attribution` outside the iframe.

## Update this bundle

- Text and numbers live in **`content.json`** — edit there, not in `index.html`.
- This bundle is free-form — `content.json` holds whatever keys `index.html` reads. Keep the keys stable; renaming one can break the render.
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
- `lib/` — vendored v1 DLS tokens + base styles + helpers + self-hosted Libre
  Franklin (snapshot at authoring time; don't edit)

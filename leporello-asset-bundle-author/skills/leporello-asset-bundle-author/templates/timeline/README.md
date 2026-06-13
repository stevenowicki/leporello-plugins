# [CLAUDE-PLACEHOLDER:title]

[CLAUDE-PLACEHOLDER: one sentence — what this bundle shows on air.]

Built from the `timeline` template. Editorial intent lives in `brief.md`; AI-resumption context in `CLAUDE.md`.

## Data sources

[CLAUDE-PLACEHOLDER: where the facts/numbers come from, in plain language — this mirrors `manifest.sources[]`. Note anything that goes stale and when it was last verified. If the bundle makes no factual claims, say so.]

## Preview locally

```bash
npx serve .          # or, from the skill:  scripts/preview.sh <this-dir>
```

Open the served URL. The bundle renders at 16:9 (1920×1080).

## Update this bundle

- Text and dates live in **`content.json`** — edit there, not in `index.html`.
- Beats live in `content.json > events[]` (`date` / `title` / `accent`). Aim for **3–5**;
  the renderer sorts chronologically and shows the first five. Set `accent: true` on the
  single most important beat (at most one). Don't fix crowding with positioning — cut beats.
- `dateMode`: `"month"` renders "MON YYYY"; `"day"` renders "MON D, YYYY".
- `background.image`: path to the ambient background (defaults to `./lib/timeline-bg.png`;
  keep any replacement low-contrast — it sits behind text under a left scrim).
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
- `lib/` — vendored v1 DLS tokens + base CSS + helpers, the Libre Franklin woff2, and the
  ambient background image (snapshot at authoring time; don't edit)

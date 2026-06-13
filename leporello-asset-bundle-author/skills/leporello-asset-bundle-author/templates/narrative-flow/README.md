# [CLAUDE-PLACEHOLDER:title]

[CLAUDE-PLACEHOLDER: one sentence — what this bundle shows on air.]

Built from the `narrative-flow` template (v1 DLS). On air it shows **one step at a time** as a full broadcast frame — a giant step number, a headline-tier title, and one line of context — with a progress rail bottom-left. The presenter taps the stage to advance (loops) or taps a rail pip to jump. Editorial intent lives in `brief.md`; AI-resumption context in `CLAUDE.md`.

## Data sources

[CLAUDE-PLACEHOLDER: where the facts/numbers come from, in plain language — this mirrors `manifest.sources[]`. Note anything that goes stale and when it was last verified. If the bundle makes no factual claims, say so.]

## Preview locally

```bash
npx serve .          # or, from the skill:  scripts/preview.sh <this-dir>
```

Open the served URL. The bundle renders at 16:9 (1920×1080).

## Update this bundle

- Text and numbers live in **`content.json`** — edit there, not in `index.html`.
- Steps live in `content.json > steps[]` — keep to 3–6; more than that and the broadcast viewer can't track them. At most one step with `accent: true`. Each step can carry a short `railLabel` for the bottom rail (falls back to its title).
- After editing, re-validate and re-package (run from the asset-bundle-author skill):
  ```bash
  scripts/validate.sh <this-dir>     # expect 0 errors
  scripts/package.sh  <this-dir>     # writes <slug>.lepo
  ```
- Re-upload the `.lepo` in the Leporello admin (or via the MCP `publish_bundle` flow). Each upload is a new immutable version.

## Files

- `index.html` — entry point; renders `content.json`
- `content.json` — the editable content (eyebrow / headline / subhead / source / steps[])
- `manifest.json` — bundle metadata + `sources[]`
- `static/backdrop.svg` — the self-contained ambient background-media layer (swap for a producer image/video)
- `brief.md` — editorial intent · `CLAUDE.md` — AI-resumption context
- `lib/` — vendored DLS tokens + base CSS + helpers + Libre Franklin woff2 (snapshot at authoring time; don't edit)

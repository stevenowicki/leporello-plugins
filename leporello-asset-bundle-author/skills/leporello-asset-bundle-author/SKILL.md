---
name: leporello-asset-bundle-author
description: Use this skill whenever the user wants to create, edit, or update a Leporello asset bundle (`.lepo`) — interactive content for live broadcast. Trigger on mentions of Leporello, .lepo, "asset for [show]", "bundle for [show]", "build me a graphic for", "interactive about", or any request to author broadcast content with journalistic standards. Also use when iterating on an existing asset bundle.
---

# Leporello Asset Bundle Author

This skill produces Leporello asset bundles — interactive broadcast content
built under journalistic standards: sourced facts, no fabrication, visible
uncertainty, broadcast-grade legibility.

## Design system — author token-first

> ⚠️ **The two rules this skill most often breaks. Verify BOTH before you call a bundle
> done — never preview-as-final, show the producer, or upload until they hold:**
>
> 1. **TYPEFACE IS LIBRE FRANKLIN — via the vendored `lib/`, never a system stack.**
>    The #1 failure is authoring fresh HTML with `-apple-system` / `system-ui`. **Start
>    EVERY bundle — template OR bespoke — by copying a template's `lib/` (the woff2 +
>    `tokens.css` + `base.css`) into your bundle and `<link>`-ing it**, then resolve all
>    type through `var(--lep-font-sans)`. If `scripts/dls_check.mjs` reports a `font`
>    violation, you skipped this — fix it, don't ship it.
> 2. **THE GRAPHIC IS THE PRESENTER'S BACKDROP, NOT THE SCRIPT.** The presenter explains;
>    the graphic gives them something to point at. So: a **short headline (a few words,
>    not a sentence)**, **≤1** subhead, and **≤1–2** on-graphic markers. **Strip the
>    explanatory annotations, descriptive captions, and "here's what happened" labels** —
>    that's the presenter's job, and stripping it is what makes our work read as
>    *broadcast*, not a magazine infographic. When in doubt, cut text.

Every bundle is rendered against the **v1 Leporello DLS** (authoritative
direction: `docs/prelim/dls/m1/direction/direction.md`; tokens snapshot in the
skill's and each template's `lib/`). The single rule that governs all visual
authoring:

> **Everything sizes, colors, and spaces from `var(--lep-*)`. Never invent a value
> that already has a token.** There is no pt/px escape hatch — that freelancing of
> values is exactly the failure the v1 DLS was built to stop.

Internalize before authoring:

- **Typeface: Libre Franklin** (SIL OFL 1.1), self-hosted variable woff2 in each
  bundle's `lib/`, via `var(--lep-font-sans)`. Not Inter (banned); Helvetica/Roboto
  fallback-only. Tabular figures on every numeric tier.
- **Type ramp — px @ the 1920×1080 reference, each a token** (`--lep-size-*`):
  kicker 34 / headline 84 / headline-map 72 / subhead 40 / hero-number 150 /
  data-label 64 / legend 34 / label-featured 40 / label-orientation 22 / source 22.
  One element dramatically largest (hero ≈ 3–4× the next); value ≥ its label.
- **Named regions** (direction §4): the **composition zone** (x 0 → 1574) holds all
  critical content; the right **~18% presenter column** (x 1574 → 1920) holds the
  presenter's body + nav rail and takes **no** critical content. An optional
  full-bleed **background-media layer** (image OR video, with a MANDATORY scrim)
  fills dead space; **ambient layers run full-bleed** through the presenter column.
  **Presenter-operated controls go top-right** near the nav, never center/bottom.
- **Composition rules** (direction §5): one takeaway per asset; charts
  **scale-to-fill both axes** (§5.7); **rosters encode their metric** with a
  proportional bar per row (§5.13); **no pie charts**; **attribution is OFF on the
  frame** — captured as metadata, never drawn (§5.14).
- **Maps render FULL-BLEED** — a live MapLibre map is NEVER wrapped in
  `fitStage()` / `transform: scale()`; only the non-map `.lep-stage` templates are.
- **Map labels are two-tier** (direction §6): featured (40px, story) dominates
  recessed orientation (22px, ~0.7 opacity). **Telestration default stroke 8px**
  (§7).

Use `lib/helpers.js` — `fitStage()`, `mountBackgroundMedia()`, `renderRoster()` —
rather than re-implementing these. Details: `references/design-system.md`.

## Posture

The skill is a **research and authoring collaborator**, not a passive editor.
It actively helps the producer gather content, find sources, and shape the
visual — while deferring to the producer on subject-matter judgment and
editorial direction. The producer course-corrects; the skill proposes.

The skill is **opinionated about ethics** (won't fabricate, won't bury
uncertainty) and **flexible about everything else**.

## Supervise your own output — the producer should not have to fix the design

The producer is the editor, not the design QA. Generated content that *looks* fine
routinely misses DLS-specific discipline — wrong typeface, content pushed into the
presenter's right column, an on-frame attribution strip — and a human shouldn't have
to catch those. So **you supervise your own output before you ship it** (Workflow step
11): render it, run the automated DLS gate, critique it by eye against the rubric, and
remediate until it's clean. Never hand the producer a bundle you haven't put through
the gate.

**Complex requests → decompose with sub-agents.** Some requests are genuinely involved
(multi-asset packages, a bespoke interactive, dense data work, a novel layout). When a
request is more than a single straightforward bundle, plan it first, then use sub-agents
to parallelize — e.g. one to gather/verify sourcing, one or more to build, and an
**independent critic** sub-agent that judges the render against `references/dls-rubric.md`
with fresh eyes. Keep the producer in the loop on editorial calls; keep the design
supervision on your side.

## First-run setup — check dependencies BEFORE building

The first time you use this skill in a new environment (and any time a script
errors with "command not found"), **run `scripts/check_deps.sh` first.** It verifies
the producer-installed prerequisites (**Node.js** + **Python 3**, plus a bash shell
with `zip`/`unzip`) and auto-installs the rest (Playwright + a Chromium engine for the
render-gate). The producer is likely **not** a developer — assume nothing is installed.

- If it exits non-zero, it printed exactly what's missing. **STOP and give the producer
  those install instructions** (point them at `references/dependencies.md`) — do not try
  to limp ahead; the validate/lint/render steps will just fail later.
- If a tool truly can't be present (e.g. native Windows without WSL), say so plainly and
  fall back to what works: you can still author + upload via MCP and rely on **server-side
  validation at upload**, but the local **render-gate (`dls_check.mjs`) and lint won't run**
  — tell the producer their bundle wasn't fully checked locally.

Full dependency list (what they install vs. what's automatic): `references/dependencies.md`.

## Workflow — for any new asset bundle

1. **Identify the bundle type.** Read `references/template-catalog.md`. Pick
   the closest template, or default to `generic` for novel content types.
   Templates are starting points, not constraints — if nothing fits cleanly,
   ask the producer "should I start from `generic` and build novel?" and proceed.

2. **Read the template's docs** at `templates/<type>/TEMPLATE.md` to
   understand its layout and customization hooks. (Skip for `generic` —
   it's intentionally minimal.) Note: `TEMPLATE.md` documents the *template*;
   the `README.md` and `CLAUDE.md` in the same folder are per-bundle
   skeletons you fill in and ship (see step 5).

3. **Read `references/editorial-standards.md` and
   `references/broadcast-standards.md` BEFORE writing any factual content.**
   Non-negotiable. These shape what the skill will and won't do.

4. **Copy the template (or scaffold a novel structure)** to a working
   directory. Don't regenerate from scratch when a template applies — modify it.

5. **Draft the editorial brief (`brief.md`).** Before generating any
   content, write the bundle's `brief.md` capturing the producer's ask,
   editorial framing, template choice + rationale, and any constraints
   the producer has set. This is the durable record of editorial intent
   — it travels with the bundle forever. Keep it producer-readable
   Markdown. See `references/bundle-format.md` ("Editorial brief")
   for the section list. Update it as the producer steers the work in
   later steps; the brief is a living document until the bundle is
   packaged. **Always set `manifest.brief: "brief.md"`** for new bundles.

   The brief is one of **three resumability docs** every bundle ships at its
   root (see `references/bundle-format.md` → "Resumability artifacts"):
   `brief.md` (editorial *why*), `README.md` (producer *how-to-run*), and
   `CLAUDE.md` (AI *how-to-resume*). The template scaffolds `README.md` and
   `CLAUDE.md` as skeletons with `[CLAUDE-PLACEHOLDER:*]` markers — you fill
   them in at finalize (step 8). Don't ship the skeletons.

6. **Research and propose content collaboratively.** This is the heart of
   the skill. The skill actively helps gather and verify content:

   - **Search for relevant sources** — web search, primary documents,
     expert-recommended sources, prior Leporello bundles for context.
   - **Propose content claims with citations attached** — every fact paired
     with a `manifest.sources[]` entry and a `sourceRefs` per claim.
   - **The producer reviews each item** — accepts, edits, replaces a source,
     or rejects.
   - **Defer to producer expertise on obscure or subject-matter topics.**
     Push back if a proposed source looks unreliable; accept the producer's
     override when they justify it (recorded in `editorialReview.notes`).
   - **If the producer wants to include a claim with no verifiable source,
     ask, don't refuse.** It may be a primary-source observation, editorial
     commentary, or producer-attributed opinion — tag accordingly
     (`type: "producer-note"` or similar) and surface visually as such.
   - **Refuse to fabricate** — invented quotes, statistics, dates, names,
     attributions are non-negotiable refusals. No override.

7. **Apply broadcast-graphics standards, token-first.** Build against the v1 DLS
   ramp + regions (above) — size from `--lep-size-*`, color from the palette
   tokens, keep critical content inside the composition zone, run ambient layers
   full-bleed. Contrast that survives compression, hierarchy that holds at viewing
   distance, prefer-visual-over-text composition. Push back on text-heavy
   compositions (the `clint-demo-hints` examples are reference cases of what's too
   much text). See `references/broadcast-standards.md` and
   `references/design-system.md`.

8. **Finalize the resumability docs.** Before packaging, bring all three
   root docs to match what actually shipped:
   - `brief.md` — content decisions, source decisions, any visual
     deviations from DLS defaults, and the v1 iteration-log entry.
   - `README.md` — fill the producer-ops skeleton: one-line description,
     the real data sources, how to update this specific bundle.
   - `CLAUDE.md` — fill the AI-resume skeleton: where the data lives,
     non-obvious decisions, template-specific gotchas, open threads.

   **Replace every `[CLAUDE-PLACEHOLDER:*]` marker** — the validator warns
   on any that remain. Set `manifest.readme: "README.md"` and
   `manifest.claude: "CLAUDE.md"` (or rely on the root-file convention).
   All three docs should match the artifact at the moment of packaging.

9. **Preview locally.** Run `scripts/preview.sh` (under the hood: `npx serve .`)
   so the producer can see the rendered bundle in a browser before committing
   to upload. Iterate visual tweaks here.

10. **Validate + lint (mechanical gates).** Run `scripts/validate.sh` (manifest
    schema, paths, JSON) — it also runs `scripts/lint_tokens.py`, which flags
    hardcoded hex/px at storytelling tiers (everything must resolve to `var(--lep-*)`).
    Fix every violation. If `leporello.validate_bundle_local` MCP is available, run it too.

11. **Supervise — the DLS gate (MANDATORY before upload).** Do NOT ship a bundle that
    hasn't passed this. It catches the discipline that "looks fine" output misses:
    - **a. Automated DLS check:** `node scripts/dls_check.mjs <bundle-dir>` — renders the
      bundle (HEADED; headless renders live maps black) and checks the rules a static lint
      can't: **Libre Franklin actually applied** (not a system/Inter/Roboto stack),
      **critical content clears the right ~18% presenter column** (x < 1574), **no on-frame
      attribution**, **headline is broadcast-big**. Non-zero exit = violations — fix each.
    - **b. Vision critique:** render + screenshot the bundle and judge it against
      `references/dls-rubric.md` (hierarchy, restraint, fills-the-width, numbers-as-heroes,
      no overlaps, "would Steve present this?"). Name every FAIL and fix it.
    - **c. Loop a → b → fix until both are clean.** A bundle is shippable only when it is.

12. **Package.** Run `scripts/package.sh` to produce the `.lepo` ZIP.

13. **Upload (if requested).** Deploy via MCP. The bundle bytes never go through
    a tool call (a `.lepo` can be many MB) — you upload the raw file to a
    presigned URL with the shell, then register it. Three steps:
    - **Pick the destination org.** Call `leporello.list_orgs()` to see the
      orgs you can deploy to (each is `{slug, name, id}`). If the producer
      named one ("deploy it to Center of Gravity"), match it and pass the
      matching **slug** as `org`. If exactly one org comes back, you may omit
      `org` — it defaults to that one. If several come back and the producer
      didn't say which, **ask** before uploading (don't guess the tenant).
    - **Get an upload URL.** Call `leporello.create_bundle_upload(filename="<name>.lepo")`.
      It returns `{upload_url, staging_key}`.
    - **Stream the bytes with the shell — do NOT read the `.lepo` into the
      conversation.** Run: `curl -T <path-to>.lepo "<upload_url>"` (the `-T`
      uploads the raw file; quote the URL — it has `&`s).
    - **Publish.** Call `leporello.publish_bundle(staging_key="<key>", org="<slug>")`.
      It validates + unpacks + registers and echoes `org_slug`, `version_number`,
      `created` (true = new bundle, false = new version of an existing slug), and
      `hosted_url` — confirm to the producer *which org* it landed in.
    - If `publish_bundle` returns `org_required`, you can reach more than one
      org: surface `available_orgs` and ask which. If it returns
      `validation_failed`, fix the bundle and start again from
      `create_bundle_upload` (the staged upload is discarded on failure).
    - If MCP isn't configured, instruct the producer to drag-drop the `.lepo`
      into Leporello's admin UI (admin is already scoped to their org).

## Workflow — iterating on an existing asset bundle

1. **Identify the starting point.** Ask:
   - Work from the latest version published to Leporello, OR
   - Work from a local copy (producer may have unpublished local edits
     in progress).

   Default to asking; don't assume.

   To pull a published bundle down: call `leporello.download_bundle(id_or_slug,
   org="<slug>")` (optionally `version=<n>`). It returns a presigned
   `download_url` + `filename` — fetch and unpack with the shell, NOT through a
   tool call: `curl -o <filename> "<download_url>" && unzip <filename> -d <dir>`.
   The archive includes the `brief.md` / `README.md` / `CLAUDE.md` you wrote, so
   read those first to recover the editorial intent before changing anything.

2. **Apply the requested change as a targeted patch.** Do NOT regenerate.

   - **Content change** ("update the death toll to 47") → modify the
     relevant content file. Prompt: "Should the source change as well, or
     is the new value supported by the existing source?" If existing source
     no longer supports the claim, gather a new one collaboratively.
   - **Visual change** ("make the bar chart red") → modify `index.html` or
     CSS. Preserve content files.
   - **Add/remove items** → modify the appropriate content array.

3. **Update `brief.md` to reflect the new current state.** Rewrite the
   sections that the change affects (e.g., if the death-toll figure
   changes, update "Content decisions" and "Source decisions" to match).
   The brief is a current-state document, not an archaeology of every
   prior version — earlier versions' framing is already preserved in
   their own `.lepo` bundles. Then **append one entry to the iteration
   log** describing what changed and why:

   ```
   - v<n> (YYYY-MM-DD): <one-line summary of the diff and the reason>
   ```

   The iteration log is the only section that is append-only.

   Also update `README.md` and `CLAUDE.md` if the change affects them —
   e.g. a new data source belongs in README's "Data sources" and CLAUDE's
   "Where the data lives"; a non-obvious new design choice belongs in
   CLAUDE's "Non-obvious decisions." Same current-state model as the brief.

4. **Update `manifest.editorialReview.notes`** with a short summary of
   what changed and why. (The brief is the long story; this field is
   the short attestation.)

5. **Preview locally** if the change has visual impact.

6. **Re-validate, re-package, re-publish** as a new version using the same
   three-step upload flow as step 13 of the create workflow:
   `create_bundle_upload` → `curl -T <file> "<upload_url>"` → `publish_bundle`.
   Publishing find-or-creates by `manifest.bundleId`, so re-publishing the same
   slug just adds a new version (`created` comes back false). Pass the same `org`
   the bundle already lives in (omit only if you can reach exactly one).
   `list_bundles()` / `get_bundle()` report each bundle's `owner_org_slug` if you
   need to confirm which org a slug belongs to.

## What this skill does NOT do

- **Does not generate Leporello packages or shows.** Asset bundles are
  content; packages are container constructs managed in admin.
- **Does not host backends.** Bundles can call external APIs the producer
  controls; this skill does not provision any server-side infrastructure.
- **Does not invent facts, quotes, statistics, dates, names, or
  attributions.** Hard refusal. No override.
- **Treats DLS overrides on a sliding scale:**
  - **UI chrome colors** (frame, headers, navigation, base typography) —
    strong pushback. The DLS is the brand; chrome is where it lives.
  - **Data-viz colors** (chart palettes, choropleth fills, status indicators)
    — DLS guidance is the default, but well-justified deviations are OK
    when the data demands it. Skill accepts producer-justified overrides.
  - **Asset-bundle chrome** (the bundle's own frame, headers within the
    iframe) — light pushback. The bundle has more flexibility here than
    the surrounding admin UI.
- **Does not silently strip citations.** If a patch removes a sourced fact,
  the corresponding `manifest.sources[]` entry stays unless the producer
  explicitly asks to remove it.

## Reference files (load on demand)

- `references/bundle-format.md` — structural rules for `.lepo` files
- `references/editorial-standards.md` — sourcing, uncertainty, corrections
- `references/broadcast-standards.md` — broadcast-graphics rules reconciled to the
  v1 DLS (the px@1080 ramp, named regions, scale-to-fill charts, no pie, attribution
  off-frame)
- `references/design-system.md` — v1 DLS token vocabulary (Libre Franklin, the
  `--lep-*` ramp/palette/region tokens); author token-first, no escape hatch
- `references/template-catalog.md` — template selection guide (the restyled v1
  templates: full-bleed live maps, roster photo-collection, rebuilt timeline +
  narrative-flow)
- `references/dls-rubric.md` — the supervision checklist applied by eye to a render
  (step 11b); the perceptual backstop to `scripts/dls_check.mjs`
- `references/dependencies.md` — what the producer must install (Node, Python) vs. what
  the skill auto-installs (Playwright/Chromium); run `scripts/check_deps.sh` first

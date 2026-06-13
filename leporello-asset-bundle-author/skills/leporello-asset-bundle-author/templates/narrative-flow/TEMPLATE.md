# `narrative-flow` template

Step-by-step explainer, restyled to the **v1 DLS** (M2 pass — the LEPO-38 rebuild).
Reads as "step 1 → step 2 → step 3 → step 4," but **one step at a time**, each staged as
its own clean broadcast frame rather than a row of cramped cards.

> This file is template documentation. It is **NOT** copied into authored bundles. The
> per-bundle docs are `brief.md` / `README.md` / `CLAUDE.md` (skeletons with
> `[CLAUDE-PLACEHOLDER:*]` markers the skill fills).

## What changed in the v1 DLS rebuild

The pre-DLS template crammed every step into a single row of small equal-width cards
(28px titles, 22px body, chevron connectors) — the anti-broadcast failure mode (type
below the readable floor, no focal point). The rebuild treats **each step as its own full
broadcast frame**:

- A giant **step number** at the hero-number tier (one lone figure per frame, so it earns
  the tier).
- A **headline-tier** step title and a single **subhead-tier** line of context.
- A first-class **progress rail** bottom-left (legend tier) — one pip per step, the active
  one lit, plus a position-in-flow fill bar.
- An ambient **background-media** layer fills the otherwise-dead right field, under the
  mandatory left scrim.

The presenter advances step-by-step (tap the stage to go next + loop, or tap a rail pip to
jump). The active step owns the composition zone; the rest recede.

## When to use

- The story is a **sequence of discrete steps**, each one idea, where order matters.
- The connections between steps matter (one thing leads to the next).
- The presenter wants to walk the audience through the steps one at a time.

**Don't use when:**
- The story is fundamentally chronological with dates that matter (use `timeline`).
- The "steps" are an unordered bulleted list (use `generic` and write the list).
- You have more than ~6 steps — the viewer can't track that many. Split into multiple
  assets or pick a denser visualization.

## What's in it

```
templates/narrative-flow/
├── TEMPLATE.md      this file (template docs — NOT copied into bundles)
├── README.md        per-bundle producer-ops skeleton ([CLAUDE-PLACEHOLDER:*])
├── CLAUDE.md        per-bundle AI-resume skeleton ([CLAUDE-PLACEHOLDER:*])
├── brief.md         per-bundle editorial-brief skeleton ([CLAUDE-PLACEHOLDER:*])
├── manifest.json    skeleton — [CLAUDE-PLACEHOLDER:*] for slug/title/etc.;
│                    technical fields (dlsVersion 1.5, telestrator "default",
│                    no external deps) pre-filled
├── index.html       one-step-per-frame renderer + progress rail + tap-to-advance
├── content.json     SAMPLE content (a fine starting example — overwrite per bundle)
├── static/
│   └── backdrop.svg self-contained ambient background-media layer (no external deps)
└── lib/             vendored DLS: tokens.css, base.css, helpers.js,
                     libre-franklin-latin-var.woff2 (the self-hosted primary typeface)
```

## Content shape (`content.json`)

```json
{
  "eyebrow": "HOW IT WORKS",
  "headline": "From tip to broadcast",
  "subhead": "optional — carried for future use, not rendered on-frame",
  "source": "optional bottom-right strip text",
  "steps": [
    {
      "number": 1,
      "title": "A tip comes in",
      "railLabel": "The tip",
      "description": "one tight sentence of context",
      "accent": false,
      "sourceRefs": []
    }
  ]
}
```

| Field | Where it renders | Notes |
|---|---|---|
| `eyebrow` | kicker line, top-left of the active frame | maps to the DLS kicker tier |
| `headline` | the **progress rail header** (not a big on-frame title) | the per-step `title` carries the headline tier instead |
| `subhead` | not rendered on-frame | carried in content for future use; the per-step `description` does the contextual work |
| `source` | optional bottom-right source strip | use only for a real provenance line; leave out if the bundle makes no factual claim |
| `steps[]` | one full frame each | keep 3–6 (see density ceiling) |
| `steps[].number` | the giant hero number | optional — defaults to position+1; rendered zero-padded to 2 digits |
| `steps[].title` | headline-tier step title | 3–5 words |
| `steps[].railLabel` | short label in the progress-rail pip | optional — falls back to `title` if omitted; keep it 1–2 words so the rail stays compact |
| `steps[].description` | subhead-tier context line | ONE tight sentence — two start to crowd the frame |
| `steps[].accent` | tints the hero number + rail | the **initial** accent; at most one step `true` |
| `steps[].sourceRefs` | not rendered (joins to `manifest.sources[]`) | citation plumbing, invisible on-air |

### Live interactivity

- **Tap the stage** → advance to the next step (loops after the last).
- **Tap a rail pip** → jump straight to that step.
- The **accent** (`accent: true`) sets the initial emphasized step — the hero number and
  rail go `data-accent` orange instead of `data-primary` blue. Use it for "the step this
  segment is really about." Emphasis changes are in-memory only; the `content.json` state
  always wins on (re-)load.

## DLS rules this template follows

- **Self-hosted Libre Franklin** (`lib/libre-franklin-latin-var.woff2`, SIL OFL 1.1) is
  the primary typeface, `@font-face`-loaded by `lib/base.css`. Never swap in a system or
  webfont stack.
- **Type ramp** (reference px @1080): kicker 34 / headline 84 / subhead 40 /
  hero-number 150+ / legend 34. The template binds these via `--lep-size-*` tokens — author
  against the tokens, never literal px.
- **Composition zone:** all critical content stays left of **x1574** (inside the
  ~18% presenter column on the right). The active frame is pinned inside the comp zone with
  the title-safe inset; the progress rail sits bottom-left.
- **Background-media + scrim (§5.4):** the ambient layer is mounted via
  `leporello.mountBackgroundMedia({ stage, image, scrim: 'left' })` — the left scrim is
  mandatory so text over the media stays legible. Swap `static/backdrop.svg` for a producer
  image/video by changing that call's `image`.
- **Attribution OFF (§5.14):** no on-frame attribution/credit strip. The optional `source`
  line is a content provenance note, not a station credit. The on-air shell already shows
  admin attribution.
- **`fitStage` is fine here.** This template has **no live map**, so the 1920×1080 canvas
  is scaled with `leporello.fitStage('.lep-stage')` as normal. (Contrast the `map` /
  `iran-alignment` templates, which render MapLibre full-bleed and must NOT be wrapped in
  `fitStage`/`transform: scale` — see those templates' `TEMPLATE.md`.)
- **Telestration:** `manifest.telestrator` is `"default"` (raster/PixiJS overlay). There is
  no `window.leporelloMap` and no `lepo-tele` postMessage receiver — those are map-template
  concerns only.

## Density ceiling

- **3 steps:** comfortable.
- **4–5 steps:** ideal — reads quickly, each frame has room.
- **6 steps:** maximum. Keep descriptions to one short sentence.
- **7+ steps:** too many. Merge steps, or split into a two-asset sequence.

## Common customizations

- **Swap the backdrop:** replace `static/backdrop.svg` (or point `mountBackgroundMedia` at
  a producer image/video). Keep `scrim: 'left'`.
- **Drop the source strip:** omit `content.source` — illustrative bundles should label it
  as a sample or leave it out.
- **Quieter / louder numbers:** the hero number is sized in `index.html`'s `<style>`
  (`.flow-number`). Stay within the hero-number tier (≥150px) so it still reads as the
  focal figure.
- **Rail labels:** give each step a short `railLabel` so the bottom rail stays compact when
  titles are long.

## Things not to change

- The `data-version` / `data-updated` plumbing (`leporello.applyVersionStamp`).
- The manifest schema shape, and the pre-filled technical fields (`dlsVersion: "1.5"`,
  `telestrator: "default"`, empty `externalDependencies`).
- The vendored `lib/` — including the Libre Franklin woff2. It's a snapshot at authoring
  time; don't edit or substitute it.
- The "sources stay invisible" rule (no inline `[src-X]` markers, no citation list).

## Density check

Per `references/broadcast-standards.md`: one frame, one point. Each step's "one point" is a
single idea the presenter can land in a few seconds. If you're fitting two sentences of
description into a step, you're over-stuffing — cut to one tight sentence, or move the
elaboration to presenter notes.

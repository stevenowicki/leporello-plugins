# Template Catalog

Templates are starting points, not constraints. **The skill must be able to author novel asset bundles from scratch when no template fits** — Leporello has shipped many one-off interactive types before this skill existed, and the skill must remain capable of producing things outside the catalog.

When a producer's request doesn't fit a template cleanly, ask: "Which is closest, or should I start from `generic`?" and proceed.

---

## v1 templates

All eight templates are **restyled to the v1 DLS** (`dlsVersion: "1.5"`): Libre
Franklin, the px@1080 type ramp, the named composition regions, attribution
off-frame. Each vendors the v1 `lib/` (tokens.css + base.css + helpers.js + the
Libre Franklin woff2). Author **token-first** — every size/color/inset is a
`var(--lep-*)`, never a literal.

| Template | Status | When to use | Notes |
|---|---|---|---|
| `generic` | **Available** | Anything that doesn't fit another template. Minimal scaffold — DLS imports + manifest skeleton + bare `index.html`. **Default fallback.** | Raster telestrator. |
| `stat-callout` | **Available** | One number, comparison, or short callout. | Hero-number tier (`--lep-size-hero-number`, 150px). Optional full-bleed background-media + scrim to kill dead space. |
| `quote-card` | **Available** | Single quote with speaker, attribution, sources. | Speaker/title/context block is editorial framing, not a citation — the one on-frame "source-like" surface that's allowed. |
| `timeline` | **Available** (rebuilt, LEPO-37) | Chronological story, 3–5 beats. | **Swim-lane axis retired** in the v1 pass (it crammed sub-floor type). Now reads as **vertical beats** down the comp zone over an ambient background-media layer. Renderer hard-caps at 5. |
| `narrative-flow` | **Available** (rebuilt, LEPO-38) | Step-by-step explainer where order matters. | **No longer a row of cramped cards.** Now **one step per broadcast frame**: a hero-tier step number, headline-tier title, subhead line, a first-class bottom-left progress rail, ambient background. Presenter advances step-by-step. ~6 steps max. |
| `photo-collection` | **Available** (now a roster) | A story's **cast** (people/orgs) that each carry a **comparable metric** to rank by (approval, vote share, capacity). | **Reframed from a grid of small cards → a candidate ROSTER** (Kornacki shape): a vertical stack of ~4–5 LARGE rows, portrait + big name + hero value, leader-first, **each row a proportional bar** (§5.13, via `leporello.renderRoster`). Raster telestrator. Caps at 5. |
| `map` | **Available** | Geographic story: control, events, alignment, routes, ranges. A handful of regions and/or labeled places. | **Full-bleed live MapLibre** (NOT fitStage — see below): basemap + GeoJSON regions + **two-tier geo-anchored labels** (featured 40px / orientation 22px) + geo-anchored markers. DLS chrome (lockup, legend) on a separate non-scaled overlay. `telestrator: "map"` → the cross-origin **bundle map-telestrator** (strokes in lng/lat, persist across pan/zoom). |
| `iran-alignment` | **Available** | "Who's aligned with whom": blocs, axes, coalitions, with an optional snapshot stepper for how alignment shifts over time. | **Full-bleed live MapLibre.** Countries come from the **shared geo layer** (`admin0` PMTiles, colored by ISO-3 `shapeGroup` via a `match` expression) — no country geometry ships in the bundle. A baked-in static SVG fallback mirrors the choropleth for offline capture. Stepper is a presenter-operated control (top-right). `telestrator: "map"`. |

> **Maps render FULL-BLEED — never wrap a live MapLibre map in fitStage /
> `transform: scale()`.** A scaled map breaks tile resolution, hit-testing, and
> the geo-anchored telestrator. The map and iran-alignment templates render the
> MapLibre canvas at true viewport size and put the DLS chrome on a separate
> non-scaled overlay. `fitStage()` is correct only for the non-map templates
> (generic / stat-callout / quote-card / timeline / narrative-flow /
> photo-collection), which author on the 1920×1080 `.lep-stage`.

> **Dashboard intentionally not in this catalog.** Originally proposed as a 1B template, but dropped during scoping. Multi-card grids tend to be either composable from `stat-callout × N` (a layout decision the producer makes themselves) or fully bespoke like the cyber-threat-monitor (which needs custom HTML/CSS, not a template). A generic dashboard template fits neither case. When a producer wants a dashboard, the right answer is usually "compose stat-callouts in a package" or "start from `generic` and build the custom shape."

For novel content types that don't fit any catalog template, `generic` is the right starting point.

---

## How a template is structured

Every v1 template directory contains:

```
templates/<type>/
├── TEMPLATE.md         — template docs: when to use, content shape, customization hooks.
│                         NOT copied into authored bundles. Read this first.
├── brief.md            — per-bundle editorial-brief skeleton (you fill + ship)
├── README.md           — per-bundle producer-ops skeleton ([CLAUDE-PLACEHOLDER:*])
├── CLAUDE.md           — per-bundle AI-resume skeleton ([CLAUDE-PLACEHOLDER:*])
├── manifest.json       — pre-filled manifest skeleton; dlsVersion 1.5, telestrator set
├── index.html          — structural template (HTML + CSS + JS), token-first
├── content.json        — worked EXAMPLE content (real shape, replace every value)
└── lib/                — vendored v1 DLS: tokens.css, base.css, helpers.js,
                          libre-franklin-latin-var.woff2
```

`TEMPLATE.md` documents the *template*; `brief.md` / `README.md` / `CLAUDE.md` are
the three **per-bundle resumability skeletons** you fill in and ship (the skeletons
themselves are never shipped — replace every `[CLAUDE-PLACEHOLDER:*]` marker).

`generic` is intentionally minimal — a skeleton manifest, an `index.html` with a
`<main>` wrapper that hydrates from `content.json`, the vendored `lib/`, and a
`content.json` with a single placeholder.

---

## Choosing a template — heuristics

**Default to `generic` when:**

- The content shape is unusual or you're not sure which template fits.
- The producer is building a one-off interactive that doesn't match any obvious pattern.
- The producer explicitly says "build something novel."
- The closest template would require gutting most of the template's structure to fit.

**Use a specific template when:**

- The content cleanly matches the template's shape (e.g., chronological events → `timeline`, single number → `stat-callout`).
- The producer asks for it by name.
- A canonical example in the catalog matches what the producer is describing.

When in doubt, ask. Templates are conveniences; jamming content into the wrong template is worse than starting from `generic`.

---

## Template evolution

Templates will grow and change over time — new templates added, existing templates revised. **Because every bundle is self-contained (CSS + JS inline or vendored under `lib/`), editing a template does not affect existing bundles.** Bundles already in production reference their own snapshot of the template's structure at upload time; the template directory is just a starting point for new bundles.

This is why bundles include `lib/tokens.css` directly rather than referencing a remote DLS — the bundle's tokens are baked in at authoring time.

---

## Generic template — what it gives you

The `generic` template includes:

- A manifest skeleton with the required fields stubbed (with `[CLAUDE-PLACEHOLDER]` markers where the skill must fill in).
- An `index.html` with:
  - DOCTYPE and minimal document chrome.
  - A 1920×1080 `.lep-stage` (scaled by `leporello.fitStage()`) with a `<main>` wrapper containing a single titled section.
  - Imports of the vendored v1 `lib/tokens.css` and `lib/base.css` (Libre Franklin + the ramp + named-region tokens).
  - A `<script>` block that fetches `./content.json`, populates title + body, and stamps the version (`leporello.applyVersionStamp`).
  - `data-version` and `data-updated` attributes on the root element. **No on-frame attribution/source footer** — attribution is metadata only (§5.14).
- A `content.json` with `title`, `body`, `sourceRefs` placeholders.
- An `editorialReview`-shaped manifest block left empty for the producer to fill at review time.

It's a working bundle out of the box — you can run `scripts/preview.sh` against the template directory and see a rendered (placeholder) bundle in a browser. The skill's job for a `generic` build is to fill in the placeholders with real, sourced content and adjust the layout as needed.

---

## When you build novel

If no template fits and `generic` is too minimal for what you're building (e.g., a complex interactive with custom controls, animations, or a unique visual structure), still:

1. **Start by copying `generic`.** It gives you the manifest skeleton, the DLS imports, the `data-version`/`data-updated` plumbing, and the source-list rendering for free.
2. **Add what you need on top.** Custom CSS, additional content files, vendored JS libraries under `lib/`. The `generic` template is small enough to extend without fighting it.
3. **Document what you built** in the bundle's `manifest.description` so the next iteration (skill or human) knows the structural choices.

Don't reinvent the wheel — the manifest, source-list, and footer plumbing should be consistent across bundles even when the visual layer is novel.

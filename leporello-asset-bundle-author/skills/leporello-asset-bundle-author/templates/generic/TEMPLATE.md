# `generic` template

The minimal scaffold, restyled to the **v1 DLS** (Libre Franklin, the named
on-screen regions, the broadcast type ramp). The fallback when nothing else fits,
and the right starting point for anything novel. It renders a clean figure frame —
a top-left lockup, one hero number, a metric-encoding roster — over an ambient
background-media layer with a mandatory legibility scrim.

> Authoritative DLS: `docs/prelim/dls/m1/direction/direction.md`. This template
> implements it; don't invent token values.

## What's in it

```
templates/generic/
├── TEMPLATE.md          this file (template docs — NOT copied into bundles)
├── README.md            per-bundle producer-ops skeleton ([CLAUDE-PLACEHOLDER:*])
├── CLAUDE.md            per-bundle AI-resume skeleton ([CLAUDE-PLACEHOLDER:*])
├── manifest.json        manifest skeleton with [CLAUDE-PLACEHOLDER:*] markers
├── brief.md             editorial brief skeleton — durable record of intent
├── index.html           lockup + hero + roster, hydrates from content.json
├── content.json         a filled-in SAMPLE (illustrative data) — replace it
└── lib/                 vendored DLS lib (snapshot at authoring time; don't edit)
    ├── tokens.css       v1 DLS tokens (--lep-* custom properties)
    ├── base.css         broadcast reset + type roles + named-region + roster +
    │                    background-media/scrim machinery
    ├── helpers.js       runtime utilities (loadContent, renderRoster,
    │                    mountBackgroundMedia, fitStage, applyVersionStamp)
    └── libre-franklin-latin-var.woff2   self-hosted variable font (SIL OFL 1.1)
```

`content.json` ships as a working **sample** (a fictional "demo region" battery
figure, clearly labelled illustrative). It's an example of the shape, not a
finished bundle — replace every value with real, sourced content.

## What you fill in

- `manifest.json` placeholders — `slug`/`bundleId`, `title`, `attribution`,
  `description` (`[CLAUDE-PLACEHOLDER:*]`), `createdAt`
  (`[CLAUDE-PLACEHOLDER:iso8601-now]`), plus `sources[]` and any story `tags`.
  The technical fields are pre-set and correct: `dlsVersion: "1.5"`,
  `telestrator: "default"`, `externalDependencies: []`, `dimensions` (16:9),
  `tags: ["generic"]` (add story tags alongside). Generic ships no map, so it uses
  the default raster (PixiJS) telestrator — leave `telestrator` as `default`.
- `content.json` — replace the sample with real content (keys below).
- `brief.md` — producer's ask, framing, content/source/visual decisions, the v1
  iteration-log entry. See `references/bundle-format.md` ("Editorial brief").
- `editorialReview` block on the manifest, once the producer reviews.

The skill's job is to replace every `[CLAUDE-PLACEHOLDER:*]` marker with real,
sourced content and add `sources[]` entries that the `sourceRefs` arrays reference.

## content.json — keys `index.html` reads

Any field you omit is hidden gracefully — drop pieces for a pure hero-stat frame,
or drop `hero` and lead with the roster.

- `eyebrow` — the kicker / category label (top of the lockup).
- `headline` — the slide's one-sentence point (the largest *text*).
- `subhead` — one line of supporting context.
- `rule` (bool) — show the single accent hairline under the headline (a
  typographic separator, not chrome — §5.10).
- `hero` — the asset's one figure (§5.1, one takeaway per asset):
  - `value` (string, e.g. `"41%"`) — carries its own unit so the frame makes no
    format assumption; rendered at the hero-number tier (the single largest thing
    on screen, ~3–4× the next-largest text).
  - `unit?` — a small leading glyph (`+`, `$`) sharing the hero baseline.
  - `caption?` — short line under the number.
  - `trendArrow?`, `trendText?`, `trendDir?` — optional trend chip. `trendDir`
    only recolors it (`up`→accent, `down`→primary, `flat`→muted); the glyph comes
    from `trendArrow` so direction is explicit.
- `roster[]` — supporting list that **encodes its own metric** (§5.13): each
  `{ label, value, display? }`. Bars are proportional to `value`, the leader gets
  the story accent, the value cell is ≥ the label. NOT just printed numbers.
  - `rosterHeading?` — small eyebrow over the bars.
  - `rosterSort?` (bool, default true) — sort rows descending by value.
  - `rosterLeaderIndex?` — which row gets the accent; `null` colors every bar
    `data-primary` (no single leader).
- `sourceText` — the bottom-right source strip. For a real story this names the
  data source; for illustrative content say so. (Sources for *claims* still live
  in `manifest.sources[]` — see "DLS rules", attribution-off below.)
- `background` — the ambient full-bleed layer behind the lockup (§4 / §5.4),
  `{ image | video, scrim, poster? }`:
  - `image` / `video` — a vendored `static/` file or a self-contained data-URI.
    The shipped sample uses an inline-SVG gradient data-URI (no external CDN) so
    the bundle validates and renders standalone.
  - `scrim` — `default` | `heavy` | `left`. **Mandatory and non-negotiable** —
    the helper always mounts a scrim so the lockup stays legible over media.
  - `poster?` — poster frame for a video background.

## DLS rules this template follows

- **Type ramp** (direction §2, px@1080): kicker 34 / headline 84 (72 on full-bleed
  maps — N/A here) / subhead 40 / hero-number 150 / data-label 64 / legend 34 /
  source 22. Pulled straight from `--lep-size-*` tokens; never author in rem/pt.
- **Named regions** (§4): lockup top-left, primary stage inside the composition
  zone (x0–1574, left of the ~18% presenter column on the right). Keep critical
  content left of x1574 and inside the title-safe inset; ambient layers
  (background) may run full-bleed through the presenter column.
- **Presenter-controls zone** (§5.15): the top-right is reserved for on-air nav —
  nothing critical there.
- **One takeaway per asset** (§5.1) + tight text budget (§5.2): one hero figure,
  no body-copy walls. For a second takeaway, prefer a second asset over crowding.
- **Rosters encode their metric** (§5.13): proportional bars, not bare numbers.
- **Attribution OFF inside the frame** (§5.14): no visible attribution footer — the
  on-air shell surfaces `manifest.attribution` outside the iframe. `sourceText` is
  the editorial source line for the data shown, not a repeat of the attribution.
- **Color budget** (§3): ≤2 categorical story colors (`--lep-data-accent` for the
  one element that tells the story, `--lep-data-primary` for the rest) + neutrals.
  Passes a grayscale read.
- **Self-hosted Libre Franklin** (SIL OFL 1.1) via the vendored `lib/*.woff2`
  — no font CDN; bundles are self-contained.

## How it renders

`index.html` mounts a 1920×1080 stage scaled-to-fit the viewport via
`leporello.fitStage('.lep-stage')`. (Generic is a non-map template, so `fitStage`
is correct — the map / iran-alignment templates render their MapLibre map
**full-bleed** and never wrap it in `fitStage`/`transform:scale`.) The loader
prefers `fetch()` of `content.json`/`manifest.json` (served over http on air) and
falls back to inline `<script type="application/json">` blocks so the bundle still
renders from a `file://` preview / capture harness. Keep the inline blocks in sync
with `content.json`.

## Common customizations

The generic template is intentionally simple. To extend it without leaving the spec:

- **More roster rows** — add entries to `roster[]`.
- **No roster / pure hero stat** — omit `roster`; the hero figure stands alone.
- **Real background media** — drop a file under `static/` and point `background.image`
  / `background.video` at `./static/...`. The scrim stays mandatory.
- **Add interactivity** — add `<script>` blocks or vendor a JS library under `lib/`.
  No CDN; bundles are self-contained.

When the customization grows beyond what `generic` carries comfortably, that's the
signal to reach for a more specific template (`stat-callout`, `quote-card`,
`timeline`, `map`, `iran-alignment`, `photo-collection`).

## Don't change

- The `manifest.json` schema shape (required fields, types) and the pre-set
  technical fields (`dlsVersion`, `telestrator`, `externalDependencies`,
  `dimensions`).
- The `data-version` / `data-updated` plumbing (`applyVersionStamp`) in `index.html`.
- The vendored `lib/` files (incl. the woff2). Bundles include their own snapshot at
  authoring time; updating tokens here does not retroactively change rendered
  bundles.

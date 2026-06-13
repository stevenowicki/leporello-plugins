# `timeline` template

A chronological story read as **vertical beats** down the composition zone — earliest
at the top, latest at the bottom. Restyled to the v1 DLS (Libre Franklin, the named
composition regions, attribution-off). The horizontal swim-lane axis the template
originally shipped with was retired in the v1 pass (LEPO-37): it crammed many small
cards along a thin line, the type fell below the broadcast floor, and the progression
was hard to read at distance.

**Anchored on:** a generic project-history beat list ("idea → prototype → preview →
team → ship"). The template is the *shape*, not a copy of that sample.

## When to use

- The story is fundamentally about **when** things happened and in what order.
- A presenter wants to walk through the chronology beat-by-beat.
- You have **3–5 beats** that each carry one short, broadcast-scale headline.

**Don't use when:**
- The story is a sequence but not a chronology (use `narrative-flow`).
- You have one or two events — a `stat-callout` with a date carries more weight.
- You have more than five beats — cut to the five that matter; the renderer hard-caps
  at five anyway (over-filling silently drops the tail).
- You need converging parallel threads (swim-lanes) — that is a separate layout, not a
  tweak to this template.

## What's in it

```
templates/timeline/
├── TEMPLATE.md          this file (template docs — NOT copied into bundles)
├── README.md            per-bundle producer-ops skeleton ([CLAUDE-PLACEHOLDER:*])
├── CLAUDE.md            per-bundle AI-resume skeleton ([CLAUDE-PLACEHOLDER:*])
├── manifest.json        skeleton with [CLAUDE-PLACEHOLDER:*] markers
├── brief.md             editorial brief skeleton with timeline-specific framing
├── index.html           renders the top-left lockup + vertical beat bands over an
│                        ambient background-media layer
├── content.json         eyebrow / headline / subhead / dateRange / dateMode /
│                        background / events[]  (sample content — replace it)
└── lib/                 vendored DLS tokens + base CSS + helpers, the Libre Franklin
                         woff2, and a generated ambient background PNG
```

## Content shape

```json
{
  "eyebrow": "string  (kicker, 34px ALL-CAPS)",
  "headline": "string (84px — the frame's center of gravity; wraps to 2 lines)",
  "subhead": "string  (40px, optional supporting context)",
  "dateMode": "month | day",
  "dateRange": { "start": "YYYY-MM-DD", "end": "YYYY-MM-DD" },
  "source": "string (optional) — METADATA ONLY, never drawn on frame (§5.14)",
  "background": { "image": "./lib/timeline-bg.png" },
  "events": [
    {
      "date": "YYYY-MM-DD",
      "title": "short string — one or two lines, ~3-8 words",
      "accent": false,
      "sourceRefs": ["src-N", ...]
    }
  ]
}
```

### How a beat renders

Each event is a **full-width band** that owns an equal vertical slot (`flex:1`) so the
rhythm is even top-to-bottom and the hairline rules between bands land on a regular
grid. Inside a band:

- a compact **meta line** — a glowing dot + the date, rendered ALL-CAPS at the legend
  tier (34px), with the **year tinted the story color** so the progression reads down
  the left edge at a glance;
- a **title hero** (56px bold, between the 40px subhead and 64px data-label tiers) on
  its own line, running the full band width and clamped to two lines. The title — not
  the date — is the content the viewer reads.

`dateMode` controls the meta line: `"month"` → "MON YYYY"; `"day"` → "MON D, YYYY".
Dates are parsed and formatted as **UTC** so a `YYYY-MM-DD` value never shifts a
day/year under the renderer's local timezone.

### The accent beat

Set `accent: true` on the **single** most important beat (per broadcast-standards: one
slide, one point). That band gets a warm orange wash + a left accent edge that span the
slot **divider-to-divider** (aligned exactly to the hairlines above and below), a
scaled-up dot, an orange-tinted year, and an extrabold title. At most one accent per
timeline. The wash alignment is structural — it relies on each beat owning an equal
slot — so don't reintroduce floating top/bottom offsets on it.

### Background-media

The template mounts an ambient, low-contrast background image full-bleed via
`helpers.mountBackgroundMedia({ image, scrim: 'left' })` behind everything. The
**left-weighted scrim is mandatory** for legibility (direction §5.4): it keeps the
lockup + beat list readable while the otherwise-dead right field stays visible. A
generated placeholder ships at `lib/timeline-bg.png`; swap `content.background.image`
for a story-appropriate texture (keep it low-contrast — it sits behind text).

## DLS rules this template follows

- **Libre Franklin**, self-hosted woff2 in `lib/`, declared `@font-face` in
  `lib/tokens.css`. No web-font CDN, no system-font fallback as the primary face.
- **Type ramp (px @1080):** kicker 34 · headline 84 · subhead 40 · the beat title 56 ·
  date/legend 34. All pulled from the vendored v1 tokens — **no invented values**.
- **Composition zone:** all critical content (lockup + beats) sits left of **x1574**,
  clearing the ~18% presenter column on the right. The beat bands span the title-safe
  inset out to ~x1500 by design — that fills the zone and fixes the original
  stranded-content / dead-right-third failure.
- **Background-media layer + scrim** (§5.4): ambient image full-bleed under a mandatory
  left-weighted scrim.
- **Attribution OFF on frame** (§5.14): no source strip, no inline `[src-X]` footnotes,
  no attribution footer. `content.source` and `manifest.sources[]` are metadata only —
  validated at upload, available to admin / presenter / future-Claude, never drawn. The
  re-vendored `lib/base.css` hard-kills `.lep-source*` with `display:none`.

## Common customizations

- **Date format:** edit the `fmt()` helper in `index.html` for a non-English locale or a
  specific format string. Keep it UTC.
- **Beat count:** 3–5. The renderer sorts chronologically and slices to five, so
  over-filling can't break the frame — but aim low; a dense timeline fails on air.
- **Background:** swap `content.background.image`. Low-contrast only.

## Things not to change

- The `data-version` / `data-updated` plumbing on the root element.
- The manifest schema shape (keep the `[CLAUDE-PLACEHOLDER:*]` markers until you fill
  them per bundle).
- The vendored `lib/` (tokens, base, helpers, the woff2). Bundles include their own
  snapshot at authoring time.
- The "attribution stays off frame" rule (§5.14) and the equal-slot mechanism that keeps
  the accent wash aligned to the hairlines.

## Density check

Per `references/broadcast-standards.md`: the viewer has 10–30 seconds. Aim for **3–5
beats**, each one short line the presenter can land. More than five and the renderer
drops the tail; even at five, keep each title tight.

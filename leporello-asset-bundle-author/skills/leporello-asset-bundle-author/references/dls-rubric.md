# DLS critique rubric — the supervision checklist

Apply this by **looking at a rendered screenshot** of the bundle (1920×1080), after
the mechanical gates (`validate.sh`, `lint_tokens.py`, `dls_check.mjs`) pass. It's the
perceptual backstop — it catches what static + measurement checks can't. Score each
PASS / FAIL with a one-line reason; any FAIL means remediate and re-render. Authoritative
source: `docs/prelim/dls/m1/direction/direction.md` (§2 north star, §4 regions, §5 rules).

> **Render maps HEADED.** Headless Chromium composites live MapLibre WebGL as black —
> a false fail. Use a headed browser (or trust `dls_check.mjs`, which is headed).

## Hard gates (any FAIL blocks upload)

1. **Typeface** — text is **Libre Franklin**, not a system/Inter/Roboto stack. (Also
   enforced by `dls_check.mjs`; if it flagged `font`, you vendored the lib but didn't
   apply it, or authored fresh HTML without the font.)
2. **Presenter-safe column** — critical content (headline, hero numbers, legend, data
   labels, panels) clears the **right ~18%** (x < 1574). The presenter stands there and
   the 110px nav rail lives there; anything past it gets blocked/clipped on air. Ambient
   layers (full-bleed maps, background media) may run edge-to-edge. (Also in `dls_check`.)
3. **Headline scale** — the headline reads big (≈84px @1080 / 6–9% cap-height). A timid
   headline is the single most common miss vs. broadcast.
4. **Attribution off-frame** — no source/credit strip drawn on the frame. Source is
   manifest metadata; the presenter cites it. (Also in `dls_check`.)
5. **No overlaps / no clipping** — nothing collides, nothing falls off a safe edge,
   no element grazes another (subhead↔tally, board↔legend, label↔label).

## Quality bar (FAIL if clearly off)

6. **Text restraint** — one kicker + one headline + ≤1 subhead + the data. No paragraphs,
   no footnotes/asterisks. The graphic gives the presenter something to talk *to*.
7. **Left-weighted, fills the width** — content gravity is left, but it *uses* the
   composition-zone width; it isn't stranded at ~50–60% with a dead right field. If it
   can't fill, add a background-media layer (image/video, scrimmed) — don't leave a void.
8. **Numbers are heroes** — the value tier is the largest type; in a roster/tally the
   value ≥ its label; tabular figures; the metric is **encoded** (proportional bars),
   not just printed. On-bar labels stay legible when a bar is short (halo).
9. **Hierarchy in ≤3 seconds** — one clear takeaway; the eye lands on the point first.
10. **Color serves the story** — ≤2 categorical colors or one ≤5-stop ramp + neutrals;
    no decorative color. Party/team colors are content-appropriate and TV-safe (not
    pure #00F/#F00 — they bloom).
11. **Presenter-operated controls top-right** — steppers/switchers/pagination near the
    nav, never center/bottom (a consumer-touch pattern).
12. **Reads composed, not empty** — generous dark field is fine when *intentional*;
    an accidental empty third is not.

## The "would Steve present this?" test

Picture the frame on an 85" wall with a presenter standing at the right, framed by a
camera and re-compressed to the home viewer. Is it legible, is the point instant, does
it read as *Leporello* (Libre Franklin, the dark surface, the regions) and not as a
generic web slide? If not, name what's off and fix it.

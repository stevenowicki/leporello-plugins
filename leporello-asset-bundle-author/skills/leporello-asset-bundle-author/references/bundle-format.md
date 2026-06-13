# `.lepo` Bundle Format — Reference

A `.lepo` is a ZIP archive containing a self-contained, statically-hostable web artifact intended to render inside an iframe in the on-air app. This file is the working reference for skill authoring; the canonical spec lives in the main Leporello repo at `docs/prelim/bundle-format-spec.md`.

## File layout

```
bundle.lepo                          (ZIP)
├── manifest.json                    REQUIRED
├── index.html                       REQUIRED (entry point)
├── content.json                     OPTIONAL (the editable-content split)
├── brief.md                         OPTIONAL (editorial intent — skill always writes)
├── README.md                        OPTIONAL (producer ops — skill always writes)
├── CLAUDE.md                        OPTIONAL (AI-resumption context — skill always writes)
├── static/                          OPTIONAL (images, video, data, etc.)
│   ├── images/
│   ├── video/
│   └── data/
└── lib/                             OPTIONAL (vendored CSS/JS)
    ├── styles.css
    └── app.js
```

The three root Markdown docs (`brief.md`, `README.md`, `CLAUDE.md`) are the **resumability artifacts** — see "Resumability artifacts" below.

**Hard rules:**
- Valid ZIP. Decompresses without errors.
- `manifest.json` and `index.html` at the root.
- All paths inside the ZIP use forward slashes. No leading `/`. No `..`.
- No symlinks.
- Total uncompressed size ≤ **50 MB**. Individual file ≤ **10 MB**.
- File names case-sensitive; manifest references must match disk exactly.

The term `static/` is deliberately not called `assets/` — that term is reserved for Leporello's top-level concept (the things producers add to packages).

## Manifest schema

```json
{
  "schemaVersion": "1.0",

  "bundleId": "iran-timeline",
  "title": "Iran War — Master Timeline",
  "slug": "iran-timeline",

  "entry": "index.html",
  "content": "content.json",
  "brief": "brief.md",

  "attribution": "Reuters · MTAC · Clemson Media Forensics Hub",
  "description": "Four-lane swim diagram covering Feb 27 — Apr 26.",

  "sources": [
    {
      "id": "src-1",
      "title": "Reuters: Iran strikes Israeli embassy",
      "url": "https://www.reuters.com/...",
      "publisher": "Reuters",
      "publishedAt": "2026-04-14T08:00:00Z",
      "accessedAt": "2026-04-14T12:00:00Z"
    }
  ],

  "generatedBy": "claude-leporello-skill@0.1.0",
  "editorialReview": {
    "reviewedBy": "producer-user-id",
    "reviewedAt": "2026-04-15T09:30:00Z",
    "notes": "Cross-checked all source links."
  },

  "createdAt": "2026-04-15T09:30:00Z",

  "dimensions": { "aspectRatio": "16:9", "minWidth": 1280, "minHeight": 720 },
  "dlsVersion": "1.5",

  "telestrator": "default",

  "externalDependencies": [],
  "tags": ["timeline", "iran-war", "geopolitics"]
}
```

### Required fields

| Field | Type | Notes |
|---|---|---|
| `schemaVersion` | string | v1 bundles target `"1.0"`. |
| `bundleId` | string | Stable producer-supplied slug. Lowercase ASCII + digits + hyphens. Length 3–64. Server enforces uniqueness within the org. |
| `title` | string | Display string. |
| `entry` | string | Path to HTML entry. Almost always `"index.html"`. |
| `sources` | array | Citation objects. **Required field, may be empty array** for bundles with no factual claims (pure quote cards, etc.). |
| `attribution` | string | Free-form attribution string (e.g., `"Reuters · MTAC"`). **Metadata only** — captured here for the producer/admin review; NOT drawn on the broadcast frame (direction §5.14). |
| `generatedBy` | string | Tool that produced the bundle. `claude-leporello-skill@<version>` for skill-generated, `manual` for hand-built, `claude-leporello-skill@<version>+edited` for skill-then-hand-edited. |
| `createdAt` | string | ISO 8601. |

### Server-assigned (omit from manifest)

| Field | Notes |
|---|---|
| `version` | Server assigns the next integer string under the bundle ID. The skill **does not** write this field; the upload pipeline writes it into the stored manifest. |

### Optional fields

| Field | Notes |
|---|---|
| `content` | Path to primary content JSON. Defaults to `"content.json"` if file exists and field omitted. Set to `null` for monolithic bundles. |
| `brief` | Path to the editorial brief (Markdown). Defaults to `"brief.md"` if the file exists at the bundle root and the field is omitted. See "Editorial brief" below. The skill **always** writes this for new bundles. |
| `readme` | Path to the producer operating doc (Markdown). Defaults to `"README.md"` at the bundle root if omitted. See "Resumability artifacts" below. The skill **always** writes this for new bundles. |
| `claude` | Path to the AI-resumption context doc (Markdown). Defaults to `"CLAUDE.md"` at the bundle root if omitted. See "Resumability artifacts" below. The skill **always** writes this for new bundles. |
| `slug` | Human-readable URL fragment. Defaults to `bundleId`. |
| `description` | Long-form admin-visible text. |
| `editorialReview` | Producer attestation block. Soft-warn if missing. |
| `dimensions` | Rendering hints. Renderer ignores in v1. |
| `dlsVersion` | Informational; tracks which DLS the bundle was authored against. New bundles target the v1 DLS — write `"1.5"` (matches the restyled templates' vendored `lib/`). |
| `externalDependencies` | Array of CDN URLs the bundle loads at runtime. Best-effort transparency, not enforced. |
| `tags` | Searchable labels. |
| `telestrator` | Enum: `"default"` (raster canvas, the default if omitted) or `"map"` (lng/lat-anchored map telestrator). |

## Source object shape

Every citation in `sources[]`:

```json
{
  "id": "src-1",
  "title": "Article or document title",
  "url": "https://...",
  "publisher": "Publisher name",
  "publishedAt": "ISO 8601 timestamp",
  "accessedAt": "ISO 8601 timestamp"
}
```

- `id` is referenced by `sourceRefs` arrays in content.
- `url` may be omitted for primary-source documents with no public URL — note in `title` (e.g., `"Court filing, EDNY 23-cv-1234"`).
- `accessedAt` is when the producer (or skill, on the producer's behalf) verified the source supported the claim. Important for live-changing pages.

## `sourceRefs` convention

In `content.json` (or any other content file), per-fact citation:

```json
{
  "title": "Cease-fire negotiations resume",
  "description": "...",
  "sourceRefs": ["src-1", "src-3"]
}
```

`sourceRefs` strings must match `manifest.sources[].id`. Strongly encouraged for any factual claim. Producer-notes (editorial commentary, primary-source observations without a public URL) get a `type: "producer-note"` marker instead.

**`sourceRefs` does not render visibly.** Sources are required metadata, validated at upload, available to the producer / admin source-review UI / presenter notes / future-Claude. They are not rendered as inline `[src-X]` footnotes or as a numbered citation list on the broadcast frame. See `references/broadcast-standards.md` ("Sources don't render visibly") for the rationale. The exception is editorial framing like a quote-card's speaker block — that's not citation, it's "who said it, where, when."

## Editorial brief (`brief.md`)

Every skill-generated bundle ships with a Markdown `brief.md` at the bundle root. It is the **durable record of editorial intent** — what the producer was trying to make, what decisions were made along the way, what got rejected and why. The producer's planning conversation with the skill, written down so it survives past the Claude Code session.

The brief and `manifest.editorialReview.notes` are complementary:
- `editorialReview.notes` is the short producer attestation — "I reviewed this, here's my one-line sign-off."
- `brief.md` is the long story — framing, choices, iteration log.

### Conventional sections

The skill writes (and producers may edit) the following sections. The list is conventional, not enforced — drop sections that don't apply, add sections that do.

```markdown
# <Bundle title>

## Producer's ask
What the producer came in wanting — verbatim or close.

## Editorial framing
What this bundle is about, the angle, what it's NOT trying to be.

## Template + rationale
Why this template (or why generic-from-scratch).

## Content decisions
What's in, what's out, what got cut and why.

## Source decisions
Which sources we chose, which we rejected, producer overrides on
source quality (with the SME justification recorded).

## Visual decisions
Color callouts, hierarchy choices, DLS deviations with rationale.

## Iteration log
- v1 (YYYY-MM-DD): initial publish — <one-line summary>
- v2 (YYYY-MM-DD): <what changed, why>
```

### Iteration model

The brief reflects the **current state** of the bundle. When patching, the skill **rewrites** affected sections to match what the bundle now is — not what it was at v1. Every prior version's `.lepo` is preserved at its own S3 prefix with its own `brief.md` intact, so the historical record across versions already exists at the bundle level. Carrying old framing forward inside a new version's brief would duplicate that and make v10 unreadable.

The **iteration log** is the one section that is append-only, because it is by definition a cross-version log. Each new version adds a one-line entry summarizing the diff and the reason:

```markdown
## Iteration log
- v1 (2026-04-15): initial publish — Iran timeline, four-lane swim
- v2 (2026-04-22): added Brent oil sparkline; extended end date to Apr 26
- v3 (2026-04-27): casualty count corrected 47 → 43 per AP
```

Substantive reframings (template change, scope flip) are handled the same way: rewrite the affected sections to reflect the new shape, and log the reframing in the iteration log. To see the prior framing, read the prior version's bundle.

### Missing brief

- **Skill-generated bundle without `brief.md`** → soft warning. The skill is expected to produce one; missing means something went wrong.
- **Hand-built bundle without `brief.md`** → accepted silently.
- **`manifest.brief` referencing a missing file** → hard error.

## Resumability artifacts (`README.md`, `CLAUDE.md`)

A `.lepo` can be downloaded, handed to another producer, or reopened by a Claude session with no memory of how it was built. Three root-level Markdown docs make it resumable cold, split by audience:

| File | Audience | Holds |
|---|---|---|
| `brief.md` | Editorial | **Why** it exists — ask, framing, what got cut, iteration log. |
| `README.md` | Producer (ops) | **How to run it** — what it is, where data comes from, how to preview/validate/package, how to update. |
| `CLAUDE.md` | AI (resume) | **Implementation context** — non-obvious rationale, annotated source links, decisions that would otherwise live only in the original conversation. Mirrors the main-repo `CLAUDE.md` convention. |

`brief.md` answers *why*, `README.md` answers *how a human runs/edits it*, `CLAUDE.md` answers *what an AI needs to resume safely*. Don't duplicate content across them. All three live at the **bundle root**.

The skill **always writes all three** for new bundles, and rewrites them to current state when patching (same iteration model as `brief.md`). Each template ships a `README.md` + `CLAUDE.md` skeleton with `[CLAUDE-PLACEHOLDER:*]` markers — fill them in, don't ship the skeleton. (The template's own documentation lives in `TEMPLATE.md`, not `README.md`, precisely so the copied `README.md` is the per-bundle producer doc.)

### When they're missing

- **Skill-generated bundle without `README.md` or `CLAUDE.md`** → soft warning. The skill is expected to produce both.
- **Hand-built bundle without them** → accepted silently.
- **`manifest.readme` / `manifest.claude` referencing a missing file** → hard error.

## `index.html` conventions

- **Single-document entry.** No SPA routing within a bundle. The iframe is a leaf.
- **Self-contained or content-split.** Two valid patterns:
  - **Monolithic:** all text + data + styles + scripts inline.
  - **Content-split:** `index.html` fetches `./content.json` at runtime and populates the DOM. Strongly preferred for anything that might need a producer hand-edit.
- **Relative paths only.** `./static/...`, `./lib/...`. No leading `/`. No `<base href>`.
- **No top-frame navigation.** Bundles must not attempt `window.top.location = ...`.
- **Root element annotation.** Add `data-version` and `data-updated` attributes to `<html>` or top wrapper, populated from manifest at render time.

## Static files (allowed formats)

- **Images:** PNG, JPEG, WebP, SVG, GIF.
- **Video:** MP4 (H.264 + AAC). No streaming protocols.
- **Data:** JSON, CSV, GeoJSON, PMTiles.
- **Disallowed:** executables, archives-within-archives, anything with active content other than HTML/CSS/JS.

## External dependencies

Inside the iframe, bundles can fetch live data, load CDN libraries, hit APIs — anything the browser allows. There is **no `sandbox` attribute** on bundle iframes (v1 trade-off: producer-controlled environment, intentional permissiveness).

The `externalDependencies[]` array is for **transparency**, not restriction:
- Skill-generated bundles **must** populate this accurately.
- Hand-built bundles often won't, and that's accepted.
- Upload validation does not scan source for undeclared URLs.
- Declared entries should be HTTPS (mixed-content blocking ruins the bundle in practice anyway).

Producer-side considerations the skill surfaces but does not enforce:
- Third-party analytics and trackers compromise journalistic neutrality. Recommend against; accept if producer insists.
- Inline web fonts from a CDN (Google Fonts, etc.) work fine; vendoring into `lib/` is more robust for broadcast.
- Live data feeds: the bundle should degrade gracefully (last-known value, "loading", or fallback rather than a blank panel).

## Validation rules at upload

The upload endpoint runs these checks. The local `scripts/validate.sh` mirrors the structural and manifest checks; content and security checks live server-side.

**Structural (hard):**
- Valid ZIP.
- Contains `manifest.json` and `index.html` at root.
- All paths normalized (no `..`, no leading `/`, no symlinks).
- Within size caps.
- File paths use allowed characters.

**Manifest (hard):**
- Valid JSON.
- Required fields present and well-typed.
- `schemaVersion` recognized.
- `bundleId` matches slug rules (lowercase ASCII + digits + hyphens, 3–64 chars).
- `sources[]` entries have valid URL format if `url` is present.
- All `entry` and `content` paths reference files that exist in the bundle.

**Content (hard):**
- `index.html` is well-formed (DOCTYPE present, parseable HTML).
- `content.json`, if present, is valid JSON.
- Image / video / data files match declared MIME types.

**Editorial (soft — warn, never block):**
- `editorialReview` absent → warning.
- Skill-generated bundle missing a resumability artifact (`brief.md` / `README.md` / `CLAUDE.md`) → warning. Hand-built bundles exempt.
- `[CLAUDE-PLACEHOLDER]` markers in content or in any resumability doc → warning.

## Bundle scope

A bundle lives at one of three scope tiers, set by admin (not by the bundle itself):

- **show** (default on creation) — visible only to producers entitled to that show.
- **org** — visible to all producers in the owning org.
- **global** — visible to every org. Promote/demote restricted to Leporello admin role.

The bundle author doesn't choose scope at upload time — that's a downstream admin decision. The manifest shape is the same regardless.

## Versioning

Every upload produces a new immutable version under the same `bundleId`. Versions are integer strings starting at `"1"`, incrementing. The server assigns the version number; the producer omits it from the manifest. Old versions remain hosted indefinitely at concrete S3 prefixes.

## Storage layout (informational)

The skill doesn't write to S3, but the resulting URLs follow this pattern, which producers may see surfaced in admin or in `leporello.publish_bundle` responses:

```
<org>.interactives.leporello.tv/bundles/<bundle-id>/v<n>/index.html
```

`<bundle-id>` in the URL is the producer-supplied slug.

## Post-upload mutability

The artifact stored in S3 (`manifest.json`, `index.html`, supporting files) is **immutable per version**. New content = new version.

The one exception: `editorialReview` may be added or updated post-upload via admin. Storage mechanism (DB overlay vs. S3 manifest rewrite) is deferred; either way, per-version semantics are preserved.

Other manifest fields are not mutable post-upload — to change them, upload a new version.

## Telestrator field

The `telestrator` enum tells the on-air renderer which telestrator to mount on top of the bundle's iframe:

- `"default"` (omit or use this) — raster canvas telestrator. Strokes are pixel-anchored to the iframe rect. Suitable for everything that isn't a map.
- `"map"` — `MapTelestrator`. Strokes are lng/lat-anchored and re-project through pan/zoom. The bundle is expected to expose a `window.leporelloMap` reference (or similar handshake — to be specced) so the telestrator can hook into the bundle's MapLibre instance.

For v1 the skill produces `"default"` for non-map templates and `"map"` for the (forthcoming) map template. Don't invent other values.

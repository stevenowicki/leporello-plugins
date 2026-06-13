# `leporello-asset-bundle-author` — skill source

This directory is the source of the **Leporello asset-bundle authoring skill** — a Claude Code skill that helps producers build `.lepo` asset bundles under journalistic standards (sourced facts, no fabrication, visible uncertainty, broadcast-grade legibility).

The skill produces self-contained interactive HTML bundles that get loaded into Leporello packages and rendered on-air in front of a presenter.

For the full design context, see [`docs/prelim/skill-and-mcp-spec.md`](../../docs/prelim/skill-and-mcp-spec.md) in the main repo.

## Setup (do this first)

The skill needs a couple of base tools on your machine. **You install Node.js and
Python 3 yourself; the skill installs everything else.** Run `scripts/check_deps.sh`
once — it checks what's present and installs the rest (a Chromium engine for the design
checks). Full list and per-OS instructions: [`references/dependencies.md`](references/dependencies.md).

## What's in here

```
leporello-asset-bundle-author/
├── README.md                ← you are here
├── SKILL.md                 ← the loader manifest Claude Code reads
├── references/              ← load-on-demand reference docs
│   ├── bundle-format.md
│   ├── editorial-standards.md
│   ├── broadcast-standards.md
│   ├── design-system.md
│   └── template-catalog.md
├── templates/               ← starting scaffolds for new bundles
│   ├── generic/             ← minimal fallback (1A)
│   ├── timeline/ narrative-flow/ stat-callout/ quote-card/   ← 1B
│   └── …                    ← photo-collection / map land in 1C
│       each template holds:
│         TEMPLATE.md        ← template docs (NOT copied into the bundle)
│         README.md, CLAUDE.md ← per-bundle resumability skeletons
│                              (copied into the bundle, then filled in)
│         manifest.json, brief.md, content.json, index.html, lib/
├── lib/                     ← vendored DLS tokens, base CSS, JS helpers
│   ├── tokens.css
│   ├── base.css
│   └── helpers.js
└── scripts/
    ├── package.sh           ← zip a working dir into .lepo
    ├── preview.sh           ← serve a working dir via `npx serve`
    └── validate.sh          ← offline schema + structure check
```

## Installing locally for development

Claude Code only auto-discovers skills under `~/.claude/skills/` (user-global) or `<project>/.claude/skills/` (project-local). This `skills/` directory in the Leporello repo is the **source** of the skill, not an installation path — Claude Code will not find it here.

The simplest dev workflow is to symlink the source into your user-global Claude Code skills folder, so edits in this directory flow through to the running skill without copy/sync:

```bash
mkdir -p ~/.claude/skills
ln -s "$(pwd)/skills/leporello-asset-bundle-author" ~/.claude/skills/leporello-asset-bundle-author
```

Run that from the root of the Leporello repo. Restart Claude Code, then verify with the `/skills` command (in a real Claude Code session — not always available in every environment).

The skill should then trigger on prompts mentioning Leporello, asset bundles, `.lepo`, broadcast graphics, or similar phrases anywhere on the machine — not just inside the Leporello repo.

To uninstall: `rm ~/.claude/skills/leporello-asset-bundle-author`.

## Eventually: marketplace distribution

The dev install above is a stopgap. The eventual distribution path is the Leporello plugin marketplace:

```
/plugin marketplace add leporello.tv/marketplace
/plugin install leporello-asset-bundle-author
```

That ships in **Phase 4** (see [`docs/prelim/multi-tenancy-and-producer-authoring.md`](../../docs/prelim/multi-tenancy-and-producer-authoring.md)). Until then, symlink-from-repo is the dev workflow.

## Day-to-day commands

Once installed, the everyday loop for a producer is:

```bash
# preview a working bundle in a browser
./skills/leporello-asset-bundle-author/scripts/preview.sh <bundle-dir>

# validate structure + manifest before packaging (no network)
./skills/leporello-asset-bundle-author/scripts/validate.sh <bundle-dir>

# package the working dir into a .lepo
./skills/leporello-asset-bundle-author/scripts/package.sh <bundle-dir> out.lepo

# validate a packaged .lepo (same checks, run on the ZIP)
./skills/leporello-asset-bundle-author/scripts/validate.sh out.lepo
```

The skill orchestrates these for you during a Claude Code session; the raw commands are documented here for hand-debugging.

## Reference example

A minimal `.lepo` lives at [`examples/hello-leporello/`](../../examples/hello-leporello/) (plus the packaged `examples/hello-leporello.lepo`) for smoke-testing the scripts and as a worked example of the file shape.

## Roadmap

This skill ships in three sessions:

- **1A (shipped):** scaffolding + `generic` template + `brief.md` spec field
- **1B:** workhorse templates — `timeline`, `narrative-flow`, `stat-callout`, `quote-card`. `dashboard` was originally planned for 1B and dropped during scoping; see [`references/template-catalog.md`](references/template-catalog.md) for the rationale.
- **1C:** specialized templates — `photo-collection`, `map` (the latter with the `telestrator: "map"` manifest hint and a MapLibre scaffold)

Phase 2 builds the Leporello-side bundle upload pipeline (admin drag-and-drop, S3 hosting, on-air iframe render). Phase 4 adds the MCP server (`mcp.leporello.tv`) so the skill can upload directly without producer involvement, and ships the marketplace install path.

## Contributing

Edit in place; the symlinked install picks up changes immediately. Run `./scripts/validate.sh examples/hello-leporello` after any change that touches the manifest schema or validator — the reference example is the canonical "this should always pass cleanly" fixture. If your change requires the example to update, that's the signal that the change is a spec-level edit, not just a skill-internal one — update the spec at `docs/prelim/bundle-format-spec.md` too.

Open PRs against `feat/multi-tenant`, not `main`. The long-running branch ships to `main` only at the coordinated cutover (see the branching-strategy section of the parent planning doc).

# Leporello plugins

Public Claude Code plugin marketplace for [Leporello](https://leporello.tv) — the
broadcast presentation tool. Producers install the asset-bundle authoring skill and
the `mcp.leporello.tv` connector from here with two one-time commands:

```bash
claude plugin marketplace add stevenowicki/leporello-plugins
claude plugin install leporello-asset-bundle-author@leporello
```

> Install uses the `claude plugin …` CLI (or `/plugin` inside a *terminal* `claude`
> session — the in-app `/plugin` command isn't available in the Claude Desktop app).
> Once installed, the plugin runs fully inside Claude Desktop.

Then restart Claude Desktop and run `/leporello-setup` once. Full guide:
https://leporello.tv/docs/producers/custom-interactives

> This repo is generated. Source of truth is the private Leporello monorepo
> (`plugins/` + `skills/` + `dls/`); CI publishes here on change. Do not edit by hand.

# Leporello plugins

Public Claude Code plugin marketplace for [Leporello](https://leporello.tv) — the
broadcast presentation tool. Producers install the asset-bundle authoring skill and
the `mcp.leporello.tv` connector from here in two lines:

```
/plugin marketplace add stevenowicki/leporello-plugins
/plugin install leporello-asset-bundle-author
```

Then run `/leporello-setup` once and start building. Full guide:
https://leporello.tv/docs/producers/custom-interactives

> This repo is generated. Source of truth is the private Leporello monorepo
> (`plugins/` + `skills/` + `dls/`); CI publishes here on change. Do not edit by hand.

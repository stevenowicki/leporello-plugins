---
description: One-time setup for the Leporello asset-bundle skill — installs the Node/Python prerequisites for you (with your approval), connects your Leporello account token, and verifies everything works.
---

# Leporello setup

You are running the producer's one-time setup for the Leporello asset-bundle
skill. Your job is to get them from "just installed the plugin" to "can build and
deploy an interactive" with as little friction as possible. **You do the work; they
just approve each step.** Be warm, brief, and concrete — this person is a broadcast
producer, not a developer. Never dump raw error output at them; translate it.

Work through these phases **in order**. After each phase, say one short line about
what just happened before moving on.

## Phase 1 — Detect the environment

Run `uname -s` (and, if it looks like Windows/WSL, check `uname -r` for "microsoft").
Establish which of these you're on: **macOS**, **Linux**, or **WSL on Windows**.
If a plain Windows shell with no POSIX tools (no `uname`, no `bash`), STOP and tell
them this skill needs WSL — point them to the Windows section of
https://leporello.tv/docs/producers/custom-interactives and offer to help set up WSL.

## Phase 2 — Check prerequisites

Run the dependency preflight:

```
bash "${CLAUDE_PLUGIN_ROOT}/skills/leporello-asset-bundle-author/scripts/check_deps.sh"
```

It prints `[ok]` / `[MISS]` per tool and auto-installs the Playwright browser engine.
Read its output. The tools it can flag as `[MISS]` are: **Node.js**, **npx**,
**Python3**, **zip**, **unzip**.

- If nothing is missing → say so and skip to Phase 4.
- If something is missing → go to Phase 3 and install it for them.

## Phase 3 — Install the missing prerequisites (with approval)

For each missing tool, you will RUN the install command yourself. Each command
surfaces a permission prompt — that prompt **is** the producer's approval, so always
let them see the real command. **Never run an installer silently, and never assume a
password.** After installing, re-run `check_deps.sh` to confirm.

Pick the command by platform:

**macOS**
- Installs go through Homebrew. First check whether it exists: `command -v brew`.
- If Homebrew is **missing**, install it first:
  ```
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  ```
  ⚠️ Before running it, tell the producer in plain words: *"This installs Homebrew,
  the standard Mac software installer. macOS will ask you to type your Mac login
  password in the terminal — that's expected and it won't be shown as you type."*
  This is the one step where they must type something themselves. After it finishes,
  make sure `brew` is on PATH for this session (Apple Silicon: `eval "$(/opt/homebrew/bin/brew shellenv)"`; Intel: `eval "$(/usr/local/bin/brew shellenv)"`).
- Then install whatever's missing: `brew install node python` (drop whichever is
  already present). `zip`/`unzip` ship with macOS — if those are the only misses,
  something is unusual; don't try to brew them, just report it.

**Linux**
- Detect the package manager: `apt-get` (Debian/Ubuntu), else `dnf` (Fedora/RHEL).
- Debian/Ubuntu: `sudo apt-get update && sudo apt-get install -y nodejs npm python3 zip unzip`
  (install only the missing ones). Warn them sudo may prompt for their password.
- Fedora/RHEL: `sudo dnf install -y nodejs python3 zip unzip` (missing ones only).
- If the distro's `nodejs` is older than v18, mention they may want the NodeSource
  LTS instead, but don't block on it — the skill only needs a modern-ish Node.

**WSL on Windows**
- Treat exactly like Debian/Ubuntu Linux above (WSL default is Ubuntu).

After the installs, **re-run `check_deps.sh`**. It must come back all-`[ok]` (and it
will finish by installing Chromium for the design render-gate). If a tool is still
missing, read the error, explain the likely cause in one sentence, and either retry
or hand them the download link from the script's hint. Do not proceed to Phase 4
until the preflight passes.

## Phase 4 — Connect their Leporello account (the token)

The skill uploads to **their** organization via a per-user machine token. Walk them
through getting it, then store it for them:

1. Ask them to sign in to https://admin.leporello.tv → **Settings → API Tokens** →
   **Generate** (name it after this device) → copy the token. It starts with `lp_`
   and is shown only once.
2. Ask them to paste the token to you.
3. Store it in their Claude settings env (NOT a shell profile — Claude Desktop
   launched from the dock won't read a shell profile, but it always reads this):
   - Read `~/.claude/settings.json` if it exists (create `{}` if not).
   - Merge — do **not** clobber existing keys — so the file ends up with:
     `{ "env": { "LEPORELLO_TOKEN": "lp_…their token…" } }`
   - Preserve any other existing `env` entries and top-level settings.
   - Write it back as valid JSON.
4. Tell them the token is stored and to **treat it like a password** — if it ever
   leaks they can revoke it on that same admin page instantly.

The plugin's MCP config reads `${LEPORELLO_TOKEN}` from that env at launch, so the
connection is now wired. It takes effect on the **next Claude restart**.

## Phase 5 — Verify, then hand off

The MCP env var is only picked up on a fresh launch, so the `leporello` MCP tools may
not be live in *this* session yet. Tell the producer:

> Setup's done. **Quit and reopen Claude Desktop once**, then come back here and say
> *"list my Leporello organizations"* — if it answers, you're fully connected and
> ready to build your first interactive.

If the `leporello` MCP tools already happen to be available in this session, you may
call `list_orgs` yourself to confirm the connection live and skip making them restart.

End by pointing them at the build-and-deploy walkthrough:
https://leporello.tv/docs/producers/custom-interactives — and offer to build
something with them right now (e.g. a quote card or a district map) as a first run.

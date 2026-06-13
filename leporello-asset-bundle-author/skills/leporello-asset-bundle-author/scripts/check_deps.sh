#!/usr/bin/env bash
# Dependency preflight for the Leporello asset-bundle skill. Run this FIRST
# (Workflow step 0) in any new environment. It:
#   1. verifies the prerequisites the PRODUCER must install (these can't be
#      auto-installed — they're the base tools everything else builds on), and
#   2. auto-installs the rest (the Playwright browser engine for the DLS
#      render-gate).
# Exits non-zero with copy-paste install instructions if anything is missing,
# so the skill can STOP and tell the producer exactly what to do rather than
# fail later with a cryptic error.
set -uo pipefail
skill_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
missing=0

chk() { # label  command  hint
  if command -v "$2" >/dev/null 2>&1; then
    printf '  [ok]   %-9s %s\n' "$1" "$($2 --version 2>&1 | head -1)"
  else
    printf '  [MISS] %-9s — %s\n' "$1" "$3"; missing=1
  fi
}

echo "Leporello skill — dependency preflight"
echo ""
echo "Required (install these yourself — they cannot be auto-installed):"
chk "Node.js"  node    "install the LTS from https://nodejs.org  (also gives you 'npx')"
chk "npx"      npx     "ships with Node.js — install Node from https://nodejs.org"
chk "Python3"  python3 "install 3.10+ from https://www.python.org/downloads/"
chk "zip"      zip     "preinstalled on macOS/Linux; on Windows run this skill under WSL or Git Bash"
chk "unzip"    unzip   "preinstalled on macOS/Linux; on Windows run this skill under WSL or Git Bash"

if [ "$missing" = 1 ]; then
  echo ""
  echo "[STOP] Install the [MISS] items above, reopen your terminal, then run this again."
  echo "       See references/dependencies.md for step-by-step setup."
  exit 1
fi

echo ""
echo "Auto-installing the rest (one time; the browser download is a few hundred MB):"
if [ ! -d "$skill_dir/node_modules/playwright" ] && ! node -e "require.resolve('playwright')" >/dev/null 2>&1; then
  echo "  - npm install (Playwright)…"
  if ( cd "$skill_dir" && npm install --no-audit --no-fund >/dev/null 2>&1 ); then
    echo "  [ok]   Playwright installed"
  else
    echo "  [MISS] npm install failed — check your Node.js install (https://nodejs.org)"; exit 1
  fi
else
  echo "  [ok]   Playwright already available"
fi

echo "  - playwright install chromium…"
if ( cd "$skill_dir" && npx --yes playwright install chromium >/dev/null 2>&1 ); then
  echo "  [ok]   Chromium ready — the DLS render-gate (scripts/dls_check.mjs) is enabled"
else
  echo "  [warn] Chromium install had trouble — dls_check may not run; the vision-critique still applies"
fi

echo ""
echo "[ok] Preflight complete. You're ready to build."

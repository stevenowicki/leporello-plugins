#!/usr/bin/env bash
# Preview a bundle working directory in a browser.
#
# Usage:  scripts/preview.sh [working-dir] [port]
#
# Defaults to the current directory and port 3000.
# Under the hood: `npx --yes serve <dir> -l <port>`.

set -euo pipefail

dir="${1:-.}"
port="${2:-3000}"

if [[ ! -d "$dir" ]]; then
  echo "error: $dir is not a directory" >&2
  exit 66
fi

if [[ ! -f "$dir/index.html" ]]; then
  echo "warning: $dir/index.html not found — preview may 404" >&2
fi

if ! command -v npx >/dev/null 2>&1; then
  echo "error: npx not found. Install Node.js to use the preview script." >&2
  exit 69
fi

echo "serving $dir at http://localhost:$port — Ctrl-C to stop"
exec npx --yes serve "$dir" -l "$port"

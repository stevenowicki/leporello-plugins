#!/usr/bin/env bash
# Package a working bundle directory into a .lepo (ZIP).
#
# Usage:  scripts/package.sh <working-dir> [output.lepo]
#
# Defaults output to <working-dir>/../<dirname>.lepo.

set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "usage: $0 <working-dir> [output.lepo]" >&2
  exit 64
fi

src="${1%/}"

if [[ ! -d "$src" ]]; then
  echo "error: $src is not a directory" >&2
  exit 66
fi

if [[ ! -f "$src/manifest.json" ]]; then
  echo "error: $src/manifest.json not found — not a bundle directory" >&2
  exit 65
fi

if [[ ! -f "$src/index.html" ]]; then
  echo "error: $src/index.html not found — every bundle requires one" >&2
  exit 65
fi

src_abs="$(cd "$src" && pwd)"
dirname="$(basename "$src_abs")"

if [[ $# -ge 2 ]]; then
  out="$2"
else
  out="$(dirname "$src_abs")/${dirname}.lepo"
fi

# Ensure output is absolute so cd into src doesn't break the relative path.
case "$out" in
  /*) out_abs="$out" ;;
  *) out_abs="$(pwd)/$out" ;;
esac

# Remove any stale archive at the destination.
rm -f "$out_abs"

# Zip from inside the src dir so file paths in the archive are relative
# to the bundle root (manifest.json, not workdir/manifest.json).
( cd "$src_abs" && zip -qr "$out_abs" . -x ".DS_Store" -x "__MACOSX/*" -x "*/.DS_Store" )

echo "packaged: $out_abs"

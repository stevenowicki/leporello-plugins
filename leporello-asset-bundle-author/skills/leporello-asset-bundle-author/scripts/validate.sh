#!/usr/bin/env bash
# Validate a Leporello bundle — local checks only, no network.
#
# Accepts either a working directory or a packaged .lepo file.
#
# Two gates run, in order:
#   1. _validate.py     — structural + manifest validation (authoritative;
#                         its errors fail the bundle).
#   2. lint_tokens.py   — token-discipline linter (hardcoded hex / raw px
#                         font-sizes / raw radii that should be --lep-* tokens).
#                         WARNING-only by default so it never blocks a producer
#                         mid-prep; with --strict it becomes a hard gate too.
#
# Usage:
#   scripts/validate.sh <working-dir> [--strict]
#   scripts/validate.sh <bundle.lepo> [--strict]
#
# Exit codes:
#   0  valid (structural errors=0; in --strict, token violations=0 too).
#   1  invalid (structural errors>0, OR --strict and token violations>0).
#   64 usage error.

set -euo pipefail

strict=""
target=""
for arg in "$@"; do
  case "$arg" in
    --strict) strict="--strict" ;;
    -*) echo "error: unknown flag $arg" >&2; exit 64 ;;
    *)
      if [[ -n "$target" ]]; then
        echo "error: multiple targets given" >&2; exit 64
      fi
      target="$arg"
      ;;
  esac
done

if [[ -z "$target" ]]; then
  echo "usage: $0 <working-dir-or-bundle.lepo> [--strict]" >&2
  exit 64
fi

if [[ ! -e "$target" ]]; then
  echo "error: $target does not exist" >&2
  exit 64
fi

# If target is a .lepo (or any zip), unpack to a tempdir and validate that.
cleanup_dir=""
trap '[[ -n "$cleanup_dir" ]] && rm -rf "$cleanup_dir"' EXIT

if [[ -f "$target" ]]; then
  cleanup_dir="$(mktemp -d)"
  if ! unzip -qq "$target" -d "$cleanup_dir" 2>/dev/null; then
    echo "ERROR  not a valid ZIP archive: $target" >&2
    exit 1
  fi
  bundle_dir="$cleanup_dir"
elif [[ -d "$target" ]]; then
  bundle_dir="$target"
else
  echo "error: $target is neither a file nor a directory" >&2
  exit 64
fi

# Hand off to the python validator for the actual checks. Python is available
# on every dev machine that runs Claude Code; keeps the script readable and
# avoids reimplementing JSON validation in bash.
script_dir="$(cd "$(dirname "$0")" && pwd)"

# Gate 1 — structural + manifest validation (authoritative).
validate_rc=0
python3 "$script_dir/_validate.py" "$bundle_dir" || validate_rc=$?

# Gate 2 — token-discipline linter. Non-fatal by default; --strict makes it
# a hard gate. We always run it (even when gate 1 failed) so the producer sees
# every issue in one pass. Its exit code only matters under --strict.
echo "--- token discipline ---" >&2
lint_rc=0
python3 "$script_dir/lint_tokens.py" $strict "$bundle_dir" || lint_rc=$?

# Structural errors always fail. Token violations fail only under --strict
# (lint_tokens.py already exits non-zero only when --strict is passed).
if [[ "$validate_rc" -ne 0 ]]; then
  exit "$validate_rc"
fi
exit "$lint_rc"

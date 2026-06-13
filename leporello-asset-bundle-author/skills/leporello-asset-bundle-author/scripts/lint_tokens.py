#!/usr/bin/env python3
"""Token-discipline linter for Leporello asset bundles.

Generated bundles are supposed to be styled entirely from the v1 DLS tokens
(the `--lep-*` CSS custom properties in `lib/tokens.css`). It's easy for a
generated `.lepo` to drift — a hardcoded `#4fb3ff` instead of
`var(--lep-data-primary)`, a raw `84px` headline instead of
`var(--lep-size-headline)`, a `border-radius: 8px` instead of
`var(--lep-radius-md)`. This linter catches that drift before the bundle ships.

WHAT IT SCANS
  - Standalone CSS files (`*.css`), EXCEPT the vendored `lib/tokens.css` itself
    (that file *defines* the raw values — it is the one place they're allowed).
  - `<style>...</style>` blocks inside HTML files.
  It deliberately does NOT scan:
  - JavaScript (MapLibre `setPaintProperty('fill-color', '#15436e')` and the
    like take literal color strings — they cannot be CSS `var()`).
  - Inline SVG markup (illustration `fill=`/`stroke=` attributes are artwork,
    not tokens).
  - HTML attributes outside `<style>`.

WHAT IT FLAGS  (each with the offending value + a suggested `var(--lep-*)`)
  1. Hardcoded hex colors in a CSS color context. Hex values that EXACTLY match
     a token get a precise suggestion ("use var(--lep-data-primary)"); other
     opaque hex colors are flagged as untokenized with the nearest guidance.
  2. Raw px font-sizes that match a ramp token (write `84px`, mean
     `var(--lep-size-headline)`). Off-ramp sizes that DON'T match a tier (an
     intentional hero override like `270px`, a `26px` micro-tag) are a
     legitimate authoring freedom and are NOT flagged by default — pass
     `--pedantic` to surface them as advisories.
  3. Raw px border-radius values that match a radius token.

WHITELIST (documented, narrow — avoids false positives)
  - `rgba(...)` / `hsla(...)` values entirely: scrims, halos, shadows,
    text-strokes and translucent borders are parametric, not palette tokens.
    (The few rgba values that ARE tokens — overlay/telestration-halo — are
    intentionally not enforced; they're compositional, not drift-prone.)
  - Pure black / white shorthands `#000`, `#000000`, `#fff`, `#ffffff` — used
    for functional fills (true-black letterbox, white-halo) where a semantic
    token would be misleading. (`#ffffff` is also the halo token; either is OK.)
  - Any value already written as `var(--lep-...)`.
  - The vendored `lib/` directory (tokens.css, base.css, helpers.js, fonts):
    it's the hand-authored, design-reviewed foundation shipped verbatim with
    every bundle — not generated content. The linter audits the generated
    template layer (`index.html` + per-template `<style>`), not the library.
  - Lines carrying a trailing `/* lint-tokens:allow <reason> */` comment.

INLINE ESCAPE HATCH
  Put `/* lint-tokens:allow reason */` at the end of a declaration line to
  suppress that one line. Use sparingly and say why.

EXIT CODE
  0  no violations (or violations present but not --strict).
  1  violations present AND --strict.
  By default this linter is a WARNING gate: it prints findings and exits 0 so it
  never blocks a producer mid-broadcast-prep. Pass --strict (CI / pre-publish)
  to make any violation fatal.

NOTE FOR LATER: the API-side bundle validator (api/app/bundles/validator.py)
should mirror this check server-side so drift can't be smuggled past a
hand-edited upload. Tracked as a follow-up; this client-side gate is first.

USAGE
  scripts/lint_tokens.py <bundle-dir-or-file> [more files...] [--strict]
  scripts/lint_tokens.py <bundle.lepo> [--strict]      # zip is unpacked
  scripts/lint_tokens.py <dir> --pedantic              # also surface off-ramp
                                                       # (non-tier) font-sizes
"""

from __future__ import annotations

import re
import sys
import tempfile
import zipfile
from pathlib import Path

# ---------------------------------------------------------------------------
# Token tables, loaded from lib/tokens.css so the linter can never drift from
# the canonical token values. We map each raw value -> its --lep-* variable.
# ---------------------------------------------------------------------------

HEX_RE = re.compile(r"#[0-9a-fA-F]{3,8}\b")
PX_RE = re.compile(r"(?<![\w.])(\d+(?:\.\d+)?)px\b")
VAR_DECL_RE = re.compile(r"(--lep-[a-z0-9-]+)\s*:\s*([^;{}]+);")
COMMENT_RE = re.compile(r"/\*.*?\*/", re.S)

# Color shorthands that are always allowed (functional black/white).
ALLOWED_BLACK_WHITE = {"#000", "#000000", "#fff", "#ffffff"}

# Font-size declarations below this px are chrome (tags, micro-labels) and the
# ramp doesn't govern them; declarations >= this and not on a tier are flagged
# as off-ramp. The ramp floor is 22px (source); we start nudging at 24px so a
# 22/legend tier isn't accidentally below the gate.
STORYTELLING_MIN_PX = 24.0

# Properties whose value is a color we should scrutinise for raw hex. We scan
# the whole declaration's value, but only emit a hex finding when the property
# is one of these (keeps us from flagging hex inside, e.g., a url() or a
# gradient stop offset — though those are rgba in practice).
COLOR_PROPS = {
    "color",
    "background",
    "background-color",
    "border",
    "border-color",
    "border-top-color",
    "border-right-color",
    "border-bottom-color",
    "border-left-color",
    "outline",
    "outline-color",
    "fill",
    "stroke",
    "box-shadow",
    "text-shadow",
    "caret-color",
    "text-decoration-color",
    "column-rule-color",
    "accent-color",
    "stop-color",
    "flood-color",
    "-webkit-text-fill-color",
}

ALLOW_COMMENT_RE = re.compile(r"/\*\s*lint-tokens:allow\b", re.IGNORECASE)


def load_token_maps(tokens_css: Path) -> tuple[dict, dict, dict]:
    """Return (hex->var, sizepx->var, radiuspx->var) parsed from tokens.css."""
    hex_map: dict[str, str] = {}
    size_map: dict[str, str] = {}
    radius_map: dict[str, str] = {}
    try:
        text = tokens_css.read_text(encoding="utf-8")
    except OSError:
        return hex_map, size_map, radius_map
    text = COMMENT_RE.sub("", text)
    for name, raw in VAR_DECL_RE.findall(text):
        val = raw.strip()
        hm = re.fullmatch(r"#[0-9a-fA-F]{3,8}", val)
        if hm:
            hex_map.setdefault(_norm_hex(val), name)
            continue
        pm = re.fullmatch(r"(\d+(?:\.\d+)?)px", val)
        if pm:
            if "size" in name:
                size_map.setdefault(val, name)
            elif "radius" in name:
                radius_map.setdefault(val, name)
    return hex_map, size_map, radius_map


def _norm_hex(h: str) -> str:
    """Lowercase + expand 3/4-digit shorthand to 6/8 for comparison."""
    h = h.lower()
    body = h[1:]
    if len(body) in (3, 4):
        body = "".join(c * 2 for c in body)
    return "#" + body


# ---------------------------------------------------------------------------
# Finding model
# ---------------------------------------------------------------------------


class Finding:
    __slots__ = ("file", "line", "kind", "value", "suggestion")

    def __init__(self, file: str, line: int, kind: str, value: str, suggestion: str):
        self.file = file
        self.line = line
        self.kind = kind
        self.value = value
        self.suggestion = suggestion

    def format(self) -> str:
        return (
            f"{self.file}:{self.line}  {self.kind}  {self.value}\n"
            f"    -> {self.suggestion}"
        )


# ---------------------------------------------------------------------------
# CSS source extraction
# ---------------------------------------------------------------------------

STYLE_BLOCK_RE = re.compile(r"<style\b[^>]*>(.*?)</style>", re.S | re.I)


def css_segments(path: Path) -> list[tuple[int, str]]:
    """Yield (start_line, css_text) segments to lint for a given file.

    For .css -> the whole file (one segment starting at line 1).
    For .html/.htm -> each <style> block, with the correct starting line so
    reported line numbers point into the original HTML.
    """
    ext = path.suffix.lower()
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return []
    if ext == ".css":
        return [(1, text)]
    if ext in (".html", ".htm"):
        segs: list[tuple[int, str]] = []
        for m in STYLE_BLOCK_RE.finditer(text):
            start = text.count("\n", 0, m.start(1)) + 1
            segs.append((start, m.group(1)))
        return segs
    return []


# ---------------------------------------------------------------------------
# The core lint pass over a CSS segment
# ---------------------------------------------------------------------------


def lint_css_segment(
    file_label: str,
    start_line: int,
    css: str,
    hex_map: dict,
    size_map: dict,
    radius_map: dict,
    findings: list[Finding],
    pedantic: bool = False,
) -> None:
    # Strip comments for property detection but keep line numbers by replacing
    # comment bodies with same-newline-count blanks.
    def blank_comment(m: re.Match) -> str:
        return "\n" * m.group(0).count("\n")

    no_comments = COMMENT_RE.sub(blank_comment, css)

    raw_lines = css.splitlines()
    clean_lines = no_comments.splitlines()

    for i, clean in enumerate(clean_lines):
        ln = start_line + i
        raw = raw_lines[i] if i < len(raw_lines) else ""

        # Per-line escape hatch.
        if ALLOW_COMMENT_RE.search(raw):
            continue

        stripped = clean.strip()
        if not stripped:
            continue

        # Identify the CSS property on this declaration line, if any. We do a
        # simple "prop: value" split; multi-line declarations (e.g. a box-shadow
        # spanning lines) still get scanned line-by-line, and we treat a line
        # with no colon as a value continuation that inherits color scrutiny
        # only when it sits inside the value list — approximated by also
        # scanning continuation lines for token-equal hex.
        prop = None
        value_part = clean
        if ":" in clean and not clean.lstrip().startswith("--"):
            head, _, tail = clean.partition(":")
            cand = head.strip().lower()
            # property names: letters, digits, hyphens only
            if re.fullmatch(r"-?[a-z][a-z0-9-]*", cand):
                prop = cand
                value_part = tail

        is_color_prop = prop in COLOR_PROPS if prop else False
        is_font_size = prop == "font-size"
        is_radius = prop in ("border-radius",) or (
            prop is not None and prop.endswith("-radius")
        )

        # --- 1. Hex colors -------------------------------------------------
        # Flag hex that exactly matches a token (strong) anywhere it appears in
        # a color-property value or a value-continuation line. Flag other
        # opaque hex only when the property is clearly a color property.
        for m in HEX_RE.finditer(value_part):
            hexval = m.group(0)
            norm = _norm_hex(hexval)
            if hexval.lower() in ALLOWED_BLACK_WHITE:
                continue
            if norm in hex_map:
                findings.append(
                    Finding(
                        file_label,
                        ln,
                        "hardcoded-color",
                        hexval,
                        f"use var({hex_map[norm]}) — exact token match",
                    )
                )
            elif is_color_prop:
                findings.append(
                    Finding(
                        file_label,
                        ln,
                        "untokenized-color",
                        hexval,
                        "no token matches this hex; pick the nearest "
                        "--lep-* color role or move this to JS/SVG if it's "
                        "MapLibre paint or artwork",
                    )
                )

        # --- 2. Font-size px ----------------------------------------------
        if is_font_size:
            for m in PX_RE.finditer(value_part):
                px = m.group(0)
                pxnum = float(m.group(1))
                if px in size_map:
                    findings.append(
                        Finding(
                            file_label,
                            ln,
                            "raw-font-size",
                            px,
                            f"use var({size_map[px]}) — token tier",
                        )
                    )
                elif pedantic and pxnum >= STORYTELLING_MIN_PX:
                    findings.append(
                        Finding(
                            file_label,
                            ln,
                            "offramp-font-size",
                            px,
                            "off-ramp size (advisory); a type tier "
                            "(--lep-size-*: 22/34/40/64/72/84/150) is usually "
                            "right, but an intentional hero override / micro-tag "
                            "is a legitimate exception",
                        )
                    )

        # --- 3. Radius px --------------------------------------------------
        if is_radius:
            for m in PX_RE.finditer(value_part):
                px = m.group(0)
                if px in radius_map:
                    findings.append(
                        Finding(
                            file_label,
                            ln,
                            "raw-radius",
                            px,
                            f"use var({radius_map[px]}) — radius token",
                        )
                    )


# ---------------------------------------------------------------------------
# File / bundle walking
# ---------------------------------------------------------------------------

LINTABLE_EXTS = {".css", ".html", ".htm"}


def _is_vendored_lib(path: Path, bundle_root: Path) -> bool:
    """True if path is inside the bundle's vendored `lib/` directory.

    The lib (tokens.css, base.css, helpers.js, fonts) is the hand-authored,
    design-reviewed foundation shipped verbatim with every bundle — it
    legitimately holds raw token values and parametric colors and is NOT
    generated content, so it's out of scope for the drift linter.
    """
    try:
        rel = path.relative_to(bundle_root)
    except ValueError:
        return path.name == "tokens.css" or "lib" in path.parts
    return rel.parts and rel.parts[0] == "lib"


def gather_files(target: Path) -> list[Path]:
    if target.is_file():
        return [target]
    out: list[Path] = []
    for p in sorted(target.rglob("*")):
        if p.is_file() and p.suffix.lower() in LINTABLE_EXTS:
            out.append(p)
    return out


def lint_target(
    target: Path,
    bundle_root: Path,
    hex_map: dict,
    size_map: dict,
    radius_map: dict,
    findings: list[Finding],
    pedantic: bool = False,
) -> None:
    for path in gather_files(target):
        if _is_vendored_lib(path, bundle_root):
            continue
        try:
            label = str(path.relative_to(bundle_root))
        except ValueError:
            label = str(path)
        for start_line, css in css_segments(path):
            lint_css_segment(
                label,
                start_line,
                css,
                hex_map,
                size_map,
                radius_map,
                findings,
                pedantic=pedantic,
            )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main(argv: list[str]) -> int:
    flags = {"--strict", "--pedantic"}
    args = [a for a in argv if a not in flags]
    strict = "--strict" in argv
    pedantic = "--pedantic" in argv

    if not args:
        print(
            "usage: lint_tokens.py <bundle-dir-or-file> [more...] "
            "[--strict] [--pedantic]",
            file=sys.stderr,
        )
        return 64

    script_dir = Path(__file__).resolve().parent
    skill_root = script_dir.parent

    findings: list[Finding] = []
    tmpdirs: list[tempfile.TemporaryDirectory] = []

    for raw_target in args:
        target = Path(raw_target)
        if not target.exists():
            print(f"lint_tokens: {target} does not exist", file=sys.stderr)
            return 64

        # If a .lepo / zip was passed, unpack it.
        if target.is_file() and zipfile.is_zipfile(target):
            td = tempfile.TemporaryDirectory()
            tmpdirs.append(td)
            with zipfile.ZipFile(target) as zf:
                zf.extractall(td.name)
            bundle_root = Path(td.name)
            scan_root = bundle_root
        elif target.is_dir():
            bundle_root = target
            scan_root = target
        else:
            # single loose file
            bundle_root = target.parent
            scan_root = target

        # Resolve the token table from the bundle's own lib/tokens.css when it
        # has one (the values it ships against), else fall back to the skill's
        # bundled tokens.css. This keeps suggestions accurate even if a bundle
        # pins an older token set.
        candidates = [
            bundle_root / "lib" / "tokens.css",
            bundle_root / "tokens.css",
            skill_root / "tokens.css",
            skill_root / "lib" / "tokens.css",
        ]
        tokens_css = next((c for c in candidates if c.is_file()), None)
        if tokens_css is None:
            print(
                "lint_tokens: WARNING no tokens.css found for "
                f"{target} — running with empty token table (exact-match "
                "suggestions disabled)",
                file=sys.stderr,
            )
            hex_map, size_map, radius_map = {}, {}, {}
        else:
            hex_map, size_map, radius_map = load_token_maps(tokens_css)

        lint_target(
            scan_root,
            bundle_root,
            hex_map,
            size_map,
            radius_map,
            findings,
            pedantic=pedantic,
        )

    for td in tmpdirs:
        td.cleanup()

    # Report.
    if findings:
        for f in findings:
            print(f.format(), file=sys.stderr)
    n = len(findings)
    by_kind: dict[str, int] = {}
    for f in findings:
        by_kind[f.kind] = by_kind.get(f.kind, 0) + 1
    breakdown = ", ".join(f"{k}={v}" for k, v in sorted(by_kind.items())) or "—"

    if n == 0:
        print("lint_tokens: 0 violations — clean", file=sys.stderr)
        return 0

    severity = "ERROR" if strict else "WARNING"
    print(
        f"lint_tokens: {n} token-discipline {severity}(s) [{breakdown}]",
        file=sys.stderr,
    )
    if not strict:
        print(
            "lint_tokens: non-fatal (warning mode). Re-run with --strict to "
            "fail on these.",
            file=sys.stderr,
        )
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

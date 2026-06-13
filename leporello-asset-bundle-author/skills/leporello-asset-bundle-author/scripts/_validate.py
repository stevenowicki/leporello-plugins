#!/usr/bin/env python3
"""Local Leporello bundle validator.

Mirrors the structural + manifest checks defined in references/bundle-format.md.
Content checks (HTML well-formedness, MIME sniffing) and security checks
(file:// references, traversal in linked URLs) live server-side.

Outputs:
  - One line per error / warning to stderr: "ERROR  <code>  <message>".
  - Summary line to stderr: "validate: N errors, M warnings".

Exit code:
  0 if errors == 0 (warnings are not fatal).
  1 otherwise.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from typing import Iterable

SCHEMA_VERSION_OK = {"1.0"}
TELESTRATOR_OK = {"default", "map"}

# Resumability root docs: (manifest field, default filename, missing-warning text).
# Found by convention at the bundle root when the manifest omits the field.
RESUMABILITY_DOCS = [
    ("brief", "brief.md", "brief.md is missing — skill-generated bundles should ship an editorial brief (editorial intent)"),
    ("readme", "README.md", "README.md is missing — skill-generated bundles should ship producer-facing operating docs"),
    ("claude", "CLAUDE.md", "CLAUDE.md is missing — skill-generated bundles should ship AI-resumption context"),
]
SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]{1,62}[a-z0-9]$")
ISO8601_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})$"
)
URL_RE = re.compile(r"^https?://", re.IGNORECASE)
HTTPS_URL_RE = re.compile(r"^https://", re.IGNORECASE)

MAX_TOTAL_BYTES = 50 * 1024 * 1024
MAX_FILE_BYTES = 10 * 1024 * 1024

ALLOWED_EXTS = {
    ".html",
    ".htm",
    ".css",
    ".js",
    ".mjs",
    ".json",
    ".csv",
    ".tsv",
    ".geojson",
    ".pmtiles",
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".svg",
    ".gif",
    ".mp4",
    ".m4v",
    ".woff",
    ".woff2",
    ".ttf",
    ".otf",
    ".txt",
    ".md",
}

errors: list[tuple[str, str]] = []
warnings: list[tuple[str, str]] = []


def err(code: str, msg: str) -> None:
    errors.append((code, msg))


def warn(code: str, msg: str) -> None:
    warnings.append((code, msg))


def iter_files(root: Path) -> Iterable[Path]:
    for p in root.rglob("*"):
        if p.is_file():
            yield p


def check_structure(root: Path) -> None:
    if not (root / "manifest.json").is_file():
        err("missing_manifest", "manifest.json not found at bundle root")
    if not (root / "index.html").is_file():
        err("missing_index", "index.html not found at bundle root")

    total_bytes = 0
    for p in iter_files(root):
        rel = p.relative_to(root)
        rel_posix = rel.as_posix()

        if p.is_symlink():
            err("symlink", f"symlinks not allowed: {rel_posix}")
            continue
        if rel_posix.startswith("/") or ".." in rel.parts:
            err("path_traversal", f"path normalization violation: {rel_posix}")

        size = p.stat().st_size
        total_bytes += size
        if size > MAX_FILE_BYTES:
            err("file_too_large", f"{rel_posix} is {size} bytes (cap {MAX_FILE_BYTES})")

        ext = p.suffix.lower()
        if ext and ext not in ALLOWED_EXTS:
            warn("unusual_ext", f"unusual file extension: {rel_posix}")

    if total_bytes > MAX_TOTAL_BYTES:
        err(
            "total_too_large",
            f"bundle is {total_bytes} bytes uncompressed (cap {MAX_TOTAL_BYTES})",
        )


def check_manifest(root: Path) -> None:
    mpath = root / "manifest.json"
    if not mpath.is_file():
        return  # already reported

    try:
        manifest = json.loads(mpath.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        err("manifest_invalid_json", f"manifest.json is not valid JSON: {e}")
        return
    except UnicodeDecodeError as e:
        err("manifest_encoding", f"manifest.json is not valid UTF-8: {e}")
        return

    if not isinstance(manifest, dict):
        err("manifest_not_object", "manifest.json must be a JSON object")
        return

    required_strings = ["schemaVersion", "bundleId", "title", "entry", "attribution", "generatedBy", "createdAt"]
    for key in required_strings:
        v = manifest.get(key)
        if v is None:
            err("missing_required", f"manifest.{key} is required")
        elif not isinstance(v, str) or not v.strip():
            err("wrong_type", f"manifest.{key} must be a non-empty string (got {type(v).__name__})")

    if "sources" not in manifest:
        err("missing_required", "manifest.sources is required (may be empty array)")
    elif not isinstance(manifest["sources"], list):
        err("wrong_type", "manifest.sources must be an array")

    sv = manifest.get("schemaVersion")
    if isinstance(sv, str) and sv not in SCHEMA_VERSION_OK:
        err("unknown_schema_version", f"schemaVersion {sv!r} not recognized; expected one of {sorted(SCHEMA_VERSION_OK)}")

    bid = manifest.get("bundleId")
    if isinstance(bid, str) and not SLUG_RE.match(bid):
        err("bad_slug", f"bundleId {bid!r}: must be lowercase ASCII + digits + hyphens, length 3-64, no leading/trailing hyphen")

    slug = manifest.get("slug")
    if slug is not None and (not isinstance(slug, str) or not SLUG_RE.match(slug)):
        err("bad_slug", f"slug {slug!r}: must match same rules as bundleId")

    created = manifest.get("createdAt")
    if isinstance(created, str) and not ISO8601_RE.match(created):
        err("bad_iso8601", f"createdAt {created!r}: must be ISO 8601 (e.g. 2026-04-15T09:30:00Z)")

    entry = manifest.get("entry")
    if isinstance(entry, str) and not (root / entry).is_file():
        err("entry_missing", f"entry {entry!r} does not exist in bundle")

    content_field = manifest.get("content")
    if isinstance(content_field, str) and not (root / content_field).is_file():
        err("content_missing", f"content {content_field!r} does not exist in bundle")

    # Resumability artifacts — the three-way root-doc split:
    #   brief.md  = editorial intent      README.md = producer ops
    #   CLAUDE.md = AI-resumption context
    # Each is referenced by an optional manifest field but found by convention at
    # the bundle root if the field is omitted. Skill-generated bundles are
    # expected to ship all three; missing one is a soft warning, not an error.
    generated_by = manifest.get("generatedBy", "")
    is_skill = isinstance(generated_by, str) and generated_by.startswith("claude-leporello-skill")

    for field, default_name, missing_msg in RESUMABILITY_DOCS:
        value = manifest.get(field)
        doc_path: Path | None = None
        if isinstance(value, str):
            if not (root / value).is_file():
                err(f"{field}_missing", f"{field} {value!r} does not exist in bundle")
            else:
                doc_path = root / value
        elif value is None and (root / default_name).is_file():
            # Convention: the file at root is found even if the manifest omits the field.
            doc_path = root / default_name

        if is_skill and doc_path is None:
            warn(f"missing_{field}", missing_msg)

        if doc_path is not None:
            try:
                text = doc_path.read_text(encoding="utf-8")
            except UnicodeDecodeError as e:
                err(f"{field}_encoding", f"{doc_path.name} is not valid UTF-8: {e}")
            else:
                if "[CLAUDE-PLACEHOLDER" in text:
                    warn(
                        f"placeholder_in_{field}",
                        f"unfilled placeholder(s) in {doc_path.name} — fill before packaging",
                    )

    tele = manifest.get("telestrator", "default")
    if tele not in TELESTRATOR_OK:
        err("bad_telestrator", f"telestrator {tele!r} not recognized; expected one of {sorted(TELESTRATOR_OK)}")

    sources = manifest.get("sources")
    seen_ids: set[str] = set()
    if isinstance(sources, list):
        for i, src in enumerate(sources):
            if not isinstance(src, dict):
                err("source_not_object", f"sources[{i}] must be an object")
                continue
            sid = src.get("id")
            if not isinstance(sid, str) or not sid:
                err("source_missing_id", f"sources[{i}].id is required and must be a string")
            elif sid in seen_ids:
                err("duplicate_source_id", f"sources[{i}].id {sid!r} is a duplicate")
            else:
                seen_ids.add(sid)
            if not isinstance(src.get("title"), str) or not src["title"]:
                err("source_missing_title", f"sources[{i}].title is required")
            url = src.get("url")
            if url is not None:
                if not isinstance(url, str):
                    err("source_bad_url_type", f"sources[{i}].url must be a string")
                elif not URL_RE.match(url):
                    err("source_bad_url_scheme", f"sources[{i}].url must be http(s)")

    ext_deps = manifest.get("externalDependencies")
    if isinstance(ext_deps, list):
        for i, u in enumerate(ext_deps):
            if not isinstance(u, str) or not HTTPS_URL_RE.match(u):
                warn("ext_dep_not_https", f"externalDependencies[{i}] should be HTTPS")

    er = manifest.get("editorialReview")
    if er is None:
        warn("missing_editorial_review", "editorialReview is missing — admin will surface a post-hoc review prompt")
    elif isinstance(er, dict):
        ra = er.get("reviewedAt")
        if ra is not None and (not isinstance(ra, str) or not ISO8601_RE.match(ra)):
            err("bad_iso8601", f"editorialReview.reviewedAt {ra!r}: must be ISO 8601")

    if "version" in manifest:
        warn(
            "version_in_manifest",
            "manifest.version is server-assigned; the upload pipeline will overwrite this value",
        )

    if isinstance(content_field, str) and (root / content_field).is_file():
        try:
            payload = json.loads((root / content_field).read_text(encoding="utf-8"))
            scan_for_placeholders(content_field, payload)
        except json.JSONDecodeError as e:
            err("content_invalid_json", f"{content_field} is not valid JSON: {e}")

    scan_manifest_placeholders("manifest.json", manifest)


def scan_for_placeholders(path: str, value, breadcrumb: str = "") -> None:
    if isinstance(value, str):
        if "[CLAUDE-PLACEHOLDER" in value:
            warn(
                "placeholder_in_content",
                f"unfilled placeholder in {path}{breadcrumb}: {value!r}",
            )
    elif isinstance(value, dict):
        for k, v in value.items():
            scan_for_placeholders(path, v, f"{breadcrumb}.{k}")
    elif isinstance(value, list):
        for i, v in enumerate(value):
            scan_for_placeholders(path, v, f"{breadcrumb}[{i}]")


def scan_manifest_placeholders(path: str, value, breadcrumb: str = "") -> None:
    # In the manifest, placeholders are errors (not warnings) — required fields
    # cannot remain unfilled at upload time.
    if isinstance(value, str):
        if "[CLAUDE-PLACEHOLDER" in value:
            err(
                "placeholder_in_manifest",
                f"unfilled placeholder in {path}{breadcrumb}: {value!r}",
            )
    elif isinstance(value, dict):
        for k, v in value.items():
            scan_manifest_placeholders(path, v, f"{breadcrumb}.{k}")
    elif isinstance(value, list):
        for i, v in enumerate(value):
            scan_manifest_placeholders(path, v, f"{breadcrumb}[{i}]")


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: _validate.py <bundle-dir>", file=sys.stderr)
        return 64

    root = Path(sys.argv[1]).resolve()
    if not root.is_dir():
        print(f"error: {root} is not a directory", file=sys.stderr)
        return 64

    check_structure(root)
    check_manifest(root)

    for code, msg in errors:
        print(f"ERROR  {code}  {msg}", file=sys.stderr)
    for code, msg in warnings:
        print(f"WARN   {code}  {msg}", file=sys.stderr)

    print(f"validate: {len(errors)} errors, {len(warnings)} warnings", file=sys.stderr)
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())

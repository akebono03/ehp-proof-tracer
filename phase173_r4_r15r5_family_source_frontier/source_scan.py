"""Read-only search for *possible* family definitions in adopted Toda TeX files.

A text occurrence is not a cited statement, proof leaf, or verified definition.
Nothing here registers a new mathematical assertion.
"""
from __future__ import annotations

from pathlib import Path
import hashlib
import re


FAMILY_LABELS = {56: r"\bar{\kappa}", 88: r"\delta"}

# These expressions are intentionally conservative candidates, not validators.
# A paragraph with a matching string still requires independent source review.
PATTERNS = {
    56: (
        ("indexed_definition", re.compile(
            r"(?:\\bar\{\\kappa\}|\\overline\{\\kappa\})_\{?n\}?\s*(?::=|=)\s*E",
            re.MULTILINE,
        )),
        ("consecutive_suspension", re.compile(
            r"E\s*(?:\\bar\{\\kappa\}|\\overline\{\\kappa\})_\{?\d+\}?\s*=",
            re.MULTILINE,
        )),
    ),
    88: (
        ("indexed_definition", re.compile(
            r"\\delta_\{?n\}?\s*(?::=|=)\s*E",
            re.MULTILINE,
        )),
        ("consecutive_suspension", re.compile(
            r"E\s*\\delta_\{?\d+\}?\s*=",
            re.MULTILINE,
        )),
    ),
}


def scan_text(text: str, *, family_id: int, relative_path: str,
              max_matches: int = 24) -> tuple[dict[str, object], ...]:
    """Return unreviewed text hits; never interpret them as equalities."""
    if family_id not in PATTERNS or type(max_matches) is not int or max_matches < 1:
        raise ValueError("Unreviewed family ID or match limit")
    hits: list[dict[str, object]] = []
    for kind, expression in PATTERNS[family_id]:
        for match in expression.finditer(text):
            excerpt = " ".join(text[max(0, match.start() - 70):
                                    min(len(text), match.end() + 100)].split())
            hits.append({
                "path": relative_path,
                "line": text.count("\n", 0, match.start()) + 1,
                "kind": kind,
                "excerpt": excerpt[:240],
                "source_reviewed": False,
            })
    return tuple(sorted(hits, key=lambda hit: (hit["path"], hit["line"], hit["kind"]))[:max_matches])


def scan_adopted_toda_sources(root: Path, *, family_id: int) -> dict[str, object]:
    """Search actual adopted TeX files; do not read archived reports as evidence."""
    root = root.resolve()
    directory = root / "sources" / "toda"
    paths = tuple(sorted(directory.glob("Toda_*_2.tex")))
    if not paths:
        raise RuntimeError("No reviewed Toda chapter source files found")
    observations: list[dict[str, object]] = []
    matches: list[dict[str, object]] = []
    for path in paths:
        raw = path.read_bytes()
        text = raw.decode("utf-8-sig")
        relative = path.relative_to(root).as_posix()
        observations.append({
            "path": relative,
            "sha256": hashlib.sha256(raw).hexdigest(),
            "lines": len(text.splitlines()),
        })
        matches.extend(scan_text(text, family_id=family_id, relative_path=relative))
    return {
        "family_id": family_id,
        "name": FAMILY_LABELS[family_id],
        "source_files": observations,
        "candidate_text_hits": matches,
        "source_definition_certified": False,
        "new_given_created": False,
        "interpretation": "TEXT_HITS_REQUIRE_INDEPENDENT_SOURCE_REVIEW",
    }

# Phase 173 R4-R15R5 — complete code and focused tests

All files listed below are new; existing project modules and imports are unchanged.

## `source_scan.py`

```python
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
```

## `audit.py`

```python
"""R15R5: correlate actual k=31 proof blockers with source-definition text hits.

This is an observational source-audit, not a public search rule or new GIVEN.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from phase169_r10b_registered_stable_family_binding.family_registry import (
    read_registered_stable_families,
)
from phase173_r4_r15r4_cited_composition_image.audit import inspect_k
from phase173_r4_r15r4_cited_composition_image.replay import cited_source_steps
from phase173_r4_r15r5_family_source_frontier.source_scan import (
    FAMILY_LABELS,
    scan_adopted_toda_sources,
)
from phase169_r10d2_general_family_definition.family_citation import (
    CitedStableFamilyDefinition,
)


def inspect_family_source_frontier(root: Path, k: int = 31) -> dict[str, object]:
    """Report exact unresolved pairs and source candidates without proof promotion."""
    if type(k) is not int or k < 3:
        raise ValueError("Expected k>=3")
    image_audit = inspect_k(k)
    if image_audit.get("status") != "SOURCE_BACKED_IMAGE_AUDIT":
        raise RuntimeError("No live source-backed image audit available")
    source_ids = frozenset(
        step.conclusion.family_id for step in cited_source_steps()
        if isinstance(step.conclusion, CitedStableFamilyDefinition)
    )
    registered = {family.family_id: family for family in read_registered_stable_families()}
    blocker_ids = sorted({
        number for candidate in image_audit["candidate_pairs"]
        if not candidate["proof_engine_replayed"]
        for number in candidate["missing_family_ids"]
    })
    unresolved = [
        {
            "source_index": entry["source_index"],
            "target_index": entry["target_index"],
            "source_generator": entry["source_generator"],
            "target_generator": entry["target_generator"],
            "factor_obligations": entry["factors"],
            "missing_family_ids": entry["missing_family_ids"],
            "proof_engine_replayed": False,
        }
        for entry in image_audit["candidate_pairs"]
        if not entry["proof_engine_replayed"]
    ]
    family_sources: list[dict[str, object]] = []
    for family_id in blocker_ids:
        family = registered.get(family_id)
        if family is None or family_id not in FAMILY_LABELS:
            raise RuntimeError("Unreviewed missing stable-family ID")
        if family_id in source_ids:
            raise RuntimeError("Source definition already cited: re-audit this blocker")
        scan = scan_adopted_toda_sources(root, family_id=family_id)
        family_sources.append({
            **scan,
            "stem": family.stem,
            "minimum_n": family.minimum_n,
            "registered_family_name": family.display,
            "cited_family_definition_available": False,
        })
    return {
        "phase": "173-R4-R15R5",
        "mode": "READ_ONLY_UNRESOLVED_GENERATOR_SOURCE_FRONTIER",
        "n": 4,
        "k": k,
        "target": f"pi_{k + 4}^4",
        "named_image_candidates": len(image_audit["candidate_pairs"]),
        "named_images_replayed": image_audit["proved_named_images"],
        "unresolved_pairs": unresolved,
        "unresolved_family_ids": blocker_ids,
        "family_sources": family_sources,
        "new_proof_steps_created": False,
        "new_given_created": False,
        "public_completion": False,
        "full_pytest_performed": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = inspect_family_source_frontier(args.root)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    print("PHASE173_R4_R15R5_K31_NAMED_REPLAYED=" + str(result["named_images_replayed"]), flush=True)
    print("PHASE173_R4_R15R5_K31_UNRESOLVED_PAIRS=" + str(len(result["unresolved_pairs"])), flush=True)
    print("PHASE173_R4_R15R5_FAMILY_IDS=" + ",".join(map(str, result["unresolved_family_ids"])), flush=True)
    for family in result["family_sources"]:
        print(
            "PHASE173_R4_R15R5_FAMILY_" + str(family["family_id"])
            + "_TEXT_HITS=" + str(len(family["candidate_text_hits"]))
            + " CITED=False",
            flush=True,
        )
    print("PHASE173_R4_R15R5_REPORT=" + str(args.output), flush=True)
    print("PHASE173_R4_R15R5_PUBLIC_COMPLETION=False", flush=True)
    passed = (
        result["named_image_candidates"] == 4
        and result["named_images_replayed"] == 1
        and len(result["unresolved_pairs"]) == 3
        and result["unresolved_family_ids"] == [56, 88]
        and all(not f["source_definition_certified"] for f in result["family_sources"])
        and result["new_given_created"] is False
    )
    print("PHASE173_R4_R15R5_AUDIT=" + ("PASS" if passed else "FAIL"), flush=True)
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
```

## `preflight.py`

```python
"""Pinned HEAD-lineage and content checks for a read-only source frontier audit."""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import subprocess


REVIEWED_BASE_HEAD = "0fc543a0d12e5fac0b2a3d842a2cf9187fd6d49c"
REVIEWED_BLOBS = {
    "phase169_r10eo_r2_definition_index/definition_index.py": "a86c1aee12a5f3bae3e24e148b86c7ae47fe2cd7",
    "phase169_r10eo_r3_reviewed_definition_bridge/reviewed_definitions.py": "d18244617e8fedb87d23c443def0c1c3147a1938",
    "phase169_r10d2_general_family_definition/family_citation.py": "b4b0c65e3eee85b557d5cfe7fa66a38a5386c3f8",
    "phase169_r10b_registered_stable_family_binding/family_registry.py": "4e461795954cc3e7a34fe9e3b47f77d00e5faeda",
    "phase173_r4_r10_general_toda56_core/core.py": "d35600804ecbbc5f8566d52e45a2f6ecf8816347",
    "data/HyoujiGen.csv": "26f33db0c83ba7f151433583fe861598399cbe6a",
    "data/sphere.csv": "b7e98a4469e0dcf2c5ea16691a7225951fd36395",
    "sources/toda/Toda_05_2.tex": "579661138928499ba04a51327f686d9b971b5314",
    "sources/toda/Toda_06_2.tex": "76934583cff01c8ea83f768e26947eb9b556653b",
}
PINNED_PRIOR_SOURCES = {
    "phase173_r4_r15r4_cited_composition_image/audit.py": "73f3d17e9194cd9b263857d415cd158532ca85dd7df376495df5ac7390cddee0",
    "phase173_r4_r15r4_cited_composition_image/replay.py": "c30ba826f4d24e19e7fd89153fd9da35d14f750eaea85e00e4695c827eab86f2",
    "phase173_r4_r15r4_cited_composition_image/bridge.py": "aa45bd3cd5b0bce95ebb0bf13645ec08b0e1620af5bf6130563aa50e56c78b2e",
}
ALLOWED_COMMITTED_PREFIX = "phase173_r4_r15r4_cited_composition_image/"
ALLOWED_PYTEST_CACHE = ".pytest_cache/v/cache/nodeids"


def git(root: Path, *args: str) -> str:
    """Get one local Git value; propagate command failures explicitly."""
    result = subprocess.run(
        ("git", *args), cwd=root, capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=False,
    )
    if result.returncode:
        raise RuntimeError("git " + " ".join(args) + ": " + result.stderr[:550])
    return result.stdout.strip()


def is_allowed_committed(path: str) -> bool:
    """Only the separately verified prior read-only package may be committed."""
    return path == ALLOWED_PYTEST_CACHE or path.startswith(ALLOWED_COMMITTED_PREFIX)


def normalized_sha256(path: Path) -> str:
    """Allow CRLF/LF package extraction without relaxing source identity."""
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def verify_source_head(root: Path) -> None:
    """Fail closed on non-reviewed production edits, source drift or Git divergence."""
    root = root.resolve()
    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root:
        raise RuntimeError("Not the EHP Proof Tracer repository root")
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("Expected develop branch")
    head = git(root, "rev-parse", "HEAD")
    remote = git(root, "rev-parse", "origin/develop")
    if head != remote:
        raise RuntimeError("Local HEAD and origin/develop diverged")
    ancestor = subprocess.run(
        ("git", "merge-base", "--is-ancestor", REVIEWED_BASE_HEAD, head),
        cwd=root, capture_output=True, check=False,
    )
    if ancestor.returncode:
        raise RuntimeError("Unreviewed HEAD lineage")
    committed = tuple(filter(None, git(
        root, "diff", "--name-only", REVIEWED_BASE_HEAD, head,
    ).splitlines()))
    if any(not is_allowed_committed(path) for path in committed):
        raise RuntimeError("Unreviewed committed source: " + repr(committed))
    if git(root, "diff", "--cached", "--name-only"):
        raise RuntimeError("Staged changes require review")
    dirty = tuple(filter(None, git(root, "diff", "--name-only").splitlines()))
    if any(path != ALLOWED_PYTEST_CACHE for path in dirty):
        raise RuntimeError("Unreviewed tracked worktree changes: " + repr(dirty))
    for relative, blob in REVIEWED_BLOBS.items():
        if git(root, "rev-parse", "HEAD:" + relative) != blob:
            raise RuntimeError("Unreviewed commit blob: " + relative)
        if git(root, "hash-object", "--", relative) != blob:
            raise RuntimeError("Unreviewed worktree blob: " + relative)
    for relative, expected in PINNED_PRIOR_SOURCES.items():
        path = root / relative
        if not path.is_file() or normalized_sha256(path) != expected:
            raise RuntimeError("Reviewed prior phase source mismatch: " + relative)
    print("PHASE173_R4_R15R5_HEAD=" + head, flush=True)
    print("PHASE173_R4_R15R5_HEAD_LINEAGE=PASS", flush=True)
    print("PHASE173_R4_R15R5_SOURCE_GUARD=PASS", flush=True)
    print("PHASE173_R4_R15R5_PRODUCTION_EDIT=NONE", flush=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    verify_source_head(args.root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## `run.ps1`

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    git fetch origin develop
    if ($LASTEXITCODE -ne 0) { throw 'R15R5 Git fetch failed' }

    python -m phase173_r4_r15r5_family_source_frontier.preflight --root "$Root"
    if ($LASTEXITCODE -ne 0) { throw 'R15R5 source preflight failed' }

    python -m pytest -q `
        phase173_r4_r15r5_family_source_frontier/tests/test_static.py `
        phase173_r4_r15r5_family_source_frontier/tests/test_scan.py
    if ($LASTEXITCODE -ne 0) { throw 'R15R5 standalone tests failed' }

    if ($DryRun) {
        Write-Output 'PHASE173_R4_R15R5_DRY_RUN=PASS'
        Write-Output 'PHASE173_R4_R15R5_PRODUCTION_EDIT=NONE'
        exit 0
    }

    python -m pytest -q `
        phase173_r4_r15r5_family_source_frontier/tests/test_integration.py `
        phase173_r4_r15r4_cited_composition_image/tests/test_integration.py `
        phase173_r4_r15r3_formal_suspension_bridge/tests/test_bridge.py `
        phase173_r4_r15r2_generator_obligation_audit/tests/test_audit.py `
        phase173_r4_r15r1_unbounded_abstract_frontier/tests/test_frontier.py `
        phase173_r4_r10_general_toda56_core/tests/test_core.py
    if ($LASTEXITCODE -ne 0) { throw 'R15R5 focused pytest failed' }
    Write-Output 'PHASE173_R4_R15R5_FOCUSED_PYTEST=PASS'

    python -m phase173_r4_r15r5_family_source_frontier.audit `
        --root "$Root" `
        --output (Join-Path $PSScriptRoot 'family_source_frontier_report.json')
    if ($LASTEXITCODE -ne 0) { throw 'R15R5 source frontier audit failed' }
    Write-Output 'PHASE173_R4_R15R5_PHASE_COMPLETED=False'
} finally {
    Pop-Location
}
```

## `tests/test_static.py`

```python
"""Static source, safety and HEAD lineage constraints for R15R5."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase173_r4_r15r5_family_source_frontier.preflight import (
    ALLOWED_PYTEST_CACHE,
    is_allowed_committed,
    normalized_sha256,
)


ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("filename", ("source_scan.py", "audit.py", "preflight.py"))
def test_new_code_parses_without_elision(filename: str) -> None:
    text = (ROOT / filename).read_text(encoding="utf-8")
    tree = ast.parse(text)
    assert not any(isinstance(node, ast.Expr)
                   and isinstance(node.value, ast.Constant)
                   and node.value.value is Ellipsis
                   for node in ast.walk(tree))
    assert "eval(" not in text
    assert "exec(" not in text


def test_prior_math_code_is_not_modified_by_runner() -> None:
    runner = (ROOT / "run.ps1").read_text(encoding="utf-8")
    assert "phase173_r4_r15r5_family_source_frontier.audit" in runner
    assert "PHASE173_R4_R15R5_FOCUSED_PYTEST=PASS" in runner
    assert "--DryRun" not in runner
    assert "git reset" not in runner
    assert "git checkout" not in runner


def test_public_proof_not_promoted() -> None:
    text = (ROOT / "audit.py").read_text(encoding="utf-8")
    assert '"public_completion": False' in text
    assert '"new_given_created": False' in text
    assert '"new_proof_steps_created": False' in text


def test_only_expected_prior_commit_paths_allowed() -> None:
    assert is_allowed_committed(ALLOWED_PYTEST_CACHE)
    assert is_allowed_committed("phase173_r4_r15r4_cited_composition_image/audit.py")
    assert not is_allowed_committed("phase173_r4_r10_general_toda56_core/core.py")
    assert not is_allowed_committed("sources/toda/Toda_06_2.tex")
    assert not is_allowed_committed("phase173_r4_r15r5_family_source_frontier/audit.py")


def test_line_ending_hash_normalization(tmp_path: Path) -> None:
    source = tmp_path / "source.py"
    source.write_bytes(b"x=1\ny=2\n")
    first = normalized_sha256(source)
    source.write_bytes(b"x=1\r\ny=2\r\n")
    assert normalized_sha256(source) == first
    source.write_bytes(b"x=1\r\ny=3\r\n")
    assert normalized_sha256(source) != first
```

## `tests/test_scan.py`

```python
"""Standalone TeX evidence scanner tests: text hits never become proof leaves."""
from __future__ import annotations

from pathlib import Path

import pytest

from phase173_r4_r15r5_family_source_frontier.source_scan import (
    scan_adopted_toda_sources,
    scan_text,
)


def test_delta_definition_is_only_an_unreviewed_text_hit() -> None:
    hits = scan_text(r"\delta_n:=E^{n-3}\delta_3", family_id=88,
                     relative_path="example.tex")
    assert len(hits) == 1
    assert hits[0]["kind"] == "indexed_definition"
    assert hits[0]["source_reviewed"] is False


def test_bar_kappa_definition_is_only_an_unreviewed_text_hit() -> None:
    hits = scan_text(r"\bar{\kappa}_n:=E^{n-7}\bar{\kappa}_7", family_id=56,
                     relative_path="example.tex")
    assert len(hits) == 1
    assert hits[0]["source_reviewed"] is False


def test_database_metadata_text_never_matches_definition() -> None:
    for family_id, text in ((56, r"\bar{\kappa}_{14}"),
                            (88, r"\Delta_3\sigma_{27}")):
        assert scan_text(text, family_id=family_id,
                         relative_path="example.tex") == ()


def test_unexpected_family_refused() -> None:
    with pytest.raises(ValueError, match="Unreviewed family ID"):
        scan_text(r"\delta_n:=E\delta_3", family_id=999,
                  relative_path="example.tex")


def test_scan_existing_local_chapter_returns_provenance_not_proof(tmp_path: Path) -> None:
    directory = tmp_path / "sources" / "toda"
    directory.mkdir(parents=True)
    (directory / "Toda_99_2.tex").write_text(
        r"\delta_n:=E^{n-3}\delta_3" + "\n", encoding="utf-8",
    )
    result = scan_adopted_toda_sources(tmp_path, family_id=88)
    assert result["family_id"] == 88
    assert len(result["candidate_text_hits"]) == 1
    assert result["source_definition_certified"] is False
    assert result["new_given_created"] is False
    assert len(result["source_files"][0]["sha256"]) == 64
```

## `tests/test_integration.py`

```python
"""Focused live-repository checks against the R15R4 actually replayed frontier."""
from __future__ import annotations

from pathlib import Path

from phase173_r4_r15r5_family_source_frontier.audit import (
    inspect_family_source_frontier,
)


ROOT = Path(__file__).resolve().parents[2]


def test_k31_source_frontier_preserves_three_unproved_pairs() -> None:
    row = inspect_family_source_frontier(ROOT, k=31)
    assert row["named_image_candidates"] == 4
    assert row["named_images_replayed"] == 1
    assert len(row["unresolved_pairs"]) == 3
    assert row["unresolved_family_ids"] == [56, 88]
    assert all(not pair["proof_engine_replayed"] for pair in row["unresolved_pairs"])
    assert row["new_given_created"] is False
    assert row["public_completion"] is False


def test_family_56_and_88_metadata_are_not_promoted_to_citations() -> None:
    row = inspect_family_source_frontier(ROOT, k=31)
    assert {entry["family_id"] for entry in row["family_sources"]} == {56, 88}
    for entry in row["family_sources"]:
        assert entry["minimum_n"] >= 2
        assert entry["stem"] >= 0
        assert entry["cited_family_definition_available"] is False
        assert entry["source_definition_certified"] is False
        assert entry["new_given_created"] is False
        assert entry["source_files"]
        assert all(hit["source_reviewed"] is False
                   for hit in entry["candidate_text_hits"])
```


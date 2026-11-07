# R21 新設コード全文

対象既存ファイル・クラス・関数の変更はありません。追加位置はリポジトリ直下の `phase174_r3_r7_r21_delta_hopf_chain_audit/` です。

## `__init__.py`

```python
"""R21 read-only mathematical dependency audit."""

```

## `audit.py`

```python
"""R21: independent Hopf/Delta proof obligations, not a proof constructor."""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEWED_HEAD = "654d46f6f225fc6b641a1760ce0e3f08598419c3"
PARENT_HEAD = "3ba55c65566bdf391d425bae04038b8b521240a4"
SOURCE = "sources/toda/Toda_05_2.tex"
START = r"\begin{proposition}\label{prop:5.9}"
END = r"\begin{lemma}\label{lemma:5.10}"
MARKERS = {
    "suspension_zero": r"E\pi_{10}^5=0",
    "hopf_short_exact": r"0\to \pi^{6}_{11}\xrightarrow{H}\pi^{11}_{11}\xrightarrow{\ \Delta\ }\pi^{5}_{9}",
    "delta_onto_lower": r"\(\Delta\) は全射で, \(\ker\Delta=\gen{2\iota_{11}}\)",
    "hopf_delta_generator": r"H(\Delta(\iota_{13}))=\pm2\iota_{11}",
    "cyclic_codomain": r"\pi_{11}^6=\mathbb Z \gen{\Delta(\iota_{13})}",
    "delta_iso": r"\pi^{13}_{13}\xrightarrow[\cong]{\Delta}\pi^{6}_{11}",
    "root_zero": r"\pi_{12}^7=0",
}
PROP27 = r"\textbf{Prop2.7.}"
PROP27_HOPF = r"H\Delta(\iota_{2n+1}) = \pm2\iota_{2m-1}"
DIAGONAL = r"\pis{n}{S^n} = \z\gen{\iota_n}"


def git(*args: str, root: Path = ROOT) -> str:
    return subprocess.run(("git",) + args, cwd=root, capture_output=True,
                          check=True, encoding="utf-8", errors="replace", text=True).stdout.strip()


def verify_checkout(root: Path = ROOT) -> dict[str, str]:
    if Path(git("rev-parse", "--show-toplevel", root=root)).resolve() != root.resolve():
        raise RuntimeError("R21 folder must be extracted under repository root")
    if git("branch", "--show-current", root=root) != "develop":
        raise RuntimeError("R21 requires develop branch")
    local = git("rev-parse", "HEAD", root=root)
    remote_line = git("ls-remote", "origin", "refs/heads/develop", root=root)
    remote = remote_line.split()[0] if remote_line else ""
    if local != REVIEWED_HEAD or remote != REVIEWED_HEAD:
        raise RuntimeError("Unreviewed Git HEAD; no checkout/reset performed")
    if git("rev-parse", "HEAD^", root=root) != PARENT_HEAD:
        raise RuntimeError("Unexpected R19 commit parent")
    if git("diff", "--name-only", root=root) or git("diff", "--cached", "--name-only", root=root):
        raise RuntimeError("Tracked changes must be reviewed separately")
    for rel in (SOURCE, "phase174_r3_r7_r19_delta_generator_source_audit/audit.py",
                "phase174_r3_r7_r18_delta_image_surjectivity/rule.py",
                "toda_delta_image_rules.py"):
        stored = subprocess.run(("git", "show", REVIEWED_HEAD + ":" + rel),
                                cwd=root, capture_output=True, check=True).stdout
        actual = (root / rel).read_bytes()
        normalized = stored.replace(b"\r\n", b"\n")
        if actual not in (stored, normalized, normalized.replace(b"\n", b"\r\n")):
            raise RuntimeError("Source changed: " + rel)
    return {"local_head": local, "remote_head": remote, "source_guard": "PASS"}


def inspect_source(source: str) -> dict[str, object]:
    if source.count(START) != 1 or source.count(END) != 1:
        raise ValueError("Proposition 5.9 boundaries ambiguous")
    section = source[source.index(START):source.index(END)]
    positions = {}
    for key, token in MARKERS.items():
        if section.count(token) != 1:
            raise ValueError("Source occurrence missing or ambiguous: " + key)
        positions[key] = section.index(token)
    if list(positions.values()) != sorted(positions.values()):
        raise ValueError("Hopf/Delta dependency order changed")
    # Proposition 2.7 must occur before Proposition 5.9, as an independent cited lemma.
    prefix = source[:source.index(START)]
    if PROP27 not in prefix or PROP27_HOPF not in prefix or DIAGONAL not in prefix:
        raise ValueError("Independent Hopf/diagonal source premise missing")
    return {
        "source": "adopted Toda_05_2.tex, Proposition 2.7 and Proposition 5.9 proof",
        "original_print_edition_verified": False,
        "independent_clauses": list(MARKERS.keys()),
        "prop27_hopf_formula_present": True,
        "diagonal_free_cyclic_statement_present": True,
        "hopf_injection_via_exactness_stated": True,
        "hopf_image_2Z_via_kernel_stated": True,
        "hopf_delta_element_primitive_in_2Z": True,
        "typed_delta_witness_proof_present": False,
        "isomorphism_arrow_is_direct_given": False,
        "mathematical_dependency_order": [
            "separately prove E pi10^5=0 and lower Delta surjectivity",
            "prove short exact sequence with injective H and image(H)=2Z",
            "use Prop2.7 Hopf(Delta(iota13))=+/-2 iota11",
            "deduce Delta(iota13) generates codomain using injective H",
            "separately certify pi13^13=Z{iota13} and typed Delta application",
            "infer image(Delta)=codomain and then surjectivity",
            "apply EHP exactness with terminal pi12^13=0 for root",
        ],
    }


def inspect_public_frontier() -> dict[str, object]:
    from phase174_r3_r7_r19_delta_generator_source_audit.audit import inspect_live_frontier
    live = inspect_live_frontier()
    required = {
        "delta_public_candidates": 0,
        "delta_image_public_candidates": 0,
        "signed_delta_witnesses": 0,
        "generator_is_typed_map_application": False,
        "verified_steps": 0,
        "search_status": "search_failed",
        "completion_claimed": False,
    }
    for key, val in required.items():
        if live.get(key) != val:
            raise RuntimeError("Public frontier changed; reassess: " + key)
    return {key: live[key] for key in required}


def report(dry_run: bool) -> dict[str, object]:
    checkout = verify_checkout()
    source = inspect_source((ROOT / SOURCE).read_text(encoding="utf-8-sig"))
    public = None if dry_run else inspect_public_frontier()
    return {
        "phase": "174-R3-R7-R21", "checkout": checkout,
        "source": source, "public_frontier": public,
        "new_given": 0, "new_math_rules": 0, "production_changes": False,
        "full_pytest": False, "root_complete": False,
        "gate": "PASS_R21_SOURCE_PREFLIGHT_ONLY" if dry_run else
                "PASS_R21_HOPF_CHAIN_SOURCE_CONFIRMED_TYPED_DELTA_PENDING",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    value = report(args.dry_run)
    directory = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir())) / "EHPProofTracerAudit" / "phase174_r3_r7_r21"
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / ("hopf_preflight.json" if args.dry_run else "hopf_source_audit.json")
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    prefix = "PHASE174_R3R7R21_"
    print(prefix + "SOURCE_GUARD=PASS")
    print(prefix + "HOPF_CHAIN_CLAUSES=7")
    print(prefix + "TYPED_DELTA_WITNESS=False")
    if value["public_frontier"] is not None:
        print(prefix + "PUBLIC_SIGNED_WITNESSES=0")
        print(prefix + "PUBLIC_VERIFIED_STEPS=0")
    print(prefix + "NEW_GIVEN=0")
    print(prefix + "NEW_RULES=0")
    print(prefix + "FULL_PYTEST=False")
    print(prefix + "ROOT_COMPLETE=False")
    print(prefix + "REPORT=" + str(path))
    print(prefix + "GATE=" + str(value["gate"]))
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

```

## `tests/__init__.py`

```python
"""Tests for the R21 read-only audit."""

```

## `tests/test_audit.py`

```python
"""Source-first R21 dependency guards; no production imports needed."""
from __future__ import annotations

import pytest

from phase174_r3_r7_r21_delta_hopf_chain_audit.audit import (
    DIAGONAL,
    END,
    MARKERS,
    PROP27,
    PROP27_HOPF,
    START,
    inspect_source,
)


def sample_source() -> str:
    prefix = PROP27 + "\n" + PROP27_HOPF + "\n" + DIAGONAL + "\n"
    body = START + "\n" + "\n".join(MARKERS.values()) + "\n" + END
    return prefix + body


def test_independent_hopf_chain_source() -> None:
    result = inspect_source(sample_source())
    assert result["hopf_injection_via_exactness_stated"] is True
    assert result["hopf_image_2Z_via_kernel_stated"] is True
    assert result["typed_delta_witness_proof_present"] is False
    assert result["isomorphism_arrow_is_direct_given"] is False
    assert len(result["mathematical_dependency_order"]) == 7


@pytest.mark.parametrize("marker", tuple(MARKERS.values()))
def test_missing_proof_clause_rejected(marker: str) -> None:
    with pytest.raises(ValueError, match="missing or ambiguous"):
        inspect_source(sample_source().replace(marker, "REMOVED"))


def test_wrong_evidence_order_rejected() -> None:
    source = sample_source()
    a, b = MARKERS["hopf_delta_generator"], MARKERS["cyclic_codomain"]
    with pytest.raises(ValueError, match="order"):
        inspect_source(source.replace(a, "TEMP").replace(b, a).replace("TEMP", b))


@pytest.mark.parametrize("marker", (PROP27, PROP27_HOPF, DIAGONAL))
def test_missing_independent_source_rejected(marker: str) -> None:
    with pytest.raises(ValueError, match="Independent"):
        inspect_source(sample_source().replace(marker, "REMOVED"))


def test_duplicate_clause_rejected() -> None:
    with pytest.raises(ValueError, match="ambiguous"):
        inspect_source(sample_source().replace(MARKERS["root_zero"], MARKERS["root_zero"] * 2))

```

## `tests/test_public.py`

```python
"""Regression: R21 must not convert R20 source evidence into a proof leaf."""
from __future__ import annotations

from phase174_r3_r7_r21_delta_hopf_chain_audit.audit import inspect_public_frontier


def test_public_frontier_stays_unfinished() -> None:
    result = inspect_public_frontier()
    assert result["delta_public_candidates"] == 0
    assert result["delta_image_public_candidates"] == 0
    assert result["signed_delta_witnesses"] == 0
    assert result["generator_is_typed_map_application"] is False
    assert result["verified_steps"] == 0
    assert result["search_status"] == "search_failed"
    assert result["completion_claimed"] is False

```

## `run.ps1`

```powershell
param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$OldPythonPath = $env:PYTHONPATH
$OldBytecode = $env:PYTHONDONTWRITEBYTECODE

Push-Location -LiteralPath $RepoRoot
try {
    $env:PYTHONPATH = $RepoRoot
    $env:PYTHONDONTWRITEBYTECODE = '1'

    & git fetch origin develop
    if ($LASTEXITCODE -ne 0) { throw 'R21 git fetch failed' }

    & python -B -m phase174_r3_r7_r21_delta_hopf_chain_audit.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R21 source preflight failed' }

    $Groups = @(
        @{ Name = 'R21_SOURCE_CONTRACT'; Path = '.\phase174_r3_r7_r21_delta_hopf_chain_audit\tests\test_audit.py' },
        @{ Name = 'R20_SOURCE_CONTRACT'; Path = '.\phase174_r3_r7_r20_delta_image_evidence_audit\tests\test_audit.py' },
        @{ Name = 'R19_SOURCE_CONTRACT'; Path = '.\phase174_r3_r7_r19_delta_generator_source_audit\tests\test_audit.py' },
        @{ Name = 'R18_MATH_RULE'; Path = '.\phase174_r3_r7_r18_delta_image_surjectivity\tests\test_rule.py' }
    )
    foreach ($Group in $Groups) {
        if (-not (Test-Path -LiteralPath $Group.Path)) {
            throw "R21 related test missing: $($Group.Path)"
        }
        Write-Output "PHASE174_R3R7R21_PYTEST_GROUP=$($Group.Name)"
        & python -B -m pytest -q --import-mode=prepend -p no:cacheprovider $Group.Path
        if ($LASTEXITCODE -ne 0) { throw "R21 focused pytest failed: $($Group.Name)" }
    }

    if ($DryRun) {
        Write-Output 'PHASE174_R3R7R21_GATE=PASS_PREFLIGHT_ONLY'
    }
    else {
        Write-Output 'PHASE174_R3R7R21_PYTEST_GROUP=PUBLIC_FRONTIER'
        & python -B -m pytest -q --import-mode=prepend -p no:cacheprovider `
            '.\phase174_r3_r7_r21_delta_hopf_chain_audit\tests\test_public.py'
        if ($LASTEXITCODE -ne 0) { throw 'R21 public regression failed' }
        & python -B -m phase174_r3_r7_r21_delta_hopf_chain_audit.audit
        if ($LASTEXITCODE -ne 0) { throw 'R21 live audit failed' }
    }
    Write-Output '(END)'
}
finally {
    $env:PYTHONPATH = $OldPythonPath
    $env:PYTHONDONTWRITEBYTECODE = $OldBytecode
    Pop-Location
}

```

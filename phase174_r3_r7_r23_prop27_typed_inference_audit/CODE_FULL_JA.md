# Phase 174 R3-R7-R23：追加コード全文

既存コードの変更なし。追加位置はリポジトリ直下の新規ディレクトリ。

## `__init__.py`

```python
"""Read-only R23 source-first audit package."""

```

## `audit.py`

```python
"""R23: read-only source-first audit of Proposition 2.7 typed Delta/Hopf requirements.

No mathematical rule, GIVEN, production provider, or certified ProofStep is created.
"""
from __future__ import annotations

import argparse
import ast
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
PHASE = "174-R3-R7-R23"
REVIEWED_HEAD = "c2f9ff3b9de5f839bc0b0c3f68100ebdec8418e3"
PARENT_HEAD = "789cdc673ddf5bfd4315e42c34920bddb0ce6067"
SOURCE = "sources/toda/Toda_05_2.tex"
CHECKED_PATHS = (
    SOURCE,
    "expression.py",
    "homotopy_groups.py",
    "toda_delta_image_rules.py",
    "phase165_r14_r6_generic_iso.py",
    "phase174_r3_r7_r18_delta_image_surjectivity/rule.py",
    "phase174_r3_r7_r21_delta_hopf_chain_audit/audit.py",
    "phase174_r3_r7_r22_typed_hopf_delta_boundary_audit/audit.py",
    "tests/test_phase50_prop27_theorem_semantics.py",
)
PROP27 = r"H\Delta(\iota_{2n+1}) = \pm2\iota_{2m-1}"
PROP59 = r"\begin{proposition}\label{prop:5.9}"
NEXT_LEMMA = r"\begin{lemma}\label{lemma:5.10}"
HOPF_FORMULA = r"H(\Delta(\iota_{13}))=\pm2\iota_{11}"
EXACT_SEQUENCE = r"0\to \pi^{6}_{11}\xrightarrow{H}\pi^{11}_{11}\xrightarrow{\ \Delta\ }\pi^{5}_{9}"
KERNEL_FORMULA = r"\(\Delta\) は全射で, \(\ker\Delta=\gen{2\iota_{11}}\)"
GENERATOR_FORMULA = r"\pi_{11}^6=\mathbb Z \gen{\Delta(\iota_{13})}"


def git(*args: str, root: Path = ROOT) -> str:
    return subprocess.run(("git",) + args, cwd=root, check=True, capture_output=True,
                          encoding="utf-8", errors="replace", text=True).stdout.strip()


def git_bytes(*args: str, root: Path = ROOT) -> bytes:
    return subprocess.run(("git",) + args, cwd=root, check=True,
                          capture_output=True).stdout


def matches_checkout(actual: bytes, stored: bytes) -> bool:
    normalized = stored.replace(b"\r\n", b"\n")
    return actual in (stored, normalized, normalized.replace(b"\n", b"\r\n"))


def classify_lineage(local: str, remote: str, parent: str, commits: int,
                     changed: tuple[str, ...], tracked: tuple[str, ...]) -> str:
    if local != REVIEWED_HEAD or remote != REVIEWED_HEAD:
        raise RuntimeError("Unreviewed local/remote develop HEAD; no reset or checkout")
    if parent != PARENT_HEAD or commits != 1:
        raise RuntimeError("Unreviewed R22 commit lineage")
    allowed_prefix = "phase174_r3_r7_r22_typed_hopf_delta_boundary_audit/"
    if not changed or any(not p.startswith(allowed_prefix) for p in changed):
        raise RuntimeError("Unexpected R22 merged files")
    if tracked:
        raise RuntimeError("Tracked changes require independent review")
    return "R22_MERGED_CLEAN"


def verify_checkout(root: Path = ROOT) -> dict[str, object]:
    if Path(git("rev-parse", "--show-toplevel", root=root)).resolve() != root.resolve():
        raise RuntimeError("Extract R23 directly under repository root")
    if git("branch", "--show-current", root=root) != "develop":
        raise RuntimeError("R23 requires develop")
    local = git("rev-parse", "HEAD", root=root)
    remote_output = git("ls-remote", "origin", "refs/heads/develop", root=root)
    remote = remote_output.split()[0] if remote_output else ""
    parent = git("rev-parse", REVIEWED_HEAD + "^", root=root)
    commits = len(git("rev-list", PARENT_HEAD + ".." + REVIEWED_HEAD, root=root).splitlines())
    changed = tuple(git("diff", "--name-only", PARENT_HEAD, REVIEWED_HEAD, root=root).splitlines())
    tracked = tuple(sorted(set(git("diff", "--name-only", root=root).splitlines()) |
                           set(git("diff", "--cached", "--name-only", root=root).splitlines())))
    lineage = classify_lineage(local, remote, parent, commits, changed, tracked)
    for path in CHECKED_PATHS:
        stored = git_bytes("show", REVIEWED_HEAD + ":" + path, root=root)
        target = root / path
        if not target.is_file() or not matches_checkout(target.read_bytes(), stored):
            raise RuntimeError("R23 reviewed source mismatch: " + path)
    return {"local_head": local, "remote_head": remote, "lineage": lineage,
            "source_guard": "PASS", "reviewed_file_count": len(CHECKED_PATHS)}


def inspect_prop27_source(content: str) -> dict[str, object]:
    if content.count(PROP59) != 1 or content.count(NEXT_LEMMA) != 1:
        raise ValueError("Prop 5.9 boundaries ambiguous")
    first = content.index(PROP59)
    last = content.index(NEXT_LEMMA)
    if last <= first:
        raise ValueError("Prop 5.9 source boundaries reversed")
    before = content[:first]
    within = content[first:last]
    if PROP27 not in before:
        raise ValueError("Cited general Prop 2.7 formula missing")
    for fragment in (EXACT_SEQUENCE, KERNEL_FORMULA, HOPF_FORMULA, GENERATOR_FORMULA):
        if within.count(fragment) != 1:
            raise ValueError("Prop 5.9 proof dependency missing/ambiguous")
    indices = [within.index(fragment) for fragment in (
        EXACT_SEQUENCE, KERNEL_FORMULA, HOPF_FORMULA, GENERATOR_FORMULA)]
    if indices != sorted(indices):
        raise ValueError("Prop 5.9 dependency order changed")
    return {"general_prop27_formula_present": True,
            "prop59_specific_hopf_formula_present": True,
            "prop59_proof_dependency_count": len(indices),
            "original_print_edition_verified": False,
            "text_is_typed_proof_step": False,
            "formula_specialization_independently_certified": False}


def inspect_static_contract(root: Path = ROOT) -> dict[str, object]:
    """Check that legacy Prop 2.7 test and generator image rules differ."""
    legacy = (root / "tests/test_phase50_prop27_theorem_semantics.py").read_text(encoding="utf-8-sig")
    delta_rules = (root / "toda_delta_image_rules.py").read_text(encoding="utf-8-sig")
    backward = (root / "phase174_r3_r7_r18_delta_image_surjectivity/rule.py").read_text(encoding="utf-8-sig")
    if "TodaProp27HopfInvariantUpToSignStatement" not in legacy or "WhiteheadProduct" not in legacy:
        raise RuntimeError("Legacy Prop 2.7 test semantics changed")
    if "TodaDeltaImageUpToSignStatement" not in delta_rules:
        raise RuntimeError("Signed Delta image premise missing")
    if "TodaDeltaImageFreeCyclicStatement" not in backward:
        raise RuntimeError("Full Delta image obligation missing")
    for path in ("toda_delta_image_rules.py", "phase174_r3_r7_r18_delta_image_surjectivity/rule.py"):
        ast.parse((root / path).read_text(encoding="utf-8-sig"))
    return {"legacy_prop27_whitehead_semantics": True,
            "delta_image_signed_premise_distinct": True,
            "full_delta_image_premise_distinct": True,
            "prop27_specialization_rule_added": False}


def inspect_public_frontier() -> dict[str, object]:
    from phase174_r3_r7_r22_typed_hopf_delta_boundary_audit.audit import (
        inspect_typed_boundary, inspect_public_boundary,
    )
    typed = inspect_typed_boundary()
    live = inspect_public_boundary()
    if typed["db_generator_is_typed_application"] is not False:
        raise RuntimeError("Unexpected database typed Delta application")
    if live["signed_delta_witnesses"] != 0 or live["verified_steps"] != 0:
        raise RuntimeError("Public source frontier changed; audit anew")
    if live["search_status"] != "search_failed" or live["completion_claimed"] is not False:
        raise RuntimeError("Public completion status changed")
    return {"typed_delta_witness": False,
            "signed_delta_witnesses": live["signed_delta_witnesses"],
            "verified_steps": live["verified_steps"],
            "search_status": live["search_status"],
            "root_complete": False}


def report(*, dry_run: bool) -> dict[str, object]:
    state = verify_checkout()
    source = inspect_prop27_source((ROOT / SOURCE).read_text(encoding="utf-8-sig"))
    static = inspect_static_contract()
    live = None if dry_run else inspect_public_frontier()
    return {"phase": PHASE, "git_state": state, "source": source,
            "existing_contracts": static, "public": live,
            "new_given": 0, "new_math_rules": 0, "production_changes": False,
            "full_pytest": False, "root_complete": False,
            "gate": "PASS_R23_PROP27_SOURCE_PREFLIGHT_ONLY" if dry_run else
                    "PASS_R23_PROP27_SEMANTIC_GAP_AUDITED_TYPED_INFERENCE_PENDING"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    result = report(dry_run=args.dry_run)
    folder = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir())) / "EHPProofTracerAudit" / "phase174_r3_r7_r23"
    folder.mkdir(parents=True, exist_ok=True)
    output = folder / ("prop27_preflight.json" if args.dry_run else "prop27_source_audit.json")
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    pre = "PHASE174_R3R7R23_"
    for key in ("local_head", "remote_head", "lineage"):
        print(pre + key.upper() + "=" + str(result["git_state"][key]))
    print(pre + "SOURCE_GUARD=PASS")
    print(pre + "GENERAL_PROP27_SOURCE=True")
    print(pre + "LEGACY_PROP27_IS_WHITEHEAD=True")
    print(pre + "TYPED_DELTA_WITNESS=False")
    if result["public"] is not None:
        print(pre + "PUBLIC_SIGNED_DELTA_WITNESSES=0")
        print(pre + "PUBLIC_VERIFIED_STEPS=0")
    print(pre + "NEW_GIVEN=0")
    print(pre + "NEW_RULES=0")
    print(pre + "FULL_PYTEST=False")
    print(pre + "ROOT_COMPLETE=False")
    print(pre + "REPORT=" + str(output))
    print(pre + "GATE=" + str(result["gate"]))
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

```

## `tests/__init__.py`

```python
"""Focused tests for R23."""

```

## `tests/test_audit.py`

```python
"""R23 source-order, lineage and read-only compatibility contracts."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase174_r3_r7_r23_prop27_typed_inference_audit.audit import (
    EXACT_SEQUENCE, GENERATOR_FORMULA, HOPF_FORMULA, KERNEL_FORMULA,
    NEXT_LEMMA, PARENT_HEAD, PROP27, PROP59, REVIEWED_HEAD,
    classify_lineage, inspect_prop27_source, matches_checkout,
)


def sample_source() -> str:
    return (PROP27 + "\n" + PROP59 + "\n" + "\n".join((
        EXACT_SEQUENCE, KERNEL_FORMULA, HOPF_FORMULA, GENERATOR_FORMULA,
    )) + "\n" + NEXT_LEMMA)


def test_source_clause_order_and_independence() -> None:
    outcome = inspect_prop27_source(sample_source())
    assert outcome["general_prop27_formula_present"] is True
    assert outcome["prop59_proof_dependency_count"] == 4
    assert outcome["text_is_typed_proof_step"] is False
    assert outcome["formula_specialization_independently_certified"] is False


@pytest.mark.parametrize("clause", (PROP27, EXACT_SEQUENCE, KERNEL_FORMULA,
                                   HOPF_FORMULA, GENERATOR_FORMULA))
def test_missing_source_clause_rejected(clause: str) -> None:
    with pytest.raises(ValueError):
        inspect_prop27_source(sample_source().replace(clause, "MISSING"))


def test_reordered_proof_clauses_rejected() -> None:
    s = sample_source().replace(KERNEL_FORMULA, "TEMP").replace(
        HOPF_FORMULA, KERNEL_FORMULA).replace("TEMP", HOPF_FORMULA)
    with pytest.raises(ValueError, match="order"):
        inspect_prop27_source(s)


def test_duplicate_proof_clause_rejected() -> None:
    with pytest.raises(ValueError):
        inspect_prop27_source(sample_source().replace(HOPF_FORMULA, HOPF_FORMULA * 2))


def test_r22_merge_lineage_only() -> None:
    changed = ("phase174_r3_r7_r22_typed_hopf_delta_boundary_audit/audit.py",)
    assert classify_lineage(REVIEWED_HEAD, REVIEWED_HEAD, PARENT_HEAD, 1,
                            changed, ()) == "R22_MERGED_CLEAN"


@pytest.mark.parametrize("local,remote,parent,commits,changed,tracked", (
    ("0" * 40, REVIEWED_HEAD, PARENT_HEAD, 1, ("phase174_r3_r7_r22_typed_hopf_delta_boundary_audit/audit.py",), ()),
    (REVIEWED_HEAD, "0" * 40, PARENT_HEAD, 1, ("phase174_r3_r7_r22_typed_hopf_delta_boundary_audit/audit.py",), ()),
    (REVIEWED_HEAD, REVIEWED_HEAD, "0" * 40, 1, ("phase174_r3_r7_r22_typed_hopf_delta_boundary_audit/audit.py",), ()),
    (REVIEWED_HEAD, REVIEWED_HEAD, PARENT_HEAD, 2, ("phase174_r3_r7_r22_typed_hopf_delta_boundary_audit/audit.py",), ()),
    (REVIEWED_HEAD, REVIEWED_HEAD, PARENT_HEAD, 1, ("proof.py",), ()),
    (REVIEWED_HEAD, REVIEWED_HEAD, PARENT_HEAD, 1, (), ()),
    (REVIEWED_HEAD, REVIEWED_HEAD, PARENT_HEAD, 1, ("phase174_r3_r7_r22_typed_hopf_delta_boundary_audit/audit.py",), ("proof.py",)),
))
def test_unreviewed_lineage_rejected(local: str, remote: str, parent: str,
                                     commits: int, changed: tuple[str, ...],
                                     tracked: tuple[str, ...]) -> None:
    with pytest.raises(RuntimeError):
        classify_lineage(local, remote, parent, commits, changed, tracked)


def test_reviewed_windows_eol_equivalence() -> None:
    stored = b"one\r\ntwo\nthree\r\n"
    assert matches_checkout(stored, stored)
    assert matches_checkout(b"one\ntwo\nthree\n", stored)
    assert matches_checkout(b"one\r\ntwo\r\nthree\r\n", stored)
    assert not matches_checkout(b"one\ntwo\nchanged\n", stored)


def test_no_unreviewed_mathematical_proof_construction() -> None:
    module_path = Path(__file__).resolve().parents[1] / "audit.py"
    code = module_path.read_text(encoding="utf-8")
    functions = {node.name for node in ast.parse(code).body if isinstance(node, ast.FunctionDef)}
    assert not functions.intersection({"install", "apply", "patch", "register_rule", "add_given"})
    assert "git reset" not in code and "git checkout" not in code

```

## `tests/test_public.py`

```python
"""R23 live public frontier must not be upgraded by source text alone."""
from __future__ import annotations

from phase174_r3_r7_r23_prop27_typed_inference_audit.audit import inspect_public_frontier


def test_public_hopf_delta_remains_open() -> None:
    result = inspect_public_frontier()
    assert result["typed_delta_witness"] is False
    assert result["signed_delta_witnesses"] == 0
    assert result["verified_steps"] == 0
    assert result["search_status"] == "search_failed"
    assert result["root_complete"] is False

```

## `run.ps1`

```powershell
param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$OldPythonPath = $env:PYTHONPATH
$OldNoBytecode = $env:PYTHONDONTWRITEBYTECODE

Push-Location -LiteralPath $RepoRoot
try {
    $env:PYTHONPATH = $RepoRoot
    $env:PYTHONDONTWRITEBYTECODE = '1'

    & git fetch origin develop
    if ($LASTEXITCODE -ne 0) { throw 'R23 git fetch failed' }

    & python -B -m phase174_r3_r7_r23_prop27_typed_inference_audit.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R23 source guard failed' }

    $Groups = @(
        @{ Name = 'R23_SOURCE_AND_LINEAGE'; Path = '.\phase174_r3_r7_r23_prop27_typed_inference_audit\tests\test_audit.py' },
        @{ Name = 'EXISTING_PROP27_SEMANTICS'; Path = '.\tests\test_phase50_prop27_theorem_semantics.py' },
        @{ Name = 'R22_SOURCE_BASELINE'; Path = '.\phase174_r3_r7_r22_typed_hopf_delta_boundary_audit\tests\test_audit.py' },
        @{ Name = 'R18_DELTA_IMAGE_RULE'; Path = '.\phase174_r3_r7_r18_delta_image_surjectivity\tests\test_rule.py' }
    )

    foreach ($Group in $Groups) {
        if (-not (Test-Path -LiteralPath $Group.Path)) {
            throw "R23 required test missing: $($Group.Path)"
        }
        Write-Output "PHASE174_R3R7R23_PYTEST_GROUP=$($Group.Name)"
        & python -B -m pytest -q --import-mode=prepend -p no:cacheprovider $Group.Path
        if ($LASTEXITCODE -ne 0) { throw "R23 pytest failed: $($Group.Name)" }
    }

    if ($DryRun) {
        Write-Output 'PHASE174_R3R7R23_GATE=PASS_PREFLIGHT_ONLY'
    }
    else {
        Write-Output 'PHASE174_R3R7R23_PYTEST_GROUP=PUBLIC_SOURCE_FRONTIER'
        & python -B -m pytest -q --import-mode=prepend -p no:cacheprovider `
            '.\phase174_r3_r7_r23_prop27_typed_inference_audit\tests\test_public.py'
        if ($LASTEXITCODE -ne 0) { throw 'R23 public frontier test failed' }
        & python -B -m phase174_r3_r7_r23_prop27_typed_inference_audit.audit
        if ($LASTEXITCODE -ne 0) { throw 'R23 live audit failed' }
    }
    Write-Output '(END)'
}
finally {
    $env:PYTHONPATH = $OldPythonPath
    $env:PYTHONDONTWRITEBYTECODE = $OldNoBytecode
    Pop-Location
}

```

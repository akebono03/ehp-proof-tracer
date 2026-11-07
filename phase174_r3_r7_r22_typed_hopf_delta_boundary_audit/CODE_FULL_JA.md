# R22：変更コード全文

変更は新規監査パッケージのみ。既存の関数・クラス・import は変更しない。

## audit.py

```python
"""Phase 174 R3-R7-R22: source-first, read-only typed Hopf/Delta audit.

This module never creates a new mathematical rule or certified proof step.
An adopted source assertion and a database display name are not proof objects.
"""
from __future__ import annotations

import argparse
from dataclasses import fields, is_dataclass
import json
import os
from pathlib import Path
import subprocess
import tempfile
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PHASE = "174-R3-R7-R22"
PARENT_HEAD = "654d46f6f225fc6b641a1760ce0e3f08598419c3"
REVIEWED_HEAD = "789cdc673ddf5bfd4315e42c34920bddb0ce6067"
TRACKED_SOURCES = (
    "sources/toda/Toda_05_2.tex",
    "expression.py",
    "homotopy_groups.py",
    "phase165_r14_r6_generic_iso.py",
    "phase174_r3_r7_r3_ehp_zero_rule/rule.py",
    "phase174_r3_r7_r18_delta_image_surjectivity/rule.py",
    "phase174_r3_r7_r19_delta_generator_source_audit/audit.py",
    "phase174_r3_r7_r20_delta_image_evidence_audit/audit.py",
    "phase174_r3_r7_r21_delta_hopf_chain_audit/audit.py",
    "phase174_r3_r7_r21_delta_hopf_chain_audit/tests/test_public.py",
    "toda_delta_image_rules.py",
)
SOURCE = "sources/toda/Toda_05_2.tex"
START = r"\begin{proposition}\label{prop:5.9}"
END = r"\begin{lemma}\label{lemma:5.10}"
CLAUSES = (
    r"E\pi_{10}^5=0",
    r"0\to \pi^{6}_{11}\xrightarrow{H}\pi^{11}_{11}\xrightarrow{\ \Delta\ }\pi^{5}_{9}",
    r"\(\Delta\) は全射で, \(\ker\Delta=\gen{2\iota_{11}}\)",
    r"H(\Delta(\iota_{13}))=\pm2\iota_{11}",
    r"\pi_{11}^6=\mathbb Z \gen{\Delta(\iota_{13})}",
    r"\pi^{13}_{13}\xrightarrow[\cong]{\Delta}\pi^{6}_{11}",
    r"\pi_{12}^7=0",
)


def git(*args: str, root: Path = ROOT) -> str:
    result = subprocess.run(("git",) + args, cwd=root, check=True,
                            capture_output=True, text=True, encoding="utf-8",
                            errors="replace")
    return result.stdout.strip()


def reviewed_bytes(path: str, *, root: Path = ROOT) -> bytes:
    return subprocess.run(("git", "show", REVIEWED_HEAD + ":" + path),
                          cwd=root, check=True, capture_output=True).stdout


def matches_checkout(actual: bytes, stored: bytes) -> bool:
    normalized = stored.replace(b"\r\n", b"\n")
    return actual in (stored, normalized, normalized.replace(b"\n", b"\r\n"))


def classify_lineage(local: str, remote: str, parent: str,
                     changed_paths: tuple[str, ...], commit_count: int,
                     tracked_changes: tuple[str, ...]) -> str:
    if remote != REVIEWED_HEAD or local not in (PARENT_HEAD, REVIEWED_HEAD):
        raise RuntimeError("Unreviewed local/remote develop HEAD")
    if parent != PARENT_HEAD or commit_count != 1:
        raise RuntimeError("Unreviewed R21 lineage")
    if not changed_paths or any(not path.startswith((
            "phase174_r3_r7_r20_delta_image_evidence_audit/",
            "phase174_r3_r7_r21_delta_hopf_chain_audit/")) for path in changed_paths):
        raise RuntimeError("Unexpected files in R20/R21 merge")
    if tracked_changes:
        raise RuntimeError("Tracked worktree modifications require review")
    if local == REVIEWED_HEAD:
        return "R21_MERGED_CLEAN"
    return "R21_MERGED_REMOTE_PARENT_LOCAL_UNTRACKED_HANDOFF"


def verify_checkout(root: Path = ROOT) -> dict[str, Any]:
    if Path(git("rev-parse", "--show-toplevel", root=root)).resolve() != root.resolve():
        raise RuntimeError("Extract R22 beneath repository root")
    if git("branch", "--show-current", root=root) != "develop":
        raise RuntimeError("R22 requires develop branch")
    local = git("rev-parse", "HEAD", root=root)
    rem = git("ls-remote", "origin", "refs/heads/develop", root=root)
    remote = rem.split()[0] if rem else ""
    parent = git("rev-parse", REVIEWED_HEAD + "^", root=root)
    count = len(git("rev-list", PARENT_HEAD + ".." + REVIEWED_HEAD, root=root).splitlines())
    changed = tuple(git("diff", "--name-only", PARENT_HEAD, REVIEWED_HEAD, root=root).splitlines())
    tracked = tuple(sorted(set(git("diff", "--name-only", root=root).splitlines()) | set(
        git("diff", "--cached", "--name-only", root=root).splitlines())))
    lineage = classify_lineage(local, remote, parent, changed, count, tracked)
    for path in TRACKED_SOURCES:
        file = root / path
        if not file.is_file() or not matches_checkout(file.read_bytes(), reviewed_bytes(path, root=root)):
            raise RuntimeError("R22 reviewed source mismatch: " + path)
    return {"local_head": local, "remote_head": remote, "lineage": lineage,
            "source_guard": "PASS", "reviewed_sources": len(TRACKED_SOURCES)}


def inspect_source(source: str) -> dict[str, Any]:
    if source.count(START) != 1 or source.count(END) != 1:
        raise ValueError("Toda Prop 5.9 boundary ambiguous")
    segment = source[source.index(START):source.index(END)]
    positions = []
    for token in CLAUSES:
        if segment.count(token) != 1:
            raise ValueError("Missing/duplicated Hopf-Delta evidence clause")
        positions.append(segment.index(token))
    if positions != sorted(positions):
        raise ValueError("Hopf-Delta source dependency order changed")
    if r"H\Delta(\iota_{2n+1}) = \pm2\iota_{2m-1}" not in source[:source.index(START)]:
        raise ValueError("Prop 2.7 missing before Prop 5.9")
    return {"adopted_source_clauses": len(CLAUSES),
            "prop27_prior_source_present": True,
            "source_is_verified_proof_step": False,
            "original_print_edition_verified": False}


def inspect_typed_boundary() -> dict[str, Any]:
    """Inspect existing class/goal objects, never create ProofSteps."""
    from dataclasses import fields as dataclass_fields
    from expression import HomotopyElement, MapApplication
    from homotopy_groups import FreeCyclicGroup, TodaDeltaMap, TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
    from phase165_r14_r6_generic_iso import MapSurjective, MapInjective, GeneratorImage
    from phase174_r3_r7_r3_ehp_zero_rule.rule import ehp_zero_inputs
    from phase174_r3_r7_r18_delta_image_surjectivity.rule import delta_surjectivity_image_inputs
    from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
    from proof import Relation, RelationType
    from toda_rules import TodaDeltaImageUpToSignStatement, TodaDeltaImageFreeCyclicStatement

    goal = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    root = ehp_zero_inputs(goal)
    if root is None or len(root) != 4 or not isinstance(root[0], MapSurjective):
        raise RuntimeError("Public EHP root shape changed")
    delta = root[0].map
    if not isinstance(delta, TodaDeltaMap) or delta.source_group != TodaPrimaryGroup(13, 13) or delta.target_group != TodaPrimaryGroup(11, 6):
        raise RuntimeError("Delta map domain/codomain changed")
    prior = exact_prior_database_result(6, 5)
    if (not isinstance(prior, Relation) or prior.relation_type is not RelationType.EQUALITY
            or prior.lhs != delta.target_group or not isinstance(prior.rhs, FreeCyclicGroup)):
        raise RuntimeError("Free cyclic codomain prior changed")
    g = prior.rhs.generator
    req = delta_surjectivity_image_inputs(root[0], prior)
    if (req is None or len(req) != 2 or req[0] != prior
            or not isinstance(req[1], TodaDeltaImageFreeCyclicStatement)):
        raise RuntimeError("R18 two independent obligations changed")
    signed_fields = tuple(f.name for f in dataclass_fields(TodaDeltaImageUpToSignStatement))
    application_fields = tuple(f.name for f in dataclass_fields(MapApplication))
    if not {"map", "element", "positive_value"}.issubset(signed_fields):
        raise RuntimeError("Signed Delta witness structure changed")
    if application_fields != ("map", "expression"):
        raise RuntimeError("MapApplication constructor contract changed")
    if not isinstance(g, HomotopyElement) or isinstance(g, MapApplication):
        raise RuntimeError("DB generator symbolic type changed")
    if not all(is_dataclass(cls) for cls in (MapInjective, MapSurjective, GeneratorImage)):
        raise RuntimeError("Generic map evidence classes changed")
    return {"source_group": [13, 13], "codomain_group": [11, 6],
            "delta_goal_typed": True, "signed_witness_fields": list(signed_fields),
            "map_application_fields": list(application_fields),
            "db_generator_type": type(g).__name__,
            "db_generator_is_typed_application": False,
            "independent_image_premise_required": True,
            "independent_codomain_premise_required": True,
            "inference_rule_registered_here": False,
            "new_proof_steps": 0}


def inspect_public_boundary() -> dict[str, Any]:
    from phase174_r3_r7_r19_delta_generator_source_audit.audit import inspect_live_frontier
    live = inspect_live_frontier()
    expected = {"delta_public_candidates": 0, "delta_image_public_candidates": 0,
                "signed_delta_witnesses": 0,
                "generator_is_typed_map_application": False,
                "verified_steps": 0, "search_status": "search_failed",
                "completion_claimed": False}
    for name, value in expected.items():
        if live.get(name) != value:
            raise RuntimeError("Public proof frontier changed: " + name)
    return {k: live[k] for k in expected}


def report(*, dry_run: bool) -> dict[str, Any]:
    state = verify_checkout()
    source = inspect_source((ROOT / SOURCE).read_text(encoding="utf-8-sig"))
    typed = None if dry_run else inspect_typed_boundary()
    public = None if dry_run else inspect_public_boundary()
    return {"phase": PHASE, "git_state": state, "source": source,
            "typed": typed, "public": public, "new_given": 0,
            "new_rules": 0, "production_changes": False, "full_pytest": False,
            "root_complete": False, "gate": ("PASS_R22_SOURCE_PREFLIGHT_ONLY" if dry_run
                   else "PASS_R22_TYPED_BOUNDARY_AUDITED_DELTA_WITNESS_PENDING")}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    value = report(dry_run=args.dry_run)
    target = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir())) / "EHPProofTracerAudit" / "phase174_r3_r7_r22"
    target.mkdir(parents=True, exist_ok=True)
    output = target / ("typed_boundary_preflight.json" if args.dry_run else "typed_boundary_audit.json")
    output.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    pre = "PHASE174_R3R7R22_"
    state = value["git_state"]
    print(pre + "LOCAL_HEAD=" + state["local_head"])
    print(pre + "REMOTE_HEAD=" + state["remote_head"])
    print(pre + "LINEAGE=" + state["lineage"])
    print(pre + "SOURCE_GUARD=PASS")
    print(pre + "SOURCE_CLAUSES=" + str(value["source"]["adopted_source_clauses"]))
    if value["typed"] is not None:
        print(pre + "DB_GENERATOR_IS_TYPED_MAP_APPLICATION=False")
        print(pre + "PUBLIC_SIGNED_DELTA_WITNESSES=0")
        print(pre + "PUBLIC_VERIFIED_STEPS=0")
    print(pre + "NEW_GIVEN=0")
    print(pre + "NEW_RULES=0")
    print(pre + "FULL_PYTEST=False")
    print(pre + "ROOT_COMPLETE=False")
    print(pre + "REPORT=" + str(output))
    print(pre + "GATE=" + value["gate"])
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## tests/test_audit.py

```python
"""R22 source/lineage and proof-boundary focused contracts."""
from __future__ import annotations

import ast
from pathlib import Path
import pytest

from phase174_r3_r7_r22_typed_hopf_delta_boundary_audit.audit import (
    CLAUSES, END, PARENT_HEAD, REVIEWED_HEAD, START,
    classify_lineage, inspect_source, matches_checkout,
)


def example_source() -> str:
    return (r"H\Delta(\iota_{2n+1}) = \pm2\iota_{2m-1}" + "\n" + START
            + "\n" + "\n".join(CLAUSES) + "\n" + END)


def test_source_chain_remains_seven_independent_text_clauses() -> None:
    result = inspect_source(example_source())
    assert result["adopted_source_clauses"] == 7
    assert result["source_is_verified_proof_step"] is False
    assert result["original_print_edition_verified"] is False


@pytest.mark.parametrize("token", CLAUSES)
def test_missing_clause_fails_closed(token: str) -> None:
    with pytest.raises(ValueError):
        inspect_source(example_source().replace(token, "MISSING"))


def test_reordered_clause_fails_closed() -> None:
    first, second = CLAUSES[2], CLAUSES[3]
    bad = example_source().replace(first, "HOLDER").replace(second, first).replace("HOLDER", second)
    with pytest.raises(ValueError, match="order"):
        inspect_source(bad)


def test_reviewed_clean_and_untracked_handoff_lineage() -> None:
    paths = ("phase174_r3_r7_r20_delta_image_evidence_audit/audit.py",
             "phase174_r3_r7_r21_delta_hopf_chain_audit/audit.py")
    assert classify_lineage(REVIEWED_HEAD, REVIEWED_HEAD, PARENT_HEAD, paths, 1, ()) == "R21_MERGED_CLEAN"
    assert classify_lineage(PARENT_HEAD, REVIEWED_HEAD, PARENT_HEAD, paths, 1, ()) == "R21_MERGED_REMOTE_PARENT_LOCAL_UNTRACKED_HANDOFF"


@pytest.mark.parametrize("local,remote,parent,paths,count,tracked", [
    ("x" * 40, REVIEWED_HEAD, PARENT_HEAD, ("phase174_r3_r7_r20_delta_image_evidence_audit/audit.py",), 1, ()),
    (REVIEWED_HEAD, "x" * 40, PARENT_HEAD, ("phase174_r3_r7_r20_delta_image_evidence_audit/audit.py",), 1, ()),
    (REVIEWED_HEAD, REVIEWED_HEAD, "x" * 40, ("phase174_r3_r7_r20_delta_image_evidence_audit/audit.py",), 1, ()),
    (REVIEWED_HEAD, REVIEWED_HEAD, PARENT_HEAD, ("proof.py",), 1, ()),
    (REVIEWED_HEAD, REVIEWED_HEAD, PARENT_HEAD, (), 1, ()),
    (REVIEWED_HEAD, REVIEWED_HEAD, PARENT_HEAD, ("phase174_r3_r7_r21_delta_hopf_chain_audit/audit.py",), 2, ()),
    (REVIEWED_HEAD, REVIEWED_HEAD, PARENT_HEAD, ("phase174_r3_r7_r21_delta_hopf_chain_audit/audit.py",), 1, ("proof.py",)),
])
def test_unreviewed_lineage_fails(local: str, remote: str, parent: str,
                                  paths: tuple[str, ...], count: int,
                                  tracked: tuple[str, ...]) -> None:
    with pytest.raises(RuntimeError):
        classify_lineage(local, remote, parent, paths, count, tracked)


def test_checkout_whole_file_EOL_variants() -> None:
    stored = b"alpha\r\nbeta\ngamma\r\n"
    assert matches_checkout(stored, stored)
    assert matches_checkout(b"alpha\nbeta\ngamma\n", stored)
    assert matches_checkout(b"alpha\r\nbeta\r\ngamma\r\n", stored)
    assert not matches_checkout(b"alpha\nbeta\nCHANGED\n", stored)


def test_readonly_audit_has_no_proof_registration_or_installer() -> None:
    source = (Path(__file__).resolve().parents[1] / "audit.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    names = {node.name for node in tree.body if isinstance(node, ast.FunctionDef)}
    assert not names.intersection({"install", "patch", "register_rule", "insert_given", "add_proof_step"})
    assert "git reset" not in source
    assert "git checkout" not in source
```

## tests/test_public.py

```python
"""Public frontier is an independently verified status, not an assumed result."""
from __future__ import annotations

from phase174_r3_r7_r22_typed_hopf_delta_boundary_audit.audit import (
    inspect_public_boundary, inspect_typed_boundary,
)


def test_typed_inputs_are_obligations_not_given_proof() -> None:
    result = inspect_typed_boundary()
    assert result["source_group"] == [13, 13]
    assert result["codomain_group"] == [11, 6]
    assert result["db_generator_is_typed_application"] is False
    assert result["independent_image_premise_required"] is True
    assert result["new_proof_steps"] == 0


def test_public_frontier_must_remain_unfinished() -> None:
    live = inspect_public_boundary()
    assert live["signed_delta_witnesses"] == 0
    assert live["verified_steps"] == 0
    assert live["search_status"] == "search_failed"
    assert live["completion_claimed"] is False
```

## run.ps1

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
    if ($LASTEXITCODE -ne 0) { throw 'R22 git fetch failed' }

    & python -B -m phase174_r3_r7_r22_typed_hopf_delta_boundary_audit.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R22 preflight failed' }

    $Groups = @(
        @{ Name = 'R22_SOURCE_AND_LINEAGE'; Path = '.\phase174_r3_r7_r22_typed_hopf_delta_boundary_audit\tests\test_audit.py' },
        @{ Name = 'R21_SOURCE_CONTRACT'; Path = '.\phase174_r3_r7_r21_delta_hopf_chain_audit\tests\test_audit.py' },
        @{ Name = 'R20_SOURCE_CONTRACT'; Path = '.\phase174_r3_r7_r20_delta_image_evidence_audit\tests\test_audit.py' },
        @{ Name = 'R18_MATH_RULE'; Path = '.\phase174_r3_r7_r18_delta_image_surjectivity\tests\test_rule.py' }
    )
    foreach ($Group in $Groups) {
        if (-not (Test-Path -LiteralPath $Group.Path)) {
            throw "Required related test missing: $($Group.Path)"
        }
        Write-Output "PHASE174_R3R7R22_PYTEST_GROUP=$($Group.Name)"
        & python -B -m pytest -q --import-mode=prepend -p no:cacheprovider $Group.Path
        if ($LASTEXITCODE -ne 0) { throw "R22 pytest failed: $($Group.Name)" }
    }
    if ($DryRun) {
        Write-Output 'PHASE174_R3R7R22_GATE=PASS_PREFLIGHT_ONLY'
    }
    else {
        Write-Output 'PHASE174_R3R7R22_PYTEST_GROUP=R22_PUBLIC_TYPED_FRONTIER'
        & python -B -m pytest -q --import-mode=prepend -p no:cacheprovider `
            '.\phase174_r3_r7_r22_typed_hopf_delta_boundary_audit\tests\test_public.py'
        if ($LASTEXITCODE -ne 0) { throw 'R22 public typed frontier pytest failed' }
        & python -B -m phase174_r3_r7_r22_typed_hopf_delta_boundary_audit.audit
        if ($LASTEXITCODE -ne 0) { throw 'R22 full read-only audit failed' }
    }
    Write-Output '(END)'
}
finally {
    $env:PYTHONPATH = $OldPythonPath
    $env:PYTHONDONTWRITEBYTECODE = $OldBytecode
    Pop-Location
}
```

## __init__.py

```python
"""R22 read-only typed Hopf/Delta proof-boundary audit."""
```

## tests/__init__.py

```python
"""Focused R22 audit tests."""
```


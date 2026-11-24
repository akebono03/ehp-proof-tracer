# Phase 176 R3R33R1 — コード全文

変更対象は新規ファイルのみ。既存関数・クラス・import は変更しない。

## `audit.py` — 新規ファイル全体（追加位置: `phase176_r3r33r1_direct_hopf_frontier/audit.py`）

```python
"""Phase 176 R3R33R1: read-only direct Hopf composition frontier."""
from __future__ import annotations

import argparse
import ast
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = "phase176_r3r33r1_direct_hopf_frontier"
FILES = {
    "expression.py": ("class Composition", "class Suspension"),
    "phase171_r2h_prop22_cited_hopf/source.py": ("def _formula_parts(", "def expand_cited_prop22_right_formula("),
    "phase176_r3r30_generic_hopf_substitution_isolated/source.py": ("def generic_hopf_substitution_inputs(",),
    "phase165_r52_r9_shared_math.py": ("def shared_expansion_provider(",),
    "phase169_r3h_source_registry.py": ("def build_adopted_toda53_hopf_reference(",),
    "tests/test_hopf_rules.py": ("def test_hopf_composition_formula(",),
}


def check_sources(root: Path) -> dict[str, bool]:
    checked = {}
    for relative, anchors in FILES.items():
        p = root / relative
        if not p.is_file():
            raise RuntimeError("MISSING_SOURCE: " + relative)
        source = p.read_text(encoding="utf-8-sig")
        ast.parse(source, filename=relative)
        if not all(anchor in source for anchor in anchors):
            raise RuntimeError("SOURCE_ANCHOR_CHANGED: " + relative)
        checked[relative] = True
    shared = (root / "phase165_r52_r9_shared_math.py").read_text(encoding="utf-8-sig")
    if shared.count("options.extend(expand_generic_hopf_substitution(goal, tuple(available)))") != 1:
        raise RuntimeError("R3R31_PUBLIC_CONNECTION_MISSING")
    return checked


def git(root: Path, *args: str) -> str:
    result = subprocess.run(("git", *args), cwd=root, text=True, capture_output=True,
                            encoding="utf-8", errors="replace", check=False)
    if result.returncode:
        raise RuntimeError("GIT_ERROR: " + result.stderr.strip())
    return result.stdout.strip()


def read_only_direct_probe() -> dict:
    from expression import Composition, GeneratorSymbol, HomotopyElement, MapApplication, Suspension
    from map_facts import EHP_H_MAP
    from phase171_r2h_prop22_cited_hopf.source import _formula_parts
    from phase176_r3r30_generic_hopf_substitution_isolated.source import generic_hopf_substitution_inputs
    from phase174_r3_r7_r7_composite_zero_audit.rule import expression_endpoints
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase165_r55_nk_only_goal import registered_group_goal_candidates
    from phase169_r10e2_unpositioned_citation.source_first import screen_independent_sources_for_derived_goal
    from proof import ProofRule, Relation, RelationType

    nu = HomotopyElement("ν′", 3, 6, 3, GeneratorSymbol("ν", decoration="′"))
    e5 = HomotopyElement("η₅", 5, 6, 5, GeneratorSymbol("η", index=5))
    e6 = HomotopyElement("η₆", 6, 7, 6, GeneratorSymbol("η", index=6))
    e7 = HomotopyElement("η₇", 7, 8, 7, GeneratorSymbol("η", index=7))

    # β = η₅∘η₆; Eβ should be η₆∘η₇. The current AST does not
    # normalize these structurally. Do not pretend the two are equal.
    beta = Composition(e5, e6)
    e_beta = Suspension(beta)
    suspension_factors = Composition(Suspension(e5), Suspension(e6))
    concrete_right = Composition(e6, e7)
    outer = Composition(nu, e_beta)
    formula = Relation(MapApplication(EHP_H_MAP, outer),
                       Composition(MapApplication(EHP_H_MAP, nu), e_beta),
                       RelationType.EQUALITY)
    substituted = Relation(MapApplication(EHP_H_MAP, outer),
                           Composition(e5, e_beta), RelationType.EQUALITY)
    desired = Relation(MapApplication(EHP_H_MAP, Composition(nu, concrete_right)),
                       Composition(e5, concrete_right), RelationType.EQUALITY)
    bridge = build_shared_typed_bridge()
    roots = registered_group_goal_candidates(bridge, n=3, k=5)
    if len(roots) != 1:
        raise RuntimeError("EXPECTED_SINGLE_GROUP_GOAL")
    context = screen_independent_sources_for_derived_goal(bridge, goal=roots[0])
    provider = shared_expansion_provider(context, proof_target=roots[0])
    given = tuple(link.step.conclusion for link in context.proof_links
                  if link.step is not None and link.step.rule is ProofRule.GIVEN)
    base = Relation(MapApplication(EHP_H_MAP, nu), e5, RelationType.EQUALITY)
    names = lambda target: [entry.rule.name for entry in provider(target)]
    return {
        "source_screened_base_hopf_present": base in given,
        "beta_endpoints": expression_endpoints(beta),
        "suspension_beta_endpoints": expression_endpoints(e_beta),
        "suspended_factors_endpoints": expression_endpoints(suspension_factors),
        "concrete_right_endpoints": expression_endpoints(concrete_right),
        "formula_typed_recognized": _formula_parts(formula) is not None,
        "substituted_typed_recognized": generic_hopf_substitution_inputs(substituted) is not None,
        "formula_candidates": names(formula),
        "substituted_candidates": names(substituted),
        "desired_candidates": names(desired),
        "suspension_composite_structurally_equal_to_factors": e_beta == suspension_factors,
        "suspension_composite_structurally_equal_to_eta6_eta7": e_beta == concrete_right,
        "requires_verified_suspension_functoriality": True,
        "requires_verified_eta_generator_suspensions": True,
        "requires_verified_equality_transport": True,
        "requires_intermediate_hopf_nu_eta6": False,
        "proof_completed": False,
        "root_group_proved": False,
        "new_given": 0,
        "full_pytest": "NOT_RUN",
    }


def output_path() -> Path:
    directory = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir()) / "EHPProofTracerAudit" / PACKAGE
    directory.mkdir(parents=True, exist_ok=True)
    return directory / "report.json"


def run(root: Path, dry_run: bool) -> int:
    report: dict = {"phase": "176_R3R33R1", "mode": "READ_ONLY", "full_pytest": "NOT_RUN"}
    try:
        root = root.resolve()
        if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root:
            raise RuntimeError("WRONG_REPOSITORY")
        if git(root, "branch", "--show-current") != "develop":
            raise RuntimeError("DEVELOP_REQUIRED")
        report["head"] = git(root, "rev-parse", "HEAD")
        report["source_checks"] = check_sources(root)
        if not dry_run:
            sys.path.insert(0, str(root))
            report["direct_frontier"] = read_only_direct_probe()
        report["gate"] = "PASS_R3R33R1_DRYRUN" if dry_run else "PASS_R3R33R1_DIRECT_FRONTIER_AUDITED_NOT_PROVED"
    except Exception as error:
        report["gate"] = "FAIL_R3R33R1"
        report["error"] = type(error).__name__ + ": " + str(error)
    path = output_path()
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8")
    print("PHASE176_R3R33R1_GATE=" + report["gate"])
    if "direct_frontier" in report:
        for field, value in report["direct_frontier"].items():
            print("PHASE176_R3R33R1_" + field.upper() + "=" + str(value))
    if "error" in report:
        print("PHASE176_R3R33R1_ERROR=" + report["error"])
    print("REPORT=" + str(path))
    print("(END)")
    return 0 if report["gate"].startswith("PASS_") else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    return run(args.root, args.dry_run)


if __name__ == "__main__":
    sys.exit(main())

```

## `tests/test_audit.py` — 新規ファイル全体（追加位置: `phase176_r3r33r1_direct_hopf_frontier/tests/test_audit.py`）

```python
"""Focused fail-closed tests for the R3R33R1 read-only audit."""
from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

FILE = Path(__file__).resolve().parents[1] / "audit.py"
SPEC = importlib.util.spec_from_file_location("phase176_r3r33r1_audit", FILE)
assert SPEC is not None and SPEC.loader is not None
AUDIT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(AUDIT)


def test_check_sources_rejects_missing_files(tmp_path: Path) -> None:
    with pytest.raises(RuntimeError, match="MISSING_SOURCE"):
        AUDIT.check_sources(tmp_path)


def test_check_sources_rejects_missing_anchor(tmp_path: Path) -> None:
    for name in AUDIT.FILES:
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("pass\n", encoding="utf-8")
    with pytest.raises(RuntimeError, match="SOURCE_ANCHOR_CHANGED"):
        AUDIT.check_sources(tmp_path)


def test_check_sources_requires_r3r31_binding(tmp_path: Path) -> None:
    for name, anchors in AUDIT.FILES.items():
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join("# " + anchor for anchor in anchors) + "\n", encoding="utf-8")
    with pytest.raises(RuntimeError, match="R3R31_PUBLIC_CONNECTION_MISSING"):
        AUDIT.check_sources(tmp_path)


def test_package_does_not_mutate_repository() -> None:
    text = FILE.read_text(encoding="utf-8")
    assert "write_bytes(" not in text
    assert "git reset" not in text
    assert "git checkout" not in text

```

## `run.ps1` — 新規ファイル全体（追加位置: `phase176_r3r33r1_direct_hopf_frontier/run.ps1`）

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    $audit = Join-Path $PSScriptRoot 'audit.py'
    $parameters = @($audit, '--root', $root)
    if ($DryRun) { $parameters += '--dry-run' }
    & python @parameters
    if ($LASTEXITCODE -ne 0) { throw 'R3R33R1 audit failed' }
    if (-not $DryRun) {
        $testFile = Join-Path (Join-Path $PSScriptRoot 'tests') 'test_audit.py'
        & python -m pytest -q -p no:cacheprovider $testFile
        if ($LASTEXITCODE -ne 0) { throw 'R3R33R1 tests failed' }
        & python -m pytest -q -p no:cacheprovider tests/test_hopf_rules.py -k 'hopf_composition_formula or hopf_invariant_reaches_hopf_composition_formula'
        if ($LASTEXITCODE -ne 0) { throw 'Hopf regression tests failed' }
    }
} finally {
    Pop-Location
}

```

# Phase 176 R3R22 コード全文

以下は追加したファイルの全文です。

## `audit.py`

```python
"""Phase 176 R3R22: read-only composite-left Hopf frontier audit.

This tool diagnoses the existing typed implementation; it never supplies a
proof step, edits production files, or registers mathematical assumptions.
"""
from __future__ import annotations

import argparse
import ast
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

PACKAGE = "phase176_r3r22_composite_hopf_frontier"
ROOT = Path(__file__).resolve().parent.parent
SOURCE_FILES = (
    "hopf_rules.py",
    "expression.py",
    "phase171_r2h_prop22_cited_hopf/source.py",
    "phase171_r2i_eta_hopf_bridge/source.py",
    "phase175_r3_pi73_hopf_lift/rule.py",
    "phase176_r3r20_cyclic_candidate_boundary/audit.py",
    "tests/test_hopf_rules.py",
)


def function_source(path: Path, name: str) -> str:
    source = path.read_text(encoding="utf-8-sig")
    tree = ast.parse(source, filename=str(path))
    functions = [node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == name]
    if len(functions) != 1:
        raise RuntimeError("FUNCTION_NOT_UNIQUE: " + str(path) + ":" + name)
    node = functions[0]
    return "\n".join(source.splitlines()[node.lineno - 1:node.end_lineno])


def inspect_source(root: Path) -> dict[str, object]:
    for name in SOURCE_FILES:
        if not (root / name).is_file():
            raise RuntimeError("SOURCE_MISSING: " + name)
    formula = function_source(root / "phase171_r2h_prop22_cited_hopf/source.py", "_formula_parts")
    combined = function_source(root / "phase171_r2h_prop22_cited_hopf/source.py", "_combined_premises")
    composition = (root / "expression.py").read_text(encoding="utf-8-sig")
    generic = function_source(root / "hopf_rules.py", "hopf_composition_formula_inference_rule")
    eta_chain = function_source(root / "phase171_r2i_eta_hopf_bridge/source.py", "_make_chain")
    hopf_lift = function_source(root / "phase175_r3_pi73_hopf_lift/rule.py", "expand_cited_hopf_lift")
    expected = {
        "prop22_requires_element_left": "isinstance(alpha, HomotopyElement)" in formula,
        "substitution_requires_element_left": "isinstance(product.left, HomotopyElement)" in combined,
        "nested_composition_not_accepted_by_is_type_compatible": "self.left," in composition and "HomotopyElement," in composition,
        "generic_rule_requires_suspended_right": "Suspension(" in generic,
        "eta_chain_requires_element_alpha": "isinstance(hopf.lhs.expression, HomotopyElement)" in eta_chain,
        "hopf_lift_uses_eta_chain_candidates": "eligible_eta_hopf_chains(available)" in hopf_lift,
    }
    if not all(expected.values()):
        raise RuntimeError("SOURCE_GUARD_CHANGED: " + repr(expected))
    return expected


def probe() -> dict[str, object]:
    from expression import Composition, GeneratorSymbol, HomotopyElement, MapApplication, Suspension
    from hopf_rules import hopf_composition_formula_inference_rule
    from map_facts import EHP_H_MAP
    from phase171_r2h_prop22_cited_hopf.source import _formula_parts, expand_cited_prop22_right_formula, TodaProp22RightFormula
    from proof import Relation, RelationType

    nu_prime = HomotopyElement("ν′", 3, source=6, target=3, generator=GeneratorSymbol("ν", 3, "prime"))
    eta6 = HomotopyElement("η₆", 6, source=7, target=6, generator=GeneratorSymbol("η", 6))
    eta5 = HomotopyElement("η₅", 5, source=6, target=5, generator=GeneratorSymbol("η", 5))
    alpha = Composition(nu_prime, eta6)
    right = Suspension(eta6)
    expected_formula = Relation(
        lhs=MapApplication(EHP_H_MAP, Composition(alpha, right)),
        rhs=Composition(MapApplication(EHP_H_MAP, alpha), right),
        relation_type=RelationType.EQUALITY,
    )
    generalized = hopf_composition_formula_inference_rule()
    direct = expand_cited_prop22_right_formula(expected_formula, (TodaProp22RightFormula(),))
    result = {
        "left_factor_is_composition": isinstance(alpha, Composition),
        "left_factor_mathematically_composable": nu_prime.source == eta6.target and eta6.source == right.target,
        "nested_composition_type_compatible": Composition(alpha, right).is_type_compatible(),
        "cited_prop22_shape_recognized": _formula_parts(expected_formula) is not None,
        "cited_prop22_expansions": len(direct),
        "generic_hopf_rule_name": generalized.name,
        "candidate_is_proof": False,
        "new_given": 0,
        "new_math_rules": 0,
        "root_proof_complete_claimed": False,
    }
    if not result["left_factor_is_composition"] or not result["left_factor_mathematically_composable"]:
        raise RuntimeError("TYPED_SAMPLE_INVALID")
    return result


def checked_git_root(root: Path) -> str:
    base = subprocess.run(("git", "rev-parse", "--show-toplevel"), cwd=root, capture_output=True, text=True, check=True)
    if Path(base.stdout.strip()).resolve() != root.resolve():
        raise RuntimeError("WRONG_REPOSITORY")
    branch = subprocess.run(("git", "branch", "--show-current"), cwd=root, capture_output=True, text=True, check=True)
    if branch.stdout.strip() != "develop":
        raise RuntimeError("DEVELOP_REQUIRED")
    head = subprocess.run(("git", "rev-parse", "HEAD"), cwd=root, capture_output=True, text=True, check=True)
    return head.stdout.strip()


def report_file() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir()) / "EHPProofTracerAudit" / PACKAGE
    base.mkdir(parents=True, exist_ok=True)
    return base / "report.json"


def execute(dry_run: bool) -> int:
    report: dict[str, object] = {
        "phase": "176_R3R22", "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "dry_run": dry_run, "gate": "FAIL_R3R22", "full_pytest": "NOT_RUN",
        "new_given": 0, "new_math_rules": 0,
    }
    try:
        report["head"] = checked_git_root(ROOT)
        report["source_guard"] = inspect_source(ROOT)
        if not dry_run:
            report["observed"] = probe()
            report["gate"] = "PASS_R3R22_COMPOSITE_LEFT_BOUNDARY_RECORDED"
        else:
            report["gate"] = "PASS_R3R22_DRYRUN"
    except Exception as exc:
        report["error"] = type(exc).__name__ + ": " + str(exc)
    path = report_file()
    path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("PHASE176_R3R22_GATE=" + str(report["gate"]))
    print("PHASE176_R3R22_HEAD=" + str(report.get("head", "UNVERIFIED")))
    for k, v in report.get("observed", {}).items():
        print("PHASE176_R3R22_" + k.upper() + "=" + str(v))
    if "error" in report:
        print("PHASE176_R3R22_ERROR=" + str(report["error"]))
    print("PHASE176_R3R22_REPORT=" + str(path))
    print("PHASE176_R3R22_FULL_PYTEST=NOT_RUN")
    print("(END)")
    return 0 if str(report["gate"]).startswith("PASS_") else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    return execute(parser.parse_args().dry_run)


if __name__ == "__main__":
    sys.exit(main())

```

## `__init__.py`

```python
"""Read-only Phase 176 R3R22 audit package."""

```

## `tests/test_audit.py`

```python
"""Focused tests for read-only composite-left Hopf audit."""
from __future__ import annotations

import json
from pathlib import Path

import pytest
from phase176_r3r22_composite_hopf_frontier import audit


def test_source_guard_requires_all_sources(tmp_path: Path) -> None:
    with pytest.raises(RuntimeError, match="SOURCE_MISSING"):
        audit.inspect_source(tmp_path)


def test_dry_run_never_probes(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(audit, "ROOT", tmp_path)
    monkeypatch.setattr(audit, "checked_git_root", lambda root: "test-head")
    monkeypatch.setattr(audit, "inspect_source", lambda root: {"ok": True})
    monkeypatch.setattr(audit, "probe", lambda: pytest.fail("probe called on dry run"))
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    assert audit.execute(True) == 0
    report = json.loads((tmp_path / "EHPProofTracerAudit" / audit.PACKAGE / "report.json").read_text(encoding="utf-8"))
    assert report["gate"] == "PASS_R3R22_DRYRUN"
    assert "observed" not in report


def test_probe_failure_fails_closed(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(audit, "checked_git_root", lambda root: "test-head")
    monkeypatch.setattr(audit, "inspect_source", lambda root: {"ok": True})
    monkeypatch.setattr(audit, "probe", lambda: (_ for _ in ()).throw(RuntimeError("probe_failed")))
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    assert audit.execute(False) == 1
    report = json.loads((tmp_path / "EHPProofTracerAudit" / audit.PACKAGE / "report.json").read_text(encoding="utf-8"))
    assert report["gate"] == "FAIL_R3R22"
    assert "probe_failed" in report["error"]


def test_actual_composite_left_boundary() -> None:
    observed = audit.probe()
    assert observed["left_factor_is_composition"]
    assert observed["left_factor_mathematically_composable"]
    assert observed["candidate_is_proof"] is False
    assert observed["new_given"] == 0
    assert observed["new_math_rules"] == 0

```

## `run.ps1`

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Push-Location $root
try {
    if ($DryRun) {
        & python -B -m phase176_r3r22_composite_hopf_frontier.audit --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'R3R22 DryRun failed' }
    } else {
        & python -B -m phase176_r3r22_composite_hopf_frontier.audit
        if ($LASTEXITCODE -ne 0) { throw 'R3R22 audit failed' }
        & python -B -m pytest -q -p no:cacheprovider `
            .\phase176_r3r22_composite_hopf_frontier\tests `
            .\tests\test_hopf_rules.py
        if ($LASTEXITCODE -ne 0) { throw 'R3R22 focused pytest failed' }
    }
} finally {
    Pop-Location
}

```


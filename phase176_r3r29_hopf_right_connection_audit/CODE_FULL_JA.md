# Phase 176 R3R29 — 新規コード全文

## audit.py

```python
"""Phase 176 R3R29: read-only public Hopf right-composition frontier audit."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = "phase176_r3r29_hopf_right_connection_audit"
ANCHORS = {
    "phase171_r2h_prop22_cited_hopf/source.py": ("def _formula_parts(", "def _combined_premises("),
    "phase165_r52_r9_shared_math.py": ("build_cited_toda55_quadruple_source", "expand_public_toda55_quadruple"),
    "phase176_r3r27r1_toda55_quadruple_isolated/source.py": ("def canonical_quadruple_goal(",),
    "phase171_r2e_toda53_double_reference.py": ("def build_adopted_toda53_double_reference(",),
    "phase171_r2i_eta_hopf_bridge/source.py": ("def expand_cited_eta_hopf_power(",),
}


def source_guard(root: Path) -> dict[str, bool]:
    checks = {}
    for relative, patterns in ANCHORS.items():
        path = root / relative
        if not path.is_file():
            raise RuntimeError("MISSING_SOURCE: " + relative)
        text = path.read_text(encoding="utf-8-sig")
        if not all(pattern in text for pattern in patterns):
            raise RuntimeError("SOURCE_SIGNATURE_CHANGED: " + relative)
        checks[relative] = True
    return checks


def git(root: Path, *args: str) -> str:
    completed = subprocess.run(("git", *args), cwd=root, capture_output=True,
                               text=True, encoding="utf-8", errors="replace")
    if completed.returncode:
        raise RuntimeError("GIT_FAILED: " + completed.stderr.strip())
    return completed.stdout.strip()


def preflight(root: Path) -> str:
    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root.resolve():
        raise RuntimeError("WRONG_REPOSITORY")
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("DEVELOP_REQUIRED")
    return git(root, "rev-parse", "HEAD")


def equation(lhs: object, rhs: object):
    from proof import Relation, RelationType
    return Relation(lhs, rhs, RelationType.EQUALITY)


def probe() -> dict[str, object]:
    from expression import Composition, MapApplication, Suspension
    from map_facts import EHP_H_MAP
    from proof import ProofRule
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase165_r55_nk_only_goal import registered_group_goal_candidates
    from phase169_r10e2_unpositioned_citation.source_first import (
        screen_independent_sources_for_derived_goal,
    )
    from phase169_r3h_source_registry import build_adopted_toda53_hopf_reference
    from phase165_r9_production_wiring import discover_goal_search_inputs
    from phase171_r2h_prop22_cited_hopf.source import (
        TodaProp22RightFormula, _formula_parts, _combined_premises,
    )
    from phase176_r3r27r1_toda55_quadruple_isolated.source import (
        Toda55UniversalQuadrupleStatement, canonical_quadruple_goal,
    )
    from phase174_r3_r7_r7_composite_zero_audit.rule import expression_endpoints

    source = build_adopted_toda53_hopf_reference(
        discover_goal_search_inputs().bridge).proof_links[0].step.conclusion
    nu_prime = source.lhs.expression
    quad = canonical_quadruple_goal(5)
    if quad is None:
        raise RuntimeError("QUADRUPLE_GOAL_UNAVAILABLE")
    eta5, eta6, eta7 = quad.rhs.left, quad.rhs.right.left, quad.rhs.right.right
    alpha = Composition(nu_prime, eta6)
    formula_lhs = MapApplication(EHP_H_MAP, Composition(alpha, Suspension(eta6)))
    formula = equation(formula_lhs,
                       Composition(MapApplication(EHP_H_MAP, alpha), Suspension(eta6)))
    target_hopf = equation(
        MapApplication(EHP_H_MAP, Composition(nu_prime, Composition(eta6, eta7))),
        quad.rhs,
    )
    bridge = build_shared_typed_bridge()
    roots = registered_group_goal_candidates(bridge, n=3, k=5)
    if len(roots) != 1:
        raise RuntimeError("ROOT_NOT_UNIQUE")
    screened = screen_independent_sources_for_derived_goal(bridge, goal=roots[0])
    given = tuple(link.step.conclusion for link in screened.proof_links
                  if link.step is not None and link.step.rule is ProofRule.GIVEN)
    provider = shared_expansion_provider(screened, proof_target=roots[0])

    def describe(goal: object) -> list[str]:
        return [item.rule.name for item in provider(goal)]

    return {
        "root_target": repr(roots[0]),
        "screened_given_count": len(given),
        "prop22_given_count": given.count(TodaProp22RightFormula()),
        "quadruple_given_count": given.count(Toda55UniversalQuadrupleStatement()),
        "nu_prime_hopf_given_count": given.count(source),
        "quadruple_goal_candidate_rules": describe(quad),
        "formula_left_endpoints": expression_endpoints(alpha),
        "formula_specialization_parts_recognized": _formula_parts(formula) is not None,
        "formula_candidate_rules": describe(formula),
        "combined_premises_for_target_count": len(_combined_premises(target_hopf, given)),
        "target_hopf_candidate_rules": describe(target_hopf),
        "root_candidate_rules": describe(roots[0]),
        "root_vs_formula_nesting_differs": target_hopf.lhs != formula.lhs,
        "target_eta_cube_representation": repr(quad.rhs),
        "quadruple_proof_was_verified_in_prior_r3r28r1": True,
        "hopf_image_proved_by_this_audit": False,
        "root_proof_claimed": False,
        "new_source_assertions": 0,
        "new_math_rules": 0,
        "full_pytest": "NOT_RUN",
    }


def report_file() -> Path:
    root = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
    path = root / "EHPProofTracerAudit" / PACKAGE
    path.mkdir(parents=True, exist_ok=True)
    return path / "report.json"


def run(dry_run: bool) -> int:
    report = {"phase": "176_R3R29", "gate": "FAIL_R3R29",
              "full_pytest": "NOT_RUN"}
    try:
        report["head"] = preflight(ROOT)
        report["source_guard"] = source_guard(ROOT)
        if dry_run:
            report["gate"] = "PASS_R3R29_DRYRUN"
        else:
            report["frontier"] = probe()
            report["gate"] = "PASS_R3R29_HOPF_RIGHT_FRONTIER_AUDITED"
    except Exception as err:
        report["error"] = type(err).__name__ + ": " + str(err)
    destination = report_file()
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2,
                                      default=str) + "\n", encoding="utf-8")
    print("PHASE176_R3R29_GATE=" + report["gate"])
    print("PHASE176_R3R29_HEAD=" + report.get("head", "UNVERIFIED"))
    for key, value in report.get("frontier", {}).items():
        print("PHASE176_R3R29_" + key.upper() + "=" + str(value))
    if "error" in report:
        print("PHASE176_R3R29_ERROR=" + report["error"])
    print("PHASE176_R3R29_REPORT=" + str(destination))
    print("PHASE176_R3R29_FULL_PYTEST=NOT_RUN")
    print("(END)")
    return 0 if report["gate"].startswith("PASS_") else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    return run(parser.parse_args().dry_run)


if __name__ == "__main__":
    sys.exit(main())
```

## tests/test_audit.py

```python
"""Focused failure-boundary contracts for Phase 176 R3R29."""
from pathlib import Path

import pytest

from phase176_r3r29_hopf_right_connection_audit import audit


def test_missing_source_fails_closed(tmp_path: Path) -> None:
    with pytest.raises(RuntimeError, match="MISSING_SOURCE"):
        audit.source_guard(tmp_path)


def test_source_signature_fails_closed(tmp_path: Path) -> None:
    for filename, anchors in audit.ANCHORS.items():
        path = tmp_path / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("".join(anchors), encoding="utf-8")
    assert all(audit.source_guard(tmp_path).values())
    item = tmp_path / next(iter(audit.ANCHORS))
    item.write_text("modified", encoding="utf-8")
    with pytest.raises(RuntimeError, match="SOURCE_SIGNATURE_CHANGED"):
        audit.source_guard(tmp_path)


def test_dryrun_never_invokes_probe(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(audit, "ROOT", tmp_path)
    monkeypatch.setattr(audit, "preflight", lambda root: "test-head")
    monkeypatch.setattr(audit, "source_guard", lambda root: {"ok": True})
    monkeypatch.setattr(audit, "probe", lambda: pytest.fail("probe should not run"))
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    assert audit.run(True) == 0


def test_probe_exception_cannot_claim_pass(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(audit, "ROOT", tmp_path)
    monkeypatch.setattr(audit, "preflight", lambda root: "test-head")
    monkeypatch.setattr(audit, "source_guard", lambda root: {"ok": True})
    monkeypatch.setattr(audit, "probe", lambda: (_ for _ in ()).throw(RuntimeError("blocked")))
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    assert audit.run(False) == 1
```

## run.ps1

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $repo
try {
    if ($DryRun) {
        python -B -m phase176_r3r29_hopf_right_connection_audit.audit --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'R3R29 DryRun failed' }
    } else {
        python -B -m phase176_r3r29_hopf_right_connection_audit.audit
        if ($LASTEXITCODE -ne 0) { throw 'R3R29 audit failed' }
        python -B -m pytest -q -p no:cacheprovider `
            .\phase176_r3r29_hopf_right_connection_audit\tests `
            .\phase176_r3r28_toda55_quadruple_public\tests\test_public.py `
            .\phase176_r3r27r1_toda55_quadruple_isolated\tests\test_source.py `
            .\phase171_r2h_prop22_cited_hopf\tests\test_cited_formula.py
        if ($LASTEXITCODE -ne 0) { throw 'R3R29 focused tests failed' }
        Write-Host 'PHASE176_R3R29_GATE=PASS_R3R29_FOCUSED_TESTS'
        Write-Host 'PHASE176_R3R29_FULL_PYTEST=NOT_RUN'
        Write-Host '(END)'
    }
} finally {
    Pop-Location
}
```

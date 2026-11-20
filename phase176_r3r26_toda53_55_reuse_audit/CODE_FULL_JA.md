# Phase 176 R3R26 新規コード全文

## audit.py

```python
"""Read-only source-first audit of Toda (5.3)/(5.5) for pi_8^3."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

PACKAGE = "phase176_r3r26_toda53_55_reuse_audit"
ROOT = Path(__file__).resolve().parent.parent
SOURCES = {
    "phase171_r2e_toda53_double_reference.py": "def build_adopted_toda53_double_reference(",
    "phase174_r3_r6_source_extension/source.py": "def expand_cited_toda55_double(",
    "phase165_r52_r9_shared_math.py": "def shared_expansion_provider(",
    "phase171_r2h_prop22_cited_hopf/source.py": "def _combined_premises(",
    "phase165_r55_nk_only_goal.py": "def registered_group_goal_candidates(",
}


def verify_sources(root: Path) -> dict[str, bool]:
    found = {}
    for name, anchor in SOURCES.items():
        path = root / name
        if not path.is_file() or anchor not in path.read_text(encoding="utf-8-sig"):
            raise RuntimeError("SOURCE_ANCHOR_MISSING: " + name)
        found[name] = True
    return found


def git(root: Path, *args: str) -> str:
    result = subprocess.run(("git", *args), cwd=root, text=True, capture_output=True, check=True)
    return result.stdout.strip()


def verify_checkout(root: Path) -> dict[str, object]:
    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root.resolve():
        raise RuntimeError("WRONG_REPOSITORY")
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("DEVELOP_REQUIRED")
    changed = tuple(git(root, "diff", "--name-only").splitlines())
    allowed = "phase171_r2h_prop22_cited_hopf/source.py"
    if any(name != allowed for name in changed):
        raise RuntimeError("UNEXPECTED_MODIFIED_FILES: " + repr(changed))
    if git(root, "diff", "--cached", "--name-only"):
        raise RuntimeError("STAGED_CHANGES_REQUIRE_REVIEW")
    return {"head": git(root, "rev-parse", "HEAD"), "modified_files": changed}


def audit_live() -> dict[str, object]:
    from expression import Composition, GeneratorSymbol, HomotopyElement, IteratedSuspension, Multiple
    from homotopy_groups import TodaPrimaryGroup
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase165_r55_nk_only_goal import registered_group_goal_candidates
    from phase169_r10e2_unpositioned_citation.source_first import screen_independent_sources_for_derived_goal
    from phase171_r2e_toda53_double_reference import ASSERTION_ID as DOUBLE_ID
    from phase174_r3_r6_source_extension.source import (
        Toda55UniversalDoubleStatement, expand_cited_toda55_double,
    )
    from phase169_r10d2_general_family_definition.family_citation import CitedStableFamilyDefinition
    from proof import ProofRule, Relation, RelationType

    bridge = build_shared_typed_bridge()
    root_goals = registered_group_goal_candidates(bridge, n=3, k=5)
    if len(root_goals) != 1:
        raise RuntimeError("ROOT_GOAL_CARDINALITY_CHANGED: " + str(len(root_goals)))
    goal = root_goals[0]
    screened = screen_independent_sources_for_derived_goal(bridge, goal=goal)
    links = tuple(link for link in screened.proof_links if link.step is not None and link.step.rule is ProofRule.GIVEN)
    sources = tuple(link.step.conclusion for link in links)
    double = tuple(link for link in links if link.assertion_id.endswith(":" + DOUBLE_ID))
    universal = tuple(link for link in links if type(link.step.conclusion) is Toda55UniversalDoubleStatement)
    nu5 = HomotopyElement("ν₅", 5, 8, 5, GeneratorSymbol("ν", index=5))
    nuprime = HomotopyElement("ν′", 3, 6, 3, GeneratorSymbol("ν", decoration="′"))
    doubled_nu5 = Relation(Multiple(2, nu5), IteratedSuspension(nuprime, 2), RelationType.EQUALITY)
    provider = shared_expansion_provider(screened, proof_target=goal)
    candidates = tuple(provider(doubled_nu5))
    direct = tuple(expand_cited_toda55_double(doubled_nu5, sources))
    family = tuple(item for item in sources if isinstance(item, CitedStableFamilyDefinition))
    eta_triple = None
    if len(double) == 1:
        eta_triple = double[0].step.conclusion.rhs
    return {
        "target": [3, 5],
        "root_goal": repr(goal),
        "screened_given_count": len(links),
        "toda53_double_given_count": len(double),
        "toda53_double_source": [repr(item.step.conclusion) for item in double],
        "toda55_universal_given_count": len(universal),
        "toda55_family_source_count": len(family),
        "nu5_double_goal": repr(doubled_nu5),
        "direct_toda55_double_candidates": len(direct),
        "shared_nu5_double_candidates": len(candidates),
        "shared_nu5_double_candidate_rules": [p.rule.name for p in candidates],
        "source_eta_triple": repr(eta_triple),
        "target_eta5_cube": "η₅η₆η₇ (mathematical target; no direct GIVEN)",
        "nu5_quadruple_proved": False,
        "hopf_image_proved_by_this_audit": False,
        "root_proof_complete_claimed": False,
        "new_given": 0,
        "new_mathematical_rules": 0,
        "full_pytest": "NOT_RUN",
    }


def report_path() -> Path:
    path = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir()) / "EHPProofTracerAudit" / PACKAGE
    path.mkdir(parents=True, exist_ok=True)
    return path / "report.json"


def execute(dry_run: bool) -> int:
    report: dict[str, object] = {
        "phase": "176_R3R26", "dry_run": dry_run,
        "utc": datetime.now(timezone.utc).isoformat(),
        "gate": "FAIL_R3R26", "full_pytest": "NOT_RUN",
        "new_given": 0, "new_mathematical_rules": 0,
    }
    try:
        report["checkout"] = verify_checkout(ROOT)
        report["source_guard"] = verify_sources(ROOT)
        if dry_run:
            report["gate"] = "PASS_R3R26_DRYRUN"
        else:
            report["observed"] = audit_live()
            report["gate"] = "PASS_R3R26_SOURCE_REUSE_FRONTIER_AUDITED"
    except Exception as exc:
        report["error"] = type(exc).__name__ + ": " + str(exc)
    path = report_path()
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE176_R3R26_GATE=" + str(report["gate"]))
    print("PHASE176_R3R26_HEAD=" + str(report.get("checkout", {}).get("head", "UNVERIFIED")))
    if "observed" in report:
        for key, value in report["observed"].items():
            print("PHASE176_R3R26_" + key.upper() + "=" + str(value))
    if "error" in report:
        print("PHASE176_R3R26_ERROR=" + report["error"])
    print("PHASE176_R3R26_REPORT=" + str(path))
    print("PHASE176_R3R26_FULL_PYTEST=NOT_RUN")
    print("(END)")
    return 0 if str(report["gate"]).startswith("PASS_") else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    return execute(args.dry_run)


if __name__ == "__main__":
    sys.exit(main())

```

## tests/test_audit.py

```python
"""Focused fail-closed contracts for R3R26 read-only audit."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from phase176_r3r26_toda53_55_reuse_audit import audit


def test_source_guard_rejects_empty_tree(tmp_path: Path) -> None:
    with pytest.raises(RuntimeError, match="SOURCE_ANCHOR_MISSING"):
        audit.verify_sources(tmp_path)


def test_dryrun_skips_live_capture(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(audit, "ROOT", tmp_path)
    monkeypatch.setattr(audit, "verify_checkout", lambda root: {"head": "test-head", "modified_files": ()})
    monkeypatch.setattr(audit, "verify_sources", lambda root: {"checked": True})
    monkeypatch.setattr(audit, "audit_live", lambda: pytest.fail("unexpected live capture"))
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    assert audit.execute(True) == 0
    p = tmp_path / "EHPProofTracerAudit" / audit.PACKAGE / "report.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    assert data["gate"] == "PASS_R3R26_DRYRUN"
    assert "observed" not in data


def test_live_failure_fails_closed(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(audit, "ROOT", tmp_path)
    monkeypatch.setattr(audit, "verify_checkout", lambda root: {"head": "test-head"})
    monkeypatch.setattr(audit, "verify_sources", lambda root: {"checked": True})
    monkeypatch.setattr(audit, "audit_live", lambda: (_ for _ in ()).throw(RuntimeError("forced_failure")))
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    assert audit.execute(False) == 1
    p = tmp_path / "EHPProofTracerAudit" / audit.PACKAGE / "report.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    assert data["gate"] == "FAIL_R3R26"
    assert "forced_failure" in data["error"]

```

## __init__.py

```python
"""Phase 176 R3R26 read-only audit package."""

```

## run.ps1

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Push-Location $root
try {
    $argsList = @('-B', '-m', 'phase176_r3r26_toda53_55_reuse_audit.audit')
    if ($DryRun) { $argsList += '--dry-run' }
    & python @argsList
    if ($LASTEXITCODE -ne 0) { throw 'R3R26 audit failed' }
    if (-not $DryRun) {
        & python -B -m pytest -q -p no:cacheprovider `
          .\phase176_r3r26_toda53_55_reuse_audit\tests `
          .\phase171_r2e_toda53_double_source\tests\test_source.py `
          .\phase174_r3_r6_source_extension\tests\test_source.py
        if ($LASTEXITCODE -ne 0) { throw 'R3R26 focused pytest failed' }
        Write-Output 'PHASE176_R3R26_GATE=PASS_R3R26_FOCUSED_TESTS'
        Write-Output 'PHASE176_R3R26_FULL_PYTEST=NOT_RUN'
        Write-Output '(END)'
    }
} finally {
    Pop-Location
}

```


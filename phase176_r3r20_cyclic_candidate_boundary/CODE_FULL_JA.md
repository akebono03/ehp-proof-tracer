# Phase 176 R3R20 追加コード全文

## audit.py

```python
"""Phase 176 R3R20 read-only cyclic-candidate boundary audit."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys

PACKAGE = "phase176_r3r20_cyclic_candidate_boundary"
ROOT = Path(__file__).resolve().parent.parent
REQUIRED = (
    "phase165_r52_r9_shared_math.py",
    "phase175_r3_pi73_hopf_lift/rule.py",
    "phase171_r2j_r4_r9_r9_public_cyclic_structure/source.py",
    "phase171_r2j_r4_r9_r7_public_cyclic_root/source.py",
    "phase168_r2_8_4_generic_specialization/specialization.py",
    "phase171_r2i_eta_hopf_bridge/source.py",
)


def inspect_source(root: Path) -> dict[str, object]:
    anchors = {
        REQUIRED[0]: "def shared_expansion_provider(",
        REQUIRED[1]: "def expand_cited_hopf_lift(",
        REQUIRED[2]: "def expand_cited_full_order_cyclic_structure(",
        REQUIRED[3]: "def expand_cited_double_cyclic_root(",
        REQUIRED[4]: "def specialize_registered_higher_stem(",
        REQUIRED[5]: "def eligible_eta_hopf_chains(",
    }
    found = {}
    for file_name, anchor in anchors.items():
        path = root / file_name
        if not path.is_file() or anchor not in path.read_text(encoding="utf-8-sig"):
            raise RuntimeError("SOURCE_ANCHOR_MISSING: " + file_name)
        found[file_name] = True
    return found


def capture() -> dict[str, object]:
    from homotopy_groups import TodaPrimaryGroup
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase165_r55_nk_only_goal import registered_group_goal_candidates, search_group_from_registered_goal
    from phase169_r10e2_unpositioned_citation.source_first import screen_independent_sources_for_derived_goal
    from phase165_r12_r2_quotient_rules import CyclicStructureStatement
    from phase175_r3_pi73_hopf_lift.rule import expand_cited_hopf_lift
    from phase171_r2j_r4_r9_r9_public_cyclic_structure.source import expand_cited_full_order_cyclic_structure
    from phase171_r2j_r4_r9_r7_public_cyclic_root.source import expand_cited_double_cyclic_root
    from phase171_r2i_eta_hopf_bridge.source import eligible_eta_hopf_chains
    from phase168_r2_8_4_generic_specialization.specialization import specialize_registered_higher_stem
    from proof import Relation, ProofRule

    bridge = build_shared_typed_bridge()
    goals = registered_group_goal_candidates(bridge, n=3, k=5)
    if len(goals) != 1:
        raise RuntimeError("NONUNIQUE_ROOT_GOALS")
    root = goals[0]
    screened = screen_independent_sources_for_derived_goal(bridge, goal=root)
    available = tuple(link.step.conclusion for link in screened.proof_links if link.step is not None and link.step.rule is ProofRule.GIVEN)
    provider = shared_expansion_provider(screened, proof_target=root)
    roots = tuple(provider(root))
    cyclic = tuple({repr(item): item for option in roots for item in option.subgoals if isinstance(item, CyclicStructureStatement)}.values())
    if len(cyclic) != 1:
        raise RuntimeError("CYCLIC_ROOT_FRONTIER_CHANGED")
    goal = cyclic[0]
    ordinary = tuple(provider(goal))
    hopf = tuple(expand_cited_hopf_lift(goal, available))
    full = tuple(expand_cited_full_order_cyclic_structure(goal, available))
    direct = tuple(expand_cited_double_cyclic_root(root, available))
    chains = eligible_eta_hopf_chains(available)
    codomain = TodaPrimaryGroup(goal.group.group_dimension, 2 * goal.group.sphere_dimension - 1)
    specialized = []
    for source in available:
        if isinstance(source, Relation):
            result = specialize_registered_higher_stem(source, codomain.sphere_dimension)
            if result is not None and result.lhs == codomain:
                specialized.append(repr(result))
    result = search_group_from_registered_goal(n=3, k=5)
    return {
        "target": [3, 5],
        "public_status": result.status.value,
        "public_open_goals": len(result.open_goals),
        "root_candidates": len(roots),
        "cyclic_children": len(cyclic),
        "cyclic_goal": repr(goal),
        "screened_givens": len(available),
        "ordinary_cyclic_candidates": len(ordinary),
        "hopf_lift_candidates": len(hopf),
        "finite_full_order_candidates": len(full),
        "double_root_candidates": len(direct),
        "hopf_eta_chain_count": len(chains),
        "hopf_eta_chains": [repr(chain.conclusion) for chain in chains[:5]],
        "matching_specialized_codomain_count": len(specialized),
        "matching_specialized_codomains": specialized[:5],
        "hopf_codomain": repr(codomain),
        "hopf_generator_match_not_proved": True,
        "finite_full_order_requires_order_four_source": True,
        "root_proof_complete": False,
        "new_given": 0,
        "new_mathematical_rules": 0,
        "full_pytest": "NOT_RUN",
    }


def checked_git_root(root: Path) -> str:
    proc = subprocess.run(("git", "rev-parse", "--show-toplevel"), cwd=root, capture_output=True, text=True, check=True)
    if Path(proc.stdout.strip()).resolve() != root.resolve():
        raise RuntimeError("WRONG_REPOSITORY")
    branch = subprocess.run(("git", "branch", "--show-current"), cwd=root, capture_output=True, text=True, check=True)
    if branch.stdout.strip() != "develop":
        raise RuntimeError("DEVELOP_REQUIRED")
    head = subprocess.run(("git", "rev-parse", "HEAD"), cwd=root, capture_output=True, text=True, check=True)
    return head.stdout.strip()


def report_file() -> Path:
    import os
    import tempfile
    base = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir()) / "EHPProofTracerAudit" / PACKAGE
    base.mkdir(parents=True, exist_ok=True)
    return base / "report.json"


def execute(dry_run: bool) -> int:
    report: dict[str, object] = {
        "phase": "176_R3R20", "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "dry_run": dry_run, "gate": "FAIL_R3R20", "full_pytest": "NOT_RUN",
        "new_given": 0, "new_mathematical_rules": 0,
    }
    try:
        report["head"] = checked_git_root(ROOT)
        report["source_guard"] = inspect_source(ROOT)
        if not dry_run:
            report["observed"] = capture()
            report["gate"] = "PASS_R3R20_CYCLIC_BOUNDARY_RECORDED"
        else:
            report["gate"] = "PASS_R3R20_READ_ONLY_DRYRUN"
    except Exception as exc:
        report["error"] = type(exc).__name__ + ": " + str(exc)
    path = report_file()
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE176_R3R20_GATE=" + str(report["gate"]))
    print("PHASE176_R3R20_HEAD=" + str(report.get("head", "UNVERIFIED")))
    if "observed" in report:
        for field, value in report["observed"].items():
            print("PHASE176_R3R20_" + field.upper() + "=" + str(value))
    if "error" in report:
        print("PHASE176_R3R20_ERROR=" + str(report["error"]))
    print("PHASE176_R3R20_REPORT=" + str(path))
    print("PHASE176_R3R20_FULL_PYTEST=NOT_RUN")
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
"""Isolated tests for Phase 176 R3R20 audit mechanics."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from phase176_r3r20_cyclic_candidate_boundary import audit


def test_source_guard_requires_all_anchors(tmp_path: Path) -> None:
    for name in audit.REQUIRED:
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
    with pytest.raises(RuntimeError, match="SOURCE_ANCHOR_MISSING"):
        audit.inspect_source(tmp_path)


def test_dry_run_does_not_capture(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(audit, "ROOT", tmp_path)
    monkeypatch.setattr(audit, "checked_git_root", lambda root: "test-head")
    monkeypatch.setattr(audit, "inspect_source", lambda root: {"test": True})
    monkeypatch.setattr(audit, "capture", lambda: pytest.fail("unexpected capture"))
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    assert audit.execute(True) == 0
    path = tmp_path / "EHPProofTracerAudit" / audit.PACKAGE / "report.json"
    report = json.loads(path.read_text(encoding="utf-8"))
    assert report["gate"] == "PASS_R3R20_READ_ONLY_DRYRUN"
    assert "observed" not in report


def test_capture_failure_fails_closed(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(audit, "checked_git_root", lambda root: "test-head")
    monkeypatch.setattr(audit, "inspect_source", lambda root: {"test": True})
    monkeypatch.setattr(audit, "capture", lambda: (_ for _ in ()).throw(RuntimeError("probe_failed")))
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    assert audit.execute(False) == 1
    report = json.loads((tmp_path / "EHPProofTracerAudit" / audit.PACKAGE / "report.json").read_text(encoding="utf-8"))
    assert report["gate"] == "FAIL_R3R20"
    assert "probe_failed" in report["error"]

```

## run.ps1

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Push-Location $root
try {
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $args = @('-B', '-m', 'phase176_r3r20_cyclic_candidate_boundary.audit')
    if ($DryRun) { $args += '--dry-run' }
    & python @args
    if ($LASTEXITCODE -ne 0) { throw 'R3R20 audit failed' }
    if (-not $DryRun) {
        & python -B -m pytest -q -p no:cacheprovider 'phase176_r3r20_cyclic_candidate_boundary/tests/test_audit.py'
        if ($LASTEXITCODE -ne 0) { throw 'R3R20 pytest failed' }
    }
} finally { Pop-Location }

```

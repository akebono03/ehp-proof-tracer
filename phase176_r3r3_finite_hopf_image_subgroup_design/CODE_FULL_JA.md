# Phase 176 R3R3 — 追加コード全文
変更対象: 新規 `phase176_r3r3_finite_hopf_image_subgroup_design/` 配下のみ。既存ファイル・クラス・関数の変更はありません。
新規関数は `audit.py` の各定義位置、テスト関数は `tests/test_audit.py` に追加します。

## audit.py
```python
"""Phase 176 R3R3: read-only finite-Hopf image-subgroup design audit.

No production rule is installed, no source or prior conclusion is certified,
and no proof result is created. Hypothetical values are labelled as such.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import traceback

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = "phase176_r3r3_finite_hopf_image_subgroup_design"
REVIEWED_HEAD = "b837ba9819a5a1b166f13739b160b4880b4599e2"
MARKER = "PHASE176_R3R3_WORKER_JSON="
SOURCES = (
    "phase175_r3_pi73_hopf_lift/rule.py",
    "phase175_r3_pi73_hopf_lift/tests/test_rule.py",
    "phase174_r3_r7_r5_zero_image_hopf_injective/rule.py",
    "phase165_r12_r2_quotient_rules.py",
    "phase165_r12_r5_structure_bridge.py",
    "phase165_r14_r6_generic_iso.py",
    "phase165_r14_r9_ehp_exactness.py",
    "phase165_r12_r12_ehp_consequences.py",
    "phase165_r52_r9_shared_math.py",
    "phase165_r55_nk_only_goal.py",
    "phase176_r3r2_finite_cyclic_hopf_frontier/audit.py",
    "sources/toda/Toda_05_2.tex",
    "sources/toda/Toda_02_2.tex",
)


def git(*args: str, check: bool = True) -> tuple[int, str]:
    result = subprocess.run(("git",) + args, cwd=ROOT, capture_output=True,
                            text=True, encoding="utf-8", errors="replace", check=False)
    if check and result.returncode:
        raise RuntimeError("GIT_READ_FAILED: " + " ".join(args) + ": " + result.stderr.strip())
    return result.returncode, result.stdout.strip()


def preflight() -> dict[str, object]:
    if Path(git("rev-parse", "--show-toplevel")[1]).resolve() != ROOT.resolve():
        raise RuntimeError("WRONG_REPOSITORY_ROOT")
    if git("branch", "--show-current")[1] != "develop":
        raise RuntimeError("DEVELOP_REQUIRED")
    if git("merge-base", "--is-ancestor", REVIEWED_HEAD, "HEAD", check=False)[0]:
        raise RuntimeError("R3_REVIEWED_HEAD_NOT_ANCESTOR")
    if git("status", "--porcelain", "--untracked-files=no")[1]:
        raise RuntimeError("TRACKED_CHANGES_REQUIRE_REVIEW")
    missing = [name for name in SOURCES if not (ROOT / name).is_file()]
    if missing:
        raise RuntimeError("SOURCE_NOT_FOUND: " + repr(missing))
    old_rule = (ROOT / SOURCES[0]).read_text(encoding="utf-8-sig")
    for token in ("def hopf_lift_inputs(", "def expand_cited_hopf_lift(",
                  "codomain.rhs.order != goal.order", "proof_rule=ProofRule.INFERENCE"):
        if token not in old_rule:
            raise RuntimeError("EXISTING_FINITE_HOPF_RULE_CHANGED_REVIEW_REQUIRED: " + token)
    return {
        "head": git("rev-parse", "HEAD")[1],
        "origin_develop": git("rev-parse", "--verify", "origin/develop", check=False)[1] or None,
        "reviewed_head_is_ancestor": True,
        "source_sha256": {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in SOURCES},
        "historical_source_guards": "FOUR_KNOWN_FAILURES_NOT_PASSING",
        "full_pytest": "NOT_RUN",
    }


def describe(value: object, limit: int = 1600) -> dict[str, str]:
    return {"type": type(value).__module__ + "." + type(value).__name__,
            "repr": repr(value)[:limit]}


def describe_options(provider, goal: object) -> dict[str, object]:
    try:
        options = tuple(provider(goal))
    except Exception as exc:
        return {"status": "PROVIDER_ERROR", "error": type(exc).__name__ + ": " + str(exc)}
    return {"status": "PROPOSALS_NOT_PROOFS", "count": len(options),
            "rules": [getattr(item.rule, "name", type(item.rule).__name__) for item in options[:10]],
            "premises": [[describe(x) for x in item.subgoals] for item in options[:10]],
            "truncated": len(options) > 10}


def classify_codomain_order(goal_order: object, codomain_order: object) -> str:
    """Only classify old rule's order guard; do not assert a theorem."""
    if type(goal_order) is not int or goal_order < 1:
        return "INVALID_GOAL_ORDER"
    if type(codomain_order) is not int or codomain_order < 1:
        return "CODOMAIN_ORDER_UNKNOWN"
    if codomain_order == goal_order:
        return "OLD_RULE_ORDER_GUARD_ACCEPTS"
    return "OLD_RULE_ORDER_GUARD_REJECTS"


def observe() -> dict[str, object]:
    from expression import Composition, GeneratorSymbol, HomotopyElement, MapApplication
    from homotopy_groups import TodaPrimaryGroup, TodaHopfInvariantMap, TodaSuspensionMap, TodaDeltaMap
    from map_facts import EHP_H_MAP
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase165_r12_r2_quotient_rules import CyclicStructureStatement
    from phase165_r14_r6_generic_iso import MapInjective
    from phase165_r14_r9_ehp_exactness import expand_generic_ehp_hopf_goal
    from phase174_r3_r7_r5_zero_image_hopf_injective.rule import (
        hopf_injectivity_from_zero_image_inputs, expand_hopf_injective_from_zero_image,
    )
    from phase175_r3_pi73_hopf_lift.rule import (
        hopf_lift_inputs, expand_cited_hopf_lift,
    )
    from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
    from proof import Relation, RelationType, ProofRule

    result = search_group_from_registered_goal(n=3, k=5)
    cyclic = [x for x in result.open_goals if isinstance(x, CyclicStructureStatement)]
    if len(cyclic) != 1 or cyclic[0].group != TodaPrimaryGroup(8, 3) or cyclic[0].order != 2:
        raise RuntimeError("R3R3_CYCLIC_GOAL_DRIFT")
    goal = cyclic[0]
    codomain = TodaPrimaryGroup(8, 5)
    hopf = TodaHopfInvariantMap(goal.group, codomain)
    inject_goal = MapInjective(hopf)
    inject_inputs = hopf_injectivity_from_zero_image_inputs(inject_goal)
    zero_image = inject_inputs[0] if inject_inputs is not None else None
    bridge = build_shared_typed_bridge()
    available = tuple(
        link.step.conclusion for link in bridge.proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
        and bridge.registry.assertion(link.assertion_id).content == link.step.conclusion
    )
    provider = shared_expansion_provider(bridge, proof_target=result.open_goals[-1])
    codomain_prior = exact_prior_database_result(5, 3)
    preceding_prior = exact_prior_database_result(2, 5)
    # An explicit unproved notation candidate: NO proof step or claim is created.
    eta5 = HomotopyElement("η₅", 5, source=6, target=5, generator=GeneratorSymbol("η", 5))
    eta6 = HomotopyElement("η₆", 6, source=7, target=6, generator=GeneratorSymbol("η", 6))
    eta7 = HomotopyElement("η₇", 7, source=8, target=7, generator=GeneratorSymbol("η", 7))
    eta_cube = Composition(eta5, Composition(eta6, eta7))
    hypothetical_hopf_image = Relation(MapApplication(EHP_H_MAP, goal.generator), eta_cube, RelationType.EQUALITY)
    old_typed_inputs = (hopf_lift_inputs(goal, codomain_prior, hypothetical_hopf_image)
                        if isinstance(codomain_prior, Relation) else None)
    image_order = getattr(getattr(codomain_prior, "rhs", None), "order", None)
    matched = sorted({
        bridge.registry._references[a.reference_id].locator
        for a in bridge.registry._assertions.values()
        if any(x in bridge.registry._references[a.reference_id].locator.lower()
               for x in ("5.7", "5.5", "5.3", "5.6", "5.8", "2.2", "4.2", "4.4"))
    })
    return {
        "target": [3, 5], "proof_status": result.status.value,
        "open_goals": len(result.open_goals),
        "target_cyclic_goal": describe(goal),
        "existing_general_lift_rule_found": True,
        "existing_rule_name": "injective Hopf preimage of a finite cyclic generator is cyclic",
        "existing_rule_sourced_only_from_past_phase": True,
        "codomain_prior": describe(codomain_prior),
        "codomain_order": image_order,
        "source_group_prior": describe(preceding_prior),
        "old_order_guard": classify_codomain_order(goal.order, image_order),
        "old_rule_inputs_for_hypothetical_image": old_typed_inputs is not None,
        "hypothetical_hopf_image_not_proved": describe(hypothetical_hopf_image),
        "existing_standalone_lift_candidates": (
            describe_options(lambda value: expand_cited_hopf_lift(value, available), goal)),
        "shared_cyclic_candidates": describe_options(provider, goal),
        "hopf_injective_zero_image_inputs": [describe(x) for x in inject_inputs] if inject_inputs is not None else [],
        "zero_image_premise": describe(zero_image),
        "hopf_injective_from_zero_image_candidates": describe_options(expand_hopf_injective_from_zero_image, inject_goal),
        "hopf_injective_from_zero_group_candidates": describe_options(expand_generic_ehp_hopf_goal, inject_goal),
        "shared_zero_image_candidates": describe_options(provider, zero_image) if zero_image is not None else {"status": "NO_TYPED_INPUT"},
        "delta": describe(TodaDeltaMap(codomain, TodaPrimaryGroup(6, 2))),
        "source_locators": matched,
        "design_boundary": (
            "EXISTING_HOPF_LIFT_REQUIRES_FULL_CODOMAIN_ORDER; "
            "N3_K5_NEEDS_TYPED_INJECTIVE_H_AND_CYCLIC_IMAGE_SUBGROUP; "
            "EACH_PREMISE_MUST_BE_PROVED_IN_ORDINARY_SOURCE_FIRST_SEARCH"
        ),
        "proof_complete": False, "new_given": 0, "new_mathematical_rules": 0,
    }


def worker(timeout: int) -> dict[str, object]:
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8")
    try:
        proc = subprocess.run((sys.executable, "-B", "-m", PACKAGE + ".audit", "--worker"),
                              cwd=ROOT, env=env, capture_output=True, text=True,
                              encoding="utf-8", errors="replace", timeout=timeout, check=False)
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError("R3R3_WORKER_TIMEOUT") from exc
    markers = [line[len(MARKER):] for line in proc.stdout.splitlines() if line.startswith(MARKER)]
    if proc.returncode or len(markers) != 1:
        raise RuntimeError("R3R3_WORKER_FAILED exit=" + str(proc.returncode) + " stderr=" + proc.stderr[-3500:])
    result = json.loads(markers[0])
    if result.get("proof_complete") is not False or result.get("new_given") != 0:
        raise RuntimeError("R3R3_AUDIT_CANNOT_CLAIM_PROOF")
    return result


def report_path() -> Path:
    folder = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir()) / "EHPProofTracerAudit" / PACKAGE
    folder.mkdir(parents=True, exist_ok=True)
    return folder / "report.json"


def run(dry_run: bool, timeout: int) -> int:
    report: dict[str, object] = {
        "phase": "176_R3R3", "dry_run": dry_run,
        "mode": "READ_ONLY_FINITE_HOPF_IMAGE_SUBGROUP_DESIGN",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "gate": "FAIL_R3R3", "new_given": 0, "new_mathematical_rules": 0,
        "full_pytest": "NOT_RUN", "proof_complete": False,
    }
    try:
        report["preflight"] = preflight()
        if not dry_run:
            report["observed"] = worker(timeout)
        report["gate"] = "PASS_R3R3_READ_ONLY_DRYRUN" if dry_run else "PASS_R3R3_RULE_DESIGN_FRONTIER"
    except Exception as exc:
        report["error"] = type(exc).__name__ + ": " + str(exc)
        report["traceback"] = traceback.format_exc()[-8000:]
    path = report_path()
    path.write_text(json.dumps(report, indent=2, ensure_ascii=False, default=str) + "\n", encoding="utf-8")
    print("PHASE176_R3R3_GATE=" + report["gate"])
    print("PHASE176_R3R3_REPORT=" + str(path))
    print("PHASE176_R3R3_HEAD=" + str(report.get("preflight", {}).get("head", "UNVERIFIED")))
    if "observed" in report:
        o = report["observed"]
        print("PHASE176_R3R3_GROUP=(3,5) STATUS=" + o["proof_status"] + " OPEN=" + str(o["open_goals"]))
        print("PHASE176_R3R3_OLD_ORDER_GUARD=" + o["old_order_guard"])
        print("PHASE176_R3R3_SHARED_CYCLIC_PROPOSALS=" + str(o["shared_cyclic_candidates"].get("count", "ERROR")))
        print("PHASE176_R3R3_ZERO_IMAGE_PROPOSALS=" + str(o["shared_zero_image_candidates"].get("count", "ERROR")))
    if "error" in report:
        print("PHASE176_R3R3_ERROR=" + report["error"])
    print("PHASE176_R3R3_FULL_PYTEST=NOT_RUN")
    print("(END)")
    return 0 if report["gate"].startswith("PASS_") else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--worker", action="store_true")
    parser.add_argument("--timeout", type=int, default=120)
    args = parser.parse_args()
    if args.worker:
        try:
            print(MARKER + json.dumps(observe(), ensure_ascii=False))
            return 0
        except Exception:
            traceback.print_exc()
            return 1
    return run(args.dry_run, args.timeout)


if __name__ == "__main__":
    raise SystemExit(main())

```

## tests/test_audit.py
```python
"""Focused non-production R3R3 audit tests."""
from __future__ import annotations

import json

import pytest

from phase176_r3r3_finite_hopf_image_subgroup_design import audit


def test_old_lift_guard_accepts_only_equal_order() -> None:
    assert audit.classify_codomain_order(2, 2) == "OLD_RULE_ORDER_GUARD_ACCEPTS"
    assert audit.classify_codomain_order(2, 8) == "OLD_RULE_ORDER_GUARD_REJECTS"


def test_order_classifier_refuses_invalid_data() -> None:
    assert audit.classify_codomain_order(True, 8) == "INVALID_GOAL_ORDER"
    assert audit.classify_codomain_order(2, None) == "CODOMAIN_ORDER_UNKNOWN"


def test_expansion_is_not_labeled_as_proof() -> None:
    class Rule:
        name = "hypothetical test"

    class Proposal:
        rule = Rule()
        subgoals = ("not yet proved",)

    row = audit.describe_options(lambda goal: (Proposal(),), "request")
    assert row["status"] == "PROPOSALS_NOT_PROOFS"
    assert row["count"] == 1
    assert row["premises"][0][0]["repr"] == "'not yet proved'"


def test_proposal_exception_visible() -> None:
    def broken(goal):
        raise ValueError("not grounded")

    row = audit.describe_options(broken, object())
    assert row["status"] == "PROVIDER_ERROR"
    assert "ValueError" in row["error"]


def test_preflight_fails_closed_on_dirty_tracked_file(monkeypatch: pytest.MonkeyPatch, tmp_path) -> None:
    monkeypatch.setattr(audit, "ROOT", tmp_path)
    for name in audit.SOURCES:
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("fixture", encoding="utf-8")

    def fake_git(*args, check=True):
        key = args[0]
        if key == "rev-parse" and args[1] == "--show-toplevel":
            return 0, str(tmp_path)
        if key == "branch":
            return 0, "develop"
        if key == "merge-base":
            return 0, ""
        if key == "status":
            return 0, " M source.py"
        return 0, "head"

    monkeypatch.setattr(audit, "git", fake_git)
    with pytest.raises(RuntimeError, match="TRACKED_CHANGES_REQUIRE_REVIEW"):
        audit.preflight()


def test_dry_run_does_not_start_worker(monkeypatch: pytest.MonkeyPatch, tmp_path) -> None:
    monkeypatch.setattr(audit, "preflight", lambda: {"head": "test-head"})
    monkeypatch.setattr(audit, "worker", lambda timeout: pytest.fail("worker started"))
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    assert audit.run(True, 5) == 0
    path = tmp_path / "EHPProofTracerAudit" / audit.PACKAGE / "report.json"
    saved = json.loads(path.read_text(encoding="utf-8"))
    assert saved["gate"] == "PASS_R3R3_READ_ONLY_DRYRUN"
    assert saved["proof_complete"] is False
    assert saved["full_pytest"] == "NOT_RUN"


def test_worker_rejects_false_proof_claim(monkeypatch: pytest.MonkeyPatch) -> None:
    class Process:
        returncode = 0
        stderr = ""
        stdout = audit.MARKER + '{"proof_complete":true,"new_given":0}'

    monkeypatch.setattr(audit.subprocess, "run", lambda *args, **kwargs: Process())
    with pytest.raises(RuntimeError, match="R3R3_AUDIT_CANNOT_CLAIM_PROOF"):
        audit.worker(5)

```

## run.ps1
```powershell
param([switch]$DryRun, [int]$TimeoutSeconds = 120)
$ErrorActionPreference = 'Stop'
$folder = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $folder
Push-Location $root
try {
    if ($DryRun) {
        python -B -m phase176_r3r3_finite_hopf_image_subgroup_design.audit --dry-run --timeout $TimeoutSeconds
        if ($LASTEXITCODE -ne 0) { throw 'Phase176 R3R3 DryRun failed' }
    } else {
        python -B -m pytest -q --import-mode=importlib -p no:cacheprovider phase176_r3r3_finite_hopf_image_subgroup_design/tests
        if ($LASTEXITCODE -ne 0) { throw 'Phase176 R3R3 focused tests failed' }
        python -B -m phase176_r3r3_finite_hopf_image_subgroup_design.audit --timeout $TimeoutSeconds
        if ($LASTEXITCODE -ne 0) { throw 'Phase176 R3R3 audit failed' }
        git diff --check
        if ($LASTEXITCODE -ne 0) { throw 'Phase176 R3R3 diff check failed' }
    }
} finally {
    Pop-Location
}

```

## __init__.py
```python
"""Phase 176 R3R3 read-only design audit."""

```

## tests/__init__.py
```python
"""Focused tests for Phase 176 R3R3."""

```

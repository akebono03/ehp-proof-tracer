# Phase 171 R2J-R4-R9-R3 — 追加コード全文

既存ファイル・クラス・関数の変更はありません。全ファイルはリポジトリ直下の `phase171_r2j_r4_r9_r3_hopf_frontier_diagnostic/` に新規追加します。既存 import の変更はありません。

## 追加ファイル・関数

- `audit.py`：`_git()`、`_hopf_goal()`、`_unique_hopf_node()`、`_proof_event()`、`_failure_class()`、`inspect_first_hopf_frontier()`、`main()`。
- `tests/test_audit.py`：`_fixture()` と8つの新規テスト関数。
- `run.ps1`：限定 pytest と読み取り専用監査を実行する。

各コードブロックは import を含めたファイル全文であり、省略はありません。

## `audit.py`

```python
"""Diagnose the first unresolved Hopf-surjectivity subgoal of R9-R2.

This read-only probe replays the actual positioned pi_6^3 goal through the
normal recursive search; it observes matcher calls and proof outcomes but
never inserts a completed step, forges a GIVEN, or changes production code.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
from unittest.mock import patch

from homotopy_groups import TodaHopfInvariantMap, TodaPrimaryGroup
from phase165_r14_r6_generic_iso import MapSurjective
import phase165_r3_recursive_search as search_engine
from phase171_r2i_eta_hopf_bridge.audit import _screened_context
from phase165_r52_r9_shared_math import shared_expansion_provider
from phase171_r2j_r4_r8_cyclic_structure.audit import build_cyclic_pi63_proof
from phase171_r2j_r4_r9_r2_scoped_search_bridge.source import (
    inference_expansion_catalog,
    scoped_expansion_provider,
    walk_proof_ancestry,
)
from proof import ProofRule, ProofStep

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = Path(__file__).resolve().parent / "output"


def _git(*arguments: str) -> str:
    allowed = {
        ("branch", "--show-current"),
        ("rev-parse", "HEAD"),
        ("status", "--porcelain", "--untracked-files=no"),
    }
    if arguments not in allowed:
        raise ValueError("only read-only Git operations are permitted")
    return subprocess.run(
        ["git", *arguments], cwd=ROOT, capture_output=True,
        text=True, check=True,
    ).stdout.strip()


def _hopf_goal() -> MapSurjective:
    return MapSurjective(TodaHopfInvariantMap(
        TodaPrimaryGroup(7, 3), TodaPrimaryGroup(7, 5),
    ))


def _unique_hopf_node(root: ProofStep, hopf_goal: MapSurjective) -> ProofStep:
    """Identify the actual R4-R8 Hopf proof node, never its printed name."""
    candidates = tuple(
        step for step in walk_proof_ancestry(root)
        if type(step.conclusion) is type(hopf_goal)
        and step.conclusion == hopf_goal
    )
    if (len(candidates) != 1
            or candidates[0].rule is not ProofRule.INFERENCE
            or candidates[0].inference_rule is None):
        raise RuntimeError("R4-R8 must contain exactly one inferred pi_7^3 Hopf-surjectivity node")
    return candidates[0]


def _proof_event(kind: str, goal: object, step: ProofStep | None) -> dict:
    if kind not in ("proved", "unresolved"):
        raise ValueError("unknown canonical search event")
    if step is not None and not isinstance(step, ProofStep):
        raise TypeError("invalid search observer step")
    if kind == "proved" and step is None:
        raise ValueError("proved event requires real step")
    return {
        "kind": kind,
        "statement_type": type(goal).__name__,
        "goal": repr(goal)[:600],
        "proof_rule": step.rule.value if step is not None else None,
        "inference_rule": (
            step.inference_rule.name
            if step is not None and step.inference_rule is not None else None
        ),
    }


def _failure_class(hopf_proved: bool, match_attempts: list[dict]) -> str:
    if hopf_proved:
        return "HOPF_REPLAYED"
    if not match_attempts:
        return "HOPF_PREMISES_NOT_ALL_RECONSTRUCTED"
    if all(item["matches"] == 0 for item in match_attempts):
        return "HOPF_MATCHER_REJECTED_RECONSTRUCTED_PREMISES"
    return "HOPF_MATCHED_BUT_ROOT_NOT_ADMITTED"


def inspect_first_hopf_frontier() -> dict:
    """Replay identical citing context and record the exact first blocking H map."""
    screened, target, citing_id = _screened_context()
    root, _, r8_report = build_cyclic_pi63_proof()
    if (
        root.rule is not ProofRule.INFERENCE
        or root.conclusion != target
        or r8_report["new_given_added"] != 0
    ):
        raise RuntimeError("R4-R8 root or provenance is not validated")

    hopf_goal = _hopf_goal()
    original_hopf = _unique_hopf_node(root, hopf_goal)
    catalog = inference_expansion_catalog(root)
    hopf_routes = tuple(
        proposal for conclusion, proposal in catalog
        if type(conclusion) is type(hopf_goal) and conclusion == hopf_goal
    )
    if (
        len(hopf_routes) != 1
        or hopf_routes[0].rule is not original_hopf.inference_rule
        or hopf_routes[0].subgoals != tuple(
            parent.conclusion for parent in original_hopf.premises
        )
    ):
        raise RuntimeError("the extracted Hopf route differs from the R4-R8 proof")

    ordinary = shared_expansion_provider(screened, proof_target=target)
    scoped = scoped_expansion_provider(root, ordinary)
    if scoped(hopf_goal) != hopf_routes:
        raise RuntimeError("scoped provider dropped the original Hopf rule")

    events: list[dict] = []
    match_attempts: list[dict] = []
    original_matcher = search_engine.find_inference_matches_for_rule

    def observe(kind: str, goal: object, step: ProofStep | None) -> None:
        if len(events) < 400:
            events.append(_proof_event(kind, goal, step))

    def trace_match(rule, premises):
        result = original_matcher(rule, premises)
        if rule is original_hopf.inference_rule:
            match_attempts.append({
                "rule": rule.name,
                "matches": len(result),
                "input_proof_rules": [step.rule.value for step in premises],
                "input_statement_types": [type(step.conclusion).__name__ for step in premises],
                "input_conclusions": [repr(step.conclusion)[:700] for step in premises],
                "expected_proof_rules": [
                    parent.rule.value for parent in original_hopf.premises
                ],
            })
        return result

    canonical_root = None
    search_error = None
    with patch.object(
        search_engine, "find_inference_matches_for_rule", side_effect=trace_match,
    ):
        try:
            canonical_root = search_engine.reconstruct_registered_goal(
                target, screened, citing_id, scoped,
                lookup_mode="typed_reference_publication",
                progress_observer=observe,
            )
        except search_engine.RegisteredGoalUnresolved as exc:
            search_error = str(exc)
    complete = (
        canonical_root is not None
        and canonical_root.rule is ProofRule.INFERENCE
        and canonical_root.conclusion == target
    )
    if canonical_root is not None and not complete:
        raise RuntimeError("canonical search returned an unexpected group proof root")

    hopf_proved = any(
        event["kind"] == "proved" and event["goal"] == repr(hopf_goal)[:600]
        and event["proof_rule"] == ProofRule.INFERENCE.value
        for event in events
    )
    # The generic search itself, not the audit, determines whether a node
    # is provable.  This classification helps focus the next minimal repair.
    explanation = _failure_class(hopf_proved, match_attempts)
    unresolved = [item for item in events if item["kind"] == "unresolved"]
    hopf_events = [item for item in events if item["goal"] == repr(hopf_goal)[:600]]
    return {
        "phase": "171-R2J-R4-R9-R3",
        "mode": "AUDIT_ONLY_HOPF_FRONTIER",
        "target": repr(target),
        "citing_assertion_id": citing_id,
        "original_inference_rule_count": len(catalog),
        "hopf_goal": repr(hopf_goal),
        "hopf_r8_rule": original_hopf.inference_rule.name,
        "hopf_r8_premise_types": [
            type(step.conclusion).__name__ for step in original_hopf.premises
        ],
        "hopf_r8_premise_proof_rules": [
            step.rule.value for step in original_hopf.premises
        ],
        "hopf_r8_premise_goals": [
            repr(step.conclusion)[:1000] for step in original_hopf.premises
        ],
        "hopf_scoped_routes": len(hopf_routes),
        "hopf_public_routes": [
            {"rule": option.rule.name,
             "subgoals": [repr(item)[:350] for item in option.subgoals]}
            for option in ordinary(hopf_goal)[:10]
        ],
        "canonical_root_inferred": complete,
        "canonical_error": search_error,
        "hopf_proved_in_canonical_search": hopf_proved,
        "hopf_failure_class": explanation,
        "hopf_match_attempts": match_attempts,
        "hopf_search_events": hopf_events,
        "first_unresolved_goals": unresolved[:12],
        "observed_proven_steps": len([x for x in events if x["kind"] == "proved"]),
        "events": events[:150],
        "new_given_added": 0,
        "production_modified": False,
        "public_web_verified": False,
        "full_pytest": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    branch = _git("branch", "--show-current")
    head = _git("rev-parse", "HEAD")
    tracked_before = _git("status", "--porcelain", "--untracked-files=no")
    if branch != "develop":
        raise RuntimeError("R9-R3 requires the develop branch")
    for required in (
        "phase171_r2j_r4_r9_r2_scoped_search_bridge/source.py",
        "phase171_r2j_r4_r8_cyclic_structure/audit.py",
    ):
        if not (ROOT / required).is_file():
            raise RuntimeError("missing prerequisite: " + required)
    print("PHASE171_R2J_R4_R9_R3_BRANCH=" + branch, flush=True)
    print("PHASE171_R2J_R4_R9_R3_HEAD=" + head, flush=True)
    if args.dry_run:
        print("PHASE171_R2J_R4_R9_R3_RESULT=PASS_DRY_RUN", flush=True)
        return
    report = inspect_first_hopf_frontier()
    if _git("status", "--porcelain", "--untracked-files=no") != tracked_before:
        raise RuntimeError("tracked repository files changed during read-only audit")
    report.update({"git_head": head, "tracked_status_unchanged": True})
    OUTPUT.mkdir(parents=True, exist_ok=True)
    destination = OUTPUT / "audit.json"
    destination.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    print("PHASE171_R2J_R4_R9_R3_RULE_CATALOG=" + str(report["original_inference_rule_count"]), flush=True)
    print("PHASE171_R2J_R4_R9_R3_HOPF_FRONTIER=" + report["hopf_failure_class"], flush=True)
    print("PHASE171_R2J_R4_R9_R3_HOPF_MATCH_ATTEMPTS=" + str(len(report["hopf_match_attempts"])), flush=True)
    print("PHASE171_R2J_R4_R9_R3_CANONICAL_COMPLETE=" + str(report["canonical_root_inferred"]), flush=True)
    print("PHASE171_R2J_R4_R9_R3_NEW_GIVEN=0", flush=True)
    print("PHASE171_R2J_R4_R9_R3_PUBLIC_WEB_VERIFIED=False", flush=True)
    print("PHASE171_R2J_R4_R9_R3_TRACKED_STATUS_UNCHANGED=PASS", flush=True)
    print("PHASE171_R2J_R4_R9_R3_REPORT=" + str(destination), flush=True)
    print("PHASE171_R2J_R4_R9_R3_RESULT=PASS_AUDIT_ONLY", flush=True)


if __name__ == "__main__":
    main()
```

## `tests/test_audit.py`

```python
"""Focused fail-closed checks for the R9-R3 read-only Hopf frontier audit."""
from __future__ import annotations

from dataclasses import replace

import pytest

from homotopy_groups import TodaHopfInvariantMap, TodaPrimaryGroup
from phase165_r14_r6_generic_iso import MapSurjective
from phase171_r2j_r4_r9_r3_hopf_frontier_diagnostic.audit import (
    _failure_class,
    _git,
    _hopf_goal,
    _proof_event,
    _unique_hopf_node,
    inspect_first_hopf_frontier,
)
from proof import InferenceRule, ProofRule, ProofStep


def _fixture():
    given = ProofStep("source", (), ProofRule.GIVEN)
    goal = _hopf_goal()
    inferred = ProofStep(
        goal, (given,), ProofRule.INFERENCE,
        inference_rule=InferenceRule(name="synthetic h"),
    )
    return given, inferred


def test_hopf_goal_has_exact_ehp_map_types():
    goal = _hopf_goal()
    assert goal == MapSurjective(TodaHopfInvariantMap(
        TodaPrimaryGroup(7, 3), TodaPrimaryGroup(7, 5),
    ))


def test_original_hopf_node_requires_genuine_inference():
    _, root = _fixture()
    assert _unique_hopf_node(root, _hopf_goal()) is root
    with pytest.raises(RuntimeError):
        _unique_hopf_node(replace(root, rule=ProofRule.GIVEN, premises=()), _hopf_goal())


def test_wrong_hopf_dimension_rejected():
    _, root = _fixture()
    wrong = MapSurjective(TodaHopfInvariantMap(
        TodaPrimaryGroup(7, 4), TodaPrimaryGroup(7, 7),
    ))
    with pytest.raises(RuntimeError):
        _unique_hopf_node(root, wrong)


def test_proof_event_preserves_actual_rule_kind():
    given, root = _fixture()
    result = _proof_event("proved", root.conclusion, root)
    assert result["proof_rule"] == "inference"
    assert result["inference_rule"] == "synthetic h"
    leaf = _proof_event("proved", given.conclusion, given)
    assert leaf["proof_rule"] == "given"
    assert _proof_event("unresolved", root.conclusion, None)["proof_rule"] is None


def test_proof_event_rejects_forged_observation():
    with pytest.raises(ValueError):
        _proof_event("proved", "goal", None)
    with pytest.raises(TypeError):
        _proof_event("unresolved", "goal", object())
    with pytest.raises(ValueError):
        _proof_event("verified", "goal", None)


def test_failure_class_distinguishes_premises_and_matcher():
    assert _failure_class(True, []) == "HOPF_REPLAYED"
    assert _failure_class(False, []) == "HOPF_PREMISES_NOT_ALL_RECONSTRUCTED"
    assert _failure_class(False, [{"matches": 0}]) == "HOPF_MATCHER_REJECTED_RECONSTRUCTED_PREMISES"
    assert _failure_class(False, [{"matches": 1}]) == "HOPF_MATCHED_BUT_ROOT_NOT_ADMITTED"


def test_readonly_git_commands_only():
    with pytest.raises(ValueError):
        _git("reset", "--hard")


def test_live_diagnostic_preserves_trust_boundary():
    report = inspect_first_hopf_frontier()
    assert report["original_inference_rule_count"] >= 2
    assert report["hopf_scoped_routes"] == 1
    assert report["new_given_added"] == 0
    assert report["production_modified"] is False
    assert report["public_web_verified"] is False
    assert report["hopf_failure_class"] in (
        "HOPF_REPLAYED",
        "HOPF_PREMISES_NOT_ALL_RECONSTRUCTED",
        "HOPF_MATCHER_REJECTED_RECONSTRUCTED_PREMISES",
        "HOPF_MATCHED_BUT_ROOT_NOT_ADMITTED",
    )
```

## `run.ps1`

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Package = $PSScriptRoot
$Repo = (Resolve-Path (Join-Path $Package '..')).Path
Push-Location $Repo
try {
    if (-not (Test-Path '.git')) { throw 'Run R9-R3 at the Git repository root.' }
    python -B -m phase171_r2j_r4_r9_r3_hopf_frontier_diagnostic.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R9-R3 preflight failed' }
    if ($DryRun) {
        Write-Host 'PHASE171_R2J_R4_R9_R3_RESULT=PASS_DRY_RUN'
        return
    }
    python -B -m pytest -q -p no:cacheprovider `
        '.\phase171_r2j_r4_r9_r3_hopf_frontier_diagnostic\tests\test_audit.py' `
        '.\phase171_r2j_r4_r9_r2_scoped_search_bridge\tests\test_audit.py'
    if ($LASTEXITCODE -ne 0) { throw 'R9-R3 focused pytest failed' }
    Write-Host 'PHASE171_R2J_R4_R9_R3_FOCUSED_PYTEST=PASS'
    python -B -m phase171_r2j_r4_r9_r3_hopf_frontier_diagnostic.audit
    if ($LASTEXITCODE -ne 0) { throw 'R9-R3 Hopf frontier diagnostic failed' }
} finally {
    Pop-Location
}
```

## `__init__.py`

```python
"""Scoped Hopf-frontier diagnosis (read-only Phase 171 R2J-R4-R9-R3)."""
```

## `tests/__init__.py`

```python
"""Phase 171 R2J-R4-R9-R3 focused tests."""
```

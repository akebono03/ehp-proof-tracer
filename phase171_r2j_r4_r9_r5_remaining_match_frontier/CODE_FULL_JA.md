# 変更対象・コード全文


- 新規: `phase171_r2j_r4_r9_r5_remaining_match_frontier/audit.py`（import と全関数）

- 新規: `phase171_r2j_r4_r9_r5_remaining_match_frontier/tests/test_audit.py`（import と全テスト関数）

- 新規: `run.ps1`、`README.md`、`監査仕様.md`、`__init__.py` と `tests/__init__.py`

- 既存ファイルの変更なし。


## `README.md`

```markdown

# EHP Proof Tracer — Phase 171 R2J-R4-R9-R5

This read-only, focused diagnostic identifies the next canonical backward-search frontier after R9-R4 has independently re-derived the surjectivity of the Hopf map from the source-bound Proposition 5.3 group premise.

## Scope

This package adds only its own files. It does not change the shared inference provider, the proof search engine, the trust boundary, the Web renderer, or any preexisting test. The validated R4-R8 proof is inspected solely for its inference rules and target subgoals. The canonical search engine independently reconstructs its ProofSteps from earlier screened sources. A matcher probe records the first genuine failure, distinguishing mismatched conclusions, mismatched ProofRule status, and rejection despite apparently matching premises. This observation does not prove the ultimate root.

## Requirements

Run in a `develop` worktree after the successful R9-R4 replay, with all prior Phase 171 audit modules available. The reviewed GitHub baseline is `58416a7da55a4d97bce161625cef98f673612118`.

## Commands

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2j_r4_r9_r5_remaining_match_frontier\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2j_r4_r9_r5_remaining_match_frontier\run.ps1"
git status -sb
git diff --stat
```

Only eight new and eight related focused tests are run. The complete pytest suite is reserved for Phase closeout. The report is written to `output/audit.json` under this package and contains the first rejected matcher attempt, its full typed premises, the canonical unresolved goal, and all selected observations. It does not promote an incomplete search to complete or claim that the public Web is verified.

```



## `__init__.py`

```python

"""Phase 171 R2J-R4-R9-R5: read-only remaining matcher frontier."""

```



## `audit.py`

```python

"""Trace the first remaining canonical matcher failure after bound Hopf repair.

The audit rebuilds R4-R8's inference rule graph and uses R9-R4's existing
SourceBoundGoal provider. No completed ProofStep is handed to the search, and
no GIVEN or public route is added. All matcher attempts are observations.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
from unittest.mock import patch

import phase165_r3_recursive_search as search_engine
from phase165_r52_r9_shared_math import shared_expansion_provider
from phase168_r3_41p13_trust_boundary import (
    UnverifiedProofTree,
    verify_proof_tree_for_narrative,
)
from phase171_r2i_eta_hopf_bridge.audit import _screened_context
from phase171_r2j_r4_r8_cyclic_structure.audit import build_cyclic_pi63_proof
from phase171_r2j_r4_r9_r2_scoped_search_bridge.source import (
    inference_expansion_catalog,
    walk_proof_ancestry,
)
from phase171_r2j_r4_r9_r4_source_bound_hopf.audit import hopf_goal
from phase171_r2j_r4_r9_r4_source_bound_hopf.source import source_bound_hopf_provider
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
        raise ValueError("read-only Git commands only")
    return subprocess.run(
        ["git", *arguments], cwd=ROOT,
        check=True, capture_output=True, text=True,
    ).stdout.strip()


def _classify_match_attempt(record: dict) -> str:
    """Explain a genuine zero-match event without claiming its cause as fact."""
    if record["matches"]:
        return "MATCH_ACCEPTED"
    if record["actual_conclusions"] != record["expected_conclusions"]:
        return "PREMISE_CONCLUSION_MISMATCH"
    if record["actual_proof_rules"] != record["expected_proof_rules"]:
        return "PREMISE_PROOF_RULE_MISMATCH"
    return "MATCHER_PATTERN_OR_GUARD_REJECTION"


def _proof_event(kind: str, goal: object, step: ProofStep | None) -> dict:
    if kind not in ("proved", "unresolved"):
        raise ValueError("unknown canonical search event")
    if kind == "proved" and not isinstance(step, ProofStep):
        raise TypeError("proved event requires ProofStep")
    return {
        "kind": kind,
        "goal_type": type(goal).__name__,
        "goal": repr(goal)[:1100],
        "proof_rule": step.rule.value if step is not None else None,
    }


def inspect_remaining_match_frontier() -> dict:
    """Observe canonical reconstruction with the existing, local R9-R4 repair."""
    screened, target, citing = _screened_context()
    root, _, previous = build_cyclic_pi63_proof()
    if (
        root.rule is not ProofRule.INFERENCE
        or root.conclusion != target
        or previous["new_given_added"] != 0
    ):
        raise RuntimeError("validated inferred R4-R8 group root is required")
    catalog = inference_expansion_catalog(root)
    nodes = walk_proof_ancestry(root)
    rule_nodes = {id(step.inference_rule): step for step in nodes
                  if step.rule is ProofRule.INFERENCE}
    ordinary = shared_expansion_provider(screened, proof_target=target)
    provider, bound, source_id = source_bound_hopf_provider(
        root, screened, citing, hopf_goal(), ordinary,
    )
    original_matcher = search_engine.find_inference_matches_for_rule
    attempts: list[dict] = []
    events: list[dict] = []

    def observe(kind: str, goal: object, step: ProofStep | None) -> None:
        if len(events) < 600:
            events.append(_proof_event(kind, goal, step))

    def trace(rule, premises):
        matches = original_matcher(rule, premises)
        original = rule_nodes.get(id(rule))
        if original is not None and len(attempts) < 300:
            expected = original.premises
            item = {
                "conclusion": repr(original.conclusion)[:1100],
                "conclusion_type": type(original.conclusion).__name__,
                "inference_rule": rule.name,
                "matches": len(matches),
                "actual_proof_rules": [step.rule.value for step in premises],
                "expected_proof_rules": [step.rule.value for step in expected],
                "actual_conclusions": [repr(step.conclusion)[:1100] for step in premises],
                "expected_conclusions": [repr(step.conclusion)[:1100] for step in expected],
            }
            item["classification"] = _classify_match_attempt(item)
            attempts.append(item)
        return matches

    result = None
    failure = None
    with patch.object(search_engine, "find_inference_matches_for_rule", side_effect=trace):
        try:
            result = search_engine.reconstruct_registered_goal(
                target, screened, citing, provider,
                lookup_mode="typed_reference_publication",
                progress_observer=observe,
            )
        except search_engine.RegisteredGoalUnresolved as exc:
            failure = str(exc)
    complete = bool(result is not None and result.rule is ProofRule.INFERENCE
                    and result.conclusion == target)
    if result is not None and not complete:
        raise RuntimeError("unexpected completed canonical root")
    accepted = False
    trust_result = None
    if complete:
        from phase165_r52_partial_proof import ProofSearchStatus, make_partial_proof_result
        proof_result = make_partial_proof_result(
            n=3, k=3, status=ProofSearchStatus.COMPLETE,
            proven_steps=walk_proof_ancestry(result), conclusion=target,
        )
        try:
            trust_result = verify_proof_tree_for_narrative(
                proof_result, screened, citing_assertion_id=citing,
            )
            accepted = True
        except UnverifiedProofTree as exc:
            trust_result = str(exc)
    rejected = [record for record in attempts if record["matches"] == 0]
    unresolved = [row for row in events if row["kind"] == "unresolved"]
    hopf_rebuilt = any(row["kind"] == "proved" and row["goal"] == repr(hopf_goal())[:1100]
                       and row["proof_rule"] == ProofRule.INFERENCE.value for row in events)
    if not hopf_rebuilt:
        raise RuntimeError("R9-R4 Hopf repair regressed during frontier replay")
    first = rejected[0] if rejected else None
    classification = (
        first["classification"] if first is not None else
        "UNRESOLVED_SUBGOAL_BEFORE_MATCH" if unresolved else
        "RECONSTRUCTED" if complete else "NO_MATCHER_FAILURE_RECORDED"
    )
    return {
        "phase": "171-R2J-R4-R9-R5",
        "mode": "AUDIT_ONLY_REMAINING_MATCHER_FRONTIER",
        "head_target": repr(target),
        "source_bound_assertion_id": source_id,
        "source_bound_conclusion": repr(bound.conclusion),
        "inferred_rule_catalog": len(catalog),
        "hopf_surjectivity_rebuilt": hopf_rebuilt,
        "canonical_search_status": "complete" if complete else "partial",
        "canonical_error": failure,
        "matcher_attempts": len(attempts),
        "rejected_matcher_attempts": len(rejected),
        "first_rejection_class": classification,
        "first_rejected_match": first,
        "first_unresolved_goal": unresolved[0] if unresolved else None,
        "unresolved_goals": unresolved[:30],
        "rejected_matches": rejected[:25],
        "all_match_attempts": attempts[:70],
        "trust_boundary_accepted": accepted,
        "trust_boundary_result": trust_result,
        "new_given_added": 0,
        "public_provider_modified": False,
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
        raise RuntimeError("R9-R5 requires develop")
    for name in (
        "phase171_r2j_r4_r9_r4_source_bound_hopf/source.py",
        "phase171_r2j_r4_r8_cyclic_structure/audit.py",
    ):
        if not (ROOT / name).is_file():
            raise RuntimeError("missing prerequisite: " + name)
    print("PHASE171_R2J_R4_R9_R5_BRANCH=" + branch, flush=True)
    print("PHASE171_R2J_R4_R9_R5_HEAD=" + head, flush=True)
    if args.dry_run:
        print("PHASE171_R2J_R4_R9_R5_RESULT=PASS_DRY_RUN", flush=True)
        return
    report = inspect_remaining_match_frontier()
    if _git("status", "--porcelain", "--untracked-files=no") != tracked_before:
        raise RuntimeError("tracked files modified during read-only R9-R5 audit")
    report.update({"git_head": head, "tracked_status_unchanged": True})
    OUTPUT.mkdir(parents=True, exist_ok=True)
    path = OUTPUT / "audit.json"
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE171_R2J_R4_R9_R5_HOPF_REBUILT=" + str(report["hopf_surjectivity_rebuilt"]), flush=True)
    print("PHASE171_R2J_R4_R9_R5_MATCH_ATTEMPTS=" + str(report["matcher_attempts"]), flush=True)
    print("PHASE171_R2J_R4_R9_R5_REJECTED=" + str(report["rejected_matcher_attempts"]), flush=True)
    print("PHASE171_R2J_R4_R9_R5_FRONTIER=" + report["first_rejection_class"], flush=True)
    if report["first_rejected_match"] is not None:
        print("PHASE171_R2J_R4_R9_R5_FIRST_RULE=" + report["first_rejected_match"]["inference_rule"], flush=True)
    elif report["first_unresolved_goal"] is not None:
        print("PHASE171_R2J_R4_R9_R5_FIRST_GOAL=" + report["first_unresolved_goal"]["goal_type"], flush=True)
    print("PHASE171_R2J_R4_R9_R5_SCOPED_SEARCH=" + report["canonical_search_status"], flush=True)
    print("PHASE171_R2J_R4_R9_R5_TRUST_VERIFIED=" + str(report["trust_boundary_accepted"]), flush=True)
    print("PHASE171_R2J_R4_R9_R5_NEW_GIVEN=0", flush=True)
    print("PHASE171_R2J_R4_R9_R5_PUBLIC_WEB_VERIFIED=False", flush=True)
    print("PHASE171_R2J_R4_R9_R5_TRACKED_STATUS_UNCHANGED=PASS", flush=True)
    print("PHASE171_R2J_R4_R9_R5_REPORT=" + str(path), flush=True)
    print("PHASE171_R2J_R4_R9_R5_RESULT=PASS_AUDIT_ONLY", flush=True)


if __name__ == "__main__":
    main()

```



## `run.ps1`

```powershell

param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Package = $PSScriptRoot
$Repo = (Resolve-Path (Join-Path $Package '..')).Path
Push-Location $Repo
try {
    if (-not (Test-Path '.git')) { throw 'Run from the EHP Git repository root' }
    python -B -m phase171_r2j_r4_r9_r5_remaining_match_frontier.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R9-R5 preflight failed' }
    if ($DryRun) {
        Write-Host 'PHASE171_R2J_R4_R9_R5_RESULT=PASS_DRY_RUN'
        return
    }
    python -B -m pytest -q -p no:cacheprovider `
        '.\phase171_r2j_r4_r9_r5_remaining_match_frontier\tests\test_audit.py' `
        '.\phase171_r2j_r4_r9_r4_source_bound_hopf\tests\test_audit.py'
    if ($LASTEXITCODE -ne 0) { throw 'R9-R5 focused pytest failed' }
    Write-Host 'PHASE171_R2J_R4_R9_R5_FOCUSED_PYTEST=PASS'
    python -B -m phase171_r2j_r4_r9_r5_remaining_match_frontier.audit
    if ($LASTEXITCODE -ne 0) { throw 'R9-R5 remaining frontier replay failed' }
} finally {
    Pop-Location
}

```



## `tests/__init__.py`

```python

"""Focused R9-R5 tests."""

```



## `tests/test_audit.py`

```python

"""Focused diagnostic classifications and genuine R9-R4 replay."""
from __future__ import annotations

import pytest

from phase171_r2j_r4_r9_r5_remaining_match_frontier.audit import (
    _classify_match_attempt,
    _git,
    _proof_event,
    inspect_remaining_match_frontier,
)
from proof import ProofRule, ProofStep


def _record(matches=0, expected=None, actual=None, expected_conclusions=None,
            actual_conclusions=None):
    return {
        "matches": matches,
        "expected_proof_rules": ["inference"] if expected is None else expected,
        "actual_proof_rules": ["given"] if actual is None else actual,
        "expected_conclusions": ["same"] if expected_conclusions is None else expected_conclusions,
        "actual_conclusions": ["same"] if actual_conclusions is None else actual_conclusions,
    }


def test_reports_proof_rule_mismatch_when_conclusions_are_equal():
    assert _classify_match_attempt(_record()) == "PREMISE_PROOF_RULE_MISMATCH"


def test_reports_distinct_conclusions_before_any_proof_status_diagnosis():
    assert _classify_match_attempt(_record(
        expected_conclusions=["x"], actual_conclusions=["y"],
    )) == "PREMISE_CONCLUSION_MISMATCH"


def test_same_premise_types_and_results_mean_guard_or_pattern_rejection():
    assert _classify_match_attempt(_record(
        expected=["inference"], actual=["inference"],
    )) == "MATCHER_PATTERN_OR_GUARD_REJECTION"


def test_accepted_match_is_never_classified_as_failure():
    assert _classify_match_attempt(_record(matches=1)) == "MATCH_ACCEPTED"


def test_search_events_reject_fabricated_proved_event():
    with pytest.raises(TypeError):
        _proof_event("proved", "goal", None)
    with pytest.raises(ValueError):
        _proof_event("invalid", "goal", None)


def test_search_event_records_real_inference_not_new_given():
    step = ProofStep("group", (), ProofRule.INFERENCE)
    actual = _proof_event("proved", "group", step)
    assert actual["proof_rule"] == "inference"
    assert actual["kind"] == "proved"
    unresolved = _proof_event("unresolved", "missing", None)
    assert unresolved["proof_rule"] is None


def test_read_only_git_allowlist_rejects_mutation():
    with pytest.raises(ValueError):
        _git("reset", "--hard")


def test_live_scoped_replay_preserves_hopf_repair_and_source_boundary():
    report = inspect_remaining_match_frontier()
    assert report["hopf_surjectivity_rebuilt"] is True
    assert report["inferred_rule_catalog"] >= 3
    assert report["new_given_added"] == 0
    assert report["public_provider_modified"] is False
    assert report["public_web_verified"] is False
    assert report["canonical_search_status"] in ("complete", "partial")
    if report["trust_boundary_accepted"]:
        assert report["canonical_search_status"] == "complete"

```



## `監査仕様.md`

```markdown

# Phase 171 R2J-R4-R9-R5 監査仕様

## 目的

R4-R9-R4 では Proposition 5.3 を `SourceBoundGoal`（出典拘束付き証明目標）とし、Hopf 全射性を共通探索から再導出できた。ただし $\pi_6^3\cong\mathbb Z/4\{\nu'\}$ の共通探索は `partial` である。最初の残余停止点を推測による本番修正なしで特定する。

## 変更対象と配置

リポジトリ直下の新規 `phase171_r2j_r4_r9_r5_remaining_match_frontier/` のみを追加する。`audit.py` に `_git`、`_classify_match_attempt`、`_proof_event`、`inspect_remaining_match_frontier`、`main` を追加する。`tests/test_audit.py` に補助関数 `_record` と8件の限定テストを追加する。既存 import、関数、クラス、テストは変更しない。

## 監査方法

R4-R8 の実際の証明木から `InferenceRule` と型付き前提の集合を読み取り、R4-R9-R4 の局所 Provider で独立して `reconstruct_registered_goal` を実行する。探索器の `find_inference_matches_for_rule` を観測し、元の演繹に対応する規則の照合結果を記録する。既存の完成済み `ProofStep` を入力として探索器に注入しない。元の探索器の照合関数をそのまま呼び出し、結果は変更しない。

照合結果0件を `PREMISE_CONCLUSION_MISMATCH`、`PREMISE_PROOF_RULE_MISMATCH`、`MATCHER_PATTERN_OR_GUARD_REJECTION` に分類する。未解決の前提目標と、報告された最初の拒否を JSON に記録する。この分類は診断であり、原因の数学的証明を意味しない。

## 検証と境界

`run.ps1 -DryRun` ではブランチと前提ファイルのみ検査する。実行時は新規8件と R4-R9-R4 既存8件の限定 pytest を実行する。全体 pytest は実行しない。出力は新規フォルダの `output/audit.json` のみ。Git の追跡対象は変更しない。新規 `GIVEN` は0であり、Web 完成証明は未認定とする。

次の段階では記録された**最初の残余停止点**に限定して修正方針を決める。将来の全体 Provider 接続や Renderer 変更は本段階では行わない。

```



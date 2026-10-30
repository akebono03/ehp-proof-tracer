# Phase 171 R2J-R4-R9-R4 — 新規コード全文

既存ファイルの変更はありません。新規コードの各 import 部分と関数・テスト全文を省略せず収録します。

## `source.py`

```python
"""Scope one Hopf codomain to its earlier cited general source.

Do not change the Hopf rule, accept an adopted DB leaf as a replacement for
its inferred group premise, or insert previously completed proof steps.
"""
from __future__ import annotations

from homotopy_groups import FiniteCyclicGroup, TodaHopfInvariantMap
from phase165_r14_r6_generic_iso import MapSurjective
from phase165_r3_recursive_search import GoalExpansion, SourceBoundGoal
from phase166_r3c_publication_order import precedes_citing_assertion
from phase171_r2j_r4_r9_r2_scoped_search_bridge.source import (
    scoped_expansion_provider,
    walk_proof_ancestry,
)
from proof import ProofRule, ProofStep, Relation, RelationType
from unified_statement_registry import AssertionOrigin


def source_bound_hopf_provider(root: ProofStep, screened, citing: str,
                               hopf_goal: MapSurjective, fallback_provider):
    """Require cited *inference* for a Hopf codomain without altering other goals.

    `SourceBoundGoal` changes only the group's proof-search obligation.  The
    existing recursive engine then has to specialize the cited general theorem,
    instead of returning an independently eligible DB prior as a GIVEN.
    """
    if not (
        isinstance(hopf_goal, MapSurjective)
        and isinstance(hopf_goal.map, TodaHopfInvariantMap)
        and isinstance(citing, str)
        and citing
    ):
        raise ValueError("a typed Hopf surjectivity goal and citing ID are required")
    original = tuple(
        step for step in walk_proof_ancestry(root)
        if type(step.conclusion) is type(hopf_goal) and step.conclusion == hopf_goal
    )
    if len(original) != 1 or original[0].rule is not ProofRule.INFERENCE:
        raise ValueError("expected one inferred Hopf surjectivity ancestor")
    hopf = original[0]
    if len(hopf.premises) != 2 or hopf.inference_rule is None:
        raise ValueError("Hopf rule does not have two inferred antecedents")
    group_step, image_step = hopf.premises
    if not (
        group_step.rule is ProofRule.INFERENCE
        and image_step.rule is ProofRule.INFERENCE
        and len(group_step.premises) == 1
        and group_step.inference_rule is not None
        and isinstance(group_step.conclusion, Relation)
        and group_step.conclusion.relation_type is RelationType.EQUALITY
        and group_step.conclusion.lhs == hopf_goal.map.target_group
        and isinstance(group_step.conclusion.rhs, FiniteCyclicGroup)
        and group_step.premises[0].rule is ProofRule.GIVEN
        and not group_step.premises[0].premises
    ):
        raise ValueError("a cited, inferred cyclic codomain is required")
    source = group_step.premises[0].conclusion
    matching_links = []
    for link in screened.proof_links:
        step = link.step
        assertion = screened.registry.assertion(link.assertion_id)
        reference = screened.registry.reference(assertion.reference_id)
        if (
            isinstance(step, ProofStep)
            and step.rule is ProofRule.GIVEN
            and not step.premises
            and type(step.conclusion) is type(source)
            and step.conclusion == source
            and step.conclusion == assertion.content
            and assertion.origin is AssertionOrigin.FIXED_STATEMENT
            and reference.locator == "Proposition 5.3"
            and precedes_citing_assertion(screened, link.assertion_id, citing)
        ):
            matching_links.append(link)
    if len(matching_links) != 1:
        raise ValueError("Hopf codomain lacks a unique preceding Proposition 5.3 source")

    bound = SourceBoundGoal(group_step.conclusion, source)
    ordinary_scoped = scoped_expansion_provider(root, fallback_provider)
    original_proposal = ordinary_scoped(hopf_goal)
    expected_subgoals = (group_step.conclusion, image_step.conclusion)
    if (
        len(original_proposal) != 1
        or original_proposal[0].rule is not hopf.inference_rule
        or original_proposal[0].subgoals != expected_subgoals
        or len(ordinary_scoped(group_step.conclusion)) != 1
        or ordinary_scoped(group_step.conclusion)[0].subgoals != (source,)
    ):
        raise ValueError("original R4-R8 Hopf derivation is not source-boundable")

    def expand(goal: object) -> tuple[GoalExpansion, ...]:
        if type(goal) is type(hopf_goal) and goal == hopf_goal:
            return (GoalExpansion(hopf.inference_rule, (bound, image_step.conclusion)),)
        return ordinary_scoped(goal)

    return expand, bound, matching_links[0].assertion_id
```

## `audit.py`

```python
"""R2J-R4-R9-R4: source-bound Hopf replay through canonical backward search.

Audit only; no production provider changes. A DB-admitted cyclic group cannot
replace the inference from the screened Proposition 5.3 in this Hopf rule.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess

from homotopy_groups import TodaHopfInvariantMap, TodaPrimaryGroup
from phase165_r14_r6_generic_iso import MapSurjective
from phase165_r3_recursive_search import (
    RegisteredGoalUnresolved,
    reconstruct_registered_goal,
)
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r2_search_adapter import search_registered_partial_proof
from phase165_r52_r9_shared_math import shared_expansion_provider
from phase168_r3_41p13_trust_boundary import (
    UnverifiedProofTree,
    verify_proof_tree_for_narrative,
)
from phase171_r2i_eta_hopf_bridge.audit import _screened_context
from phase171_r2j_r4_r8_cyclic_structure.audit import build_cyclic_pi63_proof
from phase171_r2j_r4_r9_r4_source_bound_hopf.source import source_bound_hopf_provider
from proof import ProofRule

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = Path(__file__).resolve().parent / "output"


def _git(*arguments: str) -> str:
    if arguments not in {
        ("branch", "--show-current"),
        ("rev-parse", "HEAD"),
        ("status", "--porcelain", "--untracked-files=no"),
    }:
        raise ValueError("read-only Git commands only")
    return subprocess.run(
        ["git", *arguments], cwd=ROOT, text=True,
        capture_output=True, check=True,
    ).stdout.strip()


def hopf_goal() -> MapSurjective:
    return MapSurjective(TodaHopfInvariantMap(
        TodaPrimaryGroup(7, 3), TodaPrimaryGroup(7, 5),
    ))


def build_source_bound_context():
    screened, target, citing = _screened_context()
    original, _, original_report = build_cyclic_pi63_proof()
    if (
        original.rule is not ProofRule.INFERENCE
        or original.conclusion != target
        or original_report["new_given_added"] != 0
    ):
        raise RuntimeError("validated R4-R8 proof is required")
    fallback = shared_expansion_provider(screened, proof_target=target)
    provider, bound, source_id = source_bound_hopf_provider(
        original, screened, citing, hopf_goal(), fallback,
    )
    return screened, target, citing, provider, bound, source_id



def previous_hopf_match_evidence() -> dict:
    """Read the existing R9-R3 observation without accepting it as proof."""
    path = ROOT / "phase171_r2j_r4_r9_r3_hopf_frontier_diagnostic" / "output" / "audit.json"
    if not path.is_file():
        return {"available": False, "input_proof_rules": [], "expected_proof_rules": []}
    row = json.loads(path.read_text(encoding="utf-8"))
    attempts = row.get("hopf_match_attempts", [])
    if row.get("hopf_failure_class") != "HOPF_MATCHER_REJECTED_RECONSTRUCTED_PREMISES" or len(attempts) != 1:
        return {"available": False, "input_proof_rules": [], "expected_proof_rules": []}
    attempt = attempts[0]
    return {
        "available": True,
        "input_proof_rules": attempt.get("input_proof_rules", []),
        "expected_proof_rules": attempt.get("expected_proof_rules", []),
        "database_given_hypothesis_supported": (
            attempt.get("input_proof_rules") == ["given", "inference"]
            and attempt.get("expected_proof_rules") == ["inference", "inference"]
        ),
    }

def audit_source_bound_search() -> dict:
    """Reconstruct the H subgoal first; then observe the full scoped search."""
    screened, target, citing, provider, bound, source_id = build_source_bound_context()
    group = reconstruct_registered_goal(
        bound, screened, citing, provider,
        lookup_mode="typed_reference_publication",
    )
    if (
        group.rule is not ProofRule.INFERENCE
        or group.conclusion != bound.conclusion
        or len(group.premises) != 1
        or group.premises[0].rule is not ProofRule.GIVEN
        or group.premises[0].conclusion != bound.source
    ):
        raise RuntimeError("source-bounded cyclic group was not independently derived")
    hopf = reconstruct_registered_goal(
        hopf_goal(), screened, citing, provider,
        lookup_mode="typed_reference_publication",
    )
    if (
        hopf.rule is not ProofRule.INFERENCE
        or hopf.conclusion != hopf_goal()
        or len(hopf.premises) != 2
        or any(x.rule is not ProofRule.INFERENCE for x in hopf.premises)
        or hopf.premises[0].conclusion != bound.conclusion
    ):
        raise RuntimeError("source-bound Hopf surjectivity was not independently inferred")

    result = search_registered_partial_proof(
        n=3, k=3, goal=target, bridge=screened,
        citing_assertion_id=citing, expansion_provider=provider,
        lookup_mode="typed_reference_publication",
    )
    complete = (
        result.status is ProofSearchStatus.COMPLETE
        and result.conclusion == target
        and not result.open_goals
    )
    verified = False
    verification = None
    if complete:
        try:
            verification = verify_proof_tree_for_narrative(
                result, screened, citing_assertion_id=citing,
            )
            verified = True
        except UnverifiedProofTree as exc:
            verification = str(exc)
    return {
        "phase": "171-R2J-R4-R9-R4",
        "mode": "AUDIT_ONLY_SOURCE_BOUND_HOPF",
        "hopf_source_assertion_id": source_id,
        "previous_hopf_match_evidence": previous_hopf_match_evidence(),
        "bound_group_inferred": True,
        "hopf_surjective_inferred": True,
        "hopf_premise_rules": [x.rule.value for x in hopf.premises],
        "scoped_search_status": result.status.value,
        "scoped_search_complete": complete,
        "scoped_proven_steps": len(result.proven_steps),
        "scoped_open_goals": [repr(x)[:1200] for x in result.open_goals[:20]],
        "scoped_diagnostics": list(result.diagnostics[:15]),
        "trust_boundary_accepted": verified,
        "trust_boundary_result": verification,
        "public_provider_modified": False,
        "public_web_verified": False,
        "new_given_added": 0,
        "full_pytest": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    branch = _git("branch", "--show-current")
    head = _git("rev-parse", "HEAD")
    before = _git("status", "--porcelain", "--untracked-files=no")
    if branch != "develop":
        raise RuntimeError("R9-R4 requires develop")
    for path in (
        "phase171_r2j_r4_r8_cyclic_structure/audit.py",
        "phase171_r2j_r4_r9_r2_scoped_search_bridge/source.py",
        "phase171_r2j_r4_r9_r3_hopf_frontier_diagnostic/audit.py",
    ):
        if not (ROOT / path).is_file():
            raise RuntimeError("missing R9 prerequisite: " + path)
    print("PHASE171_R2J_R4_R9_R4_BRANCH=" + branch, flush=True)
    print("PHASE171_R2J_R4_R9_R4_HEAD=" + head, flush=True)
    if args.dry_run:
        print("PHASE171_R2J_R4_R9_R4_RESULT=PASS_DRY_RUN", flush=True)
        return
    report = audit_source_bound_search()
    if _git("status", "--porcelain", "--untracked-files=no") != before:
        raise RuntimeError("tracked files changed during source-bound audit")
    report.update({"git_head": head, "tracked_status_unchanged": True})
    OUTPUT.mkdir(parents=True, exist_ok=True)
    target = OUTPUT / "audit.json"
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE171_R2J_R4_R9_R4_BOUND_GROUP=INFERRED", flush=True)
    print("PHASE171_R2J_R4_R9_R4_HOPF_SURJECTIVE=INFERRED", flush=True)
    print("PHASE171_R2J_R4_R9_R4_SCOPED_SEARCH=" + report["scoped_search_status"], flush=True)
    print("PHASE171_R2J_R4_R9_R4_TRUST_VERIFIED=" + str(report["trust_boundary_accepted"]), flush=True)
    print("PHASE171_R2J_R4_R9_R4_NEW_GIVEN=0", flush=True)
    print("PHASE171_R2J_R4_R9_R4_PUBLIC_WEB_VERIFIED=False", flush=True)
    print("PHASE171_R2J_R4_R9_R4_TRACKED_STATUS_UNCHANGED=PASS", flush=True)
    print("PHASE171_R2J_R4_R9_R4_REPORT=" + str(target), flush=True)
    print("PHASE171_R2J_R4_R9_R4_RESULT=PASS_AUDIT_ONLY", flush=True)


if __name__ == "__main__":
    main()
```

## `tests/test_audit.py`

```python
"""R9-R4: source-bound Hopf goal without bypassing the matcher or DB order."""
from __future__ import annotations

from dataclasses import replace
from types import SimpleNamespace

import pytest

from phase165_r3_recursive_search import (
    RegisteredGoalUnresolved,
    SourceBoundGoal,
    reconstruct_registered_goal,
)
from phase171_r2j_r4_r9_r4_source_bound_hopf.audit import (
    _git,
    audit_source_bound_search,
    build_source_bound_context,
    hopf_goal,
    previous_hopf_match_evidence,
)
from phase171_r2j_r4_r9_r4_source_bound_hopf.source import source_bound_hopf_provider
from phase171_r2j_r4_r8_cyclic_structure.audit import build_cyclic_pi63_proof
from phase171_r2i_eta_hopf_bridge.audit import _screened_context
from proof import ProofRule


@pytest.fixture(scope="module")
def context():
    return build_source_bound_context()


def test_hopf_goal_is_unique_and_bound_to_original_group(context):
    _, _, _, provider, bound, source_id = context
    assert isinstance(bound, SourceBoundGoal)
    assert "Proposition 5.3" in source_id
    proposals = provider(hopf_goal())
    assert len(proposals) == 1
    assert proposals[0].subgoals[0] == bound
    assert proposals[0].subgoals[1] != bound


def test_cited_codomain_is_inferred_instead_of_database_given(context):
    screened, _, citing, provider, bound, _ = context
    result = reconstruct_registered_goal(
        bound, screened, citing, provider,
        lookup_mode="typed_reference_publication",
    )
    assert result.rule is ProofRule.INFERENCE
    assert result.conclusion == bound.conclusion
    assert len(result.premises) == 1
    assert result.premises[0].rule is ProofRule.GIVEN
    assert result.premises[0].conclusion == bound.source


def test_canonical_hopf_rule_reconstructs_two_inferences(context):
    screened, _, citing, provider, bound, _ = context
    result = reconstruct_registered_goal(
        hopf_goal(), screened, citing, provider,
        lookup_mode="typed_reference_publication",
    )
    assert result.rule is ProofRule.INFERENCE
    assert result.conclusion == hopf_goal()
    assert len(result.premises) == 2
    assert all(parent.rule is ProofRule.INFERENCE for parent in result.premises)
    assert result.premises[0].conclusion == bound.conclusion


def test_fake_source_bound_is_unprovable(context):
    screened, _, citing, provider, bound, _ = context
    with pytest.raises(RegisteredGoalUnresolved):
        reconstruct_registered_goal(
            SourceBoundGoal(bound.conclusion, "not a cited theorem"),
            screened, citing, provider,
            lookup_mode="typed_reference_publication",
        )


def test_wrong_hopf_target_is_not_rewritten(context):
    _, _, _, provider, _, _ = context
    wrong = replace(hopf_goal(), map=replace(
        hopf_goal().map,
        target_group=hopf_goal().map.source_group,
    ))
    assert provider(wrong) != provider(hopf_goal())


def test_missing_screened_group_source_is_rejected(context):
    screened, _, citing, _, _, _ = context
    root, _, _ = build_cyclic_pi63_proof()
    empty = SimpleNamespace(proof_links=(), registry=screened.registry)
    with pytest.raises(ValueError, match="Proposition 5.3"):
        source_bound_hopf_provider(root, empty, citing, hopf_goal(), lambda goal: ())


def test_read_only_git_commands_only():
    with pytest.raises(ValueError):
        _git("reset", "--hard")


def test_live_audit_keeps_public_boundary_unchanged():
    report = audit_source_bound_search()
    assert report["bound_group_inferred"] is True
    assert isinstance(report["previous_hopf_match_evidence"]["available"], bool)
    assert report["hopf_surjective_inferred"] is True
    assert report["hopf_premise_rules"] == ["inference", "inference"]
    assert report["new_given_added"] == 0
    assert report["public_provider_modified"] is False
    assert report["public_web_verified"] is False
    if report["trust_boundary_accepted"]:
        assert report["scoped_search_complete"] is True
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
    python -B -m phase171_r2j_r4_r9_r4_source_bound_hopf.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R9-R4 preflight failed' }
    if ($DryRun) {
        Write-Host 'PHASE171_R2J_R4_R9_R4_RESULT=PASS_DRY_RUN'
        return
    }
    python -B -m pytest -q -p no:cacheprovider `
        '.\phase171_r2j_r4_r9_r4_source_bound_hopf\tests\test_audit.py' `
        '.\phase171_r2j_r4_r9_r3_hopf_frontier_diagnostic\tests\test_audit.py'
    if ($LASTEXITCODE -ne 0) { throw 'R9-R4 focused pytest failed' }
    Write-Host 'PHASE171_R2J_R4_R9_R4_FOCUSED_PYTEST=PASS'
    python -B -m phase171_r2j_r4_r9_r4_source_bound_hopf.audit
    if ($LASTEXITCODE -ne 0) { throw 'R9-R4 source-bound replay failed' }
} finally {
    Pop-Location
}
```

## `__init__.py`

```python
"""Phase 171 R2J-R4-R9-R4 source-bound Hopf audit."""
```

## `tests/__init__.py`

```python
"""R9-R4 focused tests."""
```

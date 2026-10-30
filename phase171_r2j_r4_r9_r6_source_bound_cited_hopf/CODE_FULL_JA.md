# Phase 171 R2J-R4-R9-R6 — 変更ファイル・コード全文

変更対象は新規 `phase171_r2j_r4_r9_r6_source_bound_cited_hopf/` のみ。既存ファイル・既存 import・既存クラス・既存メソッドは一切変更しない。

追加する `source.py` の `bind_cited_hopf_codomain()` は新規モジュールの import 直後に置く。`audit.py` の `_git()`、`build_second_bound_context()`、`audit_second_source_bound_hopf()`、`main()` は、この順で新規モジュールに追加する。テスト関数は `tests/test_audit.py` の各 import と fixture 定義の後に追加する。

コード内に省略はない。

## `__init__.py` 全文

```python
"""Audit-only second Hopf source binding for Phase 171."""
```

## `source.py` 全文

```python
"""Bind a second cited Hopf codomain to its earlier general source.

Only typed proof *obligations* are changed in this scoped adapter. Neither
previously proved steps nor new GIVEN leaves are supplied to search.
"""
from __future__ import annotations

from homotopy_groups import FiniteCyclicGroup, TodaHopfInvariantMap
from phase165_r14_r6_generic_iso import MapSurjective
from phase165_r3_recursive_search import GoalExpansion, SourceBoundGoal
from phase166_r3c_publication_order import precedes_citing_assertion
from phase171_r2j_r2_cyclic_hopf_surjective.source import _valid_surjective_pair
from phase171_r2j_r4_r9_r2_scoped_search_bridge.source import walk_proof_ancestry
from proof import ProofRule, ProofStep, Relation, RelationType
from unified_statement_registry import AssertionOrigin


def bind_cited_hopf_codomain(
    root: ProofStep, screened, citing: str, provider,
    *, expected_locator: str,
) -> tuple[object, SourceBoundGoal, str, MapSurjective]:
    """Require an INFERENCE cyclic group from one cited preceding fixed source.

    Match the genuine two-premise Hopf ancestry whose second premise is a
    literature GIVEN.  Reconstruct only its cyclic codomain from the exact
    source.  The existing surjectivity InferenceRule and its guard stay intact.
    """
    if (
        not isinstance(root, ProofStep)
        or root.rule is not ProofRule.INFERENCE
        or not callable(provider)
        or not isinstance(citing, str)
        or not citing
        or not isinstance(expected_locator, str)
        or not expected_locator
    ):
        raise ValueError("valid inferred root, provider, citation and locator required")
    candidates = []
    for step in walk_proof_ancestry(root):
        if not (
            step.rule is ProofRule.INFERENCE
            and isinstance(step.conclusion, MapSurjective)
            and isinstance(step.conclusion.map, TodaHopfInvariantMap)
            and step.inference_rule is not None
            and len(step.premises) == 2
        ):
            continue
        group_step, image_step = step.premises
        if not (
            group_step.rule is ProofRule.INFERENCE
            and len(group_step.premises) == 1
            and group_step.inference_rule is not None
            and group_step.premises[0].rule is ProofRule.GIVEN
            and not group_step.premises[0].premises
            and image_step.rule is ProofRule.GIVEN
            and not image_step.premises
            and isinstance(group_step.conclusion, Relation)
            and group_step.conclusion.relation_type is RelationType.EQUALITY
            and isinstance(group_step.conclusion.rhs, FiniteCyclicGroup)
            and group_step.conclusion.lhs == step.conclusion.map.target_group
            and isinstance(image_step.conclusion, Relation)
            and _valid_surjective_pair(
                step.conclusion, group_step.conclusion, image_step.conclusion,
            )
        ):
            continue
        candidates.append(step)
    if len(candidates) != 1:
        raise ValueError("one inferred cyclic-codomain/cited-image Hopf ancestor required")
    hopf = candidates[0]
    group_step, image_step = hopf.premises
    source = group_step.premises[0].conclusion
    eligible = []
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
            and assertion.content == step.conclusion
            and assertion.origin is AssertionOrigin.FIXED_STATEMENT
            and reference.locator == expected_locator
            and precedes_citing_assertion(screened, link.assertion_id, citing)
        ):
            eligible.append(link)
    if len(eligible) != 1:
        raise ValueError("unique screened preceding source of cited Hopf codomain required")
    group_route = provider(group_step.conclusion)
    hopf_route = provider(hopf.conclusion)
    if (
        len(group_route) != 1
        or group_route[0].rule is not group_step.inference_rule
        or group_route[0].subgoals != (source,)
        or len(hopf_route) != 1
        or hopf_route[0].rule is not hopf.inference_rule
        or hopf_route[0].subgoals != (
            group_step.conclusion, image_step.conclusion,
        )
    ):
        raise ValueError("original scoped inferred route is not source-bindable")
    bound = SourceBoundGoal(group_step.conclusion, source)

    def expand(goal: object) -> tuple[GoalExpansion, ...]:
        if type(goal) is type(hopf.conclusion) and goal == hopf.conclusion:
            return (GoalExpansion(
                hopf.inference_rule,
                (bound, image_step.conclusion),
            ),)
        return provider(goal)

    return expand, bound, eligible[0].assertion_id, hopf.conclusion
```

## `audit.py` 全文

```python
"""Audit-only second Hopf reconstruction and remaining scoped search.

Preserve the first R9-R4 source-bound Hopf branch, while proving the second
H-surjectivity branch with an INFERENCE codomain, not a DB GIVEN.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess

from phase165_r3_recursive_search import reconstruct_registered_goal
from phase165_r52_r9_shared_math import shared_expansion_provider
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r2_search_adapter import search_registered_partial_proof
from phase168_r3_41p13_trust_boundary import (
    UnverifiedProofTree,
    verify_proof_tree_for_narrative,
)
from phase171_r2i_eta_hopf_bridge.audit import _screened_context
from phase171_r2j_r4_r8_cyclic_structure.audit import build_cyclic_pi63_proof
from phase171_r2j_r4_r9_r4_source_bound_hopf.audit import (
    hopf_goal as first_hopf_goal,
)
from phase171_r2j_r4_r9_r4_source_bound_hopf.source import source_bound_hopf_provider
from phase171_r2j_r4_r9_r6_source_bound_cited_hopf.source import (
    bind_cited_hopf_codomain,
)
from proof import ProofRule

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = Path(__file__).resolve().parent / "output"


def _git(*arguments: str) -> str:
    permitted = {
        ("branch", "--show-current"),
        ("rev-parse", "HEAD"),
        ("status", "--porcelain", "--untracked-files=no"),
    }
    if arguments not in permitted:
        raise ValueError("read-only Git operations only")
    return subprocess.run(
        ["git", *arguments], cwd=ROOT, check=True,
        text=True, capture_output=True,
    ).stdout.strip()


def build_second_bound_context():
    """Keep R9-R4's bound H and source-screen the other cited H branch."""
    screened, target, citing = _screened_context()
    root, _, report = build_cyclic_pi63_proof()
    if (
        root.rule is not ProofRule.INFERENCE
        or root.conclusion != target
        or report["new_given_added"] != 0
    ):
        raise RuntimeError("genuine R4-R8 inferred root required")
    fallback = shared_expansion_provider(screened, proof_target=target)
    previous, _, first_source_id = source_bound_hopf_provider(
        root, screened, citing, first_hopf_goal(), fallback,
    )
    provider, bound, second_source_id, second_hopf = bind_cited_hopf_codomain(
        root, screened, citing, previous,
        expected_locator="Proposition 5.1",
    )
    if (
        second_hopf == first_hopf_goal()
        or second_source_id == first_source_id
    ):
        raise RuntimeError("second Hopf branch must be distinct from first")
    return screened, target, citing, provider, bound, second_source_id, second_hopf


def audit_second_source_bound_hopf() -> dict:
    screened, target, citing, provider, bound, source_id, second_hopf = (
        build_second_bound_context()
    )
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
        raise RuntimeError("cited codomain not independently inferred")
    hopf = reconstruct_registered_goal(
        second_hopf, screened, citing, provider,
        lookup_mode="typed_reference_publication",
    )
    if (
        hopf.rule is not ProofRule.INFERENCE
        or hopf.conclusion != second_hopf
        or len(hopf.premises) != 2
        or tuple(x.rule for x in hopf.premises)
        != (ProofRule.INFERENCE, ProofRule.GIVEN)
        or hopf.premises[0].conclusion != bound.conclusion
    ):
        raise RuntimeError("second Hopf surjectivity was not re-derived")
    earlier_hopf = reconstruct_registered_goal(
        first_hopf_goal(), screened, citing, provider,
        lookup_mode="typed_reference_publication",
    )
    if (
        earlier_hopf.rule is not ProofRule.INFERENCE
        or any(item.rule is not ProofRule.INFERENCE
               for item in earlier_hopf.premises)
    ):
        raise RuntimeError("first source-bound Hopf branch regressed")
    result = search_registered_partial_proof(
        n=3, k=3, goal=target, bridge=screened,
        citing_assertion_id=citing,
        expansion_provider=provider,
        lookup_mode="typed_reference_publication",
    )
    complete = (
        result.status is ProofSearchStatus.COMPLETE
        and result.conclusion == target
        and not result.open_goals
    )
    accepted = False
    trust_result = None
    if complete:
        try:
            trust_result = verify_proof_tree_for_narrative(
                result, screened, citing_assertion_id=citing,
            )
            accepted = True
        except UnverifiedProofTree as error:
            trust_result = str(error)
    return {
        "phase": "171-R2J-R4-R9-R6",
        "mode": "AUDIT_ONLY_SOURCE_BOUND_SECOND_CITED_HOPF",
        "source_assertion_id": source_id,
        "source_locator": "Proposition 5.1",
        "bound_group": repr(bound.conclusion),
        "second_hopf": repr(second_hopf),
        "bound_group_inferred": True,
        "second_hopf_surjective_inferred": True,
        "second_hopf_premise_rules": [s.rule.value for s in hopf.premises],
        "first_hopf_preserved": True,
        "scoped_search_status": result.status.value,
        "scoped_search_complete": complete,
        "scoped_proven_steps": len(result.proven_steps),
        "scoped_open_goals": [repr(item)[:1200] for item in result.open_goals[:20]],
        "first_unresolved_goal": (
            repr(result.open_goals[0])[:1200] if result.open_goals else None
        ),
        "scoped_diagnostics": list(result.diagnostics[:20]),
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
    before = _git("status", "--porcelain", "--untracked-files=no")
    if branch != "develop":
        raise RuntimeError("R9-R6 requires develop")
    for relative in (
        "phase171_r2j_r4_r9_r4_source_bound_hopf/source.py",
        "phase171_r2j_r4_r9_r5_remaining_match_frontier/audit.py",
        "phase171_r2j_r4_r8_cyclic_structure/audit.py",
    ):
        if not (ROOT / relative).is_file():
            raise RuntimeError("missing prior phase dependency: " + relative)
    print("PHASE171_R2J_R4_R9_R6_BRANCH=" + branch, flush=True)
    print("PHASE171_R2J_R4_R9_R6_HEAD=" + head, flush=True)
    if args.dry_run:
        print("PHASE171_R2J_R4_R9_R6_RESULT=PASS_DRY_RUN", flush=True)
        return
    report = audit_second_source_bound_hopf()
    if _git("status", "--porcelain", "--untracked-files=no") != before:
        raise RuntimeError("tracked files modified during R9-R6 audit")
    report.update({"git_head": head, "tracked_status_unchanged": True})
    OUTPUT.mkdir(exist_ok=True)
    destination = OUTPUT / "audit.json"
    destination.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    print("PHASE171_R2J_R4_R9_R6_BOUND_GROUP=INFERRED", flush=True)
    print("PHASE171_R2J_R4_R9_R6_SECOND_HOPF=INFERRED", flush=True)
    print("PHASE171_R2J_R4_R9_R6_FIRST_HOPF_PRESERVED=PASS", flush=True)
    print("PHASE171_R2J_R4_R9_R6_SCOPED_SEARCH=" + report["scoped_search_status"], flush=True)
    if report["first_unresolved_goal"] is not None:
        print("PHASE171_R2J_R4_R9_R6_FIRST_OPEN_GOAL=" + report["first_unresolved_goal"], flush=True)
    print("PHASE171_R2J_R4_R9_R6_TRUST_VERIFIED=" + str(report["trust_boundary_accepted"]), flush=True)
    print("PHASE171_R2J_R4_R9_R6_NEW_GIVEN=0", flush=True)
    print("PHASE171_R2J_R4_R9_R6_PUBLIC_WEB_VERIFIED=False", flush=True)
    print("PHASE171_R2J_R4_R9_R6_TRACKED_STATUS_UNCHANGED=PASS", flush=True)
    print("PHASE171_R2J_R4_R9_R6_REPORT=" + str(destination), flush=True)
    print("PHASE171_R2J_R4_R9_R6_RESULT=PASS_AUDIT_ONLY", flush=True)


if __name__ == "__main__":
    main()
```

## `tests/__init__.py` 全文

```python
"""Focused R9-R6 tests."""
```

## `tests/test_audit.py` 全文

```python
"""Focused proof-rule and source-bound checks for the second cited Hopf map."""
from __future__ import annotations

from types import SimpleNamespace
from dataclasses import replace

import pytest

from phase165_r3_recursive_search import (
    RegisteredGoalUnresolved,
    SourceBoundGoal,
    reconstruct_registered_goal,
)
from phase171_r2j_r4_r8_cyclic_structure.audit import build_cyclic_pi63_proof
from phase171_r2j_r4_r9_r4_source_bound_hopf.audit import hopf_goal as first_hopf_goal
from phase171_r2j_r4_r9_r6_source_bound_cited_hopf.audit import (
    _git,
    audit_second_source_bound_hopf,
    build_second_bound_context,
)
from phase171_r2j_r4_r9_r6_source_bound_cited_hopf.source import bind_cited_hopf_codomain
from proof import ProofRule


@pytest.fixture(scope="module")
def context():
    return build_second_bound_context()


def test_second_hopf_has_one_source_bound_inferred_codomain(context):
    _, _, _, provider, bound, source_id, hopf = context
    assert isinstance(bound, SourceBoundGoal)
    assert isinstance(source_id, str) and source_id
    assert hopf != first_hopf_goal()
    options = provider(hopf)
    assert len(options) == 1
    assert options[0].subgoals[0] == bound
    assert options[0].subgoals[1] != bound


def test_reconstructs_codomain_as_inference_from_one_screened_source(context):
    screened, _, citing, provider, bound, _, _ = context
    step = reconstruct_registered_goal(
        bound, screened, citing, provider,
        lookup_mode="typed_reference_publication",
    )
    assert step.rule is ProofRule.INFERENCE
    assert step.conclusion == bound.conclusion
    assert len(step.premises) == 1
    assert step.premises[0].rule is ProofRule.GIVEN
    assert step.premises[0].conclusion == bound.source


def test_second_hopf_reconstructs_inference_given_pair(context):
    screened, _, citing, provider, bound, _, hopf = context
    step = reconstruct_registered_goal(
        hopf, screened, citing, provider,
        lookup_mode="typed_reference_publication",
    )
    assert step.rule is ProofRule.INFERENCE
    assert step.conclusion == hopf
    assert [item.rule for item in step.premises] == [ProofRule.INFERENCE, ProofRule.GIVEN]
    assert step.premises[0].conclusion == bound.conclusion


def test_first_hopf_remains_two_inferences(context):
    screened, _, citing, provider, _, _, _ = context
    step = reconstruct_registered_goal(
        first_hopf_goal(), screened, citing, provider,
        lookup_mode="typed_reference_publication",
    )
    assert step.rule is ProofRule.INFERENCE
    assert len(step.premises) == 2
    assert all(item.rule is ProofRule.INFERENCE for item in step.premises)


def test_forged_source_cannot_prove_bound_group(context):
    screened, _, citing, provider, bound, _, _ = context
    with pytest.raises(RegisteredGoalUnresolved):
        reconstruct_registered_goal(
            SourceBoundGoal(bound.conclusion, "invented source"),
            screened, citing, provider,
            lookup_mode="typed_reference_publication",
        )


def test_missing_earlier_screened_source_fails_closed(context):
    screened, _, citing, provider, _, _, _ = context
    root, _, _ = build_cyclic_pi63_proof()
    fake = SimpleNamespace(proof_links=(), registry=screened.registry)
    with pytest.raises(ValueError, match="unique screened"):
        bind_cited_hopf_codomain(
            root, fake, citing, provider,
            expected_locator="Proposition 5.1",
        )


def test_mismatched_locator_fails_closed(context):
    screened, _, citing, provider, _, _, _ = context
    root, _, _ = build_cyclic_pi63_proof()
    with pytest.raises(ValueError, match="unique screened"):
        bind_cited_hopf_codomain(
            root, screened, citing, provider,
            expected_locator="unrelated source",
        )


def test_other_hopf_goal_is_not_rewritten(context):
    _, _, _, provider, _, _, second_hopf = context
    wrong = replace(second_hopf, map=replace(
        second_hopf.map, target_group=second_hopf.map.source_group,
    ))
    assert provider(wrong) != provider(second_hopf)


def test_git_guard_blocks_writes():
    with pytest.raises(ValueError):
        _git("reset", "--hard")


def test_live_audit_has_two_genuine_inferred_hopf_goals():
    report = audit_second_source_bound_hopf()
    assert report["bound_group_inferred"] is True
    assert report["second_hopf_surjective_inferred"] is True
    assert report["first_hopf_preserved"] is True
    assert report["second_hopf_premise_rules"] == ["inference", "given"]
    assert report["new_given_added"] == 0
    assert report["public_provider_modified"] is False
    assert report["public_web_verified"] is False
    assert report["scoped_search_status"] in ("complete", "partial", "search_failed")
    if report["trust_boundary_accepted"]:
        assert report["scoped_search_complete"] is True
```

## `run.ps1` 全文

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Repo
try {
    if (-not (Test-Path '.git')) { throw 'EHP Git root required' }
    python -B -m phase171_r2j_r4_r9_r6_source_bound_cited_hopf.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R9-R6 preflight failed' }
    if ($DryRun) {
        Write-Host 'PHASE171_R2J_R4_R9_R6_RESULT=PASS_DRY_RUN'
        return
    }
    python -B -m pytest -q -p no:cacheprovider `
        '.\phase171_r2j_r4_r9_r6_source_bound_cited_hopf\tests\test_audit.py' `
        '.\phase171_r2j_r4_r9_r4_source_bound_hopf\tests\test_audit.py'
    if ($LASTEXITCODE -ne 0) { throw 'R9-R6 focused pytest failed' }
    Write-Host 'PHASE171_R2J_R4_R9_R6_FOCUSED_PYTEST=PASS'
    python -B -m phase171_r2j_r4_r9_r6_source_bound_cited_hopf.audit
    if ($LASTEXITCODE -ne 0) { throw 'R9-R6 replay failed' }
} finally {
    Pop-Location
}
```

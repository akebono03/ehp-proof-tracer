# Phase 171 R2J-R4-R5 — コード全文（R4-R5-R1 テスト修正適用済み）

変更対象は新規ディレクトリ `phase171_r2j_r4_r5_short_exact_sequence/` のみです。既存 API と R2J-R3・R4-R4 の既存テストは変更しません。R4-R5 のテスト1関数のみ修正します。

下記は現在の R4-R5 パッケージの全ファイルを省略せず掲載したものです。今回変更する関数は `tests/test_audit.py` の `test_unrelated_sequence_is_rejected_and_reordered_premises_are_matched()` だけで、追加位置は旧関数の位置です。import の変更はありません。

## `source.py`

```python
"""Typed short-exact consequence of EHP exactness, E injective and H surjective.

This module contains no source assertions, completed group presentations,
or claims about the order or generator of the middle group.
"""
from __future__ import annotations

from dataclasses import dataclass

from homotopy_groups import (
    TodaEHPExactnessWindow,
    TodaHopfInvariantMap,
    TodaPrimaryGroup,
    TodaSuspensionMap,
)
from map_facts import EHP_E_MAP, EHP_H_MAP
from phase165_r12_r11_prop42_unified import prop42_exactness_indices
from phase165_r14_r6_generic_iso import MapInjective, MapSurjective
from phase165_r3_recursive_search import GoalExpansion
from proof import InferenceRule, PremisePattern, ProofRule
from toda_rules import TodaProp42ExactnessStatement


@dataclass(frozen=True)
class EHPShortExactSequence:
    """The five-term sequence 0 -> source -> middle -> target -> 0."""

    source_group: TodaPrimaryGroup
    middle_group: TodaPrimaryGroup
    target_group: TodaPrimaryGroup
    injection: TodaSuspensionMap
    projection: TodaHopfInvariantMap


def short_exact_from_ehp(
    injection: object,
    exactness: object,
    projection: object,
) -> EHPShortExactSequence | None:
    """Validate all three well-typed, compatible mathematical premises.

    Matching names is not enough: the specialized EHP window must be valid,
    and both map endpoints must agree with all three group objects.
    """
    if (
        not isinstance(injection, MapInjective)
        or not isinstance(exactness, TodaProp42ExactnessStatement)
        or not isinstance(projection, MapSurjective)
        or not isinstance(exactness.window, TodaEHPExactnessWindow)
    ):
        return None
    window = exactness.window
    if (
        prop42_exactness_indices(exactness) is None
        or prop42_exactness_indices(exactness)[2] != "e_h"
        or (window.first_map, window.second_map) != (EHP_E_MAP, EHP_H_MAP)
        or not all(isinstance(group, TodaPrimaryGroup) for group in (
            window.source_term,
            window.middle_term,
            window.target_term,
        ))
    ):
        return None
    required_injection = TodaSuspensionMap(window.source_term, window.middle_term)
    required_projection = TodaHopfInvariantMap(window.middle_term, window.target_term)
    if injection.map != required_injection or projection.map != required_projection:
        return None
    return EHPShortExactSequence(
        source_group=window.source_term,
        middle_group=window.middle_term,
        target_group=window.target_term,
        injection=required_injection,
        projection=required_projection,
    )


def ehp_short_exact_rule(goal: EHPShortExactSequence) -> InferenceRule:
    """Deduce 0 -> A -> B -> C -> 0 from three independently inferred facts."""
    if not isinstance(goal, EHPShortExactSequence):
        raise TypeError("typed EHPShortExactSequence goal required")

    def guard(premises, bindings):
        return (
            len(premises) == 3
            and all(step.rule is ProofRule.INFERENCE for step in premises)
            and short_exact_from_ehp(
                premises[0].conclusion,
                premises[1].conclusion,
                premises[2].conclusion,
            ) == goal
        )

    return InferenceRule(
        name="EHP exactness with injective E and surjective H implies short exact sequence",
        premise_patterns=(
            PremisePattern(proof_rule=ProofRule.INFERENCE, statement_type=MapInjective),
            PremisePattern(
                proof_rule=ProofRule.INFERENCE,
                statement_type=TodaProp42ExactnessStatement,
            ),
            PremisePattern(proof_rule=ProofRule.INFERENCE, statement_type=MapSurjective),
        ),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def expand_ehp_short_exact(
    goal: object,
) -> tuple[GoalExpansion, ...]:
    """Backward obligations only; no source leaf or assumed group structure."""
    if not isinstance(goal, EHPShortExactSequence):
        return ()
    window = TodaEHPExactnessWindow(
        source_term=goal.source_group,
        middle_term=goal.middle_group,
        target_term=goal.target_group,
        first_map=EHP_E_MAP,
        second_map=EHP_H_MAP,
    )
    premises = (
        MapInjective(goal.injection),
        TodaProp42ExactnessStatement(window),
        MapSurjective(goal.projection),
    )
    if short_exact_from_ehp(*premises) != goal:
        return ()
    return (GoalExpansion(ehp_short_exact_rule(goal), premises),)
```

## `audit.py`

```python
"""Read-only replay: infer a short exact EHP sequence from cited proof trees.

R2J-R3 supplies inferred E injectivity; R4-R4 supplies inferred H
surjectivity; Proposition 4.2 supplies inferred E-H exactness. No completed
pi_6^3 group relation or DB group candidate is an admitted proof premise.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess

from phase164_r8_proofstep_factory import derive_inference_proof_step
from phase165_r12_r11_prop42_unified import (
    TodaProp42GeneralExactnessStatement,
    expand_cited_prop42_exactness,
    prop42_exactness_indices,
)
from phase165_r3_recursive_search import reconstruct_registered_goal
from phase165_r52_r9_shared_math import shared_expansion_provider
from phase166_r3c_publication_order import precedes_citing_assertion
from phase171_r2i_eta_hopf_bridge.audit import _screened_context
from phase171_r2j_r3_ehp_exactness.audit import build_r2j_r3_proof
from phase171_r2j_r4_r1_extension_frontier_audit.audit import _extension_window
from phase171_r2j_r4_r2_generator_image_replay.audit import proof_ancestry
from phase171_r2j_r4_r4_cited_hopf_surjectivity.audit import (
    build_cited_hopf_surjectivity_proof,
)
from phase171_r2j_r4_r5_short_exact_sequence.source import (
    ehp_short_exact_rule,
    expand_ehp_short_exact,
    short_exact_from_ehp,
)
from proof import ProofRule, ProofStep, find_inference_matches_for_rule
from unified_statement_registry import AssertionOrigin

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = Path(__file__).resolve().parent / "output"


def _git(*arguments: str) -> str:
    if arguments not in {
        ("branch", "--show-current"),
        ("rev-parse", "HEAD"),
        ("status", "--porcelain", "--untracked-files=no"),
    }:
        raise ValueError("only read-only Git operations are allowed")
    return subprocess.run(
        ["git", *arguments],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _cited_prop42_source(screened, citing: str):
    """Pick the one earlier, actually linked universal EHP source."""
    found = []
    for link in screened.proof_links:
        step = link.step
        assertion = screened.registry.assertion(link.assertion_id)
        reference = screened.registry.reference(assertion.reference_id)
        if (
            isinstance(step, ProofStep)
            and step.rule is ProofRule.GIVEN
            and not step.premises
            and step.conclusion == assertion.content
            and type(step.conclusion) is TodaProp42GeneralExactnessStatement
            and assertion.origin is AssertionOrigin.FIXED_STATEMENT
            and reference.locator == "Proposition 4.2 (4.4)"
            and precedes_citing_assertion(screened, link.assertion_id, citing)
        ):
            found.append(link)
    if len(found) != 1:
        raise RuntimeError("expected one screened Proposition 4.2 universal source")
    return found[0]


def _screened_leaf_ids(screened, citing: str, leaves: tuple[ProofStep, ...]) -> tuple[str, ...]:
    """Reject uncited GIVEN roots, including a forged completed target group."""
    resolved: list[str] = []
    for leaf in leaves:
        if leaf.rule is not ProofRule.GIVEN or leaf.premises:
            raise RuntimeError("proof ancestry contains a non-leaf GIVEN")
        matching_ids = []
        for link in screened.proof_links:
            step = link.step
            assertion = screened.registry.assertion(link.assertion_id)
            if (
                isinstance(step, ProofStep)
                and step.rule is ProofRule.GIVEN
                and not step.premises
                and type(step.conclusion) is type(leaf.conclusion)
                and step.conclusion == leaf.conclusion
                and assertion.origin is AssertionOrigin.FIXED_STATEMENT
                and assertion.content == step.conclusion
                and precedes_citing_assertion(screened, link.assertion_id, citing)
            ):
                matching_ids.append(link.assertion_id)
        if len(matching_ids) != 1:
            raise RuntimeError("proof leaf lacks one unambiguous screened earlier source")
        resolved.append(matching_ids[0])
    return tuple(resolved)


def build_short_exact_proof() -> tuple[ProofStep, tuple[ProofStep, ...], dict]:
    """Reconstruct all dependencies, then apply one typed inference match."""
    screened, pi63_goal, citing = _screened_context()
    prop42_source = _cited_prop42_source(screened, citing)
    _, injection_root, _, _ = build_r2j_r3_proof()
    projection_root, _, _ = build_cited_hopf_surjectivity_proof()
    exactness_goal = _extension_window()
    if prop42_exactness_indices(exactness_goal) != (2, 6, "e_h"):
        raise RuntimeError("unexpected E-H exactness indices for pi_6^3")
    options = expand_cited_prop42_exactness(
        exactness_goal, (prop42_source.step.conclusion,),
    )
    if len(options) != 1 or options[0].subgoals != (prop42_source.step.conclusion,):
        raise RuntimeError("Proposition 4.2 specialized E-H window is unavailable")
    public_options = shared_expansion_provider(screened, proof_target=pi63_goal)(exactness_goal)
    if not any(
        item.rule.name == options[0].rule.name and item.subgoals == options[0].subgoals
        for item in public_options
    ):
        raise RuntimeError("E-H exactness rule is not connected to shared provider")

    def exactness_provider(current: object):
        return expand_cited_prop42_exactness(
            current, (prop42_source.step.conclusion,),
        )

    exactness_root = reconstruct_registered_goal(
        exactness_goal,
        screened,
        citing,
        exactness_provider,
        lookup_mode="typed_reference_publication",
    )
    if (
        exactness_root.rule is not ProofRule.INFERENCE
        or exactness_root.conclusion != exactness_goal
        or len(exactness_root.premises) != 1
        or exactness_root.premises[0] is not prop42_source.step
    ):
        raise RuntimeError("E-H exactness lacks the original source-backed proof")
    expected = short_exact_from_ehp(
        injection_root.conclusion,
        exactness_root.conclusion,
        projection_root.conclusion,
    )
    if expected is None:
        raise RuntimeError("E-injective, E-H exact, H-surjective premises do not match")
    proposals = expand_ehp_short_exact(expected)
    if len(proposals) != 1 or proposals[0].subgoals != (
        injection_root.conclusion,
        exactness_root.conclusion,
        projection_root.conclusion,
    ):
        raise RuntimeError("short-exact inference obligations are not unique")
    parents = (injection_root, exactness_root, projection_root)
    rule = ehp_short_exact_rule(expected)
    matches = tuple(
        match for match in find_inference_matches_for_rule(rule, parents)
        if len(match.premises) == 3
        and all(a is b for a, b in zip(match.premises, parents))
    )
    if len(matches) != 1:
        raise RuntimeError("no unique typed inference from three proved EHP premises")
    root = derive_inference_proof_step(matches[0])
    nodes = proof_ancestry(root)
    if (
        root.rule is not ProofRule.INFERENCE
        or root.conclusion != expected
        or root.premises != parents
        or any(node.conclusion == pi63_goal for node in nodes)
        or any(node.rule not in (ProofRule.GIVEN, ProofRule.INFERENCE) for node in nodes)
    ):
        raise RuntimeError("untrusted proof ancestry or completed group import")
    leaves = tuple(node for node in nodes if node.rule is ProofRule.GIVEN)
    leaf_ids = _screened_leaf_ids(screened, citing, leaves)
    if prop42_source.assertion_id not in leaf_ids:
        raise RuntimeError("Proposition 4.2 universal source absent from proof ancestry")
    report = {
        "phase": "171-R2J-R4-R5",
        "mode": "READ_ONLY_TYPED_SHORT_EXACT_REPLAY",
        "status": "INFERRED",
        "short_exact_sequence": repr(root.conclusion),
        "e_injective": repr(injection_root.conclusion),
        "e_h_exactness": repr(exactness_root.conclusion),
        "h_surjective": repr(projection_root.conclusion),
        "prop42_source_id": prop42_source.assertion_id,
        "verified_source_ids": list(dict.fromkeys(leaf_ids)),
        "inferences": sum(step.rule is ProofRule.INFERENCE for step in nodes),
        "given_leaves": len(leaves),
        "new_given_added": 0,
        "pi63_group_proven": False,
        "order_four_proven": False,
        "production_modified": False,
        "full_pytest": False,
    }
    return root, nodes, report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    arguments = parser.parse_args()
    branch = _git("branch", "--show-current")
    if branch != "develop":
        raise RuntimeError("R2J-R4-R5 requires the develop branch")
    head = _git("rev-parse", "HEAD")
    before = _git("status", "--porcelain", "--untracked-files=no")
    if not (
        ROOT / "phase171_r2j_r4_r4_cited_hopf_surjectivity" / "audit.py"
    ).is_file():
        raise RuntimeError("R4-R4 local audit must be retained in the worktree")
    print("PHASE171_R2J_R4_R5_BRANCH=" + branch, flush=True)
    print("PHASE171_R2J_R4_R5_HEAD=" + head, flush=True)
    if arguments.dry_run:
        print("PHASE171_R2J_R4_R5_RESULT=PASS_DRY_RUN", flush=True)
        return
    root, nodes, report = build_short_exact_proof()
    if _git("status", "--porcelain", "--untracked-files=no") != before:
        raise RuntimeError("tracked worktree changed during read-only proof replay")
    report.update({"git_head": head, "tracked_status_unchanged": True})
    OUTPUT.mkdir(exist_ok=True)
    path = OUTPUT / "audit.json"
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE171_R2J_R4_R5_SHORT_EXACT=" + report["status"], flush=True)
    print("PHASE171_R2J_R4_R5_INFERENCES=" + str(report["inferences"]), flush=True)
    print("PHASE171_R2J_R4_R5_GIVEN_LEAVES=" + str(report["given_leaves"]), flush=True)
    print("PHASE171_R2J_R4_R5_NEW_GIVEN=0", flush=True)
    print("PHASE171_R2J_R4_R5_ORDER_FOUR_PROVEN=False", flush=True)
    print("PHASE171_R2J_R4_R5_PI63_PROVEN=False", flush=True)
    print("PHASE171_R2J_R4_R5_TRACKED_STATUS_UNCHANGED=PASS", flush=True)
    print("PHASE171_R2J_R4_R5_REPORT=" + str(path), flush=True)
    print("PHASE171_R2J_R4_R5_RUN=PASS", flush=True)


if __name__ == "__main__":
    main()
```

## `tests/test_audit.py`

```python
"""Focused typed EHP short-exact rule and real provenance regression tests."""
from __future__ import annotations

from dataclasses import replace

import pytest

from homotopy_groups import (
    TodaEHPExactnessWindow,
    TodaHopfInvariantMap,
    TodaPrimaryGroup,
    TodaSuspensionMap,
)
from map_facts import EHP_DELTA_MAP, EHP_E_MAP, EHP_H_MAP
from phase164_r8_proofstep_factory import derive_inference_proof_step
from phase165_r12_r11_prop42_unified import prop42_exactness_indices
from phase165_r14_r6_generic_iso import MapInjective, MapSurjective
from phase171_r2j_r4_r5_short_exact_sequence.audit import (
    _cited_prop42_source,
    _git,
    build_short_exact_proof,
)
from phase171_r2j_r4_r5_short_exact_sequence.source import (
    EHPShortExactSequence,
    ehp_short_exact_rule,
    expand_ehp_short_exact,
    short_exact_from_ehp,
)
from phase171_r2i_eta_hopf_bridge.audit import _screened_context
from proof import ProofRule, ProofStep, find_inference_matches_for_rule
from toda_rules import TodaProp42ExactnessStatement


def _premises():
    a = TodaPrimaryGroup(5, 2)
    b = TodaPrimaryGroup(6, 3)
    c = TodaPrimaryGroup(6, 5)
    injection = MapInjective(TodaSuspensionMap(a, b))
    exact = TodaProp42ExactnessStatement(TodaEHPExactnessWindow(
        a, b, c, EHP_E_MAP, EHP_H_MAP,
    ))
    projection = MapSurjective(TodaHopfInvariantMap(b, c))
    return injection, exact, projection


def test_valid_ehp_window_and_maps_propose_one_short_exact_inference():
    inputs = _premises()
    assert prop42_exactness_indices(inputs[1]) == (2, 6, "e_h")
    goal = short_exact_from_ehp(*inputs)
    assert isinstance(goal, EHPShortExactSequence)
    assert goal.source_group == TodaPrimaryGroup(5, 2)
    assert goal.middle_group == TodaPrimaryGroup(6, 3)
    assert goal.target_group == TodaPrimaryGroup(6, 5)
    proposals = expand_ehp_short_exact(goal)
    assert len(proposals) == 1
    assert proposals[0].subgoals == inputs


def test_rule_produces_checked_inference_from_three_inferred_steps():
    inputs = _premises()
    goal = short_exact_from_ehp(*inputs)
    assert goal is not None
    rules = ehp_short_exact_rule(goal)
    premises = tuple(ProofStep(value, (), ProofRule.INFERENCE) for value in inputs)
    matches = find_inference_matches_for_rule(rules, premises)
    assert len(matches) == 1
    derived = derive_inference_proof_step(matches[0])
    assert derived.rule is ProofRule.INFERENCE
    assert derived.conclusion == goal
    assert derived.premises == premises


def test_given_exactness_or_map_properties_are_not_admitted_as_inference():
    inputs = _premises()
    goal = short_exact_from_ehp(*inputs)
    assert goal is not None
    rule = ehp_short_exact_rule(goal)
    for index in range(3):
        steps = tuple(ProofStep(
            statement, (), ProofRule.GIVEN if position == index else ProofRule.INFERENCE,
        ) for position, statement in enumerate(inputs))
        assert find_inference_matches_for_rule(rule, steps) == ()


def test_wrong_suspension_or_hopf_endpoints_fail_closed():
    injection, exact, projection = _premises()
    wrong_e = replace(injection, map=TodaSuspensionMap(
        TodaPrimaryGroup(5, 2), TodaPrimaryGroup(6, 4),
    ))
    wrong_h = replace(projection, map=TodaHopfInvariantMap(
        TodaPrimaryGroup(6, 4), TodaPrimaryGroup(6, 5),
    ))
    assert short_exact_from_ehp(wrong_e, exact, projection) is None
    assert short_exact_from_ehp(injection, exact, wrong_h) is None


def test_invalid_exactness_or_wrong_ehp_map_names_fail_closed():
    injection, exact, projection = _premises()
    wrong = replace(exact, window=replace(
        exact.window, first_map=EHP_DELTA_MAP,
    ))
    assert short_exact_from_ehp(injection, wrong, projection) is None
    bad_group = replace(exact, window=replace(
        exact.window, target_term=TodaPrimaryGroup(7, 5),
    ))
    assert short_exact_from_ehp(injection, bad_group, projection) is None
    assert short_exact_from_ehp(injection, exact, object()) is None


def test_unrelated_sequence_is_rejected_and_reordered_premises_are_matched():
    inputs = _premises()
    goal = short_exact_from_ehp(*inputs)
    assert goal is not None
    incorrect = replace(goal, middle_group=TodaPrimaryGroup(7, 3))
    assert expand_ehp_short_exact(incorrect) == ()

    rule = ehp_short_exact_rule(goal)
    steps = tuple(ProofStep(item, (), ProofRule.INFERENCE) for item in inputs)
    reordered = (steps[2], steps[1], steps[0])
    matches = find_inference_matches_for_rule(rule, reordered)
    assert len(matches) == 1
    assert matches[0].premises == steps
    result = derive_inference_proof_step(matches[0])
    assert result.rule is ProofRule.INFERENCE
    assert result.conclusion == goal
    assert result.premises == steps

    wrong_injection = ProofStep(
        MapInjective(TodaSuspensionMap(
            TodaPrimaryGroup(5, 2), TodaPrimaryGroup(6, 4),
        )),
        (),
        ProofRule.INFERENCE,
    )
    assert find_inference_matches_for_rule(
        rule, (steps[2], steps[1], wrong_injection),
    ) == ()
    assert expand_ehp_short_exact(object()) == ()


def test_real_proposition42_source_is_screened_and_unique():
    screened, _, citing = _screened_context()
    link = _cited_prop42_source(screened, citing)
    assert link.step.rule is ProofRule.GIVEN
    assert not link.step.premises
    assert link.assertion_id.endswith("adopted:assertion:prop42:general")


def test_read_only_git_guard():
    with pytest.raises(ValueError):
        _git("reset", "--hard")


def test_real_short_exact_proof_has_full_inferred_parentage():
    root, nodes, report = build_short_exact_proof()
    assert root.rule is ProofRule.INFERENCE
    assert len(root.premises) == 3
    assert all(parent.rule is ProofRule.INFERENCE for parent in root.premises)
    assert report["status"] == "INFERRED"
    assert report["new_given_added"] == 0
    assert report["order_four_proven"] is False
    assert report["pi63_group_proven"] is False
    assert report["given_leaves"] >= 3
    assert sum(node.rule is ProofRule.INFERENCE for node in nodes) >= 3
```

## `run.ps1`

```powershell
param([switch]$DryRun)
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Push-Location $Root
try {
    python -B -m phase171_r2j_r4_r5_short_exact_sequence.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw "R2J-R4-R5 preflight failed" }
    if ($DryRun) {
        Write-Output "PHASE171_R2J_R4_R5_RESULT=PASS_DRY_RUN"
        exit 0
    }
    python -B -m pytest -q -p no:cacheprovider `
        phase171_r2j_r4_r5_short_exact_sequence/tests/test_audit.py `
        phase171_r2j_r3_ehp_exactness/tests/test_r2j_r3_exactness.py `
        phase171_r2j_r4_r4_cited_hopf_surjectivity/tests/test_audit.py
    if ($LASTEXITCODE -ne 0) { throw "R2J-R4-R5 focused pytest failed" }
    Write-Output "PHASE171_R2J_R4_R5_FOCUSED_PYTEST=PASS"
    python -B -m phase171_r2j_r4_r5_short_exact_sequence.audit
    if ($LASTEXITCODE -ne 0) { throw "R2J-R4-R5 short exact proof replay failed" }
    Write-Output "PHASE171_R2J_R4_R5_RESULT=PASS_AUDIT_ONLY"
}
finally {
    Pop-Location
}
```

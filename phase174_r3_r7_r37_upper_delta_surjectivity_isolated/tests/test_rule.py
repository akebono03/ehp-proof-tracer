"""General upper-Delta mathematical rule tests; hypothetical INFERENCE steps are fixtures."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import GeneratorSymbol, HomotopyElement
from homotopy_groups import TodaDeltaMap, TodaPrimaryGroup
from phase165_r14_r6_generic_iso import MapInjective, MapSurjective
from phase174_r3_r7_r25_prop27_isolated_inference.rule import typed_specialization
from phase174_r3_r7_r37_upper_delta_surjectivity_isolated.rule import (
    RULE_NAME,
    expand_upper_delta_surjectivity,
    upper_delta_surjectivity_inputs,
    upper_delta_surjectivity_rule,
)
from proof import (
    InferenceRule,
    ProofRule,
    ProofStep,
    apply_inference_match,
    find_inference_matches_for_rule,
)


def _goal(n: int) -> MapSurjective:
    return MapSurjective(typed_specialization(n).delta)


def _hypothetical(statement: object) -> ProofStep:
    """A matcher fixture only, not a certified literature-derived proof."""
    return ProofStep(
        statement, (), ProofRule.INFERENCE,
        inference_rule=InferenceRule(name="hypothetical-test-only"),
    )


@pytest.mark.parametrize("n", (4, 6, 8, 10))
def test_general_even_ehp_indices_have_four_distinct_subgoals(n: int) -> None:
    goal = _goal(n)
    required = upper_delta_surjectivity_inputs(goal)
    assert required is not None
    assert len(required) == 4
    assert required[0] == MapInjective(typed_specialization(n).hopf)
    assert required[2].map.target_group == TodaPrimaryGroup(2 * n - 3, n - 1)
    assert required[2].multiple == 2
    assert required[2].source_generator.generator == GeneratorSymbol("ι", 2 * n - 1)
    assert required[3] == typed_specialization(n)
    proposals = expand_upper_delta_surjectivity(goal)
    assert len(proposals) == 1
    assert proposals[0].rule.name == RULE_NAME
    assert proposals[0].subgoals == required
    assert goal not in required


def test_n6_matches_actual_r34_lower_delta_kernel_and_hopf_maps() -> None:
    from phase174_r3_r7_r34_prior_lower_delta_source_wiring.source import (
        checked_prior_statements,
    )
    goal = _goal(6)
    prerequisites = upper_delta_surjectivity_inputs(goal)
    assert prerequisites is not None
    _, cited_image = checked_prior_statements()
    assert prerequisites[2].map == cited_image.map
    assert prerequisites[2].source_generator == cited_image.element
    assert prerequisites[1].window.middle_term == cited_image.map.source_group
    assert prerequisites[1].window.target_term == cited_image.map.target_group


def test_four_matching_inference_steps_form_one_inference_step() -> None:
    goal = _goal(6)
    required = upper_delta_surjectivity_inputs(goal)
    assert required is not None
    proofs = tuple(_hypothetical(item) for item in required)
    matches = find_inference_matches_for_rule(upper_delta_surjectivity_rule(goal), proofs)
    assert len(matches) == 1
    step = apply_inference_match(matches[0])
    assert step.rule is ProofRule.INFERENCE
    assert step.conclusion == goal
    assert step.premises == proofs


@pytest.mark.parametrize("missing", range(4))
def test_any_missing_mathematical_premise_blocks_rule(missing: int) -> None:
    goal = _goal(6)
    required = upper_delta_surjectivity_inputs(goal)
    assert required is not None
    proofs = tuple(_hypothetical(item) for i, item in enumerate(required) if i != missing)
    assert find_inference_matches_for_rule(upper_delta_surjectivity_rule(goal), proofs) == ()


@pytest.mark.parametrize("index", range(4))
def test_direct_given_cannot_replace_a_proved_premise(index: int) -> None:
    goal = _goal(6)
    required = upper_delta_surjectivity_inputs(goal)
    assert required is not None
    proofs = [_hypothetical(item) for item in required]
    proofs[index] = ProofStep(required[index], (), ProofRule.GIVEN)
    assert find_inference_matches_for_rule(
        upper_delta_surjectivity_rule(goal), tuple(proofs)
    ) == ()


def test_wrong_even_instance_and_wrong_order_are_rejected() -> None:
    goal = _goal(6)
    required = upper_delta_surjectivity_inputs(goal)
    assert required is not None
    proofs = tuple(_hypothetical(item) for item in required)
    wrong_hopf = list(proofs)
    wrong_hopf[0] = _hypothetical(upper_delta_surjectivity_inputs(_goal(4))[0])
    assert find_inference_matches_for_rule(
        upper_delta_surjectivity_rule(goal), tuple(wrong_hopf)
    ) == ()


def test_wrong_kernel_coefficient_or_iota_rejected() -> None:
    goal = _goal(6)
    required = upper_delta_surjectivity_inputs(goal)
    assert required is not None
    for bad_kernel in (
        replace(required[2], multiple=4),
        replace(required[2], source_generator=HomotopyElement(
            "other", 11, 11, 11, GeneratorSymbol("ι", 11)
        )),
    ):
        proofs = list(_hypothetical(item) for item in required)
        proofs[2] = _hypothetical(bad_kernel)
        assert find_inference_matches_for_rule(
            upper_delta_surjectivity_rule(goal), tuple(proofs)
        ) == ()


def test_forged_prop27_instance_rejected() -> None:
    goal = _goal(6)
    required = upper_delta_surjectivity_inputs(goal)
    assert required is not None
    proofs = list(_hypothetical(item) for item in required)
    proofs[3] = _hypothetical(replace(required[3], sign_undetermined=False))
    assert find_inference_matches_for_rule(
        upper_delta_surjectivity_rule(goal), tuple(proofs)
    ) == ()


@pytest.mark.parametrize("bad", (
    object(), "upper-delta", MapSurjective(object()),
    MapSurjective(TodaDeltaMap(TodaPrimaryGroup(13, 13), TodaPrimaryGroup(11, 5))),
    MapSurjective(TodaDeltaMap(TodaPrimaryGroup(11, 11), TodaPrimaryGroup(9, 5))),
    MapSurjective(TodaDeltaMap(TodaPrimaryGroup(9, 9), TodaPrimaryGroup(7, 5))),
))
def test_invalid_or_odd_upper_delta_goals_have_no_candidate(bad: object) -> None:
    assert upper_delta_surjectivity_inputs(bad) is None
    assert expand_upper_delta_surjectivity(bad) == ()


def test_no_real_proof_or_source_is_installed_by_expansion() -> None:
    proposals = expand_upper_delta_surjectivity(_goal(6))
    assert len(proposals) == 1
    assert all(not isinstance(p, ProofStep) for p in proposals[0].subgoals)
    assert proposals[0].rule.conclusion_pattern == _goal(6)

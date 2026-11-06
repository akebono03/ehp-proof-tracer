"""Focused general-mathematics checks for the isolated R18 inference."""
from __future__ import annotations

import pytest

from expression import GeneratorSymbol, HomotopyElement, Zero
from homotopy_groups import FreeCyclicGroup, TodaDeltaMap, TodaPrimaryGroup
from phase164_r8_proofstep_factory import derive_inference_proof_step
from phase165_r14_r6_generic_iso import MapSurjective
from phase174_r3_r7_r18_delta_image_surjectivity.rule import (
    RULE_NAME,
    delta_surjectivity_from_full_free_cyclic_image_rule,
    delta_surjectivity_image_inputs,
    expand_delta_surjectivity_from_full_free_cyclic_image,
)
from proof import (
    InferenceRule, ProofRule, ProofStep, Relation, RelationType,
    find_inference_matches_for_rule,
)
from toda_rules import TodaDeltaImageFreeCyclicStatement


def _fixture(q: int, n: int):
    delta = TodaDeltaMap(
        TodaPrimaryGroup(q + 2, 2 * n + 1),
        TodaPrimaryGroup(q, n),
    )
    generator = HomotopyElement(
        name="g", dimension=n, source=q, target=n,
        generator=GeneratorSymbol("g", n),
    )
    return (
        MapSurjective(delta),
        Relation(delta.target_group, FreeCyclicGroup(generator), RelationType.EQUALITY),
    )


def _inferred(statement: object) -> ProofStep:
    return ProofStep(
        conclusion=statement, premises=(), rule=ProofRule.INFERENCE,
        inference_rule=InferenceRule(name="test-only independent inferred fixture"),
    )


@pytest.mark.parametrize("q,n", ((11, 6), (9, 5), (13, 7), (17, 9)))
def test_general_delta_dimensions_without_named_stem(q: int, n: int) -> None:
    goal, group = _fixture(q, n)
    obligations = delta_surjectivity_image_inputs(goal, group)
    assert obligations is not None
    assert obligations[0] == group
    assert obligations[1] == TodaDeltaImageFreeCyclicStatement(
        goal.map, group.rhs,
    )
    proposals = expand_delta_surjectivity_from_full_free_cyclic_image(goal, group)
    assert len(proposals) == 1
    assert proposals[0].rule.name == RULE_NAME
    assert proposals[0].subgoals == obligations
    assert goal not in obligations


def test_only_two_matching_inferred_steps_can_prove_surjectivity() -> None:
    goal, group = _fixture(11, 6)
    obligations = delta_surjectivity_image_inputs(goal, group)
    assert obligations is not None
    rule = delta_surjectivity_from_full_free_cyclic_image_rule(goal, group)
    proofs = tuple(_inferred(statement) for statement in obligations)
    matches = find_inference_matches_for_rule(rule, proofs)
    assert len(matches) == 1
    result = derive_inference_proof_step(matches[0])
    assert result.rule is ProofRule.INFERENCE
    assert result.conclusion == goal
    assert result.premises == proofs


def test_given_cannot_replace_either_proof() -> None:
    goal, group = _fixture(11, 6)
    obligations = delta_surjectivity_image_inputs(goal, group)
    assert obligations is not None
    rule = delta_surjectivity_from_full_free_cyclic_image_rule(goal, group)
    proofs = list(_inferred(s) for s in obligations)
    for i in range(2):
        replaced = list(proofs)
        replaced[i] = ProofStep(obligations[i], (), ProofRule.GIVEN)
        assert find_inference_matches_for_rule(rule, tuple(replaced)) == ()


def test_wrong_image_or_codomain_generator_is_rejected() -> None:
    goal, group = _fixture(11, 6)
    obligations = delta_surjectivity_image_inputs(goal, group)
    assert obligations is not None
    rule = delta_surjectivity_from_full_free_cyclic_image_rule(goal, group)
    other_generator = HomotopyElement("other", 6, 11, 6)
    wrong_image = _inferred(TodaDeltaImageFreeCyclicStatement(
        goal.map, FreeCyclicGroup(other_generator),
    ))
    wrong_group = _inferred(Relation(
        goal.map.target_group, FreeCyclicGroup(other_generator), RelationType.EQUALITY,
    ))
    proofs = tuple(_inferred(s) for s in obligations)
    assert find_inference_matches_for_rule(rule, (proofs[0], wrong_image)) == ()
    assert find_inference_matches_for_rule(rule, (wrong_group, proofs[1])) == ()


@pytest.mark.parametrize("candidate", (object(), "surj", MapSurjective(object())))
def test_invalid_goal_has_no_expansion(candidate: object) -> None:
    _, group = _fixture(11, 6)
    assert delta_surjectivity_image_inputs(candidate, group) is None
    assert expand_delta_surjectivity_from_full_free_cyclic_image(candidate, group) == ()


def test_wrong_delta_indices_and_wrong_group_are_rejected() -> None:
    goal, group = _fixture(11, 6)
    wrong_delta = MapSurjective(TodaDeltaMap(
        TodaPrimaryGroup(14, 13), TodaPrimaryGroup(11, 6),
    ))
    wrong_group = Relation(TodaPrimaryGroup(10, 6), group.rhs, RelationType.EQUALITY)
    assert delta_surjectivity_image_inputs(wrong_delta, group) is None
    assert delta_surjectivity_image_inputs(goal, wrong_group) is None
    assert delta_surjectivity_image_inputs(goal, Relation(
        group.lhs, FreeCyclicGroup(Zero()), RelationType.EQUALITY,
    )) is None
    assert delta_surjectivity_image_inputs(goal, Relation(
        group.lhs, group.rhs, RelationType.ORDER,
    )) is None


def test_no_direct_proof_leaf_or_conclusion_inserted() -> None:
    goal, group = _fixture(11, 6)
    proposals = expand_delta_surjectivity_from_full_free_cyclic_image(goal, group)
    assert len(proposals) == 1
    assert all(not isinstance(s, ProofStep) for s in proposals[0].subgoals)
    assert proposals[0].rule.conclusion_pattern == goal

"""Focused generic matching, invalid-source and full R4-R8 inference tests."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import GeneratorSymbol, HomotopyElement
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase164_r8_proofstep_factory import derive_inference_proof_step
from phase168_r2_8_3_generator_identity.identity import same_registered_group_presentation
from phase171_r2j_r4_r6_middle_cardinality.source import FiniteGroupCardinality
from phase171_r2j_r4_r7_nonzero_nu_order.source import FiniteElementOrder
from phase171_r2j_r4_r8_cyclic_structure.audit import _git, build_cyclic_pi63_proof
from phase171_r2j_r4_r8_cyclic_structure.source import (
    cyclic_group_from_generator_order,
    expand_cyclic_group_from_full_element_order,
    inferred_cyclic_group_rule,
)
from proof import ProofRule, ProofStep, Relation, RelationType, find_inference_matches_for_rule


def _fixture():
    group = TodaPrimaryGroup(6, 3)
    nu = HomotopyElement(
        name="ν′", dimension=3, source=6, target=3,
        generator=GeneratorSymbol(family="ν", decoration="′"),
    )
    database_nu = HomotopyElement(
        name="ν'", dimension=3, source=6, target=3,
        generator=GeneratorSymbol(family=r"\nu'"),
    )
    cardinality = FiniteGroupCardinality(group, 4)
    element_order = FiniteElementOrder(group, nu, 4)
    goal = Relation(
        group, FiniteCyclicGroup(4, database_nu), RelationType.EQUALITY,
    )
    return cardinality, element_order, goal


def test_full_order_generates_canonical_finite_cyclic_group():
    cardinality, element_order, _ = _fixture()
    actual = cyclic_group_from_generator_order(cardinality, element_order)
    assert actual == Relation(
        cardinality.group, FiniteCyclicGroup(4, element_order.element),
        RelationType.EQUALITY,
    )


def test_registered_nu_prime_presentation_identity_is_checked():
    cardinality, element_order, goal = _fixture()
    canonical = cyclic_group_from_generator_order(cardinality, element_order)
    assert canonical is not None
    assert canonical.rhs.generator != goal.rhs.generator
    assert same_registered_group_presentation(canonical.rhs, goal.rhs)
    assert cyclic_group_from_generator_order(
        cardinality, element_order, requested=goal,
    ) == goal


def test_different_generator_id_does_not_become_a_group_theorem():
    cardinality, element_order, goal = _fixture()
    unrelated = HomotopyElement(
        name="unrelated", dimension=3, source=6, target=3,
        generator=GeneratorSymbol(family="κ"),
    )
    bad = replace(goal, rhs=FiniteCyclicGroup(4, unrelated))
    assert cyclic_group_from_generator_order(
        cardinality, element_order, requested=bad,
    ) is None
    assert expand_cyclic_group_from_full_element_order(
        bad, cardinality, element_order,
    ) == ()


def test_wrong_group_cardinality_and_generator_order_fail_closed():
    cardinality, element_order, goal = _fixture()
    assert cyclic_group_from_generator_order(
        replace(cardinality, group=TodaPrimaryGroup(7, 3)), element_order,
    ) is None
    assert cyclic_group_from_generator_order(
        replace(cardinality, order=2), element_order,
    ) is None
    assert cyclic_group_from_generator_order(
        cardinality, replace(element_order, order=2),
    ) is None
    assert cyclic_group_from_generator_order(
        cardinality, element_order,
        requested=replace(goal, rhs=FiniteCyclicGroup(2, goal.rhs.generator)),
    ) is None


def test_boolean_and_invalid_orders_cannot_generate_a_cyclic_group():
    cardinality, element_order, _ = _fixture()
    for invalid in (True, 0, -4):
        assert cyclic_group_from_generator_order(
            replace(cardinality, order=invalid), element_order,
        ) is None
        assert cyclic_group_from_generator_order(
            cardinality, replace(element_order, order=invalid),
        ) is None


def test_wrong_element_endpoints_cannot_be_used_even_with_correct_order():
    cardinality, element_order, goal = _fixture()
    wrong = replace(element_order, element=replace(element_order.element, source=7))
    assert cyclic_group_from_generator_order(cardinality, wrong) is None
    wrong_requested = replace(
        goal, rhs=FiniteCyclicGroup(4, replace(goal.rhs.generator, target=4)),
    )
    assert cyclic_group_from_generator_order(
        cardinality, element_order, requested=wrong_requested,
    ) is None


def test_exact_typed_goal_can_be_matched_without_generator_catalog():
    cardinality, element_order, _ = _fixture()
    anonymous = replace(
        element_order, element=replace(
            element_order.element,
            name="x", generator=GeneratorSymbol(family="unique"),
        ),
    )
    canonical = cyclic_group_from_generator_order(cardinality, anonymous)
    assert canonical is not None
    assert cyclic_group_from_generator_order(
        cardinality, anonymous, requested=canonical,
    ) == canonical


def test_valid_premises_produce_real_inference_with_canonical_order():
    cardinality, element_order, goal = _fixture()
    steps = (
        ProofStep(cardinality, (), ProofRule.INFERENCE),
        ProofStep(element_order, (), ProofRule.INFERENCE),
    )
    rule = inferred_cyclic_group_rule(goal)
    matches = find_inference_matches_for_rule(rule, steps[::-1])
    assert len(matches) == 1
    assert matches[0].premises == steps
    root = derive_inference_proof_step(matches[0])
    assert root.rule is ProofRule.INFERENCE
    assert root.conclusion == goal
    assert root.premises == steps


def test_given_or_unverified_element_order_cannot_be_promoted():
    cardinality, element_order, goal = _fixture()
    rule = inferred_cyclic_group_rule(goal)
    assert find_inference_matches_for_rule(rule, (
        ProofStep(cardinality, (), ProofRule.GIVEN),
        ProofStep(element_order, (), ProofRule.INFERENCE),
    )) == ()
    assert find_inference_matches_for_rule(rule, (
        ProofStep(cardinality, (), ProofRule.INFERENCE),
        ProofStep(element_order, (), ProofRule.GIVEN),
    )) == ()


def test_one_backward_obligation_and_invalid_target_rejected():
    cardinality, element_order, goal = _fixture()
    proposals = expand_cyclic_group_from_full_element_order(
        goal, cardinality, element_order,
    )
    assert len(proposals) == 1
    assert proposals[0].subgoals == (cardinality, element_order)
    assert expand_cyclic_group_from_full_element_order(
        object(), cardinality, element_order,
    ) == ()
    with pytest.raises(ValueError):
        inferred_cyclic_group_rule(replace(goal, relation_type=RelationType.ZERO))


def test_read_only_git_guard_rejects_mutation():
    with pytest.raises(ValueError):
        _git("reset", "--hard")


def test_real_registered_pi63_goal_is_inferred_from_r7_ancestry():
    root, nodes, report = build_cyclic_pi63_proof()
    assert root.rule is ProofRule.INFERENCE
    assert root.conclusion == root.inference_rule.conclusion_pattern
    assert report["status"] == "INFERRED"
    assert report["pi63_cyclic_group_proven"] is True
    assert report["new_given_added"] == 0
    assert report["public_proof_search_wired"] is False
    assert report["public_web_verified"] is False
    assert len(report["verified_source_ids"]) >= 3
    assert len(root.premises) == 2
    assert all(step.rule is ProofRule.INFERENCE for step in root.premises)
    assert sum(step.rule is ProofRule.INFERENCE for step in nodes) >= 4
    assert sum(step.rule is ProofRule.GIVEN for step in nodes) >= 3

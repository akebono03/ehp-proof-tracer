"""Typed general annihilator specialization: no target GIVEN and no aliasing."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import Composition, HomotopyElement, Zero
from phase164_r8_proofstep_factory import derive_inference_proof_step
from phase174_r3_r7_r12_toda59_annihilator_source.rule import (
    RULE_NAME, annihilator_specialization_inputs, canonical_annihilator_instance,
    cited_annihilator_specialization_rule, expand_cited_annihilator_specialization,
)
from phase174_r3_r7_r12_toda59_annihilator_source.source import (
    CitedFamilyAnnihilator, SOURCE_ANNIHILATOR_LOCATOR,
)
from proof import InferenceRule, ProofRule, ProofStep, Relation, RelationType, find_inference_matches_for_rule


def schema() -> CitedFamilyAnnihilator:
    return CitedFamilyAnnihilator(4, 2, 6, 3, SOURCE_ANNIHILATOR_LOCATOR)


@pytest.mark.parametrize("n", (6, 7, 11, 20))
def test_any_permitted_index_uses_same_generic_cited_rule(n: int) -> None:
    claim = schema()
    goal = canonical_annihilator_instance(claim, n)
    assert isinstance(goal, Relation)
    assert goal.relation_type is RelationType.EQUALITY
    assert isinstance(goal.lhs, Composition)
    assert goal.lhs.left.generator.index == n
    assert goal.lhs.right.generator.index == n + 3
    assert goal.lhs.left.source == goal.lhs.right.target
    assert goal.rhs == Zero()
    options = expand_cited_annihilator_specialization(goal, (claim,))
    assert len(options) == 1
    assert options[0].subgoals == (claim,)
    assert options[0].rule.name == RULE_NAME


def test_proved_cited_schema_yields_inferred_instance_with_provenance() -> None:
    claim = schema()
    goal = canonical_annihilator_instance(claim, 6)
    assert goal is not None
    rule = cited_annihilator_specialization_rule(goal, claim)
    cited = ProofStep(
        conclusion=claim, premises=(), rule=ProofRule.GIVEN,
        inference_rule=InferenceRule(name="test-only source assertion"),
    )
    matches = find_inference_matches_for_rule(rule, (cited,))
    assert len(matches) == 1
    derived = derive_inference_proof_step(matches[0])
    assert derived.conclusion == goal
    assert derived.rule is ProofRule.INFERENCE
    assert derived.premises == (cited,)
    assert derived.inference_rule is rule


def test_without_screened_cited_schema_no_rule_is_proposed() -> None:
    claim = schema()
    goal = canonical_annihilator_instance(claim, 6)
    assert expand_cited_annihilator_specialization(goal, ()) == ()
    assert annihilator_specialization_inputs(goal, ()) == ()
    assert find_inference_matches_for_rule(
        cited_annihilator_specialization_rule(goal, claim), (),
    ) == ()


def test_the_cited_schema_requires_a_given_not_a_speculative_inference() -> None:
    claim = schema()
    goal = canonical_annihilator_instance(claim, 6)
    rule = cited_annihilator_specialization_rule(goal, claim)
    inferred = ProofStep(
        claim, (), ProofRule.INFERENCE,
        inference_rule=InferenceRule(name="test-only unauthenticated schema"),
    )
    assert find_inference_matches_for_rule(rule, (inferred,)) == ()


@pytest.mark.parametrize("n", (0, 1, 4, 5, True, "6", None))
def test_invalid_or_below_range_indices_fail_closed(n: object) -> None:
    assert canonical_annihilator_instance(schema(), n) is None


@pytest.mark.parametrize("modified", (
    CitedFamilyAnnihilator(4, 2, 6, 4, SOURCE_ANNIHILATOR_LOCATOR),
    CitedFamilyAnnihilator(4, 2, 9, 3, SOURCE_ANNIHILATOR_LOCATOR),
    CitedFamilyAnnihilator(4, 99, 6, 3, SOURCE_ANNIHILATOR_LOCATOR),
    CitedFamilyAnnihilator(99, 2, 6, 3, SOURCE_ANNIHILATOR_LOCATOR),
    CitedFamilyAnnihilator(4, 2, 6, -1, SOURCE_ANNIHILATOR_LOCATOR),
))
def test_incorrect_family_or_dimension_schema_never_generates_target(modified) -> None:
    claim = schema()
    goal = canonical_annihilator_instance(claim, 6)
    assert annihilator_specialization_inputs(goal, (modified,)) == ()


def test_noncanonical_nu_symbol_is_not_silently_equated() -> None:
    claim = schema()
    goal = canonical_annihilator_instance(claim, 6)
    assert goal is not None
    a = goal.lhs.left
    bad_nu = replace(a, name="nu_6")
    changed = Relation(
        Composition(bad_nu, goal.lhs.right), Zero(), RelationType.EQUALITY,
    )
    assert annihilator_specialization_inputs(changed, (claim,)) == ()
    assert expand_cited_annihilator_specialization(changed, (claim,)) == ()


def test_bad_right_eta_or_reversed_product_is_not_matched() -> None:
    claim = schema()
    goal = canonical_annihilator_instance(claim, 6)
    assert goal is not None
    wrong = Relation(
        Composition(goal.lhs.right, goal.lhs.left), Zero(), RelationType.EQUALITY,
    )
    assert expand_cited_annihilator_specialization(wrong, (claim,)) == ()
    changed = Relation(
        Composition(goal.lhs.left, replace(goal.lhs.right, name="eta_9")),
        Zero(), RelationType.EQUALITY,
    )
    assert expand_cited_annihilator_specialization(changed, (claim,)) == ()


def test_wrong_relation_type_and_forged_zero_are_rejected() -> None:
    claim = schema()
    goal = canonical_annihilator_instance(claim, 6)
    assert goal is not None
    assert expand_cited_annihilator_specialization(
        Relation(goal.lhs, Zero(), RelationType.ZERO), (claim,),
    ) == ()
    assert expand_cited_annihilator_specialization(
        Relation(goal.lhs, 0, RelationType.EQUALITY), (claim,),
    ) == ()


def test_no_direct_target_step_is_constructed_by_backward_expansion() -> None:
    claim = schema()
    goal = canonical_annihilator_instance(claim, 6)
    options = expand_cited_annihilator_specialization(goal, (claim,))
    assert len(options) == 1
    assert all(not isinstance(x, ProofStep) for x in options[0].subgoals)
    assert options[0].subgoals == (claim,)


def test_wrong_or_duplicate_source_objects_cannot_be_used_as_evidence() -> None:
    claim = schema()
    goal = canonical_annihilator_instance(claim, 6)
    wrong = CitedFamilyAnnihilator(4, 2, 7, 3, SOURCE_ANNIHILATOR_LOCATOR)
    assert annihilator_specialization_inputs(goal, (wrong,)) == ()
    assert annihilator_specialization_inputs(goal, (claim, claim)) == (claim,)
    with pytest.raises(TypeError):
        annihilator_specialization_inputs(goal, [claim])

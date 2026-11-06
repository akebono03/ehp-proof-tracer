"""Focused proof contracts for generic composition reassociation."""
from __future__ import annotations

import pytest

from expression import Composition, HomotopyElement, Zero
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r3_recursive_search import GoalExpansion
from phase164_r8_proofstep_factory import derive_inference_proof_step
from phase169_r10e5_composite_generator_image.rule import expand_composite_generator_image
from phase174_r3_r7_r9_composition_associativity.rule import (
    RULE_NAME,
    expand_generator_image_associativity,
    generator_image_associativity_inputs,
    generator_image_associativity_rule,
    right_associated_composition,
    typed_composition_factors,
)
from proof import (
    InferenceRule, ProofRule, ProofStep, find_inference_matches_for_rule,
)


def element(name: str, source: int, target: int) -> HomotopyElement:
    return HomotopyElement(name, target, source=source, target=target)


def sample(sphere: int = 5) -> tuple[GeneratorImage, GeneratorImage]:
    source_f = element("f", sphere + 3, sphere)
    source_g = element("g", sphere + 4, sphere + 3)
    source_h = element("h", sphere + 5, sphere + 4)
    target_f = element("Ef", sphere + 4, sphere + 1)
    target_g = element("Eg", sphere + 5, sphere + 4)
    target_h = element("Eh", sphere + 6, sphere + 5)
    source = Composition(source_f, Composition(source_g, source_h))
    target_left = Composition(Composition(target_f, target_g), target_h)
    target_right = Composition(target_f, Composition(target_g, target_h))
    mapping = TodaSuspensionMap(
        TodaPrimaryGroup(sphere + 5, sphere),
        TodaPrimaryGroup(sphere + 6, sphere + 1),
    )
    return (
        GeneratorImage(mapping, source, target_left),
        GeneratorImage(mapping, source, target_right),
    )


@pytest.mark.parametrize("sphere", (3, 5, 9, 17))
def test_generic_reassociation_preserves_factors_and_map(sphere: int) -> None:
    left, right = sample(sphere)
    normalized = right_associated_composition(left.target_generator)
    assert normalized == right.target_generator
    assert typed_composition_factors(normalized) == typed_composition_factors(left.target_generator)
    assert generator_image_associativity_inputs(left) == (right,)
    choices = expand_generator_image_associativity(left)
    assert len(choices) == 1
    assert isinstance(choices[0], GoalExpansion)
    assert choices[0].subgoals == (right,)
    assert choices[0].rule.name == RULE_NAME


def test_prior_composite_rule_requires_matching_parentheses() -> None:
    left, right = sample()
    assert expand_composite_generator_image(left) == ()
    options = expand_composite_generator_image(right)
    assert len(options) == 1
    assert len(options[0].subgoals) == 2
    assert all(isinstance(child, GeneratorImage) for child in options[0].subgoals)


def test_inferred_premise_derives_exact_original_goal_and_preserves_tree() -> None:
    left, right = sample()
    rule = generator_image_associativity_rule(left)
    inferred = ProofStep(
        conclusion=right,
        premises=(),
        rule=ProofRule.INFERENCE,
        inference_rule=InferenceRule(name="test-only independently proved image"),
    )
    matches = find_inference_matches_for_rule(rule, (inferred,))
    assert len(matches) == 1
    result = derive_inference_proof_step(matches[0])
    assert result.conclusion == left
    assert result.premises == (inferred,)
    assert result.inference_rule is rule
    assert result.rule is ProofRule.INFERENCE


def test_given_and_unproved_image_do_not_close_goal() -> None:
    left, right = sample()
    rule = generator_image_associativity_rule(left)
    given = ProofStep(right, (), ProofRule.GIVEN)
    assert find_inference_matches_for_rule(rule, (given,)) == ()
    assert find_inference_matches_for_rule(rule, ()) == ()


def test_unrelated_or_wrong_map_does_not_close_goal() -> None:
    left, right = sample()
    rule = generator_image_associativity_rule(left)
    unrelated = sample(6)[1]
    premise = ProofStep(
        unrelated, (), ProofRule.INFERENCE,
        inference_rule=InferenceRule(name="test-only unrelated evidence"),
    )
    assert find_inference_matches_for_rule(rule, (premise,)) == ()
    wrong_source = GeneratorImage(right.map, unrelated.source_generator, right.target_generator)
    proof = ProofStep(
        wrong_source, (), ProofRule.INFERENCE,
        inference_rule=InferenceRule(name="test-only wrong source"),
    )
    assert find_inference_matches_for_rule(rule, (proof,)) == ()


def test_right_associated_goal_is_not_reexpanded_into_itself() -> None:
    left, right = sample()
    assert generator_image_associativity_inputs(right) is None
    assert expand_generator_image_associativity(right) == ()
    assert right_associated_composition(left.target_generator) == right.target_generator


def test_wrong_suspension_dimensions_are_rejected() -> None:
    left, right = sample()
    wrong = GeneratorImage(
        TodaSuspensionMap(TodaPrimaryGroup(10, 5), TodaPrimaryGroup(11, 8)),
        left.source_generator, left.target_generator,
    )
    assert expand_generator_image_associativity(wrong) == ()
    assert expand_generator_image_associativity(object()) == ()
    assert expand_generator_image_associativity(GeneratorImage(
        "E", left.source_generator, left.target_generator,
    )) == ()


def test_composition_with_bad_endpoint_is_rejected() -> None:
    a = element("a", 9, 6)
    b = element("b", 12, 10)
    c = element("c", 13, 12)
    bad = Composition(Composition(a, b), c)
    assert typed_composition_factors(bad) is None
    assert right_associated_composition(bad) is None
    assert right_associated_composition(a) is None
    assert right_associated_composition(Composition(a, b)) is None


def test_zero_and_non_map_factors_are_rejected() -> None:
    left, right = sample()
    assert typed_composition_factors(Zero()) is None
    bad = GeneratorImage(
        left.map, left.source_generator,
        Composition(Composition(Zero(), right.target_generator.left),
                    right.target_generator.right),
    )
    assert expand_generator_image_associativity(bad) == ()


def test_isolated_rule_does_not_fabricate_any_proof_step() -> None:
    left, right = sample()
    choices = expand_generator_image_associativity(left)
    assert len(choices) == 1
    assert not any(isinstance(child, ProofStep) for child in choices[0].subgoals)
    assert left not in choices[0].subgoals
    assert choices[0].subgoals == (right,)

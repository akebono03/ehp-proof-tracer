"""Mathematical and provenance guards for the isolated finite-cyclic zero-image rule."""
from __future__ import annotations

import pytest

from expression import HomotopyElement, Zero
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup, TodaSuspensionMap
from map_property_rules import ImageZeroStatement
from phase165_r14_r6_generic_iso import GeneratorImage
from phase164_r8_proofstep_factory import derive_inference_proof_step
from phase174_r3_r7_r6_cyclic_generator_zero_image.rule import (
    RULE_NAME,
    cyclic_generator_zero_image_inputs,
    expand_zero_image_from_cyclic_generator,
    zero_image_from_cyclic_generator_rule,
)
from proof import (
    InferenceRule, ProofRule, ProofStep, Relation, RelationType,
    find_inference_matches_for_rule,
)


def fixture_case(degree: int = 10, sphere: int = 5, order: int = 2):
    domain = TodaPrimaryGroup(degree, sphere)
    mapping = TodaSuspensionMap(domain, TodaPrimaryGroup(degree + 1, sphere + 1))
    generator = HomotopyElement("a", sphere, source=degree, target=sphere)
    presentation = Relation(
        lhs=domain,
        rhs=FiniteCyclicGroup(order=order, generator=generator),
        relation_type=RelationType.EQUALITY,
    )
    return ImageZeroStatement(mapping), presentation


def inferred(statement: object) -> ProofStep:
    return ProofStep(
        conclusion=statement, premises=(), rule=ProofRule.INFERENCE,
        inference_rule=InferenceRule(name="test-only independently inferred fixture"),
    )


@pytest.mark.parametrize("degree,sphere,order", (
    (10, 5, 2), (11, 6, 4), (20, 12, 8), (14, 7, 3),
))
def test_generic_valid_suspension_and_cyclic_presentation(
    degree: int, sphere: int, order: int,
) -> None:
    goal, presentation = fixture_case(degree, sphere, order)
    children = cyclic_generator_zero_image_inputs(goal, presentation)
    assert children is not None
    assert children[0] == presentation
    assert children[1] == GeneratorImage(
        goal.map, presentation.rhs.generator, Zero()
    )
    candidates = expand_zero_image_from_cyclic_generator(goal, presentation)
    assert len(candidates) == 1
    assert candidates[0].subgoals == children
    assert candidates[0].rule.name == RULE_NAME


def test_two_proved_premises_derive_zero_image_and_keep_ancestors() -> None:
    goal, presentation = fixture_case()
    children = cyclic_generator_zero_image_inputs(goal, presentation)
    assert children is not None
    proofs = tuple(inferred(child) for child in children)
    rule = zero_image_from_cyclic_generator_rule(goal, presentation)
    matches = find_inference_matches_for_rule(rule, proofs)
    assert len(matches) == 1
    derived = derive_inference_proof_step(matches[0])
    assert derived.rule is ProofRule.INFERENCE
    assert derived.conclusion == goal
    assert derived.inference_rule is rule
    assert derived.premises == proofs


def test_unproved_presentation_or_zero_image_never_closes_root() -> None:
    goal, presentation = fixture_case()
    children = cyclic_generator_zero_image_inputs(goal, presentation)
    assert children is not None
    rule = zero_image_from_cyclic_generator_rule(goal, presentation)
    proved = tuple(inferred(child) for child in children)
    assert find_inference_matches_for_rule(rule, proved[:1]) == ()
    assert find_inference_matches_for_rule(rule, proved[1:]) == ()
    for index in (0, 1):
        forged = list(proved)
        forged[index] = ProofStep(children[index], (), ProofRule.GIVEN)
        assert find_inference_matches_for_rule(rule, tuple(forged)) == ()


def test_wrong_generator_and_wrong_map_are_rejected() -> None:
    goal, presentation = fixture_case()
    children = cyclic_generator_zero_image_inputs(goal, presentation)
    assert children is not None
    rule = zero_image_from_cyclic_generator_rule(goal, presentation)
    p = inferred(children[0])
    wrong_generator = inferred(GeneratorImage(
        goal.map, HomotopyElement("b", 5, source=10, target=5), Zero()
    ))
    wrong_mapping = inferred(GeneratorImage(
        TodaSuspensionMap(TodaPrimaryGroup(11, 6), TodaPrimaryGroup(12, 7)),
        presentation.rhs.generator, Zero(),
    ))
    assert find_inference_matches_for_rule(rule, (p, wrong_generator)) == ()
    assert find_inference_matches_for_rule(rule, (p, wrong_mapping)) == ()


def test_zero_must_be_typed_expression_not_integer_or_false() -> None:
    goal, presentation = fixture_case()
    children = cyclic_generator_zero_image_inputs(goal, presentation)
    assert children is not None
    rule = zero_image_from_cyclic_generator_rule(goal, presentation)
    for fake_zero in (0, False, None, "0"):
        fake = inferred(GeneratorImage(goal.map, presentation.rhs.generator, fake_zero))
        assert find_inference_matches_for_rule(rule, (inferred(children[0]), fake)) == ()


def test_wrong_sphere_or_non_suspension_map_yields_no_candidate() -> None:
    goal, presentation = fixture_case()
    bad_map = TodaSuspensionMap(
        TodaPrimaryGroup(10, 5), TodaPrimaryGroup(11, 8)
    )
    assert expand_zero_image_from_cyclic_generator(
        ImageZeroStatement(bad_map), presentation
    ) == ()
    assert expand_zero_image_from_cyclic_generator(object(), presentation) == ()
    assert expand_zero_image_from_cyclic_generator(ImageZeroStatement("E"), presentation) == ()


def test_wrong_group_and_nongroup_claims_are_rejected() -> None:
    goal, presentation = fixture_case()
    wrong = Relation(
        lhs=TodaPrimaryGroup(11, 5), rhs=presentation.rhs,
        relation_type=RelationType.EQUALITY,
    )
    assert expand_zero_image_from_cyclic_generator(goal, wrong) == ()
    assert expand_zero_image_from_cyclic_generator(goal, object()) == ()
    assert expand_zero_image_from_cyclic_generator(goal, Relation(
        lhs=presentation.lhs, rhs=presentation.rhs,
        relation_type=RelationType.ZERO,
    )) == ()


def test_bad_orders_and_untyped_generators_are_not_used() -> None:
    goal, presentation = fixture_case()
    for order in (0, 1, -1, True, "2"):
        wrong = Relation(
            presentation.lhs,
            FiniteCyclicGroup(order=order, generator=presentation.rhs.generator),
            RelationType.EQUALITY,
        )
        assert expand_zero_image_from_cyclic_generator(goal, wrong) == ()
    for generator in (None, "a", 0, Zero()):
        wrong = Relation(
            presentation.lhs,
            FiniteCyclicGroup(order=2, generator=generator),
            RelationType.EQUALITY,
        )
        assert expand_zero_image_from_cyclic_generator(goal, wrong) == ()


def test_no_proof_leaf_or_direct_target_is_constructed() -> None:
    goal, presentation = fixture_case()
    candidates = expand_zero_image_from_cyclic_generator(goal, presentation)
    assert len(candidates) == 1
    assert all(not isinstance(x, ProofStep) for x in candidates[0].subgoals)
    assert goal not in candidates[0].subgoals

"""Source-independent generic composite-zero inference contracts."""
from __future__ import annotations

import pytest

from expression import Composition, HomotopyElement, Zero
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import GeneratorImage
from phase164_r8_proofstep_factory import derive_inference_proof_step
from phase174_r3_r7_r7_composite_zero_audit.rule import (
    RULE_NAME,
    composite_zero_generator_inputs,
    expand_generator_zero_from_composite,
    expression_endpoints,
    generator_zero_from_composite_rule,
)
from proof import (
    InferenceRule,
    ProofRule,
    ProofStep,
    Relation,
    RelationType,
    find_inference_matches_for_rule,
)


def element(name: str, source: int, target: int) -> HomotopyElement:
    return HomotopyElement(name, dimension=target, source=source, target=target)


def sample(degree: int = 10, sphere: int = 5):
    mapping = TodaSuspensionMap(
        TodaPrimaryGroup(degree, sphere),
        TodaPrimaryGroup(degree + 1, sphere + 1),
    )
    generator = element("g", degree, sphere)
    nu = element("a", sphere + 4, sphere + 1)
    eta = element("b", sphere + 5, sphere + 4)
    eta_second = element("c", degree + 1, sphere + 5)
    composite = Composition(Composition(nu, eta), eta_second)
    goal = GeneratorImage(mapping, generator, Zero())
    intermediate = GeneratorImage(mapping, generator, composite)
    return goal, intermediate


def inferred(statement: object) -> ProofStep:
    return ProofStep(
        conclusion=statement,
        premises=(),
        rule=ProofRule.INFERENCE,
        inference_rule=InferenceRule(name="test-only inferred fixture"),
    )


@pytest.mark.parametrize("degree,sphere", ((10, 5), (11, 6), (15, 10)))
def test_composite_zero_general_dimensions(degree: int, sphere: int) -> None:
    # In the generic fixture a has source sphere+4, so degree must be sphere+5.
    if degree != sphere + 5:
        return
    goal, intermediate = sample(degree, sphere)
    required = composite_zero_generator_inputs(goal, intermediate)
    assert required is not None
    assert required[0] == intermediate
    assert required[1] == Relation(
        intermediate.target_generator.left, Zero(), RelationType.EQUALITY,
    )
    candidates = expand_generator_zero_from_composite(goal, intermediate)
    assert len(candidates) == 1
    assert candidates[0].subgoals == required
    assert candidates[0].rule.name == RULE_NAME


def test_source_example_has_consistent_sphere_dimensions() -> None:
    goal, intermediate = sample(10, 5)
    assert expression_endpoints(intermediate.target_generator) == (11, 6)
    assert expression_endpoints(intermediate.target_generator.left) == (10, 6)
    assert expression_endpoints(intermediate.target_generator.right) == (11, 10)
    assert composite_zero_generator_inputs(goal, intermediate) is not None


def test_both_certified_ancestors_are_required() -> None:
    goal, intermediate = sample()
    required = composite_zero_generator_inputs(goal, intermediate)
    assert required is not None
    rule = generator_zero_from_composite_rule(goal, intermediate)
    proofs = tuple(inferred(item) for item in required)
    match = find_inference_matches_for_rule(rule, proofs)
    assert len(match) == 1
    derived = derive_inference_proof_step(match[0])
    assert derived.conclusion == goal
    assert derived.rule is ProofRule.INFERENCE
    assert derived.premises == proofs
    assert derived.inference_rule is rule
    assert find_inference_matches_for_rule(rule, proofs[:1]) == ()
    assert find_inference_matches_for_rule(rule, proofs[1:]) == ()


@pytest.mark.parametrize("index", (0, 1))
def test_direct_given_is_not_accepted(index: int) -> None:
    goal, intermediate = sample()
    required = composite_zero_generator_inputs(goal, intermediate)
    assert required is not None
    proofs = list(inferred(item) for item in required)
    proofs[index] = ProofStep(required[index], (), ProofRule.GIVEN)
    rule = generator_zero_from_composite_rule(goal, intermediate)
    assert find_inference_matches_for_rule(rule, tuple(proofs)) == ()


def test_wrong_generator_does_not_prove_target() -> None:
    goal, intermediate = sample()
    wrong = GeneratorImage(intermediate.map, element("other", 10, 5), intermediate.target_generator)
    assert composite_zero_generator_inputs(goal, wrong) is None
    assert expand_generator_zero_from_composite(goal, wrong) == ()


def test_mismatched_map_rejected() -> None:
    goal, intermediate = sample()
    wrong_map = TodaSuspensionMap(TodaPrimaryGroup(11, 6), TodaPrimaryGroup(12, 7))
    wrong = GeneratorImage(wrong_map, intermediate.source_generator, intermediate.target_generator)
    assert composite_zero_generator_inputs(goal, wrong) is None


def test_wrong_target_generator_shape_rejected() -> None:
    goal, intermediate = sample()
    for invalid in (Zero(), element("a", 11, 6), "some expression", 0):
        candidate = GeneratorImage(goal.map, goal.source_generator, invalid)
        assert expand_generator_zero_from_composite(goal, candidate) == ()


def test_wrong_composition_dimensions_rejected() -> None:
    goal, intermediate = sample()
    wrong = GeneratorImage(
        goal.map, goal.source_generator,
        Composition(Composition(element("a", 9, 6), element("b", 11, 10)),
                    element("c", 12, 11)),
    )
    assert composite_zero_generator_inputs(goal, wrong) is None


def test_wrong_domain_or_target_dimensions_rejected() -> None:
    goal, intermediate = sample()
    bad = GeneratorImage(
        TodaSuspensionMap(TodaPrimaryGroup(10, 5), TodaPrimaryGroup(11, 9)),
        goal.source_generator, Zero(),
    )
    bad_image = GeneratorImage(bad.map, goal.source_generator, intermediate.target_generator)
    assert composite_zero_generator_inputs(bad, bad_image) is None
    assert composite_zero_generator_inputs(object(), intermediate) is None


def test_wrong_zero_type_or_untyped_source_rejected() -> None:
    goal, intermediate = sample()
    for wrong_zero in (0, "0", None, False):
        bad = GeneratorImage(goal.map, goal.source_generator, wrong_zero)
        assert composite_zero_generator_inputs(bad, intermediate) is None
    bad_source = GeneratorImage(goal.map, "g", Zero())
    matching = GeneratorImage(goal.map, "g", intermediate.target_generator)
    assert composite_zero_generator_inputs(bad_source, matching) is None


def test_wrong_annihilator_relation_cannot_close_proof() -> None:
    goal, intermediate = sample()
    required = composite_zero_generator_inputs(goal, intermediate)
    assert required is not None
    rule = generator_zero_from_composite_rule(goal, intermediate)
    wrong_left = Relation(element("x", 10, 6), Zero(), RelationType.EQUALITY)
    wrong_type = Relation(required[1].lhs, Zero(), RelationType.ZERO)
    wrong_right = Relation(required[1].lhs, 0, RelationType.EQUALITY)
    for bad_relation in (wrong_left, wrong_type, wrong_right):
        assert find_inference_matches_for_rule(
            rule, (inferred(required[0]), inferred(bad_relation)),
        ) == ()


def test_no_proof_step_or_target_given_constructed_by_expansion() -> None:
    goal, intermediate = sample()
    option, = expand_generator_zero_from_composite(goal, intermediate)
    assert len(option.subgoals) == 2
    assert all(not isinstance(child, ProofStep) for child in option.subgoals)
    assert goal not in option.subgoals

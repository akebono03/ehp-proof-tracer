"""Tests for generic source-free transport of a proved zero composite."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import Composition, GeneratorSymbol, HomotopyElement, Zero
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import GeneratorImage
from phase164_r8_proofstep_factory import derive_inference_proof_step
from phase175_r4r14r4_general_zero_transport.rule import (
    RULE_NAME,
    composite_value_zero_inputs,
    expand_proved_composite_zero_image,
    proved_composite_zero_image_rule,
)
from proof import (
    InferenceRule, ProofRule, ProofStep, find_inference_matches_for_rule,
)


def _element(name: str, source: int, target: int) -> HomotopyElement:
    return HomotopyElement(
        name=name, dimension=target, source=source, target=target,
        generator=GeneratorSymbol(name),
    )


def _cases(factors: int) -> tuple[GeneratorImage, GeneratorImage]:
    first = _element("a", 7, 4)
    second = _element("b", 11, 7)
    value: object = Composition(first, second)
    if factors == 3:
        value = Composition(value, _element("c", 13, 11))
    source_degree = 10 if factors == 2 else 12
    source_generator = _element("g", source_degree, 3)
    mapping = TodaSuspensionMap(
        TodaPrimaryGroup(source_degree, 3),
        TodaPrimaryGroup(source_degree + 1, 4),
    )
    return (
        GeneratorImage(mapping, source_generator, Zero()),
        GeneratorImage(mapping, source_generator, value),
    )


@pytest.mark.parametrize("factors", (2, 3))
def test_two_premises_prove_zero_image_for_any_factor_count(factors: int) -> None:
    goal, image = _cases(factors)
    required = composite_value_zero_inputs(goal, image)
    assert required is not None
    options = expand_proved_composite_zero_image(goal, image)
    assert len(options) == 1
    assert options[0].rule.name == RULE_NAME
    assert options[0].subgoals == required
    steps = tuple(ProofStep(
        conclusion=statement, premises=(), rule=ProofRule.INFERENCE,
        inference_rule=InferenceRule(name="test-only proof witness"),
    ) for statement in required)
    matches = find_inference_matches_for_rule(options[0].rule, steps)
    assert len(matches) == 1
    result = derive_inference_proof_step(matches[0])
    assert result.conclusion == goal
    assert result.rule is ProofRule.INFERENCE
    assert result.premises == steps


def test_unproved_or_given_premise_cannot_complete() -> None:
    goal, image = _cases(2)
    required = composite_value_zero_inputs(goal, image)
    assert required is not None
    rule = proved_composite_zero_image_rule(goal, image)
    first = ProofStep(required[0], (), ProofRule.INFERENCE)
    second = ProofStep(required[1], (), ProofRule.INFERENCE)
    assert find_inference_matches_for_rule(rule, (first,)) == ()
    assert find_inference_matches_for_rule(
        rule, (first, replace(second, rule=ProofRule.GIVEN)),
    ) == ()
    assert find_inference_matches_for_rule(rule, ()) == ()


def test_wrong_image_value_and_mismatched_map_rejected() -> None:
    goal, image = _cases(2)
    wrong = replace(image, map=TodaSuspensionMap(
        TodaPrimaryGroup(12, 3), TodaPrimaryGroup(13, 4),
    ))
    assert composite_value_zero_inputs(goal, wrong) is None
    assert expand_proved_composite_zero_image(goal, wrong) == ()
    wrong_value = replace(image, target_generator=Zero())
    assert composite_value_zero_inputs(goal, wrong_value) is None
    with pytest.raises(ValueError):
        proved_composite_zero_image_rule(goal, wrong)


def test_no_new_sources_or_proof_steps_are_created() -> None:
    goal, image = _cases(2)
    options = expand_proved_composite_zero_image(goal, image)
    assert len(options) == 1
    assert all(not isinstance(x, ProofStep) for x in options[0].subgoals)

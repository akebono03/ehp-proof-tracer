"""Isolated algebraic inference contracts; every fixture premise is synthetic.

Only the actual ProofStep matcher may infer the root. These test fixtures are
not registered references and are not a proof of pi_9^5 in production.
"""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import Composition, GeneratorSymbol, HomotopyElement
from homotopy_groups import (
    DirectSumGroup, FiniteCyclicGroup, TodaDeltaMap,
    TodaPrimaryGroup, TodaSuspensionMap,
)
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from phase165_r12_r5_structure_bridge import finite_cyclic_structure_as_relation_inference_rule
from phase165_r14_r6_generic_iso import GeneratorImage
from phase175_r4r3_two_summand_quotient.rule import (
    RULE_NAME, expand_two_summand_quotient,
    two_summand_quotient_inputs, two_summand_quotient_rule,
)
from proof import (
    InferenceRule, ProofRule, ProofStep, Relation, RelationType,
    apply_inference_match, find_inference_matches_for_rule,
)


def fixture():
    """Typed pi8^4/pi9^5 example, with no asserted source truth."""
    a_group = TodaPrimaryGroup(8, 4)
    c_group = TodaPrimaryGroup(10, 9)
    b_group = TodaPrimaryGroup(9, 5)
    nu4 = HomotopyElement(
        "ν₄", 4, source=7, target=4,
        generator=GeneratorSymbol("ν", 4),
    )
    nuprime_e = HomotopyElement(
        "Eν′", 4, source=7, target=4,
        generator=GeneratorSymbol("ν", decoration="′"),
    )
    eta7 = HomotopyElement(
        "η₇", 7, source=8, target=7,
        generator=GeneratorSymbol("η", 7),
    )
    nu5 = HomotopyElement(
        "ν₅", 5, source=8, target=5,
        generator=GeneratorSymbol("ν", 5),
    )
    eta8 = HomotopyElement(
        "η₈", 8, source=9, target=8,
        generator=GeneratorSymbol("η", 8),
    )
    eta9 = HomotopyElement(
        "η₉", 9, source=10, target=9,
        generator=GeneratorSymbol("η", 9),
    )
    a = Composition(nu4, eta7)
    killed = Composition(nuprime_e, eta7)
    y = Composition(nu5, eta8)
    source = Relation(
        a_group,
        DirectSumGroup((FiniteCyclicGroup(2, a), FiniteCyclicGroup(2, killed))),
        RelationType.EQUALITY,
    )
    delta_source = Relation(
        c_group, FiniteCyclicGroup(2, eta9), RelationType.EQUALITY,
    )
    delta = GeneratorImage(TodaDeltaMap(c_group, a_group), eta9, killed)
    suspension = GeneratorImage(TodaSuspensionMap(a_group, b_group), a, y)
    goal = CyclicStructureStatement(b_group, y, 2)
    return goal, source, delta_source, delta, suspension


def synthetic(value: object, kind: ProofRule = ProofRule.INFERENCE) -> ProofStep:
    return ProofStep(
        value, (), kind,
        inference_rule=InferenceRule("synthetic fixture only: not a cited proof"),
    )


def inferred_parent_steps():
    values = two_summand_quotient_inputs(*fixture())
    assert values is not None
    return tuple(synthetic(value) for value in values)


def test_proved_six_premise_rule_and_group_relation() -> None:
    goal, prior, source, delta, suspension = fixture()
    required = two_summand_quotient_inputs(goal, prior, source, delta, suspension)
    assert required is not None and len(required) == 6
    rule = two_summand_quotient_rule(goal, prior, source, delta, suspension)
    assert rule.name == RULE_NAME
    parents = inferred_parent_steps()
    matches = find_inference_matches_for_rule(rule, parents)
    assert len(matches) == 1
    cyclic = apply_inference_match(matches[0])
    assert cyclic.rule is ProofRule.INFERENCE
    assert cyclic.conclusion == goal
    assert cyclic.premises == parents
    bridge = finite_cyclic_structure_as_relation_inference_rule()
    relations = find_inference_matches_for_rule(bridge, (cyclic,))
    assert len(relations) == 1
    final = apply_inference_match(relations[0])
    assert final.conclusion == Relation(
        goal.group, FiniteCyclicGroup(2, goal.generator), RelationType.EQUALITY,
    )
    assert final.premises == (cyclic,)


def test_exposure_is_only_a_backward_proposal() -> None:
    goal, prior, source, delta, suspension = fixture()
    results = expand_two_summand_quotient(goal, prior, source, delta, suspension)
    assert len(results) == 1
    assert results[0].subgoals == two_summand_quotient_inputs(*fixture())
    assert all(not isinstance(item, ProofStep) for item in results[0].subgoals)


@pytest.mark.parametrize("index", range(6))
def test_missing_any_one_proof_rejects_conclusion(index: int) -> None:
    goal, prior, source, delta, suspension = fixture()
    rule = two_summand_quotient_rule(goal, prior, source, delta, suspension)
    parents = inferred_parent_steps()
    absent = parents[:index] + parents[index + 1:]
    assert not find_inference_matches_for_rule(rule, absent)


@pytest.mark.parametrize("index", (2, 3, 4, 5))
def test_cannot_substitute_a_given_for_derived_map_or_exactness(index: int) -> None:
    goal, prior, source, delta, suspension = fixture()
    rule = two_summand_quotient_rule(goal, prior, source, delta, suspension)
    parents = list(inferred_parent_steps())
    parents[index] = synthetic(parents[index].conclusion, ProofRule.GIVEN)
    assert not find_inference_matches_for_rule(rule, tuple(parents))


def test_prior_relations_can_be_previous_admitted_results() -> None:
    goal, prior, source, delta, suspension = fixture()
    rule = two_summand_quotient_rule(goal, prior, source, delta, suspension)
    parents = list(inferred_parent_steps())
    parents[0] = synthetic(prior, ProofRule.GIVEN)
    parents[1] = synthetic(source, ProofRule.GIVEN)
    matches = find_inference_matches_for_rule(rule, tuple(parents))
    assert len(matches) == 1
    assert apply_inference_match(matches[0]).conclusion == goal


@pytest.mark.parametrize("where", ("prior", "source", "delta", "suspension", "goal"))
def test_rejects_wrong_group_dimensions(where: str) -> None:
    goal, prior, source, delta, suspension = fixture()
    if where == "prior":
        prior = replace(prior, lhs=TodaPrimaryGroup(8, 5))
    elif where == "source":
        source = replace(source, lhs=TodaPrimaryGroup(10, 10))
    elif where == "delta":
        delta = replace(delta, map=TodaDeltaMap(source.lhs, goal.group))
    elif where == "suspension":
        suspension = replace(
            suspension, map=TodaSuspensionMap(source.lhs, goal.group),
        )
    else:
        goal = replace(goal, group=TodaPrimaryGroup(10, 6))
    assert two_summand_quotient_inputs(goal, prior, source, delta, suspension) is None
    assert not expand_two_summand_quotient(goal, prior, source, delta, suspension)


@pytest.mark.parametrize("where", ("prior", "source", "goal"))
def test_rejects_wrong_order(where: str) -> None:
    goal, prior, source, delta, suspension = fixture()
    if where == "prior":
        original = prior.rhs.summands
        prior = replace(prior, rhs=DirectSumGroup(
            (FiniteCyclicGroup(4, original[0].generator), original[1]),
        ))
    elif where == "source":
        source = replace(source, rhs=FiniteCyclicGroup(4, source.rhs.generator))
    else:
        goal = replace(goal, order=4)
    assert two_summand_quotient_inputs(goal, prior, source, delta, suspension) is None


def test_rejects_same_killed_and_surviving_summand() -> None:
    goal, prior, source, delta, suspension = fixture()
    suspension = replace(suspension, source_generator=delta.target_generator)
    assert two_summand_quotient_inputs(goal, prior, source, delta, suspension) is None


def test_rejects_non_independent_basis_generators() -> None:
    goal, prior, source, delta, suspension = fixture()
    a = prior.rhs.summands[0]
    prior = replace(prior, rhs=DirectSumGroup((a, a)))
    assert two_summand_quotient_inputs(goal, prior, source, delta, suspension) is None


def test_rejects_wrong_delta_image_or_generator() -> None:
    goal, prior, source, delta, suspension = fixture()
    delta = replace(delta, target_generator=goal.generator)
    assert two_summand_quotient_inputs(goal, prior, source, delta, suspension) is None
    goal, prior, source, delta, suspension = fixture()
    suspension = replace(suspension, target_generator=delta.target_generator)
    assert two_summand_quotient_inputs(goal, prior, source, delta, suspension) is None


def test_rejects_fake_generator_types_with_only_matching_names() -> None:
    goal, prior, source, delta, suspension = fixture()
    malformed = HomotopyElement(
        "ν₅η₈", 5, source=9, target=4,
        generator=GeneratorSymbol("faked-name"),
    )
    bad = replace(goal, generator=malformed)
    image = replace(suspension, target_generator=malformed)
    assert two_summand_quotient_inputs(bad, prior, source, delta, image) is None


def test_no_assumed_target_as_premise() -> None:
    goal, prior, source, delta, suspension = fixture()
    values = two_summand_quotient_inputs(goal, prior, source, delta, suspension)
    assert values is not None
    assert all(statement != goal for statement in values)
    assert all(statement != Relation(
        goal.group, FiniteCyclicGroup(2, goal.generator), RelationType.EQUALITY,
    ) for statement in values)

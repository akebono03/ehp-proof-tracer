"""Focused isolated proof-contract tests; fabricated steps are fixtures only."""
from __future__ import annotations

import pytest

from expression import Composition, GeneratorSymbol, HomotopyElement
from homotopy_groups import FiniteCyclicGroup, FreeCyclicGroup, TodaDeltaMap, TodaPrimaryGroup
from phase165_r12_r2_quotient_rules import KernelMultipleStatement
from phase174_r3_r7_r35_isolated_cyclic_delta_kernel.rule import (
    RULE_NAME, conditional_inputs, cyclic_delta_kernel_rule,
    expand_cyclic_delta_kernel, expression_coordinates,
)
from proof import (
    InferenceRule, ProofRule, ProofStep, Relation, RelationType,
    find_inference_matches_for_rule, apply_inference_match,
)
from toda_rules import TodaDeltaImageUpToSignStatement


def fixture(q: int = 9, n: int = 5):
    domain = TodaPrimaryGroup(q + 2, 2 * n + 1)
    target = TodaPrimaryGroup(q, n)
    delta = TodaDeltaMap(domain, target)
    iota = HomotopyElement(
        "iota", 2 * n + 1, q + 2, 2 * n + 1,
        GeneratorSymbol("ι", 2 * n + 1),
    )
    nu = HomotopyElement("a", n, q - 1, n, GeneratorSymbol("a", n))
    eta = HomotopyElement("b", q - 1, q, q - 1, GeneratorSymbol("b", q - 1))
    composite = Composition(nu, eta)
    src = Relation(domain, FreeCyclicGroup(iota), RelationType.EQUALITY)
    dst = Relation(target, FiniteCyclicGroup(2, composite), RelationType.EQUALITY)
    image = TodaDeltaImageUpToSignStatement(delta, iota, composite)
    goal = KernelMultipleStatement(delta, domain, iota, 2)
    return goal, src, dst, image


@pytest.mark.parametrize("q,n", [(9, 5), (11, 6), (13, 7), (17, 9)])
def test_general_ehp_windows_support_composition(q, n):
    goal, source, target, image = fixture(q, n)
    assert expression_coordinates(target.rhs.generator) == (q, n)
    assert conditional_inputs(goal, source, target, image) == (source, target, image)
    proposals = expand_cyclic_delta_kernel(goal, (target, image))
    assert len(proposals) == 1
    assert proposals[0].subgoals == (source, target, image)
    assert proposals[0].rule.name == RULE_NAME


def test_real_verified_premise_types_produce_inference_only():
    goal, source, target, image = fixture()
    rule = cyclic_delta_kernel_rule(goal, source, target, image)
    parent = InferenceRule(name="test-only source diagonal inference")
    facts = (
        ProofStep(source, (), ProofRule.INFERENCE, inference_rule=parent),
        ProofStep(target, (), ProofRule.GIVEN),
        ProofStep(image, (), ProofRule.GIVEN),
    )
    matches = find_inference_matches_for_rule(rule, facts)
    assert len(matches) == 1
    derived = apply_inference_match(matches[0])
    assert derived.rule is ProofRule.INFERENCE
    assert derived.conclusion == goal
    assert derived.premises == facts


def test_missing_any_one_of_three_premises_rejects_proof():
    goal, src, dst, image = fixture()
    rule = cyclic_delta_kernel_rule(goal, src, dst, image)
    facts = (
        ProofStep(src, (), ProofRule.INFERENCE),
        ProofStep(dst, (), ProofRule.GIVEN),
        ProofStep(image, (), ProofRule.GIVEN),
    )
    for index in range(3):
        assert not find_inference_matches_for_rule(
            rule, tuple(f for i, f in enumerate(facts) if i != index)
        )


def test_unproved_diagonal_given_not_mistaken_for_inference():
    goal, src, dst, image = fixture()
    rule = cyclic_delta_kernel_rule(goal, src, dst, image)
    facts = (
        ProofStep(src, (), ProofRule.GIVEN),
        ProofStep(dst, (), ProofRule.GIVEN),
        ProofStep(image, (), ProofRule.GIVEN),
    )
    assert not find_inference_matches_for_rule(rule, facts)


def test_wrong_signed_witness_rejected():
    goal, src, dst, image = fixture()
    altered = TodaDeltaImageUpToSignStatement(image.map, image.element, src.rhs.generator)
    assert conditional_inputs(goal, src, dst, altered) is None
    assert expand_cyclic_delta_kernel(goal, (dst, altered)) == ()


def test_wrong_order_rejected():
    goal, src, dst, image = fixture()
    altered = Relation(dst.lhs, FiniteCyclicGroup(4, dst.rhs.generator), RelationType.EQUALITY)
    assert conditional_inputs(goal, src, altered, image) is None
    assert expand_cyclic_delta_kernel(goal, (altered, image)) == ()


def test_wrong_composition_rejected():
    goal, src, dst, image = fixture()
    a = HomotopyElement("a", 5, 7, 5)
    b = HomotopyElement("b", 8, 9, 8)
    broken = Composition(a, b)
    assert expression_coordinates(broken) is None
    wrong = Relation(dst.lhs, FiniteCyclicGroup(2, broken), RelationType.EQUALITY)
    wrong_image = TodaDeltaImageUpToSignStatement(image.map, image.element, broken)
    assert conditional_inputs(goal, src, wrong, wrong_image) is None


def test_ambiguous_source_witnesses_rejected():
    goal, src, dst, image = fixture()
    assert expand_cyclic_delta_kernel(goal, (dst, image, image)) == ()
    assert expand_cyclic_delta_kernel(goal, (dst, dst, image)) == ()


def test_unrelated_goal_does_not_expand():
    assert expand_cyclic_delta_kernel("pi12_7", ()) == ()


def test_no_source_facts_no_proposal():
    goal, src, dst, image = fixture()
    assert expand_cyclic_delta_kernel(goal, ()) == ()
    assert expand_cyclic_delta_kernel(goal, (dst,)) == ()
    assert expand_cyclic_delta_kernel(goal, (image,)) == ()

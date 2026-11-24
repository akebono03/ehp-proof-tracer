"""Synthetic premise fixtures test the rule, not any actual Toda group proof."""
from dataclasses import replace
from math import gcd

import pytest

from expression import Composition, GeneratorSymbol, HomotopyElement, MapApplication, Multiple
from homotopy_groups import FiniteCyclicGroup, TodaDeltaMap, TodaEHPExactnessWindow, TodaHopfInvariantMap, TodaPrimaryGroup
from map_facts import EHP_DELTA_MAP, EHP_E_MAP, EHP_H_MAP
from phase165_r12_r2_quotient_rules import CyclicStructureStatement, KernelMultipleStatement
from phase165_r12_r12_ehp_consequences import EHPImageEqualsKernelStatement
from phase165_r14_r6_generic_iso import MapInjective
from phase176_r3r43r1_finite_cyclic_subgroup_lift_isolated.rule import (
    RULE_NAME, expand_finite_cyclic_subgroup_lift, finite_cyclic_subgroup_lift_inputs,
    finite_cyclic_subgroup_lift_rule,
)
from proof import (InferenceRule, ProofRule, ProofStep, Relation, RelationType,
                   apply_inference_match, find_inference_matches_for_rule)


def fixture(n=3, i=8, m=8, q=4):
    a, b, c = TodaPrimaryGroup(i, n), TodaPrimaryGroup(i, 2*n-1), TodaPrimaryGroup(i-2, n-1)
    x = Composition(HomotopyElement("x", n, i-1, n, GeneratorSymbol("x")),
                    HomotopyElement("y", i-1, i, i-1, GeneratorSymbol("y")))
    y = HomotopyElement("b", 2*n-1, i, 2*n-1, GeneratorSymbol("b"))
    goal = CyclicStructureStatement(a, x, m // gcd(m, q))
    exact = EHPImageEqualsKernelStatement(TodaEHPExactnessWindow(a, b, c, EHP_H_MAP, EHP_DELTA_MAP))
    group = Relation(b, FiniteCyclicGroup(m, y), RelationType.EQUALITY)
    kernel = KernelMultipleStatement(TodaDeltaMap(b, c), b, y, q)
    image = Relation(MapApplication(EHP_H_MAP, x), Multiple(q, y), RelationType.EQUALITY)
    return goal, exact, group, kernel, image


def inferred(value, kind=ProofRule.INFERENCE):
    return ProofStep(value, (), kind, inference_rule=InferenceRule("synthetic test fixture only"))


@pytest.mark.parametrize("n,i,m,q,order", [(3,8,8,4,2), (4,10,16,6,8), (5,12,8,3,8), (4,10,8,8,1), (4,10,8,12,2)])
def test_general_order_and_replay(n, i, m, q, order):
    args = fixture(n, i, m, q)
    goal, exact, group, kernel, image = args
    assert goal.order == order
    required = finite_cyclic_subgroup_lift_inputs(*args)
    assert required == (MapInjective(TodaHopfInvariantMap(goal.group, group.lhs)), exact, group, kernel, image)
    options = expand_finite_cyclic_subgroup_lift(*args)
    assert len(options) == 1
    assert options[0].subgoals == required
    assert all(not isinstance(v, ProofStep) for v in required)
    assert options[0].rule.name == RULE_NAME
    parents = tuple(inferred(v) for v in required)
    matches = find_inference_matches_for_rule(options[0].rule, parents)
    assert len(matches) == 1
    step = apply_inference_match(matches[0])
    assert step.conclusion == goal and step.rule is ProofRule.INFERENCE
    assert step.premises == parents


@pytest.mark.parametrize("index", range(5))
def test_missing_premise_rejected(index):
    args = fixture()
    required = finite_cyclic_subgroup_lift_inputs(*args)
    parents = tuple(inferred(v) for j, v in enumerate(required) if j != index)
    assert not find_inference_matches_for_rule(finite_cyclic_subgroup_lift_rule(*args), parents)


@pytest.mark.parametrize("index", range(5))
def test_given_not_accepted_as_inferred_premise(index):
    args = fixture()
    required = finite_cyclic_subgroup_lift_inputs(*args)
    parents = tuple(inferred(v, ProofRule.GIVEN if j == index else ProofRule.INFERENCE)
                    for j, v in enumerate(required))
    assert not find_inference_matches_for_rule(finite_cyclic_subgroup_lift_rule(*args), parents)


@pytest.mark.parametrize("case", ["order", "bool_order", "bad_m", "bool_m", "window_map", "window_term",
                                  "kernel_map", "kernel_domain", "kernel_generator", "image_map", "image_source",
                                  "image_coefficient", "image_generator", "bad_composition", "bad_codomain_generator"])
def test_incompatible_witnesses_rejected(case):
    goal, exact, group, kernel, image = fixture()
    y = group.rhs.generator
    other = replace(y, generator=GeneratorSymbol("other"))
    if case == "order":
        goal = replace(goal, order=4)
    elif case == "bool_order":
        # The existing statement constructor rejects bool; bypass is not needed.
        with pytest.raises(ValueError):
            replace(goal, order=True)
        return
    elif case == "bad_m":
        group = replace(group, rhs=replace(group.rhs, order=0))
    elif case == "bool_m":
        group = replace(group, rhs=replace(group.rhs, order=True))
    elif case == "window_map":
        exact = replace(exact, window=replace(exact.window, second_map=EHP_E_MAP))
    elif case == "window_term":
        exact = replace(exact, window=replace(exact.window, target_term=TodaPrimaryGroup(7,2)))
    elif case == "kernel_map":
        kernel = replace(kernel, map=TodaDeltaMap(group.lhs, TodaPrimaryGroup(7,2)))
    elif case == "kernel_domain":
        kernel = replace(kernel, domain=goal.group)
    elif case == "kernel_generator":
        kernel = replace(kernel, source_generator=other)
    elif case == "image_map":
        image = replace(image, lhs=MapApplication(EHP_E_MAP, goal.generator))
    elif case == "image_source":
        image = replace(image, lhs=MapApplication(EHP_H_MAP, replace(goal.generator, left=replace(goal.generator.left, generator=GeneratorSymbol("other")))))
    elif case == "image_coefficient":
        image = replace(image, rhs=Multiple(2,y))
    elif case == "image_generator":
        image = replace(image, rhs=Multiple(4,other))
    elif case == "bad_composition":
        goal = replace(goal, generator=replace(goal.generator, right=replace(goal.generator.right, target=6, dimension=6)))
        image = replace(image, lhs=MapApplication(EHP_H_MAP, goal.generator))
    elif case == "bad_codomain_generator":
        wrong = replace(y, source=9)
        group = replace(group, rhs=replace(group.rhs, generator=wrong))
        kernel = replace(kernel, source_generator=wrong)
        image = replace(image, rhs=Multiple(4,wrong))
    args = goal, exact, group, kernel, image
    assert finite_cyclic_subgroup_lift_inputs(*args) is None
    assert expand_finite_cyclic_subgroup_lift(*args) == ()
    with pytest.raises(ValueError):
        finite_cyclic_subgroup_lift_rule(*args)


def test_bool_image_coefficient_is_not_integer_one():
    goal, exact, group, kernel, image = fixture(q=1)
    invalid = replace(image, rhs=Multiple(True, group.rhs.generator))
    assert finite_cyclic_subgroup_lift_inputs(goal, exact, group, kernel, invalid) is None
    required = finite_cyclic_subgroup_lift_inputs(goal, exact, group, kernel, image)
    parents = tuple(inferred(v) for v in required[:-1]) + (inferred(invalid),)
    assert not find_inference_matches_for_rule(
        finite_cyclic_subgroup_lift_rule(goal, exact, group, kernel, image), parents)


def test_wrong_verified_injection_does_not_match():
    args = fixture()
    required = finite_cyclic_subgroup_lift_inputs(*args)
    wrong = MapInjective(TodaHopfInvariantMap(args[0].group, TodaPrimaryGroup(9,5)))
    parents = (inferred(wrong),) + tuple(inferred(v) for v in required[1:])
    assert not find_inference_matches_for_rule(finite_cyclic_subgroup_lift_rule(*args), parents)


def test_actual_shape_is_only_a_candidate():
    goal, exact, group, kernel, image = fixture()
    nu_prime = HomotopyElement("ν′",3,6,3,GeneratorSymbol("ν",decoration="′"))
    eta6 = HomotopyElement("η₆",6,7,6,GeneratorSymbol("η",6))
    eta7 = HomotopyElement("η₇",7,8,7,GeneratorSymbol("η",7))
    nu5 = HomotopyElement("ν₅",5,8,5,GeneratorSymbol("ν",5))
    x = Composition(nu_prime, Composition(eta6,eta7))
    goal = replace(goal, generator=x)
    group = replace(group, rhs=FiniteCyclicGroup(8,nu5))
    kernel = replace(kernel, source_generator=nu5)
    image = Relation(MapApplication(EHP_H_MAP,x), Multiple(4,nu5), RelationType.EQUALITY)
    options = expand_finite_cyclic_subgroup_lift(goal, exact, group, kernel, image)
    assert len(options) == 1 and len(options[0].subgoals) == 5
    assert not find_inference_matches_for_rule(options[0].rule, ())

"""R32 isolated conditional kernel contract, no fabricated certified proof."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import GeneratorSymbol, HomotopyElement, Zero
from homotopy_groups import (
    FiniteCyclicGroup, FreeCyclicGroup, TodaDeltaMap, TodaPrimaryGroup,
)
from phase165_r12_r2_quotient_rules import KernelMultipleStatement
from phase174_r3_r7_r32_lower_delta_kernel_audit.kernel_contract import (
    conditional_kernel_premises, generator_has_group_coordinates,
    signed_cyclic_kernel_membership, valid_ehp_lower_delta,
)
from proof import Relation, RelationType
from toda_rules import TodaDeltaImageUpToSignStatement


def fixture(q: int = 9, n: int = 5, order: int = 2):
    delta = TodaDeltaMap(TodaPrimaryGroup(q + 2, 2 * n + 1), TodaPrimaryGroup(q, n))
    g = HomotopyElement("g", q + 2, q + 2, 2 * n + 1, GeneratorSymbol("g", n))
    h = HomotopyElement("h", q, q, n, GeneratorSymbol("h", n))
    goal = KernelMultipleStatement(delta, delta.source_group, g, order)
    domain = Relation(delta.source_group, FreeCyclicGroup(g), RelationType.EQUALITY)
    codomain = Relation(delta.target_group, FiniteCyclicGroup(order, h), RelationType.EQUALITY)
    signed = TodaDeltaImageUpToSignStatement(delta, g, h)
    return goal, domain, codomain, signed


@pytest.mark.parametrize("q,n,order", ((9, 5, 2), (11, 6, 4), (13, 7, 3), (17, 9, 8)))
def test_generic_well_typed_finite_cyclic_kernel_hypotheses(q: int, n: int, order: int):
    goal, source, target, signed = fixture(q, n, order)
    assert valid_ehp_lower_delta(goal.map)
    assert conditional_kernel_premises(goal, source, target, signed) == (
        source, target, signed,
    )


@pytest.mark.parametrize("order", (1, 2, 3, 4, 8, 13))
def test_cyclic_kernel_arithmetic_for_positive_and_negative_signs(order: int):
    for coefficient in range(-3 * order - 1, 3 * order + 2):
        for sign in (-1, 1):
            assert signed_cyclic_kernel_membership(order, coefficient, sign) == (
                coefficient % order == 0
            )


@pytest.mark.parametrize("bad", ((0, 0, 1), (-1, 2, 1), (2, True, 1),
                                      (2, 2, 0), (2, 2, 3), (2, 2, True),
                                      (2, 2.5, 1), (True, 2, 1)))
def test_arithmetic_rejects_untyped_inputs(bad):
    with pytest.raises(ValueError):
        signed_cyclic_kernel_membership(*bad)


def test_incorrect_map_dimensions_and_fake_map_rejected():
    goal, source, target, signed = fixture()
    assert not valid_ehp_lower_delta(TodaDeltaMap(
        TodaPrimaryGroup(12, 11), goal.map.target_group,
    ))
    assert not valid_ehp_lower_delta("Delta")
    assert not valid_ehp_lower_delta(TodaDeltaMap(
        TodaPrimaryGroup(5, 3), TodaPrimaryGroup(3, 1),
    ))
    wrong = replace(goal, map=TodaDeltaMap(
        TodaPrimaryGroup(12, 11), goal.map.target_group,
    ))
    assert conditional_kernel_premises(wrong, source, target, signed) is None


def test_wrong_kernel_multiple_is_rejected():
    goal, source, target, signed = fixture(order=4)
    assert conditional_kernel_premises(replace(goal, multiple=2), source, target, signed) is None


def test_source_generator_and_source_group_must_match_exactly():
    goal, source, target, signed = fixture()
    other = HomotopyElement("g-prime", 11, 11, 11)
    wrong = replace(source, rhs=FreeCyclicGroup(other))
    assert conditional_kernel_premises(goal, wrong, target, signed) is None
    assert conditional_kernel_premises(goal, replace(source, lhs=TodaPrimaryGroup(10, 10)),
                                       target, signed) is None
    assert conditional_kernel_premises(replace(goal, domain=TodaPrimaryGroup(10, 10)),
                                       source, target, signed) is None


def test_target_must_be_finite_cyclic_with_exact_generator():
    goal, source, target, signed = fixture()
    wrong_gen = HomotopyElement("h-other", 9, 9, 5)
    assert conditional_kernel_premises(goal, source, replace(target, rhs=FiniteCyclicGroup(2, wrong_gen)),
                                       signed) is None
    assert conditional_kernel_premises(goal, source, replace(target, rhs=FreeCyclicGroup(wrong_gen)),
                                       signed) is None
    assert conditional_kernel_premises(goal, source, replace(target, lhs=TodaPrimaryGroup(9, 6)),
                                       signed) is None
    assert conditional_kernel_premises(goal, source, replace(target, rhs=FiniteCyclicGroup(2, Zero())),
                                       signed) is None


def test_signed_generator_witness_must_be_exact_map_and_elements():
    goal, source, target, signed = fixture()
    wrong_source = HomotopyElement("g-other", 11, 11, 11)
    wrong_target = HomotopyElement("h-other", 9, 9, 5)
    for bad in (replace(signed, element=wrong_source),
                replace(signed, positive_value=wrong_target),
                replace(signed, map=TodaDeltaMap(TodaPrimaryGroup(13, 13), TodaPrimaryGroup(11, 6)))):
        assert conditional_kernel_premises(goal, source, target, bad) is None
    assert conditional_kernel_premises(goal, source, target, "(5.10)") is None


def test_wrong_relation_kind_and_untyped_element_rejected():
    goal, source, target, signed = fixture()
    assert conditional_kernel_premises(goal, replace(source, relation_type=RelationType.ORDER),
                                       target, signed) is None
    assert conditional_kernel_premises(goal, source, replace(target, relation_type=RelationType.ORDER),
                                       signed) is None
    assert not generator_has_group_coordinates(Zero(), goal.map.target_group)
    assert not generator_has_group_coordinates(
        HomotopyElement("wrong-degree", 9, 11, 5), goal.map.target_group,
    )


def test_no_raw_goal_is_accepted_as_source_evidence():
    goal, source, target, signed = fixture()
    assert conditional_kernel_premises(goal, goal, target, signed) is None
    assert conditional_kernel_premises(goal, source, goal, signed) is None
    assert conditional_kernel_premises(goal, source, target, goal) is None

"""R52-R23: reverse adapters to existing Toda pi4^3 proof rules.

Only map existing rules to typed subgoals.  No facts are manufactured.
"""
from __future__ import annotations

from expression import GeneratorSymbol, HomotopyElement, Multiple, Suspension
from homotopy_groups import (
    FiniteCyclicGroup,
    FreeCyclicGroup,
    TodaDeltaMap,
    TodaEHPExactnessWindow,
    TodaPrimaryGroup,
    TodaPrimaryGroupZeroStatement,
    TodaSuspensionMap,
)
from map_facts import EHP_DELTA_MAP, EHP_E_MAP, EHP_H_MAP
from phase165_r3_recursive_search import GoalExpansion
from proof import Relation, RelationType
import toda_rules as rules


def _eta(index: int) -> HomotopyElement:
    return HomotopyElement(
        name=f"η{str(index).translate(str.maketrans('0123456789', '₀₁₂₃₄₅₆₇₈₉'))}",
        dimension=index,
        source=index + 1,
        target=index,
        generator=GeneratorSymbol(family="η", index=index),
    )


def _iota5() -> HomotopyElement:
    return HomotopyElement(
        name="ι_5", dimension=5,
        generator=GeneratorSymbol(family="ι", index=5),
    )


def _objects():
    source = TodaPrimaryGroup(3, 2)
    target = TodaPrimaryGroup(4, 3)
    delta_source = TodaPrimaryGroup(5, 5)
    e = TodaSuspensionMap(source_group=source, target_group=target)
    delta = TodaDeltaMap(source_group=delta_source, target_group=source)
    eta2 = _eta(2)
    eta3 = _eta(3)
    twice = Multiple(coefficient=2, expression=eta2)
    return source, target, delta_source, e, delta, eta2, eta3, twice


def expand_existing_pi43_rules(goal: object) -> tuple[GoalExpansion, ...]:
    """Use five historic rules where inverse premises can be reconstructed.

    The Delta-image rule requires additional typed Whitehead-square premises;
    its inverse is deliberately not synthesized without those source witnesses.
    """
    source, target, delta_source, e, delta, eta2, eta3, twice = _objects()
    if isinstance(goal, Relation) and goal.relation_type is RelationType.EQUALITY:
        if goal.lhs == target and goal.rhs == FiniteCyclicGroup(2, eta3):
            return (GoalExpansion(
                rules.toda_pi4_3_eta3_generator_inference_rule(),
                (
                    Relation(target, FiniteCyclicGroup(2, Suspension(expression=eta2))),
                    Relation(eta3, Suspension(expression=eta2)),
                ),
            ),)
        if goal.lhs == target and goal.rhs == FiniteCyclicGroup(2, Suspension(expression=eta2)):
            return (GoalExpansion(
                rules.toda_pi4_3_finite_cyclic_inference_rule(),
                (
                    Relation(source, FreeCyclicGroup(eta2)),
                    rules.TodaSuspensionKernelFreeCyclicStatement(
                        map=e, kernel_group=FreeCyclicGroup(twice),
                    ),
                    rules.TodaSuspensionSurjectiveStatement(map=e),
                ),
            ),)
    if isinstance(goal, rules.TodaSuspensionKernelFreeCyclicStatement):
        if goal.map == e and goal.kernel_group == FreeCyclicGroup(twice):
            return (GoalExpansion(
                rules.toda_pi4_3_exactness_delta_image_to_suspension_kernel_inference_rule(),
                (
                    rules.TodaDeltaImageFreeCyclicStatement(
                        map=delta, image_group=FreeCyclicGroup(twice),
                    ),
                    rules.TodaProp42ExactnessStatement(
                        TodaEHPExactnessWindow(
                            source_term=delta_source, middle_term=source,
                            target_term=target, first_map=EHP_DELTA_MAP,
                            second_map=EHP_E_MAP,
                        ),
                    ),
                ),
            ),)
    if isinstance(goal, rules.TodaSuspensionSurjectiveStatement):
        if goal.map == e:
            return (GoalExpansion(
                rules.toda_pi4_3_zero_right_implies_suspension_surjective_inference_rule(),
                (
                    TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(4, 5)),
                    rules.TodaProp42ExactnessStatement(
                        TodaEHPExactnessWindow(
                            source_term=source, middle_term=target,
                            target_term=TodaPrimaryGroup(4, 5),
                            first_map=EHP_E_MAP, second_map=EHP_H_MAP,
                        ),
                    ),
                ),
            ),)
    return ()

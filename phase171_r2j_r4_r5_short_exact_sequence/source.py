"""Typed short-exact consequence of EHP exactness, E injective and H surjective.

This module contains no source assertions, completed group presentations,
or claims about the order or generator of the middle group.
"""
from __future__ import annotations

from dataclasses import dataclass

from homotopy_groups import (
    TodaEHPExactnessWindow,
    TodaHopfInvariantMap,
    TodaPrimaryGroup,
    TodaSuspensionMap,
)
from map_facts import EHP_E_MAP, EHP_H_MAP
from phase165_r12_r11_prop42_unified import prop42_exactness_indices
from phase165_r14_r6_generic_iso import MapInjective, MapSurjective
from phase165_r3_recursive_search import GoalExpansion
from proof import InferenceRule, PremisePattern, ProofRule
from toda_rules import TodaProp42ExactnessStatement


@dataclass(frozen=True)
class EHPShortExactSequence:
    """The five-term sequence 0 -> source -> middle -> target -> 0."""

    source_group: TodaPrimaryGroup
    middle_group: TodaPrimaryGroup
    target_group: TodaPrimaryGroup
    injection: TodaSuspensionMap
    projection: TodaHopfInvariantMap


def short_exact_from_ehp(
    injection: object,
    exactness: object,
    projection: object,
) -> EHPShortExactSequence | None:
    """Validate all three well-typed, compatible mathematical premises.

    Matching names is not enough: the specialized EHP window must be valid,
    and both map endpoints must agree with all three group objects.
    """
    if (
        not isinstance(injection, MapInjective)
        or not isinstance(exactness, TodaProp42ExactnessStatement)
        or not isinstance(projection, MapSurjective)
        or not isinstance(exactness.window, TodaEHPExactnessWindow)
    ):
        return None
    window = exactness.window
    if (
        prop42_exactness_indices(exactness) is None
        or prop42_exactness_indices(exactness)[2] != "e_h"
        or (window.first_map, window.second_map) != (EHP_E_MAP, EHP_H_MAP)
        or not all(isinstance(group, TodaPrimaryGroup) for group in (
            window.source_term,
            window.middle_term,
            window.target_term,
        ))
    ):
        return None
    required_injection = TodaSuspensionMap(window.source_term, window.middle_term)
    required_projection = TodaHopfInvariantMap(window.middle_term, window.target_term)
    if injection.map != required_injection or projection.map != required_projection:
        return None
    return EHPShortExactSequence(
        source_group=window.source_term,
        middle_group=window.middle_term,
        target_group=window.target_term,
        injection=required_injection,
        projection=required_projection,
    )


def ehp_short_exact_rule(goal: EHPShortExactSequence) -> InferenceRule:
    """Deduce 0 -> A -> B -> C -> 0 from three independently inferred facts."""
    if not isinstance(goal, EHPShortExactSequence):
        raise TypeError("typed EHPShortExactSequence goal required")

    def guard(premises, bindings):
        return (
            len(premises) == 3
            and all(step.rule is ProofRule.INFERENCE for step in premises)
            and short_exact_from_ehp(
                premises[0].conclusion,
                premises[1].conclusion,
                premises[2].conclusion,
            ) == goal
        )

    return InferenceRule(
        name="EHP exactness with injective E and surjective H implies short exact sequence",
        premise_patterns=(
            PremisePattern(proof_rule=ProofRule.INFERENCE, statement_type=MapInjective),
            PremisePattern(
                proof_rule=ProofRule.INFERENCE,
                statement_type=TodaProp42ExactnessStatement,
            ),
            PremisePattern(proof_rule=ProofRule.INFERENCE, statement_type=MapSurjective),
        ),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def expand_ehp_short_exact(
    goal: object,
) -> tuple[GoalExpansion, ...]:
    """Backward obligations only; no source leaf or assumed group structure."""
    if not isinstance(goal, EHPShortExactSequence):
        return ()
    window = TodaEHPExactnessWindow(
        source_term=goal.source_group,
        middle_term=goal.middle_group,
        target_term=goal.target_group,
        first_map=EHP_E_MAP,
        second_map=EHP_H_MAP,
    )
    premises = (
        MapInjective(goal.injection),
        TodaProp42ExactnessStatement(window),
        MapSurjective(goal.projection),
    )
    if short_exact_from_ehp(*premises) != goal:
        return ()
    return (GoalExpansion(ehp_short_exact_rule(goal), premises),)

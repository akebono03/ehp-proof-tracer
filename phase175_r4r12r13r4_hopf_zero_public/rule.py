"""Generic EHP intermediate Hopf-zero rules for the shared backward search.

The zero-map conclusion is about H, NOT about its codomain group. Both
consecutive exactness windows are checked using Toda Proposition 4.2 indices.
This module supplies conditional rules only; no literature GIVEN is created.
"""
from __future__ import annotations

from homotopy_groups import (
    TodaDeltaMap,
    TodaEHPExactnessWindow,
    TodaHopfInvariantMap,
    TodaPrimaryGroup,
    TodaSuspensionMap,
)
from map_facts import EHP_DELTA_MAP, EHP_E_MAP, EHP_H_MAP
from phase165_r12_r11_prop42_unified import prop42_exactness_indices
from phase165_r14_r6_generic_iso import MapInjective, MapSurjective
from phase165_r3_recursive_search import GoalExpansion
from proof import InferenceRule, PremisePattern, ProofRule
from toda_rules import TodaHopfInvariantZeroStatement, TodaProp42ExactnessStatement


DELTA_TO_H_ZERO = "EHP injective Delta and H-Delta exactness imply zero Hopf map"
H_ZERO_TO_E_SURJ = "EHP zero Hopf map and E-H exactness imply suspension surjectivity"


def hopf_zero_inputs(goal: object) -> tuple[MapInjective, TodaProp42ExactnessStatement] | None:
    """Require the unique correctly indexed H-Delta exactness window."""
    if not isinstance(goal, TodaHopfInvariantZeroStatement):
        return None
    h = goal.map
    if not isinstance(h, TodaHopfInvariantMap):
        return None
    b, c = h.source_group, h.target_group
    if not isinstance(b, TodaPrimaryGroup) or not isinstance(c, TodaPrimaryGroup):
        return None
    if any(type(x) is not int for x in (
        b.group_dimension, b.sphere_dimension, c.group_dimension, c.sphere_dimension,
    )):
        return None
    n = b.sphere_dimension - 1
    i = b.group_dimension
    if n < 1 or c != TodaPrimaryGroup(i, 2 * n + 1):
        return None
    d = TodaPrimaryGroup(i - 2, n)
    exact = TodaProp42ExactnessStatement(TodaEHPExactnessWindow(
        source_term=b,
        middle_term=c,
        target_term=d,
        first_map=EHP_H_MAP,
        second_map=EHP_DELTA_MAP,
    ))
    if prop42_exactness_indices(exact) != (n, i, "h_delta"):
        return None
    return MapInjective(TodaDeltaMap(c, d)), exact


def hopf_zero_from_injective_delta_rule(goal: TodaHopfInvariantZeroStatement) -> InferenceRule:
    required = hopf_zero_inputs(goal)
    if required is None:
        raise ValueError("invalid typed H-Delta zero-map goal")

    def guard(premises, bindings):
        return (
            len(premises) == 2
            and all(step.rule is ProofRule.INFERENCE for step in premises)
            and tuple(step.conclusion for step in premises) == required
            and hopf_zero_inputs(goal) == required
        )

    return InferenceRule(
        name=DELTA_TO_H_ZERO,
        description=(
            "Exactness gives im(H)=ker(Delta); an independently proved "
            "injective Delta has zero kernel, hence H is the zero map."
        ),
        premise_patterns=(
            PremisePattern(proof_rule=ProofRule.INFERENCE,
                           statement_type=MapInjective, statement_pattern=required[0]),
            PremisePattern(proof_rule=ProofRule.INFERENCE,
                           statement_type=TodaProp42ExactnessStatement,
                           statement_pattern=required[1]),
        ),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def expand_hopf_zero_from_injective_delta(goal: object) -> tuple[GoalExpansion, ...]:
    required = hopf_zero_inputs(goal)
    if required is None:
        return ()
    return (GoalExpansion(hopf_zero_from_injective_delta_rule(goal), required),)


def suspension_surjective_inputs(
    goal: object,
) -> tuple[TodaHopfInvariantZeroStatement, TodaProp42ExactnessStatement] | None:
    """Require actual H=0, rather than the false shortcut that codomain(H)=0."""
    if not isinstance(goal, MapSurjective):
        return None
    e = goal.map
    if not isinstance(e, TodaSuspensionMap):
        return None
    a, b = e.source_group, e.target_group
    if not isinstance(a, TodaPrimaryGroup) or not isinstance(b, TodaPrimaryGroup):
        return None
    if any(type(x) is not int for x in (
        a.group_dimension, a.sphere_dimension, b.group_dimension, b.sphere_dimension,
    )):
        return None
    if b != TodaPrimaryGroup(a.group_dimension + 1, a.sphere_dimension + 1):
        return None
    n = a.sphere_dimension
    i = b.group_dimension
    c = TodaPrimaryGroup(i, 2 * n + 1)
    exact = TodaProp42ExactnessStatement(TodaEHPExactnessWindow(
        source_term=a,
        middle_term=b,
        target_term=c,
        first_map=EHP_E_MAP,
        second_map=EHP_H_MAP,
    ))
    if prop42_exactness_indices(exact) != (n, i, "e_h"):
        return None
    return TodaHopfInvariantZeroStatement(TodaHopfInvariantMap(b, c)), exact


def suspension_surjective_from_zero_hopf_rule(goal: MapSurjective) -> InferenceRule:
    required = suspension_surjective_inputs(goal)
    if required is None:
        raise ValueError("invalid typed E-H surjectivity goal")

    def guard(premises, bindings):
        return (
            len(premises) == 2
            and all(step.rule is ProofRule.INFERENCE for step in premises)
            and tuple(step.conclusion for step in premises) == required
            and suspension_surjective_inputs(goal) == required
        )

    return InferenceRule(
        name=H_ZERO_TO_E_SURJ,
        description=(
            "Exactness gives im(E)=ker(H); an independently proved zero "
            "Hopf map has full kernel, so E is surjective."
        ),
        premise_patterns=(
            PremisePattern(proof_rule=ProofRule.INFERENCE,
                           statement_type=TodaHopfInvariantZeroStatement,
                           statement_pattern=required[0]),
            PremisePattern(proof_rule=ProofRule.INFERENCE,
                           statement_type=TodaProp42ExactnessStatement,
                           statement_pattern=required[1]),
        ),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def expand_suspension_surjective_from_zero_hopf(
    goal: object,
) -> tuple[GoalExpansion, ...]:
    required = suspension_surjective_inputs(goal)
    if required is None:
        return ()
    return (GoalExpansion(suspension_surjective_from_zero_hopf_rule(goal), required),)

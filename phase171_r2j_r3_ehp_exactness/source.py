"""Prove Delta=0 and E injective from already proved typed EHP premises.

No source or target group is assumed, and no new GIVEN is introduced.
An explicit, well-indexed Proposition 4.2 window is required at each step.
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
from toda_rules import TodaDeltaZeroStatement, TodaProp42ExactnessStatement


def _h_delta_inputs(goal: object) -> tuple[MapSurjective, TodaProp42ExactnessStatement] | None:
    if not isinstance(goal, TodaDeltaZeroStatement) or not isinstance(goal.map, TodaDeltaMap):
        return None
    delta = goal.map
    group, target = delta.source_group, delta.target_group
    if not isinstance(group, TodaPrimaryGroup) or not isinstance(target, TodaPrimaryGroup):
        return None
    q, h_sphere, n = group.group_dimension, group.sphere_dimension, target.sphere_dimension
    if not all(type(x) is int for x in (q, h_sphere, n)):
        return None
    if n < 1 or h_sphere != 2 * n + 1 or target.group_dimension != q - 2:
        return None
    h_source = TodaPrimaryGroup(q, n + 1)
    exact = TodaProp42ExactnessStatement(TodaEHPExactnessWindow(
        source_term=h_source, middle_term=group, target_term=target,
        first_map=EHP_H_MAP, second_map=EHP_DELTA_MAP,
    ))
    if prop42_exactness_indices(exact) is None:
        return None
    return MapSurjective(TodaHopfInvariantMap(h_source, group)), exact


def _delta_e_inputs(goal: object) -> tuple[TodaDeltaZeroStatement, TodaProp42ExactnessStatement] | None:
    if not isinstance(goal, MapInjective) or not isinstance(goal.map, TodaSuspensionMap):
        return None
    suspension = goal.map
    source, target = suspension.source_group, suspension.target_group
    if not isinstance(source, TodaPrimaryGroup) or not isinstance(target, TodaPrimaryGroup):
        return None
    q, n = source.group_dimension, source.sphere_dimension
    if not all(type(x) is int for x in (
        q, n, target.group_dimension, target.sphere_dimension,
    )) or n < 1 or target != TodaPrimaryGroup(q + 1, n + 1):
        return None
    previous = TodaPrimaryGroup(q + 2, 2 * n + 1)
    delta_zero = TodaDeltaZeroStatement(TodaDeltaMap(previous, source))
    exact = TodaProp42ExactnessStatement(TodaEHPExactnessWindow(
        source_term=previous, middle_term=source, target_term=target,
        first_map=EHP_DELTA_MAP, second_map=EHP_E_MAP,
    ))
    if prop42_exactness_indices(exact) is None:
        return None
    return delta_zero, exact


def delta_zero_from_surjective_hopf_rule(goal: TodaDeltaZeroStatement) -> InferenceRule:
    """When im(H) is all of B=ker(Delta), Delta is the zero map."""
    inputs = _h_delta_inputs(goal)
    if inputs is None:
        raise ValueError("invalid typed H-Delta exactness goal")

    def guard(premises, bindings):
        return (
            len(premises) == 2
            and all(step.rule is ProofRule.INFERENCE for step in premises)
            and (premises[0].conclusion, premises[1].conclusion) == inputs
            and _h_delta_inputs(goal) == inputs
        )

    return InferenceRule(
        name="EHP H surjectivity and H-Delta exactness imply zero Delta",
        premise_patterns=(
            PremisePattern(proof_rule=ProofRule.INFERENCE, statement_type=MapSurjective),
            PremisePattern(proof_rule=ProofRule.INFERENCE, statement_type=TodaProp42ExactnessStatement),
        ),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def suspension_injective_from_zero_delta_rule(goal: MapInjective) -> InferenceRule:
    """Exactness im(Delta)=ker(E) and Delta=0 force E injective."""
    inputs = _delta_e_inputs(goal)
    if inputs is None:
        raise ValueError("invalid typed Delta-E exactness goal")

    def guard(premises, bindings):
        return (
            len(premises) == 2
            and all(step.rule is ProofRule.INFERENCE for step in premises)
            and (premises[0].conclusion, premises[1].conclusion) == inputs
            and _delta_e_inputs(goal) == inputs
        )

    return InferenceRule(
        name="EHP zero Delta and Delta-E exactness imply suspension injectivity",
        premise_patterns=(
            PremisePattern(proof_rule=ProofRule.INFERENCE, statement_type=TodaDeltaZeroStatement),
            PremisePattern(proof_rule=ProofRule.INFERENCE, statement_type=TodaProp42ExactnessStatement),
        ),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def expand_cited_ehp_surjectivity_consequences(goal: object) -> tuple[GoalExpansion, ...]:
    """Generic backward goals only; actual premises must be reconstructed."""
    hd = _h_delta_inputs(goal)
    if hd is not None:
        return (GoalExpansion(delta_zero_from_surjective_hopf_rule(goal), hd),)
    de = _delta_e_inputs(goal)
    if de is not None:
        return (GoalExpansion(suspension_injective_from_zero_delta_rule(goal), de),)
    return ()

"""Conditional Delta-E exactness rule; no source registration or public hook."""
from __future__ import annotations

from homotopy_groups import (
    TodaDeltaMap, TodaEHPExactnessWindow, TodaPrimaryGroup, TodaSuspensionMap,
)
from map_facts import EHP_DELTA_MAP, EHP_E_MAP
from map_property_rules import ImageZeroStatement
from phase165_r12_r11_prop42_unified import prop42_exactness_indices
from phase165_r14_r6_generic_iso import MapSurjective
from phase165_r3_recursive_search import GoalExpansion
from proof import InferenceRule, PremisePattern, ProofRule
from toda_rules import TodaProp42ExactnessStatement

RULE_NAME = 'EHP Delta-E exactness and zero suspension image imply Delta surjectivity'


def delta_surjective_inputs(goal: object):
    """Reconstruct a typed consecutive window, not a zero-group hypothesis."""
    if type(goal) is not MapSurjective or type(goal.map) is not TodaDeltaMap:
        return None
    delta = goal.map
    a, b = delta.source_group, delta.target_group
    if type(a) is not TodaPrimaryGroup or type(b) is not TodaPrimaryGroup:
        return None
    if any(type(v) is not int for g in (a, b)
           for v in (g.group_dimension, g.sphere_dimension)):
        return None
    q, n = b.group_dimension, b.sphere_dimension
    if n < 2 or q < n or a != TodaPrimaryGroup(q + 2, 2*n + 1):
        return None
    c = TodaPrimaryGroup(q + 1, n + 1)
    exact = TodaProp42ExactnessStatement(TodaEHPExactnessWindow(
        a, b, c, EHP_DELTA_MAP, EHP_E_MAP,
    ))
    if prop42_exactness_indices(exact) != (n, q + 1, 'delta_e'):
        return None
    return exact, ImageZeroStatement(TodaSuspensionMap(b, c))


def delta_surjective_from_zero_suspension_rule(goal: MapSurjective) -> InferenceRule:
    required = delta_surjective_inputs(goal)
    if required is None:
        raise ValueError('invalid typed Delta-E surjectivity goal')

    def guard(premises, bindings):
        return (
            len(premises) == 2
            and all(p.rule is ProofRule.INFERENCE for p in premises)
            and tuple(p.conclusion for p in premises) == required
            and delta_surjective_inputs(goal) == required
        )

    return InferenceRule(
        name=RULE_NAME,
        description='Exactness gives im(Delta)=ker(E). If E has zero image, its kernel is the whole domain, hence Delta is surjective.',
        premise_patterns=(
            PremisePattern(proof_rule=ProofRule.INFERENCE,
                           statement_type=TodaProp42ExactnessStatement,
                           statement_pattern=required[0]),
            PremisePattern(proof_rule=ProofRule.INFERENCE,
                           statement_type=ImageZeroStatement,
                           statement_pattern=required[1]),
        ),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def expand_delta_surjective_from_zero_suspension(goal: object):
    required = delta_surjective_inputs(goal)
    if required is None:
        return ()
    return (GoalExpansion(delta_surjective_from_zero_suspension_rule(goal), required),)

"""Conditional equal-cardinality injectivity; no provider or source registration."""
from __future__ import annotations

from homotopy_groups import TodaDeltaMap, TodaHopfInvariantMap, TodaSuspensionMap
from phase165_r14_r6_generic_iso import MapInjective, MapSurjective
from phase165_r3_recursive_search import GoalExpansion
from phase171_r2j_r4_r6_middle_cardinality.source import FiniteGroupCardinality
from phase174_r3_r7_r32_lower_delta_kernel_audit.kernel_contract import valid_ehp_lower_delta
from phase177_r14_finite_cyclic_delta_injective_isolated.rule import group_endpoints
from proof import InferenceRule, PremisePattern, ProofRule

RULE_NAME = 'surjective homomorphism between finite groups of equal cardinality is injective'


def valid_finite_group_map(mapping: object) -> bool:
    """Accept concrete typed EHP homomorphisms, not arbitrary map-shaped objects."""
    if type(mapping) not in (TodaDeltaMap, TodaHopfInvariantMap, TodaSuspensionMap):
        return False
    a = group_endpoints(mapping.source_group)
    b = group_endpoints(mapping.target_group)
    if a is None or b is None:
        return False
    q, n = a
    if type(mapping) is TodaSuspensionMap:
        return b == (q + 1, n + 1)
    if type(mapping) is TodaHopfInvariantMap:
        return n >= 3 and b == (q, 2*n - 1)
    return valid_ehp_lower_delta(mapping)


def finite_surjective_injective_inputs(goal: object, order: object):
    """Construct three open obligations, with no generator or group decomposition."""
    if (type(goal) is not MapInjective
            or not valid_finite_group_map(goal.map)
            or type(order) is not int or order < 1):
        return None
    mapping = goal.map
    return (FiniteGroupCardinality(mapping.source_group, order),
            FiniteGroupCardinality(mapping.target_group, order),
            MapSurjective(mapping))


def expand_finite_surjective_injective(goal: object, order: object):
    required = finite_surjective_injective_inputs(goal, order)
    if required is None:
        return ()

    def guard(premises, bindings):
        if (len(premises) != 3
                or any(p.rule is not ProofRule.INFERENCE for p in premises)):
            return False
        a, b, onto = (p.conclusion for p in premises)
        return (type(a) is FiniteGroupCardinality
                and type(b) is FiniteGroupCardinality
                and type(a.order) is int and type(b.order) is int
                and group_endpoints(a.group) is not None
                and group_endpoints(b.group) is not None
                and type(onto) is MapSurjective
                and valid_finite_group_map(onto.map)
                and (a, b, onto) == required
                and finite_surjective_injective_inputs(goal, a.order) == required)

    rule = InferenceRule(
        name=RULE_NAME,
        description=(
            'For a proved surjective homomorphism f:A->B of finite groups, '
            '|A|=|ker(f)|*|B|. Equal positive cardinalities imply '
            '|ker(f)|=1, so f is injective.'
        ),
        premise_patterns=(
            PremisePattern(proof_rule=ProofRule.INFERENCE,
                           statement_type=FiniteGroupCardinality,
                           statement_pattern=required[0]),
            PremisePattern(proof_rule=ProofRule.INFERENCE,
                           statement_type=FiniteGroupCardinality,
                           statement_pattern=required[1]),
            PremisePattern(proof_rule=ProofRule.INFERENCE,
                           statement_type=MapSurjective,
                           statement_pattern=required[2]),
        ),
        match_guard=guard,
        conclusion_pattern=goal,
    )
    return (GoalExpansion(rule, required),)

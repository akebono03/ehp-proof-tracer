"""Bridge a proved generic map isomorphism to the typed suspension statement."""
from homotopy_groups import (
    TodaPrimaryGroup, TodaSuspensionIsomorphismStatement, TodaSuspensionMap,
)
from phase165_r14_r6_generic_iso import MapIsomorphism
from phase165_r3_recursive_search import GoalExpansion
from proof import InferenceRule, PremisePattern, ProofRule

RULE_NAME = 'proved generic isomorphism implies typed suspension isomorphism'


def suspension_isomorphism_inputs(goal):
    """Accept only a concrete, well-typed one-fold sphere suspension."""
    if type(goal) is not TodaSuspensionIsomorphismStatement or type(goal.map) is not TodaSuspensionMap:
        return None
    a, b = goal.map.source_group, goal.map.target_group
    if type(a) is not TodaPrimaryGroup or type(b) is not TodaPrimaryGroup:
        return None
    q, n, p, m = a.group_dimension, a.sphere_dimension, b.group_dimension, b.sphere_dimension
    if (any(type(v) is not int for v in (q, n, p, m))
            or n < 2 or q < n or p != q + 1 or m != n + 1):
        return None
    return (MapIsomorphism(goal.map),)


def suspension_isomorphism_bridge_rule(goal):
    """Require the same suspension map's independently inferred isomorphism."""
    required = suspension_isomorphism_inputs(goal)
    if required is None:
        raise ValueError('invalid typed suspension isomorphism goal')

    def guard(premises, bindings):
        return (len(premises) == 1
                and premises[0].rule is ProofRule.INFERENCE
                and type(premises[0].conclusion) is MapIsomorphism
                and bool(premises[0].premises)
                and premises[0].inference_rule is not None
                and (premises[0].conclusion,) == required
                and suspension_isomorphism_inputs(goal) == required)

    return InferenceRule(
        name=RULE_NAME,
        description='Read the same proved suspension isomorphism in its Toda typed representation.',
        premise_patterns=(PremisePattern(
            statement_type=MapIsomorphism, proof_rule=ProofRule.INFERENCE,
            statement_pattern=required[0]),),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def expand_suspension_isomorphism_bridge(goal):
    """Generate one unresolved obligation, never a theorem or a proof leaf."""
    required = suspension_isomorphism_inputs(goal)
    if required is None:
        return ()
    return (GoalExpansion(suspension_isomorphism_bridge_rule(goal), required),)

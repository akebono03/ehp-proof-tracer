"""Derive a zero suspension image from a verified adopted earlier zero group.

No public provider, new source assertion, or proof leaf is registered here.
"""
from homotopy_groups import (
    TodaPrimaryGroup, TodaPrimaryGroupZeroStatement, TodaSuspensionMap,
)
from map_property_rules import ImageZeroStatement
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r3_recursive_search import GoalExpansion
from phase169_r10e4_ordered_db_prior.db_prior import (
    admitted_db_step, group_coordinates, verified_db_step,
)
from proof import InferenceRule, PremisePattern, ProofRule

RULE_NAME = 'adopted earlier zero group implies zero suspension image'


def zero_domain_inputs(goal):
    """Construct the exact zero-domain obligation of a concrete suspension."""
    if type(goal) is not ImageZeroStatement or type(goal.map) is not TodaSuspensionMap:
        return None
    a, b = goal.map.source_group, goal.map.target_group
    if type(a) is not TodaPrimaryGroup or type(b) is not TodaPrimaryGroup:
        return None
    q, n = a.group_dimension, a.sphere_dimension
    p, m = b.group_dimension, b.sphere_dimension
    if (any(type(v) is not int for v in (q, n, p, m))
            or n < 2 or q < n or p != q + 1 or m != n + 1):
        return None
    return (TodaPrimaryGroupZeroStatement(a),)


def verified_zero_domain_inputs(goal, *, proof_target, bridge):
    """Check existing DB admission; return an obligation, not its witness."""
    required = zero_domain_inputs(goal)
    if (required is None or not isinstance(bridge, RegistryBridgeResult)
            or group_coordinates(proof_target) is None):
        return None
    witness = admitted_db_step(required[0], proof_target=proof_target, bridge=bridge)
    if witness is None or not verified_db_step(witness, proof_target=proof_target, bridge=bridge):
        return None
    return required


def zero_domain_image_rule(goal, *, proof_target, bridge):
    """Recheck the actual adopted GIVEN at inference-match time."""
    required = verified_zero_domain_inputs(goal, proof_target=proof_target, bridge=bridge)
    if required is None:
        raise ValueError('a verified earlier zero domain and typed suspension are required')

    def guard(premises, bindings):
        return (len(premises) == 1
                and premises[0].rule is ProofRule.GIVEN
                and type(premises[0].conclusion) is TodaPrimaryGroupZeroStatement
                and premises[0].conclusion == required[0]
                and verified_db_step(premises[0], proof_target=proof_target, bridge=bridge)
                and verified_zero_domain_inputs(goal, proof_target=proof_target, bridge=bridge) == required)

    return InferenceRule(
        name=RULE_NAME,
        description='A homomorphism from the trivial group sends its sole element to zero, so its image is zero. The earlier DB premise retains its verified GIVEN provenance.',
        premise_patterns=(PremisePattern(
            proof_rule=ProofRule.GIVEN,
            statement_type=TodaPrimaryGroupZeroStatement,
            statement_pattern=required[0],
        ),),
        conclusion_pattern=goal,
        match_guard=guard,
    )


def expand_zero_domain_image(goal, *, proof_target, bridge):
    """Propose only a backward obligation; do not insert the DB proof step."""
    required = verified_zero_domain_inputs(goal, proof_target=proof_target, bridge=bridge)
    if required is None:
        return ()
    return (GoalExpansion(zero_domain_image_rule(goal, proof_target=proof_target, bridge=bridge), required),)

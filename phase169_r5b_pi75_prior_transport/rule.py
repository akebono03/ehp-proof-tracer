"""Expose a previously positioned lower-group RESULT only as a proof subgoal.

This adapter adds no mathematical inference rule, no new GIVEN, and no
completion-state dependency.  Existing cited Toda (4.5) and eta-generator
proof obligations remain mandatory.
"""
from __future__ import annotations

from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r3_recursive_search import GoalExpansion
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase169_r3m_prior_result_catalog.prior_results import resolve_prior_group_result
from phase169_r3o_stable_composite_rule import expand_cited_toda45_composite_transport
from proof import Relation, RelationType


def expand_prior_cited_toda45_composite_transport(
    goal: object,
    available: tuple[object, ...],
    bridge: RegistryBridgeResult,
    *,
    proof_target: object,
) -> tuple[GoalExpansion, ...]:
    """Offer the existing three-premise transport for the R5 pi_7^5 root.

    A candidate from the database is NOT a premise witness.  Its unique prior
    fixed-source relation is checked using the common publication-order
    catalog; the normal recursive solver must derive that relation separately.
    """
    if not isinstance(available, tuple):
        raise TypeError("available must be a tuple")
    if not isinstance(bridge, RegistryBridgeResult):
        raise TypeError("bridge must be a RegistryBridgeResult")
    if goal != proof_target:
        return ()
    if not (
        isinstance(goal, Relation)
        and goal.relation_type is RelationType.EQUALITY
        and goal.lhs == TodaPrimaryGroup(7, 5)
        and isinstance(goal.rhs, FiniteCyclicGroup)
        and goal.rhs.order == 2
    ):
        return ()

    citing_id = resolve_specialized_goal_citing_id(bridge, proof_target)
    if citing_id is None:
        return ()
    prior = resolve_prior_group_result(
        bridge, source_n=4, source_k=2, citing_assertion_id=citing_id,
    )
    if (
        not prior.eligible
        or prior.relation is None
        or prior.source_assertion_id is None
        or prior.relation.lhs != TodaPrimaryGroup(6, 4)
    ):
        return ()

    # The existing R3O rule validates Toda (4.5)'s stable range, the exact
    # composite-generator image, and three actual proof substeps.  Supplying
    # a candidate Relation here never promotes a DB row to a GIVEN ProofStep.
    proposed = expand_cited_toda45_composite_transport(
        goal, (prior.relation,) + available,
    )
    return tuple(
        option for option in proposed
        if len(option.subgoals) == 3
        and option.subgoals[0] == prior.relation
    )

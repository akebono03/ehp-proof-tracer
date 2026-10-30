"""Source-anchored backward proposals for finite order-four cyclic presentations.

This proposer never derives an order or returns a ProofStep. It proposes two
subgoals only when a typed cited double relation identifies a candidate
for the generator of the requested group. All subgoals must be proved by the
normal recursive engine. No dimensions, generator names, or source IDs are
hard-coded in the rule.
"""
from __future__ import annotations

from expression import HomotopyElement, Multiple
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase168_r2_8_3_generator_identity.identity import same_registered_group_presentation
from phase169_r10e5_composite_generator_image.rule import _endpoints
from phase171_r2j_r4_r6_middle_cardinality.source import FiniteGroupCardinality
from phase171_r2j_r4_r7_nonzero_nu_order.source import FiniteElementOrder
from phase171_r2j_r4_r8_cyclic_structure.source import (
    expand_cyclic_group_from_full_element_order,
)
from phase165_r3_recursive_search import GoalExpansion
from proof import Relation, RelationType


def expand_cited_double_cyclic_root(
    goal: object, available: tuple[object, ...],
) -> tuple[GoalExpansion, ...]:
    """Offer a generic order-four root obligation, not an assumed group result.

    A screened fixed 2*x=... citation only identifies x; it does NOT prove
    2*x nonzero, order(x)=4, or cardinality of the group. Those are separate
    required inferences with their own registered source ancestry.
    """
    if not isinstance(available, tuple):
        raise TypeError("available must be a tuple")
    if (
        not isinstance(goal, Relation)
        or goal.relation_type is not RelationType.EQUALITY
        or not isinstance(goal.lhs, TodaPrimaryGroup)
        or not isinstance(goal.rhs, FiniteCyclicGroup)
        or type(goal.rhs.order) is not int
        or goal.rhs.order != 4
    ):
        return ()
    dimensions = (goal.lhs.group_dimension, goal.lhs.sphere_dimension)
    candidates: list[GoalExpansion] = []
    for claim in available:
        if (
            not isinstance(claim, Relation)
            or claim.relation_type is not RelationType.EQUALITY
            or not isinstance(claim.lhs, Multiple)
            or type(claim.lhs.coefficient) is not int
            or claim.lhs.coefficient != 2
            or not isinstance(claim.lhs.expression, HomotopyElement)
            or _endpoints(claim.lhs.expression) != dimensions
            or claim.rhs is None
        ):
            continue
        candidate = FiniteCyclicGroup(4, claim.lhs.expression)
        if (
            candidate != goal.rhs
            and not same_registered_group_presentation(candidate, goal.rhs)
        ):
            continue
        cardinality = FiniteGroupCardinality(goal.lhs, 4)
        element_order = FiniteElementOrder(goal.lhs, claim.lhs.expression, 4)
        routes = expand_cyclic_group_from_full_element_order(
            goal, cardinality, element_order,
        )
        if len(routes) != 1:
            continue
        if not any(
            existing.subgoals == routes[0].subgoals
            and existing.rule.name == routes[0].rule.name
            for existing in candidates
        ):
            candidates.append(routes[0])
    # Multiple incompatible cited candidates must not be resolved by an
    # arbitrary source or by a database-presentation guess.
    return tuple(candidates) if len(candidates) == 1 else ()

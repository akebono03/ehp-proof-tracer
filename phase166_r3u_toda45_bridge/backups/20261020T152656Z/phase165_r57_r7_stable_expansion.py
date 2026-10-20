"""R57-R7: source-anchored backward expansions for Toda (4.5) transport.

No proof leaves, no generator normalization, and no group-number branches.
"""
from __future__ import annotations

from expression import IteratedSuspension
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase165_r3_recursive_search import GoalExpansion
from proof import Relation, RelationType
from toda_rules import Toda45IsomorphismStatement
from toda_stable_group_transport import (
    toda_45_generic_finite_cyclic_transport_inference_rule,
)


def expand_registered_toda45_finite_cyclic_goal(
    goal: object,
    available: tuple[object, ...],
) -> tuple[GoalExpansion, ...]:
    """Use only exact, already admissible typed Reference conclusions.

    The rule itself checks its premises again before deriving the conclusion.
    An IteratedSuspension is not silently identified with a named eta symbol.
    """
    if not isinstance(available, tuple):
        raise TypeError("available must be a tuple")
    if not (
        isinstance(goal, Relation)
        and goal.relation_type is RelationType.EQUALITY
        and isinstance(goal.lhs, TodaPrimaryGroup)
        and isinstance(goal.rhs, FiniteCyclicGroup)
    ):
        return ()
    options = []
    for iso in available:
        if not isinstance(iso, Toda45IsomorphismStatement):
            continue
        transport_map = iso.map
        if transport_map.target_group != goal.lhs:
            continue
        for base in available:
            if not (
                isinstance(base, Relation)
                and base.relation_type is RelationType.EQUALITY
                and isinstance(base.lhs, TodaPrimaryGroup)
                and isinstance(base.rhs, FiniteCyclicGroup)
                and base.lhs == transport_map.source_group
                and base.rhs.order == goal.rhs.order
            ):
                continue
            expected_generator = IteratedSuspension(
                expression=base.rhs.generator,
                exponent=transport_map.exponent,
            )
            if goal.rhs.generator != expected_generator:
                continue
            candidate = GoalExpansion(
                toda_45_generic_finite_cyclic_transport_inference_rule(),
                (base, iso),
            )
            if not any(item.subgoals == candidate.subgoals for item in options):
                options.append(candidate)
    return tuple(options)

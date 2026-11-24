"""Source-screened backward candidates for the audited Toda (5.5) connection."""
from __future__ import annotations

from collections.abc import Callable

from expression import Composition, HomotopyElement, MapApplication, Multiple
from map_facts import EHP_H_MAP
from phase165_r3_recursive_search import GoalExpansion
from phase176_r3r27r1_toda55_quadruple_isolated.source import canonical_quadruple_goal
from phase176_r3r40r1_eta_notation_bridge.source import connection_backward_plan
from proof import Relation, RelationType


def public_quadruple_backward_plan(
    goal: object, available: tuple[object, ...],
) -> tuple[tuple[Relation, GoalExpansion], ...]:
    """Derive a finite candidate from the goal and screened H(alpha) values.

    The existing audited planner validates both independent input obligations.
    Neither the source availability nor this plan certifies their truth.
    """
    if not isinstance(available, tuple):
        raise TypeError('available must be a tuple')
    if (not isinstance(goal, Relation)
            or goal.relation_type is not RelationType.EQUALITY
            or not isinstance(goal.lhs, MapApplication)
            or goal.lhs.map != EHP_H_MAP
            or not isinstance(goal.lhs.expression, Composition)
            or not isinstance(goal.lhs.expression.right, Composition)
            or not isinstance(goal.rhs, Multiple)
            or not isinstance(goal.rhs.expression, HomotopyElement)
            or type(goal.rhs.coefficient) is not int
            or goal.rhs.coefficient != 4):
        return ()
    forward = canonical_quadruple_goal(goal.rhs.expression.dimension)
    if forward is None or forward.lhs != goal.rhs:
        return ()
    alpha = goal.lhs.expression.left
    gamma = goal.lhs.expression.right
    plans = []
    for item in available:
        if (not isinstance(item, Relation)
                or item.relation_type is not RelationType.EQUALITY
                or item.lhs != MapApplication(EHP_H_MAP, alpha)
                or not isinstance(item.rhs, HomotopyElement)
                or available.count(item) != 1):
            continue
        transported = Relation(goal.lhs, Composition(item.rhs, gamma))
        plan = connection_backward_plan(transported, forward, available)
        if plan and plan[-1][0] == goal:
            plans.append(plan)
    # Ambiguous routes are not silently selected by a notation heuristic.
    return plans[0] if len(plans) == 1 else ()


def build_public_quadruple_connection_provider(
    available: tuple[object, ...],
) -> Callable[[object], tuple[GoalExpansion, ...]]:
    """Keep only candidate obligations in a single DFS context, not proofs."""
    if not isinstance(available, tuple):
        raise TypeError('available must be a tuple')
    stages: list[tuple[Relation, GoalExpansion]] = []

    def expand(goal: object) -> tuple[GoalExpansion, ...]:
        if not isinstance(goal, Relation):
            return ()
        known = tuple(option for target, option in stages if target == goal)
        if known:
            return known
        plan = public_quadruple_backward_plan(goal, available)
        if not plan:
            return ()
        # Shared sub-obligations may recur across plans; keep identical ones.
        for target, option in plan:
            for previous, old in stages:
                if target == previous and (old.rule.name != option.rule.name
                                           or old.subgoals != option.subgoals):
                    return ()
        for target, option in plan:
            if not any(target == previous for previous, _ in stages):
                stages.append((target, option))
        return tuple(option for target, option in stages if target == goal)

    return expand

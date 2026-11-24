"""Audit-only backward connection using existing equality rules."""
from __future__ import annotations

from collections.abc import Callable

from expression import HomotopyElement, Multiple
from phase165_r3_recursive_search import GoalExpansion
from phase176_r3r27r1_toda55_quadruple_isolated.source import (
    canonical_quadruple_goal,
    expand_cited_quadruple,
)
from phase176_r3r39_public_equality_transport.source import (
    right_hopf_transport_backward_plan,
)
from proof import Relation, RelationType
from relation_rules import (
    equality_symmetry_inference_rule,
    equality_transitivity_inference_rule,
)


def quadruple_hopf_backward_plan(
    goal: object, available: tuple[object, ...],
) -> tuple[tuple[Relation, GoalExpansion], ...]:
    """Require a source-eligible canonical quadruple and typed Hopf transport.

    The two independent statements are open DFS obligations. No name-based
    rewriting, reassociation, direct GIVEN, or new inference rule is used.
    """
    if not isinstance(available, tuple):
        raise TypeError("available must be a tuple")
    if (not isinstance(goal, Relation)
            or goal.relation_type is not RelationType.EQUALITY
            or not isinstance(goal.rhs, Multiple)
            or type(goal.rhs.coefficient) is not int
            or goal.rhs.coefficient != 4
            or not isinstance(goal.rhs.expression, HomotopyElement)):
        return ()
    forward = canonical_quadruple_goal(goal.rhs.expression.dimension)
    if forward is None or forward.lhs != goal.rhs:
        return ()
    if len(expand_cited_quadruple(forward, available)) != 1:
        return ()
    transported = Relation(goal.lhs, forward.rhs, RelationType.EQUALITY)
    if len(right_hopf_transport_backward_plan(transported, available)) != 6:
        return ()
    reversed_quadruple = Relation(forward.rhs, forward.lhs, RelationType.EQUALITY)
    return (
        (reversed_quadruple, GoalExpansion(
            equality_symmetry_inference_rule(), (forward,),
        )),
        (goal, GoalExpansion(
            equality_transitivity_inference_rule(),
            (transported, reversed_quadruple),
        )),
    )


def build_audit_connection_provider(
    goal: Relation, available: tuple[object, ...],
) -> Callable[[object], tuple[GoalExpansion, ...]]:
    """Install exactly the two open expansions in an explicit audit context."""
    plan = quadruple_hopf_backward_plan(goal, available)

    def expand(target: object) -> tuple[GoalExpansion, ...]:
        return tuple(proposal for statement, proposal in plan
                     if isinstance(target, Relation) and target == statement)

    return expand

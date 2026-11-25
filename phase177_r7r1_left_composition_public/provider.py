"""General typed backward connection to the existing left congruence rule."""
from __future__ import annotations

from expression import Composition
from phase165_r3_recursive_search import GoalExpansion
from phase175_r4r7_prop25_typed_composition.rule import typed_endpoints
from proof import Relation, RelationType
from relation_rules import equality_preserved_under_left_composition_inference_rule


def left_composition_input(goal: object) -> Relation | None:
    """Recover only the right-factor equality of a typed same-left goal."""
    if (type(goal) is not Relation or goal.relation_type is not RelationType.EQUALITY
            or goal.source is not None or goal.note is not None
            or type(goal.lhs) is not Composition or type(goal.rhs) is not Composition
            or goal.lhs.left != goal.rhs.left):
        return None
    lhs, rhs = goal.lhs, goal.rhs
    if lhs.right == rhs.right:
        return None
    a = typed_endpoints(lhs.left)
    b = typed_endpoints(lhs.right)
    c = typed_endpoints(rhs.right)
    if a is None or b is None or c != b or a[0] != b[1]:
        return None
    if (typed_endpoints(lhs) != (b[0], a[1])
            or typed_endpoints(rhs) != (b[0], a[1])):
        return None
    return Relation(lhs.right, rhs.right)


def expand_public_left_composition(goal: object) -> tuple[GoalExpansion, ...]:
    """Propose an open subgoal; never cancel a factor or certify equality."""
    premise = left_composition_input(goal)
    if premise is None:
        return ()
    return (GoalExpansion(
        equality_preserved_under_left_composition_inference_rule(goal.lhs.left),
        (premise,),
    ),)

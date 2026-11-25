"""Typed composition associativity as an element equality, with no public hook."""
from __future__ import annotations

from expression import Composition
from phase165_r3_recursive_search import GoalExpansion
from phase175_r4r7_prop25_typed_composition.rule import typed_endpoints
from proof import InferenceRule, Relation, RelationType

RULE_NAME = 'typed composition associativity equality'


def ordered_composition_factors(value: object) -> tuple[object, ...] | None:
    """Flatten composition only; preserve every typed leaf exactly in order."""
    if typed_endpoints(value) is None:
        return None
    if type(value) is not Composition:
        return (value,)
    left = ordered_composition_factors(value.left)
    right = ordered_composition_factors(value.right)
    if left is None or right is None:
        return None
    return left + right


def is_composition_associativity_equality(goal: object) -> bool:
    """Check identical ordered factors and well-typed endpoints on both sides."""
    if (type(goal) is not Relation or goal.relation_type is not RelationType.EQUALITY
            or goal.source is not None or goal.note is not None
            or type(goal.lhs) is not Composition or type(goal.rhs) is not Composition
            or goal.lhs == goal.rhs):
        return False
    left = ordered_composition_factors(goal.lhs)
    right = ordered_composition_factors(goal.rhs)
    return (left is not None and right is not None and len(left) >= 3
            and left == right
            and typed_endpoints(goal.lhs) == typed_endpoints(goal.rhs))


def expand_composition_associativity_equality(goal: object) -> tuple[GoalExpansion, ...]:
    """Associativity alone is an inference; it changes no leaf or factor order."""
    if not is_composition_associativity_equality(goal):
        return ()

    def guard(premises, bindings):
        return (not premises and not bindings
                and is_composition_associativity_equality(goal))

    rule = InferenceRule(
        name=RULE_NAME,
        description=('Composition in the homotopy category is associative; '
                     'the exact ordered typed factors are unchanged.'),
        premise_patterns=(), match_guard=guard, conclusion_pattern=goal,
    )
    return (GoalExpansion(rule, ()),)

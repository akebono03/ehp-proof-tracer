"""Propose a typed RHS reassociation via the existing transitivity rule."""
from __future__ import annotations

from expression import Composition
from phase165_r3_recursive_search import GoalExpansion
from phase177_r10_composition_associativity_isolated.rule import (
    is_composition_associativity_equality, ordered_composition_factors,
)
from proof import Relation, RelationType
from relation_rules import equality_transitivity_inference_rule


def reassociation_inputs(goal: object) -> tuple[Relation, Relation] | None:
    """One left-associated candidate only; no factor substitution or proof."""
    if (type(goal) is not Relation or goal.relation_type is not RelationType.EQUALITY
            or goal.source is not None or goal.note is not None
            or type(goal.rhs) is not Composition or goal.lhs == goal.rhs
            or is_composition_associativity_equality(goal)):
        return None
    factors = ordered_composition_factors(goal.rhs)
    if factors is None or len(factors) < 3:
        return None
    middle = factors[0]
    for factor in factors[1:]:
        middle = Composition(middle, factor)
    if middle == goal.rhs or middle == goal.lhs:
        return None
    bridge = Relation(middle, goal.rhs)
    if not is_composition_associativity_equality(bridge):
        return None
    return Relation(goal.lhs, middle), bridge


def expand_public_reassociation_transitivity(goal: object) -> tuple[GoalExpansion, ...]:
    """Both obligations must be proved by the normal source-first search."""
    inputs = reassociation_inputs(goal)
    if inputs is None:
        return ()
    return (GoalExpansion(equality_transitivity_inference_rule(), inputs),)

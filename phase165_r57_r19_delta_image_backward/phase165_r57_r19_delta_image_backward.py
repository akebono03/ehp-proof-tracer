"""R57-R19: reverse existing free-cyclic Delta image rule over cited typed leaves.

No group-specific result or unverified GIVEN is generated. Exact statement
identity, including generator expressions, is required for a proposal.
"""
from __future__ import annotations

from homotopy_groups import FreeCyclicGroup
from phase165_r3_recursive_search import GoalExpansion
from proof import Relation, RelationType
from toda_delta_image_rules import free_cyclic_generator_delta_image_inference_rule
from toda_rules import TodaDeltaImageFreeCyclicStatement, TodaDeltaImageUpToSignStatement


def expand_registered_delta_image_goal(
    goal: object, available_statements: tuple[object, ...]
) -> tuple[GoalExpansion, ...]:
    """Reverse the existing rule using only screened signed-Delta references.

    The source's group relation is an independent proof subgoal, not a GIVEN.
    Ambiguous signed-source witnesses fail closed rather than being guessed.
    """
    if not isinstance(available_statements, tuple):
        raise TypeError("available_statements must be a tuple")
    if not isinstance(goal, TodaDeltaImageFreeCyclicStatement):
        return ()
    if not isinstance(goal.image_group, FreeCyclicGroup):
        return ()
    witnesses = tuple(
        statement for statement in available_statements
        if isinstance(statement, TodaDeltaImageUpToSignStatement)
        and statement.map == goal.map
        and statement.positive_value == goal.image_group.generator
    )
    if len(witnesses) != 1:
        return ()
    witness = witnesses[0]
    source_relation = Relation(
        lhs=goal.map.source_group,
        rhs=FreeCyclicGroup(generator=witness.element),
        relation_type=RelationType.EQUALITY,
    )
    return (GoalExpansion(
        rule=free_cyclic_generator_delta_image_inference_rule(),
        subgoals=(source_relation, witness),
    ),)

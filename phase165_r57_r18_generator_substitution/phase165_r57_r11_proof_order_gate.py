"""R57-R11: fail closed when a root group cites its own structure.

R57-R18 permits *derived* cyclic-generator substitution backed by a separately
proved equality, but never accepts an unproved symbolic structure as a root.
"""
from __future__ import annotations

from expression import Suspension
from homotopy_groups import DirectSumGroup, FiniteCyclicGroup, FreeCyclicGroup, TodaPrimaryGroup
from phase165_r3_recursive_search import GoalExpansion
from proof import Relation, RelationType


def _proved_generator_substitution_shape(root_goal: object, expansion: GoalExpansion) -> bool:
    """Only exempt substitution from an explicitly equal intermediate generator."""
    if getattr(expansion.rule, "name", None) != "generic finite cyclic generator substitution from proved equality":
        return False
    if len(expansion.subgoals) != 2:
        return False
    structure, equality = expansion.subgoals
    if not (isinstance(root_goal, Relation)
            and isinstance(root_goal.rhs, FiniteCyclicGroup)
            and isinstance(structure, Relation)
            and isinstance(structure.rhs, FiniteCyclicGroup)
            and isinstance(equality, Relation)
            and structure.relation_type is RelationType.EQUALITY
            and equality.relation_type is RelationType.EQUALITY):
        return False
    return (
        structure.lhs == root_goal.lhs
        and structure.rhs.order == root_goal.rhs.order
        and isinstance(structure.rhs.generator, Suspension)
        and equality.lhs == root_goal.rhs.generator
        and equality.rhs == structure.rhs.generator
    )


def is_unordered_root_structure_specialization(
    root_goal: object, current_goal: object, expansion: GoalExpansion,
) -> bool:
    """Reject a group-structure root derived from its own structural theorem.

    A generator substitution with a proved equality has independently
    checkable premises, unlike direct self-specialization of a source claim.
    """
    structures = (FiniteCyclicGroup, FreeCyclicGroup, DirectSumGroup)
    if not isinstance(expansion, GoalExpansion):
        raise TypeError("expansion must be GoalExpansion")
    if not (
        isinstance(root_goal, Relation)
        and root_goal.relation_type is RelationType.EQUALITY
        and isinstance(root_goal.lhs, TodaPrimaryGroup)
        and isinstance(root_goal.rhs, structures)
        and isinstance(current_goal, Relation)
        and current_goal == root_goal
    ):
        return False
    if _proved_generator_substitution_shape(root_goal, expansion):
        return False
    for premise in expansion.subgoals:
        if not (
            isinstance(premise, Relation)
            and premise.relation_type is RelationType.EQUALITY
            and isinstance(premise.lhs, TodaPrimaryGroup)
            and isinstance(premise.rhs, structures)
        ):
            continue
        source_group = premise.lhs
        if source_group == root_goal.lhs:
            return True
        if not isinstance(source_group.sphere_dimension, int):
            return True
    return False


def retain_ordered_root_expansions(
    root_goal: object, current_goal: object,
    expansions: tuple[GoalExpansion, ...],
) -> tuple[GoalExpansion, ...]:
    """Retain genuinely derived root steps; reject self-structure specialization."""
    if not isinstance(expansions, tuple):
        raise TypeError("expansions must be a tuple")
    return tuple(
        option for option in expansions
        if not is_unordered_root_structure_specialization(root_goal, current_goal, option)
    )

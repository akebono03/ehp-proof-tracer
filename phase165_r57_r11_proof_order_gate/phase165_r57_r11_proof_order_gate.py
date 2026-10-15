"""R57-R11: fail closed when a root group is only its own symbolic specialization.

This is a proof-use-order boundary, distinct from the publication order of
Toda references. It neither fabricates predecessor proofs nor GIVEN leaves.
"""
from __future__ import annotations

from homotopy_groups import DirectSumGroup, FiniteCyclicGroup, FreeCyclicGroup, TodaPrimaryGroup
from phase165_r3_recursive_search import GoalExpansion
from proof import Relation, RelationType


def is_unordered_root_structure_specialization(
    root_goal: object, current_goal: object, expansion: GoalExpansion,
) -> bool:
    """Reject direct symbolic structural facts about the requested group.

    A symbolic group theorem may be used as a mathematical reference, but
    without reviewed proof-use ordering it is not accepted as the *derivation*
    of the same requested group's structure. Other inference branches survive.
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
    """Retain only root derivations which do not self-cite a generic structure.

    This does not establish a global total ordering of all Toda groups. Such
    ordering needs registered predecessor metadata, and remains a separate gate.
    """
    if not isinstance(expansions, tuple):
        raise TypeError("expansions must be a tuple")
    return tuple(
        option for option in expansions
        if not is_unordered_root_structure_specialization(root_goal, current_goal, option)
    )

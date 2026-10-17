"""R12-R24: generic backward presentation for finite cyclic group goals.

This supplies a reverse inference candidate; it never manufactures a proof leaf,
map, source group, kernel or generator image.
"""
from __future__ import annotations

from homotopy_groups import FiniteCyclicGroup
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from phase165_r3_recursive_search import GoalExpansion
from phase165_r12_r5_structure_bridge import finite_cyclic_structure_as_relation_inference_rule
from proof import Relation, RelationType


def expand_finite_cyclic_relation(goal: object) -> tuple[GoalExpansion, ...]:
    """Reverse an existing general inference with fully bound goal data."""
    if not isinstance(goal, Relation) or goal.relation_type is not RelationType.EQUALITY:
        return ()
    if not isinstance(goal.rhs, FiniteCyclicGroup):
        return ()
    if type(goal.rhs.order) is not int or goal.rhs.order < 1:
        return ()
    source = CyclicStructureStatement(goal.lhs, goal.rhs.generator, goal.rhs.order)
    return (GoalExpansion(finite_cyclic_structure_as_relation_inference_rule(), (source,)),)

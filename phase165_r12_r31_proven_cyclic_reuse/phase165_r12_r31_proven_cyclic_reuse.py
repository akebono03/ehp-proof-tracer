"""R12-R31: inverse use of the already proved free cyclic presentation rule."""
from __future__ import annotations

from homotopy_groups import FreeCyclicGroup
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from phase165_r12_r22_quotient_closure import free_cyclic_relation_to_structure_rule
from phase165_r3_recursive_search import GoalExpansion
from proof import Relation, RelationType


def expand_free_cyclic_structure_from_relation(goal: object) -> tuple[GoalExpansion, ...]:
    """Require an independently proved Relation as a premise, never a GIVEN."""
    if not isinstance(goal, CyclicStructureStatement) or goal.order is not None:
        return ()
    relation = Relation(
        lhs=goal.group,
        rhs=FreeCyclicGroup(generator=goal.generator),
        relation_type=RelationType.EQUALITY,
    )
    return (GoalExpansion(free_cyclic_relation_to_structure_rule(), (relation,)),)

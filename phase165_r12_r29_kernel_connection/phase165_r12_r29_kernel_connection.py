"""Reverse connection to existing certified cyclic-kernel rule, without invented facts."""
from __future__ import annotations

from expression import Multiple
from homotopy_groups import FreeCyclicGroup, TodaSuspensionMap
from phase165_r12_r13_kernel_image import SuspensionKernelFreeCyclicStatement
from phase165_r12_r16_bridges import concrete_cyclic_kernel_as_multiple_rule
from phase165_r12_r2_quotient_rules import KernelMultipleStatement
from phase165_r3_recursive_search import GoalExpansion


def expand_kernel_multiple_from_suspension(goal: object) -> tuple[GoalExpansion, ...]:
    """Build a typed kernel premise; existing forward rule must re-prove the goal."""
    if not isinstance(goal, KernelMultipleStatement):
        return ()
    if not isinstance(goal.map, TodaSuspensionMap):
        return ()
    if goal.map.source_group != goal.domain:
        return ()
    if type(goal.multiple) is not int or goal.multiple < 1:
        return ()
    if getattr(goal.source_generator, "source", None) is None:
        return ()
    if getattr(goal.source_generator, "target", None) is None:
        return ()
    subgoal = SuspensionKernelFreeCyclicStatement(
        goal.map,
        FreeCyclicGroup(Multiple(goal.multiple, goal.source_generator)),
    )
    return (GoalExpansion(concrete_cyclic_kernel_as_multiple_rule(), (subgoal,)),)

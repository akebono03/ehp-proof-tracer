"""Discover finite presentations through the common source and DB gates."""
from __future__ import annotations

from homotopy_groups import FiniteCyclicGroup, TodaDeltaMap
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r12_r2_quotient_rules import KernelMultipleStatement
from phase165_r3_recursive_search import GoalExpansion
from phase169_r10e4_ordered_db_prior.db_prior import admitted_prior_group_step, verified_db_step
from phase176_r3r48_cited_finite_delta_kernel.rule import (
    conditional_inputs, finite_cyclic_delta_kernel_rule, linked_cited_steps,
)
from proof import Relation
from toda_rules import TodaDeltaImageUpToSignStatement


def build_finite_delta_kernel_provider(*, bridge, proof_target):
    """Return ordinary open obligations; never insert an accepted proof."""
    if not isinstance(bridge, RegistryBridgeResult):
        raise TypeError('typed registry bridge required')

    def presentations(group):
        items = []
        for link in bridge.proof_links:
            step = link.step
            item = None if step is None else step.conclusion
            if (type(item) is Relation and item.lhs == group
                    and type(item.rhs) is FiniteCyclicGroup
                    and step in linked_cited_steps(bridge, item) and item not in items):
                items.append(item)
        prior = admitted_prior_group_step(group, proof_target=proof_target, bridge=bridge)
        if (prior is not None and verified_db_step(prior, proof_target=proof_target, bridge=bridge)
                and prior.conclusion not in items):
            items.append(prior.conclusion)
        return tuple(items)

    def expand(goal):
        if type(goal) is not KernelMultipleStatement or type(goal.map) is not TodaDeltaMap:
            return ()
        delta = goal.map
        if goal.domain != delta.source_group:
            return ()
        signed = []
        for link in bridge.proof_links:
            step = link.step
            item = None if step is None else step.conclusion
            if (type(item) is TodaDeltaImageUpToSignStatement and item.map == delta
                    and item.element == goal.source_generator
                    and len(linked_cited_steps(bridge, item)) == 1 and item not in signed):
                signed.append(item)
        if not signed:
            return ()
        options = []
        for domain in presentations(delta.source_group):
            for codomain in presentations(delta.target_group):
                for image in signed:
                    required = conditional_inputs(goal, domain, codomain, image)
                    if required is not None:
                        options.append(GoalExpansion(finite_cyclic_delta_kernel_rule(
                            goal, *required, proof_target=proof_target, bridge=bridge), required))
        return tuple(options)

    return expand

"""Bind adjacent maps from cited exactness to existing generic inverse rules.

This module creates only GoalExpansion proposals. Cited statements are not
reclassified as proved premises, and no group-specific cases are introduced.
"""
from __future__ import annotations

from phase165_r3_recursive_search import GoalExpansion
from proof import ExactnessStatement, ProofRule
from map_property_rules import (
    KernelZeroStatement,
    ImageWholeStatement,
    exactness_and_zero_image_implies_zero_kernel_inference_rule,
    exactness_and_whole_kernel_implies_whole_image_inference_rule,
    ImageZeroStatement,
    KernelWholeStatement,
)
from unified_statement_registry import AssertionOrigin


def verified_exactness_from_bridge(bridge):
    """Collect only fixed-statement GIVEN links with identical registered content."""
    facts = []
    for link in bridge.proof_links:
        step = link.step
        if step is None or step.rule is not ProofRule.GIVEN:
            continue
        assertion = bridge.registry.assertion(link.assertion_id)
        if assertion.origin is not AssertionOrigin.FIXED_STATEMENT:
            continue
        if step.conclusion != assertion.content:
            continue
        if isinstance(step.conclusion, ExactnessStatement) and step.conclusion.is_exact is True:
            if step.conclusion not in facts:
                facts.append(step.conclusion)
    return tuple(facts)


def build_exactness_binding_provider(bridge):
    """Bind the missing adjacent map using cited EHP exactness.

    Every returned subgoal remains subject to normal recursive proof verification.
    """
    facts = verified_exactness_from_bridge(bridge)
    kernel_rule = exactness_and_zero_image_implies_zero_kernel_inference_rule()
    image_rule = exactness_and_whole_kernel_implies_whole_image_inference_rule()

    def expand(goal):
        results = []
        for fact in facts:
            if isinstance(goal, KernelZeroStatement) and goal.map == fact.second_map:
                option = GoalExpansion(
                    kernel_rule,
                    (fact, ImageZeroStatement(map=fact.first_map)),
                )
                if option not in results:
                    results.append(option)
            if isinstance(goal, ImageWholeStatement) and goal.map == fact.first_map:
                option = GoalExpansion(
                    image_rule,
                    (fact, KernelWholeStatement(map=fact.second_map)),
                )
                if option not in results:
                    results.append(option)
        return tuple(results)

    return expand

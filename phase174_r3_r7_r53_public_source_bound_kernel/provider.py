"""Source-certified inferred-domain preference for generic cyclic Delta kernels.

R53 makes R52's successful *ordinary inference obligation* reusable in the
public zero-group search. This module registers no source, GIVEN, proof step,
or new mathematical inference rule. All earlier candidate expansions remain.
"""
from __future__ import annotations

from typing import Callable

from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r12_r2_quotient_rules import KernelMultipleStatement
from phase165_r3_recursive_search import GoalExpansion, SourceBoundGoal
from phase174_r3_r7_r35_isolated_cyclic_delta_kernel.rule import (
    RULE_NAME as KERNEL_RULE,
)
from proof import ProofRule, ProofStep, Relation, find_inference_matches_for_rule
from unified_statement_registry import AssertionOrigin

SPECIALIZATION_RULE = "generic cited typed scalar specialization"


def cited_inferred_domain_sources(
    domain: Relation,
    provider: Callable[[object], tuple[GoalExpansion, ...]],
    bridge: RegistryBridgeResult,
) -> tuple[object, ...]:
    """Find only linked, positioned GIVEN sources matching a real inference.

    A registered DB group result, an unattached fact, or a citation label alone
    cannot supply a SourceBoundGoal premise.
    """
    if type(domain) is not Relation or not isinstance(bridge, RegistryBridgeResult):
        return ()
    valid: list[object] = []
    for option in provider(domain):
        if (type(option) is not GoalExpansion
                or option.rule.name != SPECIALIZATION_RULE
                or len(option.subgoals) != 1):
            continue
        source = option.subgoals[0]
        for link in bridge.proof_links:
            step = link.step
            if (not isinstance(step, ProofStep)
                    or step.rule is not ProofRule.GIVEN
                    or step.premises
                    or step.conclusion != source):
                continue
            assertion = bridge.registry.assertion(link.assertion_id)
            reference = bridge.registry.reference(assertion.reference_id)
            if (assertion.origin is not AssertionOrigin.FIXED_STATEMENT
                    or assertion.content != source
                    or type(reference.publication_position) is not int
                    or reference.publication_position < 1
                    or getattr(getattr(step.inference_rule, "literature_reference", None),
                               "locator", None) != reference.locator):
                continue
            if not find_inference_matches_for_rule(option.rule, (step,)):
                continue
            if not any(type(old) is type(source) and old == source for old in valid):
                valid.append(source)
    return tuple(valid)


def build_public_source_bound_kernel_provider(
    provider: Callable[[object], tuple[GoalExpansion, ...]],
    bridge: RegistryBridgeResult,
) -> Callable[[object], tuple[GoalExpansion, ...]]:
    """Prepend sourced domain obligations to existing general R35 proposals.

    This is strictly a preferred *search candidate*, not evidence. Its
    subgoal resolves by checked INFERENCE; the existing R35 guard continues
    to require one inferred free-cyclic group and two cited GIVEN parents.
    For goals without the exact typed rule or positioned source, return the
    original candidates unchanged and in the original order.
    """
    if not callable(provider) or not isinstance(bridge, RegistryBridgeResult):
        raise TypeError("expected a shared provider and screened source bridge")

    def expand(goal: object) -> tuple[GoalExpansion, ...]:
        original = provider(goal)
        if type(goal) is not KernelMultipleStatement:
            return original
        bound: list[GoalExpansion] = []
        for option in original:
            if (type(option) is not GoalExpansion
                    or option.rule.name != KERNEL_RULE
                    or len(option.subgoals) != 3
                    or type(option.subgoals[0]) is not Relation):
                continue
            domain = option.subgoals[0]
            for source in cited_inferred_domain_sources(domain, provider, bridge):
                proposal = GoalExpansion(
                    rule=option.rule,
                    subgoals=(SourceBoundGoal(conclusion=domain, source=source),)
                    + option.subgoals[1:],
                )
                if proposal not in bound:
                    bound.append(proposal)
        return tuple(bound) + original

    return expand

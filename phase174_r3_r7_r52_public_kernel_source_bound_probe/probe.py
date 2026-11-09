"""R52: non-installed, generic source-bound R35 kernel-domain provider probe.

Only the proof obligation is constrained. It does not construct a ProofStep,
create a GIVEN, change R35's inference rule, or specialize by group indices.
"""
from __future__ import annotations

from typing import Callable

from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r12_r2_quotient_rules import KernelMultipleStatement
from phase165_r3_recursive_search import GoalExpansion, SourceBoundGoal
from phase174_r3_r7_r35_isolated_cyclic_delta_kernel.rule import RULE_NAME as KERNEL_RULE
from proof import ProofRule, ProofStep, Relation, find_inference_matches_for_rule
from unified_statement_registry import AssertionOrigin

SPECIALIZATION_RULE = "generic cited typed scalar specialization"


def cited_inferred_domain_sources(
    domain: Relation,
    provider: Callable[[object], tuple[GoalExpansion, ...]],
    bridge: RegistryBridgeResult,
) -> tuple[object, ...]:
    """Find only individually link-certified fixed sources that infer a domain.

    A plain earlier DB row and a proposition label are insufficient. The
    existing checked specialization rule must match the actual linked GIVEN.
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


def build_source_bound_kernel_probe(
    provider: Callable[[object], tuple[GoalExpansion, ...]],
    bridge: RegistryBridgeResult,
) -> Callable[[object], tuple[GoalExpansion, ...]]:
    """Prepend a cited inference obligation for every eligible R35 kernel.

    Keep all original options as fallback. The first actual successful proof
    is still selected by the ordinary recursive engine, not by this probe.
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

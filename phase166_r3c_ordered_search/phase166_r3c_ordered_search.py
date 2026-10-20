"""Phase 166 R3-C: share Phase 163 publication order in fixed-reference lookup."""
from __future__ import annotations

from phase163_r4_registry_bridge import RegistryBridgeResult
from proof import ProofRule, ProofStep
from unified_statement_registry import AssertionOrigin


def ordered_fixed_reference_steps(
    bridge: RegistryBridgeResult,
    goal: object,
    citing_assertion_id: str,
) -> tuple[ProofStep, ...]:
    """Find linked fixed GIVEN facts strictly preceding a registered target.

    No independent review flag, TeX status, or available_after_position is used.
    Internal proof order is managed independently, not by publication ranks.
    """
    citing = bridge.registry.assertion(citing_assertion_id)
    target_ref = bridge.registry.reference(citing.reference_id)
    result: list[ProofStep] = []
    for assertion in bridge.registry._assertions.values():
        if assertion.origin is not AssertionOrigin.FIXED_STATEMENT:
            continue
        if type(assertion.content) is not type(goal) or assertion.content != goal:
            continue
        if assertion.assertion_id == citing_assertion_id:
            continue
        source_ref = bridge.registry.reference(assertion.reference_id)
        if assertion.reference_id == citing.reference_id:
            earlier = (
                assertion.component_position is not None
                and citing.component_position is not None
                and assertion.component_position < citing.component_position
            )
        else:
            earlier = (
                source_ref.publication_position is not None
                and target_ref.publication_position is not None
                and source_ref.publication_position < target_ref.publication_position
            )
        if not earlier:
            continue
        links = tuple(link for link in bridge.proof_links
                      if link.assertion_id == assertion.assertion_id)
        if len(links) > 1:
            raise ValueError("ambiguous fixed-reference ProofStepLink")
        if not links or links[0].step is None:
            continue
        step = links[0].step
        if (not isinstance(step, ProofStep) or step.rule is not ProofRule.GIVEN
                or type(step.conclusion) is not type(goal) or step.conclusion != goal):
            raise ValueError("ordered fixed-reference link is inconsistent")
        result.append(step)
    return tuple(result)

"""Strict, reusable Phase 165 citation lookup using the existing Phase 164 policy.

No assertion is approved implicitly. This path is explicitly opted into via
lookup_mode='typed_reference_ordered' with independently reviewed IDs.
"""
from __future__ import annotations

from phase163_r4_registry_bridge import RegistryBridgeResult
from phase164_r2_citation_eligibility import assess_phase164_r2_citation
from proof import ProofRule, ProofStep
from unified_statement_registry import AssertionOrigin


def ordered_typed_reference_steps(
    bridge: RegistryBridgeResult,
    goal: object,
    citing_assertion_id: str,
    *,
    verified_assertion_ids: tuple[str, ...] = (),
) -> tuple[ProofStep, ...]:
    """Return only uniquely linked GIVENs eligible by the existing citation policy.

    Missing source order, unapproved claims, and backward dependencies fail
    closed. The original registry and any earlier derived proof remain intact.
    """
    if not isinstance(bridge, RegistryBridgeResult):
        raise TypeError('bridge must be RegistryBridgeResult')
    if not isinstance(verified_assertion_ids, tuple):
        raise TypeError('verified_assertion_ids must be a tuple')
    bridge.registry.assertion(citing_assertion_id)
    steps: list[ProofStep] = []
    for assertion in bridge.registry._assertions.values():
        if assertion.origin is not AssertionOrigin.FIXED_STATEMENT:
            continue
        if type(assertion.content) is not type(goal) or assertion.content != goal:
            continue
        decision = assess_phase164_r2_citation(
            bridge, assertion.assertion_id, citing_assertion_id,
            verified_assertion_ids=verified_assertion_ids,
        )
        if not decision.usable:
            continue
        links = tuple(link for link in bridge.proof_links if link.assertion_id == assertion.assertion_id)
        if len(links) != 1 or links[0].step is None:
            continue
        step = links[0].step
        if not isinstance(step, ProofStep) or step.rule is not ProofRule.GIVEN:
            raise ValueError('ordered typed Reference must link to a GIVEN')
        if type(step.conclusion) is not type(goal) or step.conclusion != goal:
            raise ValueError('ordered typed Reference conclusion mismatch')
        steps.append(step)
    return tuple(steps)

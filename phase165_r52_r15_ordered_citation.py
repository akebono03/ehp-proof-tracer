"""Ordered typed-reference lookup based solely on documented assertion order.

Order determines whether a statement precedes the current proof. A concrete
linked GIVEN is still required to use the statement as a proof leaf. An
independent-review allowlist is not an eligibility requirement.
"""
from __future__ import annotations

from phase163_r3_registry_validation import CitationDecision, assess_citation
from phase163_r4_registry_bridge import RegistryBridgeResult
from proof import ProofRule, ProofStep
from unified_statement_registry import AssertionOrigin


def ordered_typed_reference_steps(
    bridge: RegistryBridgeResult,
    goal: object,
    citing_assertion_id: str,
    *,
    verified_assertion_ids: tuple[str, ...] = (),
) -> tuple[ProofStep, ...]:
    """Return existing linked GIVEN steps for strictly earlier fixed assertions.

    The legacy keyword is accepted for API compatibility but never controls
    availability. Unknown positions are not silently assigned an order.
    """
    if not isinstance(bridge, RegistryBridgeResult):
        raise TypeError("bridge must be RegistryBridgeResult")
    if not isinstance(verified_assertion_ids, tuple):
        raise TypeError("verified_assertion_ids must be a tuple")
    bridge.registry.assertion(citing_assertion_id)
    steps: list[ProofStep] = []
    for assertion in bridge.registry._assertions.values():
        if assertion.origin is not AssertionOrigin.FIXED_STATEMENT:
            continue
        if type(assertion.content) is not type(goal) or assertion.content != goal:
            continue
        if citing_assertion_id in assertion.dependencies:
            continue
        decision = assess_citation(
            bridge.registry, assertion.assertion_id, citing_assertion_id
        )
        if decision.decision is not CitationDecision.ALLOWED:
            continue
        links = tuple(
            link for link in bridge.proof_links
            if link.assertion_id == assertion.assertion_id
        )
        if len(links) != 1 or links[0].step is None:
            continue
        step = links[0].step
        if not isinstance(step, ProofStep) or step.rule is not ProofRule.GIVEN:
            raise ValueError("ordered typed Reference must link to a GIVEN")
        if type(step.conclusion) is not type(goal) or step.conclusion != goal:
            raise ValueError("ordered typed Reference conclusion mismatch")
        steps.append(step)
    return tuple(steps)

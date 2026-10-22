"""Read-only adapter between a completed search and its screened statement bridge."""
from __future__ import annotations

from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r52_partial_proof import PartialProofResult
from phase168_r3_3_proof_narrative_model import ProofNarrativeModel, build_proof_narrative_model
from proof import ProofRule


def build_linked_proof_narrative_model(
    result: PartialProofResult, bridge: RegistryBridgeResult,
) -> ProofNarrativeModel:
    """Project citations only from explicitly linked, used GIVEN steps and rules.

    The caller supplies the same screened bridge used by backward search.
    This adapter never searches for a citation by display text or rule name.
    """
    if not isinstance(result, PartialProofResult):
        raise TypeError("result must be PartialProofResult")
    if not isinstance(bridge, RegistryBridgeResult):
        raise TypeError("bridge must be RegistryBridgeResult")
    used_given_steps = tuple(step for step in result.proven_steps if step.rule is ProofRule.GIVEN)
    selected_links = tuple(
        link for link in bridge.proof_links
        if link.step is not None
        and any(link.step is step or link.step == step for step in used_given_steps)
    )
    return build_proof_narrative_model(
        result, registry=bridge.registry, proof_links=selected_links,
    )

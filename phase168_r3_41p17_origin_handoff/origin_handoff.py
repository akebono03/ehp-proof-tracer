"""Experimental canonical search-to-Model origin binding (R3-41P17).

Not the default Web route. The R3-41P13 full checker remains mandatory there.
This checks object ancestry and publication sources without replaying matchers.
It is not an independent certification of arbitrary InferenceRule/Bridge values.
"""
from __future__ import annotations

from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r52_partial_proof import PartialProofResult, ProofSearchStatus
from phase166_r3c_publication_order import precedes_citing_assertion
from phase168_r3_3_proof_narrative_model import ProofNarrativeModel
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_41p13_trust_boundary import UnverifiedProofTree
from proof import ProofRule, ProofStep
from proof_origin_capture import SearchOriginObservation, require_active_observation
from unified_statement_registry import AssertionOrigin


def build_origin_bound_narrative_model(
    result: PartialProofResult,
    screened_bridge: RegistryBridgeResult,
    *,
    citing_assertion_id: str,
    observation: SearchOriginObservation,
) -> ProofNarrativeModel:
    """Project a live canonical result after origin/chronology checks, no replay.

    The caller must have obtained `screened_bridge` from the same canonical
    search and its citing ID from the original registered goal. This function
    cannot authenticate arbitrary caller-supplied registries or inference rules.
    The returned ordinary Model has no transferable trusted flag.
    """
    require_active_observation(observation)
    if not isinstance(result, PartialProofResult):
        raise TypeError("result must be PartialProofResult")
    if not isinstance(screened_bridge, RegistryBridgeResult):
        raise TypeError("screened_bridge must be RegistryBridgeResult")
    if result.status is not ProofSearchStatus.COMPLETE:
        raise UnverifiedProofTree("origin handoff is limited to complete proofs")
    if not isinstance(citing_assertion_id, str) or not citing_assertion_id:
        raise UnverifiedProofTree("positioned citing assertion is required")
    try:
        citing = screened_bridge.registry.assertion(citing_assertion_id)
    except (KeyError, ValueError) as exc:
        raise UnverifiedProofTree("citing assertion is not registered") from exc
    if citing is None:
        raise UnverifiedProofTree("citing assertion is not registered")

    seen: set[int] = set()
    active: set[int] = set()

    def visit(step: ProofStep) -> None:
        if type(step) is not ProofStep:
            raise UnverifiedProofTree("a proof ancestor is not a ProofStep")
        key = id(step)
        if key in seen:
            return
        if key in active:
            raise UnverifiedProofTree("cyclic proof ancestry")
        active.add(key)
        try:
            if not observation.contains_accepted_step(step):
                raise UnverifiedProofTree("step was not accepted by this search")
            if step.rule is ProofRule.INFERENCE:
                if not observation.contains_factory_step(step):
                    raise UnverifiedProofTree("INFERENCE was not produced in this search")
                if step.inference_rule is None:
                    raise UnverifiedProofTree("INFERENCE is missing its typed rule")
                for ancestor in step.premises:
                    visit(ancestor)
            elif step.rule is ProofRule.GIVEN:
                if step.premises:
                    raise UnverifiedProofTree("GIVEN has nonempty premises")
                matches = tuple(
                    link for link in screened_bridge.proof_links
                    if link.step is step
                )
                if not any(
                    screened_bridge.registry.assertion(link.assertion_id).origin
                    is AssertionOrigin.FIXED_STATEMENT
                    and type(screened_bridge.registry.assertion(link.assertion_id).content)
                    is type(step.conclusion)
                    and screened_bridge.registry.assertion(link.assertion_id).content
                    == step.conclusion
                    and precedes_citing_assertion(
                        screened_bridge, link.assertion_id, citing_assertion_id,
                    )
                    for link in matches
                ):
                    raise UnverifiedProofTree("GIVEN is not an earlier screened source")
            else:
                raise UnverifiedProofTree("unsupported proof-step origin")
            seen.add(key)
        finally:
            active.remove(key)

    for step in result.proven_steps:
        visit(step)
    if not any(
        type(step.conclusion) is type(result.conclusion)
        and step.conclusion == result.conclusion
        for step in result.proven_steps
    ):
        raise UnverifiedProofTree("complete result has no matching root conclusion")
    return build_linked_proof_narrative_model(result, screened_bridge)

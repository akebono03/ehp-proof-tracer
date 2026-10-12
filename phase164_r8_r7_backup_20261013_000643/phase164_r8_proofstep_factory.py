"""Phase 164 R8-R2: restricted entry points for ProofStep construction.

This module does not confer trust on GIVEN evidence. It leaves calculation,
exactness, and other domain-specific constructors unchanged until reviewed.
"""
from proof import (
    InferenceMatch,
    ProofRule,
    ProofStep,
    Relation,
    apply_inference_match,
    relation_proof_step,
)


def create_relation_proof_step(relation: Relation) -> ProofStep:
    """Create a relation through the existing checked constructor."""
    if not isinstance(relation, Relation):
        raise TypeError("relation must be a Relation")
    result = relation_proof_step(relation)
    if (type(result) is not ProofStep or result.rule is not ProofRule.RELATION
            or result.conclusion is not relation or result.premises != ()):
        raise ValueError("relation constructor contract changed")
    return result


def derive_inference_proof_step(match: InferenceMatch) -> ProofStep:
    """Derive using the existing inference matcher; never bypass its rules."""
    if not isinstance(match, InferenceMatch):
        raise TypeError("match must be an InferenceMatch")
    result = apply_inference_match(match)
    if (type(result) is not ProofStep or result.rule is not ProofRule.INFERENCE
            or result.inference_rule is not match.inference_rule
            or result.premises != match.premises):
        raise ValueError("inference constructor contract changed")
    return result


def retain_existing_proof_step(step: ProofStep) -> ProofStep:
    """Preserve the exact existing object for repository lookup and replay."""
    if not isinstance(step, ProofStep):
        raise TypeError("step must be a ProofStep")
    return step

"""R8-R5 compatibility constructors, preserving legacy proof status.

These entry points centralize creation but do not certify the mathematical
truth, statement-registry enrollment or provenance of their inputs.
"""


def create_legacy_given_proof_step(
    *, conclusion, premises, rule, note=None,
    inference_rule=None, foundational_reference=None,
):
    """Construct a legacy GIVEN without promoting its trust or source status."""
    if rule is not ProofRule.GIVEN:
        raise ValueError("legacy GIVEN requires ProofRule.GIVEN")
    return ProofStep(
        conclusion=conclusion,
        premises=premises,
        rule=rule,
        note=note,
        inference_rule=inference_rule,
        foundational_reference=foundational_reference,
    )


def create_legacy_specialization_proof_step(
    *, conclusion, premises, rule, note=None,
    inference_rule=None, foundational_reference=None,
):
    """Preserve an already-checked legacy specialization; no new certification."""
    if rule is not ProofRule.INFERENCE:
        raise ValueError("legacy specialization requires ProofRule.INFERENCE")
    return ProofStep(
        conclusion=conclusion,
        premises=premises,
        rule=rule,
        note=note,
        inference_rule=inference_rule,
        foundational_reference=foundational_reference,
    )


def annotate_derived_reference_step(step: ProofStep, reference) -> ProofStep:
    """Preserve an inferred step's ancestry while attaching known citation identity.

    A reference label alone does not certify a statement's mathematical truth.
    """
    from dataclasses import replace
    from proof import FoundationalReferenceIdentity
    if not isinstance(step, ProofStep) or step.rule is not ProofRule.INFERENCE:
        raise TypeError("step must be an inferred ProofStep")
    if not isinstance(reference, FoundationalReferenceIdentity):
        raise TypeError("reference must be a FoundationalReferenceIdentity")
    if step.foundational_reference is not None and step.foundational_reference != reference:
        raise ValueError("cannot overwrite another foundational reference")
    return replace(step, foundational_reference=reference)


def project_reference_component_step(source_step: ProofStep, component) -> ProofStep:
    """Create a display-only projection without promoting its evidence status.

    This is NOT an inference and must never be inserted as a proof-tree node.
    """
    if not isinstance(source_step, ProofStep):
        raise TypeError("source_step must be a ProofStep")
    return ProofStep(
        conclusion=component,
        premises=(),
        rule=source_step.rule,
        note=source_step.note,
        inference_rule=source_step.inference_rule,
    )

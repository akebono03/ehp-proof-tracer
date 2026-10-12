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

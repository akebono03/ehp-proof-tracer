def derive_inference_proof_step(match: InferenceMatch) -> ProofStep:
    """Derive using the existing inference matcher; never bypass its rules."""
    if not isinstance(match, InferenceMatch):
        raise TypeError("match must be an InferenceMatch")
    result = apply_inference_match(match)
    if (type(result) is not ProofStep or result.rule is not ProofRule.INFERENCE
            or result.inference_rule is not match.inference_rule
            or result.premises != match.premises):
        raise ValueError("inference constructor contract changed")
    # Record identity only when a canonical caller opened an observation scope.
    # The record does not certify user-supplied InferenceMatch values.
    from proof_origin_capture import note_factory_inference
    note_factory_inference(result)
    return result

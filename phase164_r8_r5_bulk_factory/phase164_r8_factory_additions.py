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

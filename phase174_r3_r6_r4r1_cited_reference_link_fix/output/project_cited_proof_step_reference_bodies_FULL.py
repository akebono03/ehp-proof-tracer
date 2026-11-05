def project_cited_proof_step_reference_bodies(
    reference: object, cited_steps: tuple[object, ...],
) -> tuple[str, ...]:
    """Render an actual cited GIVEN when an assertion-ID body was not attached.

    Preserve the established Lemma 5.4 fallback. For Toda (4.8) and (5.5),
    require a unique canonical cited GIVEN with explicit source provenance,
    plus reverified adopted source text and chronological position. This is
    display-only: neither source links nor ProofSteps are created here.
    """
    from proof import LiteratureReference, ProofRule, ProofStep

    if not isinstance(reference, LiteratureReference) or not isinstance(cited_steps, tuple):
        return ()
    locator = reference.locator or reference.label
    candidates = tuple(
        (step, _verified_source_sentence(step.conclusion))
        for step in cited_steps
        if isinstance(step, ProofStep) and step.rule is ProofRule.GIVEN
        and not step.premises
    )
    verified = tuple(
        sentence for step, sentence in candidates
        if sentence is not None and locator == "Lemma 5.4"
    )
    if verified:
        return verified if len(verified) == 1 else ()

    from phase174_r3_r6_r4_common_reference.projection import (
        project_verified_cited_toda_given_reference_body,
    )
    return project_verified_cited_toda_given_reference_body(reference, cited_steps)

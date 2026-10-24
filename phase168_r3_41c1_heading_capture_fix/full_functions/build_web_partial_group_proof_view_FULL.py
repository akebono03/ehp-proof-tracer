def build_web_partial_group_proof_view(
    result, *, max_depth: int = 2, mode: str = "narrative",
) -> WebGroupProofView:
    """Render incomplete proof progress with the shared proof-backed Model.

    Completed compatibility results and trace mode retain their former route.
    No new references, proof steps, or search results are inferred.
    """
    from phase165_r52_r3_web_adapter import build_partial_web_group_proof_view
    from phase165_r52_partial_proof import ProofSearchStatus

    narrative_model = None
    if mode != "trace" and result.status is not ProofSearchStatus.COMPLETE:
        from phase168_r3_3_proof_narrative_model import build_proof_narrative_model

        narrative_model = build_proof_narrative_model(result)
    return build_partial_web_group_proof_view(
        result, max_depth=max_depth, mode=mode,
        narrative_model=narrative_model,
    )

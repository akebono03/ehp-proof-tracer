def build_group_proof_progress_view(
    *,
    n: int,
    k: int,
    max_depth: int = 2,
    goal: object | None = None,
    bridge: object | None = None,
    citing_assertion_id: str | None = None,
    expansion_provider: object | None = None,
    verified_assertion_ids: tuple[str, ...] = (),
):
    """Route standard searches and incomplete custom searches through one Model.

    Completed custom-search results keep the existing compatibility renderer.
    If an explicit screened RegistryBridgeResult is supplied, only its exact
    ProofStep links may contribute registered reference statements.
    """
    if (
        goal is None
        and bridge is None
        and citing_assertion_id is None
        and expansion_provider is None
        and not verified_assertion_ids
    ):
        from web_group_proof import build_standard_web_group_proof_view

        return build_standard_web_group_proof_view(
            n=n,
            k=k,
            max_depth=max_depth,
            mode="narrative",
            citation_source="model",
        )

    result = search_registered_partial_proof(
        n=n,
        k=k,
        goal=goal,
        bridge=bridge,
        citing_assertion_id=citing_assertion_id,
        expansion_provider=expansion_provider,
        verified_assertion_ids=verified_assertion_ids,
    )
    from phase165_r52_partial_proof import ProofSearchStatus

    narrative_model = None
    if result.status is not ProofSearchStatus.COMPLETE:
        from phase163_r4_registry_bridge import RegistryBridgeResult
        if isinstance(bridge, RegistryBridgeResult):
            from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
            narrative_model = build_linked_proof_narrative_model(result, bridge)
        else:
            from phase168_r3_3_proof_narrative_model import build_proof_narrative_model
            narrative_model = build_proof_narrative_model(result)

    return build_partial_web_group_proof_view(
        result,
        max_depth=max_depth,
        mode="narrative",
        narrative_model=narrative_model,
    )

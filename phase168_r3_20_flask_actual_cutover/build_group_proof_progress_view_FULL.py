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
    """Route the ordinary Flask group proof through the model-backed public entry.

    Explicit proof-search inputs retain the existing typed partial-result contract.
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
    return build_partial_web_group_proof_view(
        result,
        max_depth=max_depth,
        mode="narrative",
    )

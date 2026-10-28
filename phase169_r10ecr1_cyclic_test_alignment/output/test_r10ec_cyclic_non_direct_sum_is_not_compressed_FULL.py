def test_r10ec_cyclic_non_direct_sum_is_not_compressed():
    """Use the already verified complete cyclic pi_10^8 fixture from R10A."""
    bridge = build_shared_typed_bridge()
    contexts = []
    result = search_group_from_registered_goal(
        n=8, k=2, bridge=bridge, context_sink=contexts.append,
    )
    assert result.status is ProofSearchStatus.COMPLETE
    assert contexts
    assert isinstance(result.conclusion, Relation)
    assert isinstance(result.conclusion.rhs, FiniteCyclicGroup)
    model = build_linked_proof_narrative_model(result, contexts[-1])
    order = tuple(entry.step_index for entry in project_narrative_order(model))
    assert project_verified_direct_sum_transport(model, order) is None

def test_r10e1_zero_citation_absence_not_inferred_from_db():
    bridge = RegistryBridgeResult(UnifiedStatementRegistry(), (), ())
    goal = _zero(8, 4)
    assert universal.expand_prior_general_group_transport(
        goal, (_iso(6, 4, 2),), bridge, proof_target=goal,
    ) == ()

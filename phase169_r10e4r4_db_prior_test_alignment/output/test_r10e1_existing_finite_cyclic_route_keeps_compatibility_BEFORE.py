def test_r10e1_existing_finite_cyclic_route_keeps_compatibility(monkeypatch):
    source = _relation(5, 3, FiniteCyclicGroup(8, _element(4, 5)))
    goal = _relation(7, 3, FiniteCyclicGroup(8, _element(4, 7)))
    bridge = RegistryBridgeResult(UnifiedStatementRegistry(), (), ())
    import phase169_r7_general_stable_transport.rule as old
    seen = []

    def fake(old_goal, available, old_bridge, *, proof_target):
        seen.append((old_goal, proof_target))
        return ()

    monkeypatch.setattr(old, 'expand_prior_general_stable_transport', fake)
    assert universal.expand_prior_general_group_transport(
        goal, (_iso(5, 3, 2),), bridge, proof_target=goal,
    ) == ()
    assert seen == [(goal, goal)]

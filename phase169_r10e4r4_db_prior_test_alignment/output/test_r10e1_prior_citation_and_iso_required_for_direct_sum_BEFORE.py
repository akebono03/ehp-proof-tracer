def test_r10e1_prior_citation_and_iso_required_for_direct_sum(monkeypatch):
    source, goal = _two_component(10), _two_component(12)
    bridge = RegistryBridgeResult(UnifiedStatementRegistry(), (), ())
    monkeypatch.setattr(universal, 'resolve_specialized_goal_citing_id',
                        lambda b, target: 'registered_target')
    calls = []

    def fake_prior(b, *, source_n, source_k, citing_assertion_id):
        calls.append((source_n, source_k, citing_assertion_id))
        if source_n == 10 and source_k == 8:
            return PriorGroupResult(10, 8, source, 'registered_target',
                                    'registered_prior', True, 'prior_fixed_source')
        return PriorGroupResult(source_n, source_k, None, 'registered_target',
                                None, False, 'db_result_missing')

    monkeypatch.setattr(universal, 'resolve_prior_group_result', fake_prior)
    assert universal.expand_prior_general_group_transport(
        goal, (), bridge, proof_target=goal,
    ) == ()
    options = universal.expand_prior_general_group_transport(
        goal, (_iso(10, 8, 2),), bridge, proof_target=goal,
    )
    assert len(options) == 1
    assert len(options[0].subgoals) == 6
    assert options[0].subgoals[0] == source
    assert calls[0] == (10, 8, 'registered_target')
    assert universal.expand_prior_general_group_transport(
        goal, (_iso(10, 8, 2),), bridge, proof_target=source,
    ) == ()
    monkeypatch.setattr(universal, 'resolve_specialized_goal_citing_id',
                        lambda b, target: None)
    assert universal.expand_prior_general_group_transport(
        goal, (_iso(10, 8, 2),), bridge, proof_target=goal,
    ) == ()

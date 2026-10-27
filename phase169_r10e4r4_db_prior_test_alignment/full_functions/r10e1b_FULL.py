def test_r10e1_zero_citation_absence_not_inferred_from_db(monkeypatch):
    bridge = RegistryBridgeResult(UnifiedStatementRegistry(), (), ())
    goal = _zero(8, 4)
    # The real (n=6, k=4) DB zero result may be used even without a
    # separately registered proposition, but only as an adopted DB prior.
    options = universal.expand_prior_general_group_transport(
        goal, (_iso(6, 4, 2),), bridge, proof_target=goal,
    )
    assert len(options) == 1
    assert options[0].subgoals[0] == _zero(6, 4)
    from phase169_r10e4_ordered_db_prior import db_prior
    monkeypatch.setattr(
        db_prior, 'exact_prior_database_result', lambda *args, **kwargs: None,
    )
    assert universal.expand_prior_general_group_transport(
        goal, (_iso(6, 4, 2),), bridge, proof_target=goal,
    ) == ()

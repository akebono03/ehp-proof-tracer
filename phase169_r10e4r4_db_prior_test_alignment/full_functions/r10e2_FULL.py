def test_r10e2_missing_publication_position_is_not_a_proof_source(monkeypatch):
    source, goal = _relation(9, 9, 16), _relation(9, 12, 16)
    screened = screen_independent_sources_for_derived_goal(
        _bridge(source, positioned=False), goal=goal,
    )
    # A citation without a publication position is not a screened GIVEN.
    assert screened.proof_links == ()
    assert uniquely_screened_prior_sources(screened, goal=goal, source_n=9) == ()
    # R10E4 independently authorizes the real earlier database group result.
    options = expand_prior_general_group_transport(
        goal, (_iso(9, 7, 3),), screened, proof_target=goal,
    )
    assert len(options) == 1
    assert options[0].subgoals[0] == source
    from phase169_r10e4_ordered_db_prior import db_prior
    monkeypatch.setattr(
        db_prior, "exact_prior_database_result", lambda *args, **kwargs: None,
    )
    # Without either a screened literature source or a real DB prior,
    # the transport candidate must disappear.
    assert expand_prior_general_group_transport(
        goal, (_iso(9, 7, 3),), screened, proof_target=goal,
    ) == ()

def test_r10e2_missing_publication_position_is_not_a_proof_source():
    source, goal = _relation(9, 9, 16), _relation(9, 12, 16)
    screened = screen_independent_sources_for_derived_goal(
        _bridge(source, positioned=False), goal=goal,
    )
    assert screened.proof_links == ()
    assert uniquely_screened_prior_sources(screened, goal=goal, source_n=9) == ()
    assert expand_prior_general_group_transport(
        goal, (_iso(9, 7, 3),), screened, proof_target=goal,
    ) == ()

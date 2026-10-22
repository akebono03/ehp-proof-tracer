from phase168_r2_8_goal_binding_audit.audit import CASES, audit_case


def test_case_matrix_contains_both_concrete_and_general_targets():
    assert (2, 2, "Proposition 5.3") in CASES
    assert (5, 2, "Proposition 5.3") in CASES
    assert (2, 3, "Proposition 5.6") in CASES
    assert (6, 3, "Proposition 5.6") in CASES


def test_all_case_dimensions_are_consistent():
    assert len(CASES) == len({(n, k) for n, k, _ in CASES})
    assert all(n >= 2 and k >= 1 for n, k, _ in CASES)


def test_not_unique_result_does_not_invent_citation():
    class Dummy:
        pass
    from unittest.mock import patch
    with patch("phase168_r2_8_goal_binding_audit.audit.registered_group_goal_candidates", return_value=()):
        result = audit_case(Dummy(), 2, 2, "Proposition 5.3")
    assert result["status"] == "GOAL_NOT_UNIQUE"
    assert result["citing_assertion_id"] is None


def test_goal_without_matched_source_fails_closed():
    from unittest.mock import patch
    class Dummy:
        pass
    with patch("phase168_r2_8_goal_binding_audit.audit.registered_group_goal_candidates",
               return_value=("goal",)):
        with patch("phase168_r2_8_goal_binding_audit.audit.resolve_specialized_goal_citing_id",
                   return_value=None):
            result = audit_case(Dummy(), 2, 2, "Proposition 5.3")
    assert result["status"] == "CITING_ID_UNRESOLVED"
    assert result["generated_given_count"] is None

from phase166_r3t_search_boundary.audit import inspect

def test_pi43_status_is_observed_not_assumed():
    result = inspect()
    assert result["pi43_candidate_count"] >= 1
    assert all(x["status"] in {"COMPLETE", "PARTIAL", "SEARCH_FAILED", "NOT_SEARCHED"}
               for x in result["pi43_search"])

def test_toda45_existing_specialization_is_available():
    result = inspect()
    assert result["concrete_toda45_specialization_count"] >= 1
    assert result["pi54"]

def test_hypothetical_premises_are_not_marked_as_proved():
    result = inspect()
    assert result["mode"] == "read_only"
    assert result["hypothetical_premises_are_not_proven_by_this_audit"]
    assert not result["production_code_modified"]
    assert not result["full_pytest_run"]

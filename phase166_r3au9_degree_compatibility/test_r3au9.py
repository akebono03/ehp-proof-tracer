from phase166_r3au9_degree_compatibility.audit import inspect


def test_matching_adjacent_base_degrees():
    sphere = [{"n": "3", "k": "2", "id": "0", "Element": "2 3"}]
    master = [{"id": "2", "n": "3", "k": "1", "display": "a"},
              {"id": "3", "n": "2", "k": "1", "display": "b"}]
    summary, rows = inspect(sphere, master)
    assert rows[0]["status"] == "ALL_BASE_ADJACENCIES_MATCH"
    assert summary["statuses"]["BASE_DEGREE_MATCH"] == 1


def test_mismatch_does_not_automatically_insert_suspension():
    sphere = [{"n": "3", "k": "2", "id": "0", "Element": "2 3", "generator": ""}]
    master = [{"id": "2", "n": "3", "k": "1"}, {"id": "3", "n": "4", "k": "1"}]
    summary, rows = inspect(sphere, master)
    assert rows[0]["status"] == "REQUIRES_DEGREE_RULE_REVIEW"
    assert rows[0]["suspension_exponent_certified"] is False
    assert summary["generator_reference_optional"] is True


def test_separator_does_not_become_bad_generator():
    summary, rows = inspect([{"n": "", "Element": "", "gen_coe": ""}], [])
    assert rows[0]["status"] == "NO_FACTOR_IDS"
    assert summary["production_code_modified"] is False

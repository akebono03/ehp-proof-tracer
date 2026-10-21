from phase166_r3au5_db_convention_audit.audit import audit, ints


def test_r3au5_composition_order_preserved():
    summary, rows = audit(
        [{"n": "11", "k": "28", "id": "0", "Element": "3 2", "gen_coe": "0 1 0", "generator": ""}],
        [{"id": "2", "display": "β"}, {"id": "3", "display": "α"}],
    )
    assert rows[0]["Element_factor_names"] == '[["α"], ["β"]]'
    assert rows[0]["classification"] == "UNIT_SINGLE"
    assert summary["counts"]["reference_generator_blank"] == 1


def test_r3au5_coordinates_are_not_mapped_to_composition_factors():
    summary, rows = audit(
        [{"n": "2", "k": "8", "id": "1", "Element": "3 2", "gen_coe": "1 0 -2 0"}],
        [{"id": "2", "display": "β"}, {"id": "3", "display": "α"}],
    )
    assert rows[0]["classification"] == "LINEAR_COMBINATION"
    assert rows[0]["gen_coe_nonzero_positions_zero_based"] == "[[0, 1], [2, -2]]"
    assert rows[0]["coefficient_basis_order_verified"] is False
    assert rows[0]["typed_expression_connected"] is False


def test_r3au5_separator_not_reported_as_invalid_generator():
    summary, rows = audit([{"n": "", "k": "15", "Element": "", "gen_coe": "", "generator": ""}], [])
    assert rows[0]["classification"] == "SEPARATOR_CANDIDATE"
    assert ints("bad") is None
    assert summary["production_code_modified"] is False

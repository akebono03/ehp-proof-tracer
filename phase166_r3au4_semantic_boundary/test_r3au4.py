from phase166_r3au4_semantic_boundary.audit import inspect, integers


def test_r3au4_distinguishes_element_length_from_coefficient_vector():
    result, rows = inspect([{"Element": "2 88 9", "gen_coe": "0 1 0 0 0 0 0 0 0 0 0 0", "generator": ""}])
    assert rows[0]["element_length"] == 3
    assert rows[0]["coefficient_length"] == 12
    assert rows[0]["lengths_differ"] is True
    assert result["per_position_Element_gen_coe_alignment_assumed"] is False


def test_r3au4_optional_generator_empty_is_not_error():
    summary, rows = inspect([{"Element": "2", "gen_coe": "1", "generator": ""}])
    assert summary["optional_reference_generator_blank"] == 1
    assert rows[0]["reference_generator_missing_is_error"] is False
    assert rows[0]["typed_expression_confirmed"] is False


def test_r3au4_handles_zero_and_multiple_coefficient_vectors():
    summary, rows = inspect([
        {"Element": "0", "gen_coe": "0 0 0", "generator": "0"},
        {"Element": "1 2", "gen_coe": "2 0 -1", "generator": "a+b"},
        {"Element": "", "gen_coe": "", "generator": ""},
    ])
    assert [r["coefficient_class"] for r in rows] == [
        "ZERO_COEFFICIENT_VECTOR", "MULTIPLE_NONZERO_COEFFICIENTS", "EMPTY_DATA_ROW"
    ]
    assert summary["typed_expression_certified"] == 0
    assert integers("1 x") is None

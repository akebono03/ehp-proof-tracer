from phase166_r3au2_generator_join_audit.audit import classify_gen_coe, inspect


def test_r3au2_coefficient_shapes():
    assert classify_gen_coe("1 0 0") == "single_basis"
    assert classify_gen_coe("0 -2 0") == "single_basis_with_coefficient"
    assert classify_gen_coe("1 0 -1") == "linear_combination"
    assert classify_gen_coe("0 0") == "all_zero"
    assert classify_gen_coe("") == "empty"
    assert classify_gen_coe("x") == "invalid"


def test_r3au2_join_marks_duplicates_and_missing_ids():
    master = [{"id": "1", "display": "η", "latex": "eta"},
              {"id": "1", "display": "eta", "latex": "eta"},
              {"id": "2", "display": "ν", "latex": "nu"}]
    sphere = [
        {"n": "2", "k": "1", "id": "0", "Element": "1", "gen_coe": "1", "generator": "η"},
        {"n": "5", "k": "9", "id": "0", "Element": "99", "gen_coe": "1", "generator": "a"},
        {"n": "20", "k": "12", "id": "0", "Element": "2", "gen_coe": "1", "generator": "ν"},
    ]
    summary, rows = inspect(sphere, master)
    assert [row["element_lookup_status"] for row in rows] == [
        "DUPLICATE_ID", "UNKNOWN_ID", "RESOLVED_IDS_NOT_VERIFIED"
    ]
    assert summary["outside_112_range_rows"] == 2
    assert summary["sphere_rows"] == 3


def test_r3au2_never_certifies_renderer_output_without_link():
    summary, rows = inspect(
        [{"n": "11", "k": "28", "id": "0", "Element": "3 4",
          "gen_coe": "1 -1", "generator": "C_1\\omega_23"}],
        [{"id": "3", "display": "C", "latex": "C"},
         {"id": "4", "display": "ω", "latex": "omega"}],
    )
    assert rows[0]["gen_coe_shape"] == "linear_combination"
    assert rows[0]["latex_comparison_status"] == "NOT_CONNECTED_TO_TYPED_RENDERER"
    assert rows[0]["mathematical_identity_confirmed"] is False
    assert summary["latex_comparisons"] == 0

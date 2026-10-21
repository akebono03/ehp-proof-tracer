from pathlib import Path

from phase166_r3au_gen_coe_cross_audit.audit import classify_shape, inspect, parse_int_list


def test_r3au_parse_and_shape_categories_cover_required_forms():
    assert parse_int_list("") == ()
    assert parse_int_list("0 1 0") == (0, 1, 0)
    assert parse_int_list("0 2 0") == (0, 2, 0)
    assert parse_int_list("1 -1 0") == (1, -1, 0)
    assert parse_int_list("x 1") is None
    assert classify_shape(()) == "empty"
    assert classify_shape((0, 1, 0)) == "single_basis"
    assert classify_shape((0, 2, 0)) == "single_basis_with_coefficient"
    assert classify_shape((1, -1, 0)) == "linear_combination"
    assert classify_shape(None) == "invalid"


def test_r3au_audits_high_stems_instead_of_limiting_to_112_groups():
    rows = [
        {
            "n": "3",
            "k": "2",
            "id": "0",
            "orders": "2",
            "generator": "eta",
            "Element": "1",
            "gen_coe": "1 0",
        },
        {
            "n": "20",
            "k": "12",
            "id": "0",
            "orders": "2",
            "generator": "high stem generator",
            "Element": "2",
            "gen_coe": "0 1",
        },
    ]
    summary, records = inspect(rows, Path("sphere(3).csv"))
    assert summary["sphere_rows"] == 2
    assert summary["limited_to_112_groups"] is False
    assert records[0]["within_112_public_groups"] is True
    assert records[1]["within_112_public_groups"] is False
    assert records[1]["k"] == "12"


def test_r3au_does_not_falsely_certify_unwired_gen_coe_latex():
    rows = [
        {
            "n": "11",
            "k": "28",
            "id": "3",
            "orders": "2",
            "generator": "sigma composite",
            "Element": "10 11 12 13",
            "gen_coe": "0 0 0 1",
        }
    ]
    summary, records = inspect(rows, Path("sphere(3).csv"))
    assert summary["typed_expression_from_gen_coe_available"] is False
    assert summary["generated_latex_comparison_completed"] == 0
    assert records[0]["generated_latex_from_gen_coe"] == ""
    assert records[0]["comparison_status"] == "UNWIRED_GEN_COE_TO_TYPED_EXPRESSION"
    assert records[0]["accuracy_confirmed"] is False

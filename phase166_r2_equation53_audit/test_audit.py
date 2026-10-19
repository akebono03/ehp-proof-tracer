"""Targeted tests for the (5.3) inspection. No proof permission is conferred."""
from types import SimpleNamespace
from phase166_r2_equation53_audit.audit import classify_53_row, inspect


def test_exact_display_pair_still_untyped():
    row = {"composition": r"\eta3^3", "rep_linear": r"2\nu'"}
    assert classify_53_row(row) == "EXACT_DISPLAY_PAIR_NOT_TYPED"


def test_other_composition_is_not_equated_with_double_relation():
    row = {"composition": r"\eta3^3(2\iota6)", "rep_linear": "0"}
    assert classify_53_row(row) == "OTHER_DISPLAY_PAIR_NOT_TYPED"


def test_missing_lhs_does_not_invent_equation():
    assert classify_53_row({"composition": "", "rep_linear": r"2E\nu'"}) == "INCOMPLETE_DISPLAY_PAIR"


def test_deduplication_is_observational_only():
    rows = [
        {"reference": "(5.3), source", "n": "3.0", "k": "3", "composition": r"\eta3^3", "rep_linear": r"2\nu'"},
        {"reference": "(5.3), source", "n": "3.0", "k": "3", "composition": r"\eta3^3", "rep_linear": r"2\nu'"},
    ]
    components = (SimpleNamespace(component_key="nu_prime_double_relation", statement_role=SimpleNamespace(value="relation")),)
    details, summary = inspect(rows, components)
    assert summary["distinct_display_signatures"] == 1
    assert [x["duplicate_display_count"] for x in details] == [2, 2]
    assert summary["mathematical_identity_confirmed"] == 0
    assert summary["proof_permission_granted"] == 0

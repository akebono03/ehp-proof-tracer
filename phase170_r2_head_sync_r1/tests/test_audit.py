"""Focused offline checks for Phase 170 R2 read-only classification helpers."""
from __future__ import annotations

import importlib.util
from pathlib import Path
from types import SimpleNamespace


def load_module():
    location = Path(__file__).resolve().parents[1] / "audit.py"
    spec = importlib.util.spec_from_file_location("phase170_r2_audit", location)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_integer_csv_coordinates_allow_spreadsheet_decimal():
    audit = load_module()
    assert audit.number_is("3.0", 3)
    assert audit.number_is("3", 3)
    assert not audit.number_is("3.5", 3)
    assert not audit.number_is("nan", 3)
    assert not audit.number_is("", 3)


def test_exact_rows_keep_original_data():
    audit = load_module()
    rows = [{"n": "3.0", "k": "3", "id": "a"},
            {"n": "3", "k": "2", "id": "b"},
            {"n": "", "k": "3", "id": "c"}]
    assert audit.exact_rows(rows, 3, 3) == [rows[0]]
    assert audit.exact_rows(rows, 3, 2) == [rows[1]]


def test_element_id_parser_distinguishes_bad_entries():
    audit = load_module()
    assert audit.parse_element_ids("2 3 4") == (2, 3, 4)
    assert audit.parse_element_ids("2,3") == (2, 3)
    assert audit.parse_element_ids("") == ()
    assert audit.parse_element_ids("eta_2") is None


def test_generator_id_diagnostics_never_infer_generator_relation():
    audit = load_module()
    rows = [{"Element": "1 2"}, {"Element": "1 3"}, {"Element": "bad"}]
    info = audit.generator_diagnostics(rows, [{"id": "1"}, {"id": "2"}])
    assert info["element_unknown_ids"] == [3]
    assert len(info["element_non_integer_rows"]) == 1


def test_reason_category_distinguishes_goal_from_proof_failure():
    audit = load_module()
    assert audit.reason_category({"r1_status": "search_failed", "selected_goal_count": 0}) == "NO_TYPED_GOAL_CANDIDATE"
    assert audit.reason_category({"r1_status": "search_failed", "selected_goal_count": 2}) == "AMBIGUOUS_TYPED_GOAL"
    assert audit.reason_category({"r1_status": "search_failed", "selected_goal_count": 1}) == "GOAL_EXISTS_SEARCH_OR_PREMISE_UNRESOLVED"
    assert audit.reason_category({"r1_status": "complete", "selected_goal_count": 1}) == "COMPLETE_RECORDED"


def test_source_position_diagnostic_does_not_claim_a_missing_theorem():
    audit = load_module()
    value = audit.reason_category({"r1_status": "search_failed", "selected_goal_count": 1,
                                   "r1_diagnostics": ["publication order unavailable"]})
    assert value == "SOURCE_ORDER_OR_CITATION_DIAGNOSTIC"


def test_package_keeps_twelve_recorded_samples():
    audit = load_module()
    assert len(audit.R1_GROUPS) == 12
    assert len(set(audit.R1_GROUPS)) == 12
    assert (2, 2) in audit.R1_GROUPS
    assert (5, 4) in audit.R1_GROUPS
    assert (8, 2) in audit.R1_GROUPS

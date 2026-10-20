"""Focused, non-mutating Phase 166 R3 audit checks."""
from pathlib import Path

from phase166_r3_order_audit.audit import collect


def test_inventory_result_has_core_fields():
    result = collect()
    assert isinstance(result["all_assertions"], int)
    assert isinstance(result["all_proof_links"], int)
    assert isinstance(result["selected_assertions"], list)


def test_inventory_never_grants_eligibility():
    result = collect()
    assert "no citation eligibility is granted" in result["note"]
    assert all("usable" not in row and "verified_assertion_ids" not in row for row in result["selected_assertions"])


def test_relevant_rows_have_explicit_optional_positions():
    result = collect()
    for row in result["selected_assertions"]:
        assert row["publication_position"] is None or isinstance(row["publication_position"], int)
        assert row["available_after_position"] is None or isinstance(row["available_after_position"], int)
        assert row["component_position"] is None or isinstance(row["component_position"], int)

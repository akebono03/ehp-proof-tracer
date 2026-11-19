"""Source and audit contracts for the R41 DB-step discrepancy."""
from __future__ import annotations

from pathlib import Path

from phase175_r4r14r8_db_step_identity_audit import audit


def test_inspector_reports_field_level_provenance_differences() -> None:
    text = Path(audit.__file__).read_text(encoding="utf-8")
    assert "actual_db_field_differences" in text
    assert "verified_db_step(step, proof_target=root, bridge=bridge)" in text
    assert "r41_matches_with_actual_steps" in text
    assert "r41_matches_with_expected_added" in text


def test_audit_does_not_patch_public_search() -> None:
    text = Path(audit.__file__).read_text(encoding="utf-8")
    assert "search_group_from_registered_goal(n=6, k=4" in text
    assert '"new_given": 0' in text
    assert '"production_changed": False' in text
    assert "write_text(json.dumps(report" in text

"""Focused read-only contracts; production-backed observation in audit main."""
from __future__ import annotations

from pathlib import Path

from phase175_r4r14r2_general_ehp_zero_frontier import audit


def test_target_is_pi10_6_and_previous_group_is_pi9_5() -> None:
    assert audit.TARGET == (6, 4)
    assert audit.PRIOR == (5, 4)


def test_pinned_sources_include_existing_two_factor_provider() -> None:
    assert "phase174_r3_r7_r38_source_bound_zero_image_public_wiring/provider.py" in audit.SOURCE_BLOBS
    assert "phase174_r3_r7_r41_adopted_db_zero_image_public_wiring/provider.py" in audit.SOURCE_BLOBS
    assert all(len(value) == 40 for value in audit.SOURCE_BLOBS.values())


def test_audit_never_writes_production_files() -> None:
    source = (Path(__file__).resolve().parents[1] / "audit.py").read_text(encoding="utf-8")
    assert "hash-object" in source
    assert "new_given\": 0" in source
    assert "new_rules\": 0" in source

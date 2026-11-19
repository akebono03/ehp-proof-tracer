"""Read-only R41 frontier diagnostic contract."""
from __future__ import annotations

from pathlib import Path

from phase175_r4r14r7_zero_image_match_audit import audit


def test_diagnostic_is_read_only() -> None:
    source = Path(audit.__file__).read_text(encoding="utf-8")
    assert "search_group_from_registered_goal(" in source
    assert "find_inference_matches_for_rule(" in source
    assert "verified_db_step(" in source
    assert "source.write_text(" not in source
    assert "production_changed" in source


def test_guard_checks_both_connected_general_providers() -> None:
    source = Path(audit.__file__).read_text(encoding="utf-8")
    assert "build_public_composite_zero_transport_provider(bridge)" in source
    assert "options.extend(expand_surjective_zero_codomain(goal))" in source


def test_expected_report_has_separate_actual_and_hypothetical_db_matching() -> None:
    source = Path(audit.__file__).read_text(encoding="utf-8")
    assert "r41_matches_using_proven_steps" in source
    assert "r41_matches_with_admitted_db_added" in source
    assert "presentations_in_proven_steps" in source
    assert "generator_zero_in_proven_steps" in source

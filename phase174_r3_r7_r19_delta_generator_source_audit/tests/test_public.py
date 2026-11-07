"""Public R19 frontier must remain proof-backed and incomplete."""
from __future__ import annotations

from phase174_r3_r7_r19_delta_generator_source_audit.audit import inspect_live_frontier


def test_public_delta_generator_gap_is_not_silently_completed() -> None:
    live = inspect_live_frontier()
    assert live["root_candidates"] == 1
    assert live["delta_public_candidates"] == 0
    assert live["delta_isolated_candidates"] == 1
    assert live["codomain_presentation_candidates"] == 1
    assert live["delta_image_public_candidates"] == 0
    assert live["signed_delta_witnesses"] == 0
    assert live["db_prior_admissible"] is True
    assert live["generator_expression_type"] == "HomotopyElement"
    assert live["generator_is_typed_map_application"] is False
    assert live["search_status"] == "search_failed"
    assert live["verified_steps"] == 0
    assert live["new_given"] == 0
    assert live["new_rules"] == 0
    assert live["completion_claimed"] is False

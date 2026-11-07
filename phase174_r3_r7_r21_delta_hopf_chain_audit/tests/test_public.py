"""Regression: R21 must not convert R20 source evidence into a proof leaf."""
from __future__ import annotations

from phase174_r3_r7_r21_delta_hopf_chain_audit.audit import inspect_public_frontier


def test_public_frontier_stays_unfinished() -> None:
    result = inspect_public_frontier()
    assert result["delta_public_candidates"] == 0
    assert result["delta_image_public_candidates"] == 0
    assert result["signed_delta_witnesses"] == 0
    assert result["generator_is_typed_map_application"] is False
    assert result["verified_steps"] == 0
    assert result["search_status"] == "search_failed"
    assert result["completion_claimed"] is False

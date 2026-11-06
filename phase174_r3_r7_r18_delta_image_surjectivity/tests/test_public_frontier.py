"""Focused live comparison: isolated proposals never certify the public root."""
from __future__ import annotations

from phase174_r3_r7_r18_delta_image_surjectivity.audit import inspect_live_frontier


def test_delta_surjectivity_is_a_candidate_not_a_certified_result() -> None:
    live = inspect_live_frontier()
    assert live["public_root_proposals"] == 1
    assert live["public_delta_surjectivity_proposals"] == 0
    assert live["isolated_delta_surjectivity_proposals"] == 1
    assert live["codomain_relation_is_goal_not_proof"] is True
    assert live["new_proof_steps_created"] == 0
    assert live["completion_claimed"] is False
    assert live["production_provider_changed"] is False
    assert live["search_status"] != "complete"

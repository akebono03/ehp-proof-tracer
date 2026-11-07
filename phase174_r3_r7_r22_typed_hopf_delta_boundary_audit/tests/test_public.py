"""Public frontier is an independently verified status, not an assumed result."""
from __future__ import annotations

from phase174_r3_r7_r22_typed_hopf_delta_boundary_audit.audit import (
    inspect_public_boundary, inspect_typed_boundary,
)


def test_typed_inputs_are_obligations_not_given_proof() -> None:
    result = inspect_typed_boundary()
    assert result["source_group"] == [13, 13]
    assert result["codomain_group"] == [11, 6]
    assert result["db_generator_is_typed_application"] is False
    assert result["independent_image_premise_required"] is True
    assert result["new_proof_steps"] == 0


def test_public_frontier_must_remain_unfinished() -> None:
    live = inspect_public_boundary()
    assert live["signed_delta_witnesses"] == 0
    assert live["verified_steps"] == 0
    assert live["search_status"] == "search_failed"
    assert live["completion_claimed"] is False

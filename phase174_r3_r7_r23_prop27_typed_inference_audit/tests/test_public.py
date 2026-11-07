"""R23 live public frontier must not be upgraded by source text alone."""
from __future__ import annotations

from phase174_r3_r7_r23_prop27_typed_inference_audit.audit import inspect_public_frontier


def test_public_hopf_delta_remains_open() -> None:
    result = inspect_public_frontier()
    assert result["typed_delta_witness"] is False
    assert result["signed_delta_witnesses"] == 0
    assert result["verified_steps"] == 0
    assert result["search_status"] == "search_failed"
    assert result["root_complete"] is False

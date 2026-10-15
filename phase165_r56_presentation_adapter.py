"""Completed canonical proof searches use the same narrative as partial searches."""
from __future__ import annotations

from phase165_r52_partial_proof import PartialProofResult, ProofSearchStatus


def render_completed_shared_narrative(result: PartialProofResult) -> str:
    """Preserve the public completed entry while sharing the proof text path."""
    if not isinstance(result, PartialProofResult):
        raise TypeError("result must be PartialProofResult")
    if result.status is not ProofSearchStatus.COMPLETE or result.conclusion is None:
        raise ValueError("a complete search is required")
    if getattr(result.conclusion, "lhs", None) != result.target:
        raise ValueError("completed target does not match conclusion")
    from toda_group_proof_generic_narrative_renderer import (
        render_toda_partial_proof_narrative_markdown,
    )
    return render_toda_partial_proof_narrative_markdown(result)

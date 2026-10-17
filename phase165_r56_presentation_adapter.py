"""Adapt completed canonical searches to the established public Toda narrative.

All mathematical evidence comes from the typed search's ProofStep ancestry.
The existing public renderer owns headings, citations and mathematical prose.
"""
from __future__ import annotations

from homotopy_groups import DirectSumGroup, FiniteCyclicGroup, FreeCyclicGroup
from phase165_r52_partial_proof import PartialProofResult, ProofSearchStatus
from proof import ProofRule
from proof_repository import ProofRepositoryEntry
from toda_group_result import TodaGroupResult
from toda_group_result_proof_replay import build_complete_toda_group_result_proof_replay
from toda_group_proof_presentation import build_toda_group_proof_presentation
from toda_group_proof_narrative_renderer import render_toda_group_proof_narrative_markdown


def render_completed_shared_narrative(result: PartialProofResult) -> str:
    """Render a certified complete search via the shared typed Narrative only."""
    if not isinstance(result, PartialProofResult):
        raise TypeError("result must be PartialProofResult")
    if result.status is not ProofSearchStatus.COMPLETE or result.conclusion is None:
        raise ValueError("a complete search is required")
    if getattr(result.conclusion, "lhs", None) != result.target:
        raise ValueError("completed target does not match conclusion")
    from toda_group_proof_narrative_renderer import render_toda_partial_proof_narrative_markdown
    return render_toda_partial_proof_narrative_markdown(result)

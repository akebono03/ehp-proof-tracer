"""Adapt a completed canonical search into the existing Toda presentation renderer.

No mathematical statements are invented; the root and its recursive ProofStep
premises come solely from the completed typed search.
"""
from __future__ import annotations

from homotopy_groups import DirectSumGroup, FiniteCyclicGroup, FreeCyclicGroup
from phase165_r52_partial_proof import PartialProofResult, ProofSearchStatus
from proof import ProofRule
from proof_repository import ProofRepositoryEntry
from toda_group_result import TodaGroupResult
from toda_group_result_proof_replay import build_complete_toda_group_result_proof_replay
from toda_group_proof_presentation import build_toda_group_proof_presentation
from toda_group_proof_narrative_blocks import build_toda_group_proof_narrative_blocks
from toda_group_proof_generic_narrative_renderer import render_toda_group_proof_generic_proof_markdown


def render_completed_shared_narrative(result: PartialProofResult) -> str:
    """Render COMPLETE proofs with existing whole-proof presentation machinery."""
    if not isinstance(result, PartialProofResult):
        raise TypeError("result must be PartialProofResult")
    if result.status is not ProofSearchStatus.COMPLETE or result.conclusion is None:
        raise ValueError("a complete search is required")
    conclusion = result.conclusion
    if getattr(conclusion, "lhs", None) != result.target:
        raise ValueError("completed target does not match conclusion")
    structure = getattr(conclusion, "rhs", None)
    if not isinstance(structure, (FreeCyclicGroup, FiniteCyclicGroup, DirectSumGroup)):
        raise ValueError("unsupported group structure in completed goal")
    roots = [step for step in result.proven_steps if step.conclusion == conclusion]
    if len(roots) != 1 or roots[0].rule is not ProofRule.INFERENCE:
        raise ValueError("completed proof must contain exactly one derived root")
    root = roots[0]
    if isinstance(structure, FreeCyclicGroup):
        generators = (structure.generator,)
        orders = (None,)
    elif isinstance(structure, FiniteCyclicGroup):
        generators = (structure.generator,)
        orders = (structure.order,)
    else:
        # Direct sums require their own typed generator decomposition and must
        # not be guessed by the display adapter.
        raise ValueError("direct-sum presentation requires typed generators")
    entry = ProofRepositoryEntry(key="phase165:typed:completed", step=root, phase="165")
    group_result = TodaGroupResult(
        target=result.target,
        group_structure=structure,
        generators=generators,
        generator_orders=orders,
        source_entry=entry,
        proof_step=root,
    )
    replay = build_complete_toda_group_result_proof_replay(group_result)
    presentation = build_toda_group_proof_presentation(replay)
    blocks = build_toda_group_proof_narrative_blocks(presentation)
    body = render_toda_group_proof_generic_proof_markdown(presentation, blocks)
    # The common renderer owns mathematical prose. Here only the public
    # headings are added; citations must come from verified provenance.
    return "## 証明対象\n\n$\\pi_{%d}^{%d}$\n\n## 使用する結果（Reference）\n\n%s\n\n## 証明（Proof）\n\n%s" % (
        result.target.group_dimension,
        result.target.sphere_dimension,
        "\n".join("- " + source for source in result.references)
        if result.references else "出典情報は検証済み ProofStep との対応確認待ち。",
        body,
    )

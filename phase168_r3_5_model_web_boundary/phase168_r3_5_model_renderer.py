"""Render an explicitly supplied Proof Narrative Model without source inference."""
from __future__ import annotations

from phase165_r52_partial_proof import PartialProofResult, ProofSearchStatus
from phase168_r3_3_proof_narrative_model import ProofNarrativeModel
from proof import ProofRule
from web_group_proof_common import _group_proof_statement_latex


def render_model_backed_narrative_markdown(
    result: PartialProofResult, model: ProofNarrativeModel,
) -> str:
    """Render only used steps and citations already selected by the model.

    This is an opt-in transitional boundary. It does not attempt to reproduce
    the established long-form mathematical argument or infer references.
    """
    if not isinstance(result, PartialProofResult):
        raise TypeError("result must be PartialProofResult")
    if not isinstance(model, ProofNarrativeModel):
        raise TypeError("model must be ProofNarrativeModel")
    if model.steps != result.proven_steps:
        raise ValueError("model steps must match the searched result")
    if len(model.step_citation_numbers) != len(model.steps):
        raise ValueError("step citation mapping has the wrong length")
    if result.status is ProofSearchStatus.COMPLETE and model.root_index is None:
        raise ValueError("complete result requires a root step")

    lines = ["使用する結果", ""]
    for citation in model.citations:
        locator = citation.reference.locator or citation.reference.label
        lines.append(f"**[R{citation.number}] {locator}.**")
        lines.append("")
    lines.extend(("証明", ""))
    for index, step in enumerate(model.steps):
        latex, fallback_type = _group_proof_statement_latex(step.conclusion)
        if latex is None or fallback_type is not None:
            # Do not fabricate a mathematical statement from a Python repr.
            continue
        numbers = model.step_citation_numbers[index]
        tags = ", ".join(f"[R{number}]" for number in numbers)
        if step.rule is ProofRule.GIVEN:
            prefix = f"{tags}より, " if tags else "前提として, "
        elif index == model.root_index:
            prefix = f"{tags}を用いて, " if tags else "以上より, "
        else:
            prefix = f"{tags}を用いて, " if tags else "導出により, "
        lines.append(f"{prefix}${latex}$ を得る.")
        lines.append("")
    if result.status is ProofSearchStatus.COMPLETE:
        lines.append("□")
    return "\n".join(lines).rstrip() + "\n"

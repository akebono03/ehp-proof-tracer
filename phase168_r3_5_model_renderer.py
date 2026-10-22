"""Render an explicitly supplied Proof Narrative Model without source inference."""
from __future__ import annotations

from phase165_r52_partial_proof import PartialProofResult, ProofSearchStatus
from phase168_r3_3_proof_narrative_model import ProofNarrativeModel
from phase168_r3_12_body_binding import build_narrative_body_lines


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
    body_lines = build_narrative_body_lines(result, model)

    lines = ["使用する結果", ""]
    for citation in model.citations:
        locator = citation.reference.locator or citation.reference.label
        lines.append(f"**[R{citation.number}] {locator}.**")
        lines.append("")
    lines.extend(("証明", ""))
    for body_line in body_lines:
        tags = ", ".join(f"[R{number}]" for number in body_line.citation_numbers)
        if body_line.role == "given":
            prefix = f"{tags}より, " if tags else "前提として, "
        elif body_line.role == "root":
            prefix = f"{tags}を用いて, " if tags else "以上より, "
        else:
            prefix = f"{tags}を用いて, " if tags else "導出により, "
        lines.append(f"{prefix}${body_line.statement_latex}$ を得る.")
        lines.append("")
    if result.status is ProofSearchStatus.COMPLETE:
        lines.append("□")
    return "\n".join(lines).rstrip() + "\n"

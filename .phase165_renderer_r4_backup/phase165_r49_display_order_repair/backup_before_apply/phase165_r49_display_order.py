"""R49: finish typed reason placement after the existing narrative ordering."""

from toda_group_proof_generic_narrative_renderer import _render_generic_narrative_step
from toda_group_proof_narrative_reasons import TodaGroupProofNarrativeReasonKind


def finalize_phase165_r49_typed_reason_order(markdown: str, reason_sidecar) -> str:
    """Order the two typed reasons; keep the existing narrative pipeline authoritative."""
    if not isinstance(markdown, str):
        raise TypeError("markdown must be a str")
    paragraphs = markdown.split("\n\n")

    def normalized(value: str) -> str:
        return value.strip().rstrip(".。 ")

    def matches_line(paragraph: str, line: str) -> bool:
        return normalized(paragraph) == normalized(line)

    for reason in reason_sidecar.reasons:
        if reason.kind is not TodaGroupProofNarrativeReasonKind.EXACTNESS_TO_DELTA_ZERO:
            continue
        conclusion = _render_generic_narrative_step(reason.conclusion_step)
        reason_indices = [i for i, p in enumerate(paragraphs)
                          if "\\operatorname{Im}" in p and "\\ker" in p
                          and "は零写像" in p and "完全性より" in p]
        if len(reason_indices) != 1:
            continue
        standalone = [i for i, p in enumerate(paragraphs)
                      if matches_line(p, conclusion)]
        if len(standalone) == 1:
            paragraphs.pop(standalone[0])

    for reason in reason_sidecar.reasons:
        if reason.kind is not TodaGroupProofNarrativeReasonKind.INJECTIVE_SURJECTIVE_TO_ISOMORPHISM:
            continue
        if len(reason.premise_steps) != 2:
            continue
        conclusion = _render_generic_narrative_step(reason.conclusion_step)
        premise_lines = [_render_generic_narrative_step(step) for step in reason.premise_steps]
        if not conclusion or any(not line for line in premise_lines):
            continue
        premise_positions = []
        for line in premise_lines:
            hits = [i for i, p in enumerate(paragraphs) if matches_line(p, line)]
            if len(hits) != 1:
                break
            premise_positions.append(hits[0])
        if len(premise_positions) != 2:
            continue
        reason_hits = [i for i, p in enumerate(paragraphs)
                       if p.strip().startswith("単射性と全射性より,")
                       and normalized(conclusion) in normalized(p)]
        if len(reason_hits) != 1:
            continue
        reason_paragraph = paragraphs.pop(reason_hits[0])
        standalone_hits = [i for i, p in enumerate(paragraphs) if matches_line(p, conclusion)]
        if len(standalone_hits) == 1:
            paragraphs.pop(standalone_hits[0])
        premise_positions = []
        for line in premise_lines:
            hits = [i for i, p in enumerate(paragraphs) if matches_line(p, line)]
            if len(hits) != 1:
                break
            premise_positions.append(hits[0])
        if len(premise_positions) != 2:
            continue
        paragraphs.insert(max(premise_positions) + 1, reason_paragraph)

    return "\n\n".join(paragraphs)

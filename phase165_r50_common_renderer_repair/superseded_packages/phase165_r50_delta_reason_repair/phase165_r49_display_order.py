"""R49: place typed reasons after their rendered premises without changing proof logic."""

from toda_group_proof_generic_narrative_renderer import _render_generic_narrative_step
from toda_group_proof_narrative_reasons import TodaGroupProofNarrativeReasonKind


def finalize_phase165_r49_typed_reason_order(markdown: str, reason_sidecar) -> str:
    """Place the existing typed explanations in dependency order and deduplicate."""
    if not isinstance(markdown, str):
        raise TypeError("markdown must be a str")
    paragraphs = markdown.split("\n\n")

    def normalize(value: str) -> str:
        return value.strip().rstrip(".。 ").replace("同型写像である", "同型").replace("である", "")

    def statement_parts(step):
        rendered = _render_generic_narrative_step(step)
        if not rendered or " は" not in rendered:
            return None
        subject, property_text = rendered.split(" は", 1)
        return normalize(subject), normalize(property_text)

    def matching_indices(step):
        parts = statement_parts(step)
        if parts is None:
            return []
        subject, property_text = parts
        if property_text.startswith("単射"):
            marker = "は単射"
        elif property_text.startswith("全射"):
            marker = "は全射"
        elif property_text.startswith("同型"):
            marker = "は同型"
        else:
            return []
        return [index for index, paragraph in enumerate(paragraphs)
                if subject in normalize(paragraph) and marker in paragraph]

    for reason in reason_sidecar.reasons:
        if reason.kind is not TodaGroupProofNarrativeReasonKind.EXACTNESS_TO_DELTA_ZERO:
            continue
        detailed = [i for i, paragraph in enumerate(paragraphs)
                    if "完全性より" in paragraph
                    and "\\operatorname{Im}" in paragraph
                    and "\\ker" in paragraph
                    and "は零写像" in paragraph]
        if not detailed:
            from toda_group_proof_narrative_reason_renderer import (
                render_toda_group_proof_narrative_reason_sentence,
            )
            explanation = render_toda_group_proof_narrative_reason_sentence(reason)
            conclusion = _render_generic_narrative_step(reason.conclusion_step)
            if not explanation or not conclusion:
                continue
            # Only a proven Delta-zero typed reason may restore this text.
            # Reference linkage may prefix or replace the old bare paragraph.
            delta_mentions = [
                i for i, paragraph in enumerate(paragraphs)
                if "は零写像" in paragraph
                and "\\Delta" in paragraph
                and "\\operatorname{Im}" not in paragraph
            ]
            if len(delta_mentions) == 1:
                index = delta_mentions[0]
                paragraph = paragraphs[index]
                # Preserve a pre-existing citation prefix, when present.
                prefix = ""
                if paragraph.startswith("[R") and "]" in paragraph:
                    prefix = paragraph.split("]", 1)[0] + "]より, "
                paragraphs[index] = prefix + explanation
                detailed = [index]
            elif not delta_mentions:
                # When body suppression removed the conclusion as well,
                # anchor the exactness explanation immediately before the
                # matching Hopf-surjectivity conclusion. Never insert if the
                # proof did not expose that dependent statement.
                surjectivity = [
                    i for i, paragraph in enumerate(paragraphs)
                    if "は全射" in paragraph
                    and "H:" in paragraph
                    and "\\pi_{3}^{2}" in paragraph
                    and "\\pi_{3}^{3}" in paragraph
                ]
                if len(surjectivity) == 1:
                    paragraphs.insert(surjectivity[0], explanation)
                    detailed = [surjectivity[0]]
        if len(detailed) != 1:
            continue
        rendered = _render_generic_narrative_step(reason.conclusion_step)
        if not rendered:
            continue
        standalone = [i for i, paragraph in enumerate(paragraphs)
                      if normalize(paragraph) == normalize(rendered)]
        for index in reversed(standalone):
            paragraphs.pop(index)

    for reason in reason_sidecar.reasons:
        if reason.kind is not TodaGroupProofNarrativeReasonKind.INJECTIVE_SURJECTIVE_TO_ISOMORPHISM:
            continue
        if len(reason.premise_steps) != 2:
            continue
        premises = list(reason.premise_steps)
        premise_parts = [statement_parts(step) for step in premises]
        conclusion_parts = statement_parts(reason.conclusion_step)
        if (any(parts is None for parts in premise_parts)
                or conclusion_parts is None
                or not all(parts[0] == conclusion_parts[0] for parts in premise_parts)
                or sorted(parts[1][:2] for parts in premise_parts) != sorted(["単射", "全射"])):
            continue
        reason_hits = [i for i, paragraph in enumerate(paragraphs)
                       if "単射性と全射性より" in paragraph
                       and conclusion_parts[0] in normalize(paragraph)
                       and "は同型" in paragraph]
        if len(reason_hits) != 1:
            continue
        premise_hits = [matching_indices(step) for step in premises]
        if any(len(hits) != 1 for hits in premise_hits):
            continue
        reason_text = paragraphs.pop(reason_hits[0])
        # Remove only standalone conclusions for this exact map.
        standalone = [i for i in matching_indices(reason.conclusion_step)
                      if "単射性と全射性より" not in paragraphs[i]]
        for index in reversed(standalone):
            paragraphs.pop(index)
        premise_hits = [matching_indices(step) for step in premises]
        if any(len(hits) != 1 for hits in premise_hits):
            # Defensive restoration on any unexpected downstream wording.
            paragraphs.insert(min(reason_hits[0], len(paragraphs)), reason_text)
            continue
        paragraphs.insert(max(hits[0] for hits in premise_hits) + 1, reason_text)

    return "\n\n".join(paragraphs)

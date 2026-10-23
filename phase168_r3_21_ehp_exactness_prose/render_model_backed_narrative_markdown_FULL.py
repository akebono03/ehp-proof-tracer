def render_model_backed_narrative_markdown(
    result: PartialProofResult, model: ProofNarrativeModel,
) -> str:
    """Render verified model steps, including typed EHP image/kernel equality."""
    from map_facts import EHP_DELTA_MAP, EHP_E_MAP, EHP_H_MAP
    from phase165_r12_r11_prop42_unified import prop42_exactness_indices
    from phase165_r12_r12_ehp_consequences import EHPImageEqualsKernelStatement
    from toda_rules import TodaProp42ExactnessStatement

    if not isinstance(result, PartialProofResult):
        raise TypeError("result must be PartialProofResult")
    if not isinstance(model, ProofNarrativeModel):
        raise TypeError("model must be ProofNarrativeModel")
    body_lines = build_narrative_body_lines(result, model)
    body_by_step = {line.step_index: line for line in body_lines}

    lines = ["使用する結果", ""]
    for citation in model.citations:
        locator = citation.reference.locator or citation.reference.label
        lines.append(f"**[R{citation.number}] {locator}.**")
        lines.append("")
    lines.extend(("証明", ""))
    for index, step in enumerate(model.steps):
        body_line = body_by_step.get(index)
        if body_line is None:
            statement = step.conclusion
            if isinstance(statement, EHPImageEqualsKernelStatement):
                window = statement.window
                if prop42_exactness_indices(TodaProp42ExactnessStatement(window)) is None:
                    continue
                if window.first_map == EHP_DELTA_MAP and window.second_map == EHP_E_MAP:
                    latex = r"\operatorname{Im}\Delta=\ker E"
                elif window.first_map == EHP_E_MAP and window.second_map == EHP_H_MAP:
                    latex = r"\operatorname{Im}E=\ker H"
                else:
                    continue
                tags = ", ".join(f"[R{number}]" for number in model.step_citation_numbers[index])
                intro = f"{tags}に基づく完全性より, " if tags else "完全性より, "
                lines.append(f"{intro}${latex}$ が成り立つ.")
                lines.append("")
            continue
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

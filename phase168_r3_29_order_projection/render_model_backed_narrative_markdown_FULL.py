def render_model_backed_narrative_markdown(
    result: PartialProofResult, model: ProofNarrativeModel,
) -> str:
    """Render typed conclusions from Proof Tree; references come only from model."""
    from proof import ProofRule
    from map_facts import EHP_DELTA_MAP, EHP_E_MAP, EHP_H_MAP
    from toda_rules import TodaProp42ExactnessStatement
    from phase168_r3_29_order_projection import project_narrative_order
    from phase168_r3_26_exactness_projection import project_exactness_chains
    from phase168_r3_27_typed_statement_projection import group_tex, typed_sentence

    if not isinstance(result, PartialProofResult):
        raise TypeError("result must be PartialProofResult")
    if not isinstance(model, ProofNarrativeModel):
        raise TypeError("model must be ProofNarrativeModel")
    body_lines = build_narrative_body_lines(result, model)
    body_by_step = {line.step_index: line for line in body_lines}

    chains = project_exactness_chains(model)
    suppressed_exactness = {index for chain in chains for index in chain.step_indices}

    order = project_narrative_order(model, suppressed_exactness)
    lines = ["使用する結果", ""]
    for citation in model.citations:
        locator = citation.reference.locator or citation.reference.label
        lines.append(f"**[R{citation.number}] {locator}.**")
        lines.append("")
    lines.extend(("証明", ""))
    for chain in chains:
        map_tex = {EHP_E_MAP: "E", EHP_H_MAP: "H", EHP_DELTA_MAP: r"\Delta"}
        sequence = group_tex(chain.arrows[0][0])
        for source, symbol, target in chain.arrows:
            if group_tex(target) is None or symbol not in map_tex:
                raise ValueError("unsupported certified exactness arrow")
            sequence += rf" \xrightarrow{{{map_tex[symbol]}}} {group_tex(target)}"
        lines.append("群構造を決定するために, 次の完全列を考える.")
        lines.append("")
        lines.append(f"${sequence}$.")
        lines.append("")
    for entry in order:
        index = entry.step_index
        step = model.steps[index]
        body_line = body_by_step.get(index)
        if body_line is None:
            sentence = typed_sentence(step.conclusion, step)
            if sentence is not None:
                numbers = model.step_citation_numbers[index]
                tags = ", ".join(f"[R{number}]" for number in numbers)
                if tags and step.rule is ProofRule.GIVEN:
                    sentence = f"{tags}より, " + sentence
                lines.extend((sentence, ""))
            continue
        tags = ", ".join(f"[R{number}]" for number in body_line.citation_numbers)
        if body_line.role == "given":
            prefix = f"{tags}より, " if tags else "前提として, "
        elif body_line.role == "root":
            prefix = f"{tags}を用いて, " if tags else "以上より, "
        else:
            prefix = f"{tags}を用いて, " if tags else "導出により, "
        statement_latex = body_line.statement_latex
        if isinstance(step.conclusion, TodaProp42ExactnessStatement):
            statement_latex = statement_latex.replace(r" \text{ is exact}", "")
            lines.append(f"{prefix}${statement_latex}$ は完全列である.")
        else:
            lines.append(f"{prefix}${statement_latex}$ を得る.")
        lines.append("")
        for postponed in entry.after_indices:
            postponed_step = model.steps[postponed]
            sentence = typed_sentence(postponed_step.conclusion, postponed_step)
            if sentence is not None:
                lines.extend((sentence, ""))
    if result.status is ProofSearchStatus.COMPLETE:
        lines.append("□")
    return "\n".join(lines).rstrip() + "\n"

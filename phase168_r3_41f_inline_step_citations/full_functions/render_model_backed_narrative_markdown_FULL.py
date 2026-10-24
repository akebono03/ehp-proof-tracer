def render_model_backed_narrative_markdown(
    result: PartialProofResult, model: ProofNarrativeModel,
) -> str:
    """Render typed Proof Tree steps; preserve incomplete search state from model."""
    from proof import ProofRule
    from map_facts import EHP_DELTA_MAP, EHP_E_MAP, EHP_H_MAP
    from toda_rules import TodaProp42ExactnessStatement
    from phase168_r3_29_order_projection import project_narrative_order
    from phase168_r3_26_exactness_projection import project_exactness_chains
    from phase168_r3_27_typed_statement_projection import (
        group_tex, typed_sentence, toda45_specialization_evidence,
        project_toda45_specialization_citation_numbers,
        project_stable_eta_notation_transition,
    )

    if not isinstance(result, PartialProofResult):
        raise TypeError("result must be PartialProofResult")
    if not isinstance(model, ProofNarrativeModel):
        raise TypeError("model must be ProofNarrativeModel")
    body_lines = build_narrative_body_lines(result, model)
    body_by_step = {line.step_index: line for line in body_lines}

    incomplete = result.status is not ProofSearchStatus.COMPLETE
    if incomplete and (
        model.status is not result.status
        or model.target != result.target
        or model.open_goals != result.open_goals
        or model.diagnostics != result.diagnostics
    ):
        raise ValueError("narrative model partial state must match searched result")

    if incomplete:
        # A partial Proof Tree may contain pending premises. Display each
        # observed step in its recorded order, without claiming a new proof.
        chains = ()
        order = tuple(range(len(model.steps)))
        target_latex = group_tex(model.target)
        if target_latex is None:
            raise ValueError("unsupported partial target group")
        lines = ["## 証明対象", "", f"${target_latex}$", "", "## 使用する結果", ""]
    else:
        chains = project_exactness_chains(model)
        suppressed_exactness = {index for chain in chains for index in chain.step_indices}
        order = tuple(entry.step_index for entry in project_narrative_order(model, suppressed_exactness))
        lines = ["使用する結果", ""]

    for citation in model.citations:
        locator = citation.reference.locator or citation.reference.label
        lines.append(f"**[R{citation.number}] {locator}.**")
        lines.append("")
        for sentence in citation.statement_bodies:
            lines.extend((sentence, ""))
    if incomplete:
        if not model.citations:
            lines.extend(("参照情報を持つ ProofStep はありません。", ""))
        labels = {
            ProofSearchStatus.NOT_SEARCHED: "未探索",
            ProofSearchStatus.PARTIAL: "部分証明・未完成",
            ProofSearchStatus.SEARCH_FAILED: "証明未完成",
        }
        lines.extend(("---", "", "## 証明", "", f"**探索状態：{labels[model.status]}**", ""))
        if model.steps:
            lines.extend(("### 確認済み ProofStep（与件を含む）", ""))
    else:
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
    from homotopy_groups import TodaPrimaryGroupZeroStatement
    from expression import ScalarSymbol
    from web_group_proof_common import _group_proof_statement_latex
    for index in order:
        step = model.steps[index]
        statement = step.conclusion
        if incomplete:
            body_line = body_by_step.get(index)
            if isinstance(statement, str):
                statement_text = statement
            elif body_line is not None:
                statement_text = f"${body_line.statement_latex}$"
            else:
                sentence = typed_sentence(statement, step)
                if sentence is not None:
                    statement_text = sentence
                else:
                    # Preserve a truthful placeholder, not a guessed formula.
                    latex, fallback = _group_proof_statement_latex(statement)
                    statement_text = (f"${latex}$" if latex is not None and fallback is None
                                      else type(statement).__name__ + "（数式表示未対応）")
            role = "与件" if step.rule is ProofRule.GIVEN else "推論"
            numbers = model.step_citation_numbers[index]
            tags = ", ".join(f"[R{number}]" for number in numbers)
            if tags:
                source_prefix = f"{tags}より, " if step.rule is ProofRule.GIVEN else f"{tags}を用いて, "
            else:
                source_prefix = ""
            lines.append(f"- {role}: {source_prefix}{statement_text}")
            continue
        # The symbolic circle theorem belongs in Reference; the proof uses
        # its certified integer specialization and must not lose i > 1.
        if (isinstance(statement, TodaPrimaryGroupZeroStatement)
                and statement.group.sphere_dimension == 1
                and isinstance(statement.group.group_dimension, ScalarSymbol)):
            continue
        # Only verbalize the certified stable-eta normalization already
        # represented by this step's source relation and cited definition.
        transition = project_stable_eta_notation_transition(model, index)
        if transition is not None:
            lines.extend((transition, ""))
        body_line = body_by_step.get(index)
        if body_line is None:
            sentence = typed_sentence(step.conclusion, step)
            if sentence is not None:
                numbers = model.step_citation_numbers[index]
                tags = ", ".join(f"[R{number}]" for number in numbers)
                if tags and step.rule is ProofRule.GIVEN:
                    sentence = f"{tags}より, " + sentence
                elif step.rule is ProofRule.INFERENCE:
                    sourced_numbers = project_toda45_specialization_citation_numbers(
                        model, index
                    )
                    if sourced_numbers:
                        source_tags = ", ".join(
                            f"[R{number}]" for number in sourced_numbers
                        )
                        sentence = f"{source_tags}を " + sentence
                lines.extend((sentence, ""))
        else:
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
    if incomplete:
        if model.open_goals:
            lines.extend(("", "## 未解決 Goal", ""))
            for goal in model.open_goals:
                if isinstance(goal, str):
                    shown = goal
                else:
                    latex, fallback = _group_proof_statement_latex(goal)
                    shown = (f"${latex}$" if latex is not None and fallback is None
                             else type(goal).__name__ + "（数式表示未対応）")
                lines.append("- " + shown)
        if model.diagnostics:
            lines.extend(("", "## 探索診断", ""))
            for diagnostic in model.diagnostics:
                lines.append("- " + diagnostic)
        lines.extend(("", "未解決 Goal は証明済みの結論ではありません。"))
    else:
        lines.append("□")
    return "\n".join(lines).rstrip() + "\n"

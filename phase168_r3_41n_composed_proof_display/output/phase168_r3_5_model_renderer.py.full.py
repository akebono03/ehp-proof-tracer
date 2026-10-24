"""Render an explicitly supplied Proof Narrative Model without source inference."""
from __future__ import annotations

from phase165_r52_partial_proof import PartialProofResult, ProofSearchStatus
from phase168_r3_3_proof_narrative_model import ProofNarrativeModel
from phase168_r3_12_body_binding import build_narrative_body_lines


def render_model_backed_narrative_markdown(
    result: PartialProofResult, model: ProofNarrativeModel,
) -> str:
    """Render typed Proof Tree steps; preserve incomplete search state from model."""
    from proof import ProofRule
    from map_facts import EHP_DELTA_MAP, EHP_E_MAP, EHP_H_MAP
    from toda_rules import TodaProp42ExactnessStatement
    from phase165_r14_r14_diagonal_and_prop42 import GeneratorSuspension
    from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
    from phase165_r12_r11_prop42_unified import TodaProp42GeneralExactnessStatement
    from phase165_r12_r21_eta_generator_chain import _eta_pair
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

    def cited_general_ancestor_numbers(step, given_type):
        """Return only registered citations of typed GIVEN proof ancestors."""
        numbers = []
        visited = set()
        pending = [step]
        while pending:
            ancestor = pending.pop()
            if id(ancestor) in visited:
                continue
            visited.add(id(ancestor))
            if ancestor.rule is ProofRule.GIVEN and isinstance(ancestor.conclusion, given_type):
                for source_index, candidate in enumerate(model.steps):
                    if candidate == ancestor:
                        for number in model.step_citation_numbers[source_index]:
                            if number not in numbers:
                                numbers.append(number)
                        break
            pending.extend(ancestor.premises)
        return tuple(numbers)

    def validated_specialization_citation_numbers(step):
        """Cite a direct typed general premise only after validating its indices."""
        from homotopy_groups import TodaPrimaryGroupZeroStatement
        from phase165_r12_r15_toda51 import Toda51BelowDiagonalZeroStatement
        from phase165_r57_r20_general_specialization import specialize_typed_statement
        from proof import Relation

        if step.rule is not ProofRule.INFERENCE or len(step.premises) != 1:
            return ()
        source_step = step.premises[0]
        if source_step.rule is not ProofRule.GIVEN:
            return ()
        source = source_step.conclusion
        target = step.conclusion
        valid = False
        if isinstance(target, Relation) and isinstance(source, Relation):
            valid = specialize_typed_statement(source, target) is not None
        elif isinstance(target, TodaPrimaryGroupZeroStatement):
            if isinstance(source, TodaPrimaryGroupZeroStatement):
                valid = specialize_typed_statement(source, target) is not None
            elif isinstance(source, Toda51BelowDiagonalZeroStatement):
                group = target.group
                i, n = group.group_dimension, group.sphere_dimension
                valid = (type(i) is int and type(n) is int
                         and 0 <= i < n and n >= 2)
        if not valid:
            return ()
        return tuple(dict.fromkeys(
            number
            for source_index, candidate in enumerate(model.steps)
            if candidate == source_step
            for number in model.step_citation_numbers[source_index]
        ))

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
        # The merged sequence stands for these certified exactness ProofSteps.
        # Cite their own sources; never search bibliography labels by text.
        exactness_numbers = tuple(dict.fromkeys(
            number
            for step_index in chain.step_indices
            for number in (
                model.step_citation_numbers[step_index]
                + cited_general_ancestor_numbers(
                    model.steps[step_index], TodaProp42GeneralExactnessStatement
                )
            )
        ))
        if exactness_numbers:
            tags = ", ".join(f"[R{number}]" for number in exactness_numbers)
            lines.append(f"群構造を決定するために, {tags}を用いて次の完全列を考える.")
        else:
            lines.append("群構造を決定するために, 次の完全列を考える.")
        lines.append("")
        lines.append(f"${sequence}$.")
        lines.append("")
    # A later certified step can subsume a purely intermediate display step.
    # Keep both ProofSteps in the tree; omit prose only when the consumed
    # premise has no distinct citation and no other consumers.
    suppressed_body_indices = set()
    if not incomplete:
        from homotopy_groups import FiniteCyclicGroup, TodaDeltaMap, TodaSuspensionMap
        from phase165_r12_r12_ehp_consequences import EHPImageEqualsKernelStatement
        from phase165_r12_r13_kernel_image import SuspensionKernelFreeCyclicStatement
        from phase166_r3v_generator_transport import generator_transport_normalization_rule
        from toda_rules import TodaDeltaImageFreeCyclicStatement

        def unique_step_index(premise):
            matches = [i for i, candidate in enumerate(model.steps) if candidate is premise]
            if len(matches) == 1:
                return matches[0]
            if matches:
                return None
            matches = [i for i, candidate in enumerate(model.steps) if candidate == premise]
            return matches[0] if len(matches) == 1 else None

        def only_consumed_by(candidate, consumer):
            return sum(
                any(parent is candidate or parent == candidate for parent in step.premises)
                for step in model.steps
            ) == 1 and any(
                parent is candidate or parent == candidate for parent in consumer.premises
            )

        for later_index in order:
            consumer = model.steps[later_index]
            conclusion = consumer.conclusion
            if (consumer.rule is ProofRule.INFERENCE
                    and isinstance(conclusion, SuspensionKernelFreeCyclicStatement)
                    and len(consumer.premises) == 2):
                image_step, equality_step = consumer.premises
                image = image_step.conclusion
                equality = equality_step.conclusion
                if (isinstance(image, TodaDeltaImageFreeCyclicStatement)
                        and isinstance(equality, EHPImageEqualsKernelStatement)
                        and image.image_group == conclusion.kernel_group
                        and equality.window.first_map == EHP_DELTA_MAP
                        and equality.window.second_map == EHP_E_MAP
                        and image.map == TodaDeltaMap(
                            equality.window.source_term, equality.window.middle_term
                        )
                        and conclusion.map == TodaSuspensionMap(
                            equality.window.middle_term, equality.window.target_term
                        )):
                    earlier_index = unique_step_index(equality_step)
                    if (earlier_index is not None
                            and earlier_index in order
                            and earlier_index != model.root_index
                            and equality_step.rule is ProofRule.INFERENCE
                            and not model.step_citation_numbers[earlier_index]
                            and only_consumed_by(equality_step, consumer)):
                        suppressed_body_indices.add(earlier_index)

            if (consumer.rule is ProofRule.INFERENCE
                    and isinstance(conclusion, Relation)
                    and len(consumer.premises) == 2
                    and isinstance(conclusion.rhs, FiniteCyclicGroup)):
                transported_step, witness_step = consumer.premises
                transported = transported_step.conclusion
                if (transported_step.rule is ProofRule.INFERENCE
                        and isinstance(transported, Relation)
                        and isinstance(transported.rhs, FiniteCyclicGroup)
                        and isinstance(witness_step.conclusion, GeneratorSuspension)
                        and generator_transport_normalization_rule(conclusion).match_guard(
                            consumer.premises, {}
                        )):
                    earlier_index = unique_step_index(transported_step)
                    if (earlier_index is not None
                            and earlier_index in order
                            and earlier_index != model.root_index
                            and not model.step_citation_numbers[earlier_index]
                            and only_consumed_by(transported_step, consumer)):
                        suppressed_body_indices.add(earlier_index)
    from homotopy_groups import TodaPrimaryGroupZeroStatement
    from expression import ScalarSymbol
    from proof import Relation
    from homotopy_groups import TodaPrimaryGroup
    from web_group_proof_common import _group_proof_statement_latex
    for index in order:
        if index in suppressed_body_indices:
            continue
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
        # A cited symbolic diagonal GIVEN is the Reference's general schema.
        # Only its concrete proof specializations belong in the proof body.
        if (step.rule is ProofRule.GIVEN
                and isinstance(statement, Relation)
                and isinstance(statement.lhs, TodaPrimaryGroup)
                and isinstance(statement.lhs.group_dimension, ScalarSymbol)
                and statement.lhs.group_dimension == statement.lhs.sphere_dimension
                and any(
                    citation.number in model.step_citation_numbers[index]
                    and any(r"\pi_{n}^{n}" in body for body in citation.statement_bodies)
                    for citation in model.citations
                )):
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
                    else:
                        eta_numbers = (
                            cited_general_ancestor_numbers(step, TodaEtaFamilyGeneralDefinition)
                            if (isinstance(statement, GeneratorSuspension)
                                and _eta_pair(statement) is not None)
                            else ()
                        )
                        if eta_numbers:
                            source_tags = ", ".join(
                                f"[R{number}]" for number in eta_numbers
                            )
                            sentence = f"{source_tags}より, " + sentence
                from homotopy_groups import TodaSuspensionIsomorphismStatement
                if (isinstance(statement, TodaSuspensionIsomorphismStatement)
                        and step.rule is ProofRule.INFERENCE
                        and any(
                            isinstance(parent.conclusion, GeneratorSuspension)
                            and parent.conclusion.map == statement.map
                            for parent in step.premises
                        )):
                    sentence = "これより, " + sentence
                if sentence.endswith("である."):
                    sentence = sentence[:-4] + "."
                elif sentence.endswith("が成り立つ."):
                    sentence = sentence[:-6] + "."
                lines.extend((sentence, ""))
        else:
            tags = ", ".join(f"[R{number}]" for number in body_line.citation_numbers)
            if body_line.role == "given":
                prefix = f"{tags}より, " if tags else "前提として, "
            elif body_line.role == "root":
                prefix = f"{tags}を用いて, " if tags else "以上より, "
            else:
                if tags:
                    prefix = f"{tags}を用いて, "
                else:
                    sources = validated_specialization_citation_numbers(step)
                    prefix = (
                        ", ".join(f"[R{number}]" for number in sources) + "より, "
                        if sources else ""
                    )
            statement_latex = body_line.statement_latex
            if isinstance(step.conclusion, TodaProp42ExactnessStatement):
                statement_latex = statement_latex.replace(r" \text{ is exact}", "")
                lines.append(f"{prefix}${statement_latex}$ は完全.")
            else:
                lines.append(f"{prefix}${statement_latex}$.")
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

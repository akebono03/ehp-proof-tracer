# Phase 171 R20R13 — 全変更コード

変更ファイル: `phase168_r3_5_model_renderer.py` の関数 `render_model_backed_narrative_markdown` 全体。
新規追加: `phase171_r20r13_eta_sentence_layout/projection.py`（パッケージルート）。
既存の import 変更はありません。

## 既存 Renderer の import 全文

```python
from __future__ import annotations

from phase165_r52_partial_proof import PartialProofResult, ProofSearchStatus
from phase168_r3_3_proof_narrative_model import ProofNarrativeModel
from phase168_r3_12_body_binding import build_narrative_body_lines

```

## 変更した関数全文

```python
def render_model_backed_narrative_markdown(
    result: PartialProofResult, model: ProofNarrativeModel,
) -> str:
    """Render typed Proof Tree steps; preserve incomplete search state from model."""
    from proof import ProofRule, Relation, RelationType
    from map_facts import EHP_DELTA_MAP, EHP_E_MAP, EHP_H_MAP
    from toda_rules import TodaProp42ExactnessStatement
    from phase165_r14_r14_diagonal_and_prop42 import GeneratorSuspension
    from phase165_r14_r6_generic_iso import GeneratorImage
    from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
    from phase165_r12_r11_prop42_unified import TodaProp42GeneralExactnessStatement
    from phase165_r12_r21_eta_generator_chain import _eta_pair
    from phase168_r3_29_order_projection import project_narrative_order
    from phase168_r3_3_proof_narrative_model import root_ancestor_step_indices
    from phase168_r3_26_exactness_projection import project_exactness_chains
    from phase168_r3_27_typed_statement_projection import (
        group_tex, element_tex, typed_sentence, toda45_specialization_evidence,
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


    def direct_given_premise_citation_numbers(step):
        """Use citations of an existing direct GIVEN premise, without replaying a rule.

        The Proof Tree is supplied by Backward Search. Citation ownership is
        already stored in the Narrative Model and is not re-inferred here.
        """
        if step.rule is not ProofRule.INFERENCE or len(step.premises) != 1:
            return ()
        given_step = step.premises[0]
        if given_step.rule is not ProofRule.GIVEN:
            return ()
        # Keep the old presentationally eligible typed statement families.
        # Proof validity itself was checked before this model was constructed.
        from homotopy_groups import TodaPrimaryGroupZeroStatement
        from phase165_r12_r15_toda51 import Toda51BelowDiagonalZeroStatement
        source, target = given_step.conclusion, step.conclusion
        is_direct_relation = isinstance(source, Relation) and isinstance(target, Relation)
        is_typed_zero = (
            isinstance(target, TodaPrimaryGroupZeroStatement)
            and isinstance(source, (TodaPrimaryGroupZeroStatement,
                                    Toda51BelowDiagonalZeroStatement))
        )
        if not (is_direct_relation or is_typed_zero):
            return ()
        return tuple(dict.fromkeys(
            number
            for source_index, candidate in enumerate(model.steps)
            if candidate is given_step or candidate == given_step
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
        root_scope = root_ancestor_step_indices(model.steps, model.root_index)
        chains = tuple(
            chain for chain in project_exactness_chains(model)
            if all(index in root_scope for index in chain.step_indices)
        )
        suppressed_exactness = {index for chain in chains for index in chain.step_indices}
        order = tuple(
            entry.step_index
            for entry in project_narrative_order(model, suppressed_exactness)
            if entry.step_index in root_scope
        )
        lines = ["使用する結果", ""]

    for citation in model.citations:
        locator = citation.reference.locator or citation.reference.label
        # Display the cited locator verbatim; no series-specific alias.
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
        if not chains:
            target_name = group_tex(model.target)
            if target_name is not None:
                lines.extend((f"${target_name}$の群構造を決定する.", ""))
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
            lines.append(f"${group_tex(model.target)}$の群構造を決定するために, {tags}を用いて次の完全列を考える.")
        else:
            lines.append(f"${group_tex(model.target)}$の群構造を決定するために, 次の完全列を考える.")
        lines.append("")
        lines.append(f"${sequence}$.")
        lines.append("")
    # A later certified step can subsume a purely intermediate display step.
    # Keep both ProofSteps in the tree; omit prose only when the consumed
    # premise has no distinct citation and no other consumers.
    suppressed_body_indices = set()
    if not incomplete:
        from expression import IteratedSuspension
        from homotopy_groups import FiniteCyclicGroup, TodaDeltaMap, TodaSuspensionMap
        from phase165_r12_r12_ehp_consequences import EHPImageEqualsKernelStatement
        from phase165_r12_r13_kernel_image import SuspensionKernelFreeCyclicStatement
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
                        and transported.relation_type is RelationType.EQUALITY
                        and conclusion.relation_type is RelationType.EQUALITY
                        and isinstance(witness_step.conclusion.map, TodaSuspensionMap)
                        and isinstance(transported.rhs.generator, IteratedSuspension)
                        and type(transported.rhs.generator.exponent) is int
                        and transported.rhs.generator.exponent == 1
                        and element_tex(transported.rhs.generator.expression) is not None
                        and element_tex(transported.rhs.generator.expression)
                            == element_tex(witness_step.conclusion.source_generator)
                        and element_tex(conclusion.rhs.generator) is not None
                        and element_tex(conclusion.rhs.generator)
                            == element_tex(witness_step.conclusion.target_generator)
                        and transported.lhs == conclusion.lhs
                        and transported.rhs.order == conclusion.rhs.order
                        and transported.lhs == witness_step.conclusion.map.target_group):
                    earlier_index = unique_step_index(transported_step)
                    if (earlier_index is not None
                            and earlier_index in order
                            and earlier_index != model.root_index
                            and not model.step_citation_numbers[earlier_index]
                            and only_consumed_by(transported_step, consumer)):
                        suppressed_body_indices.add(earlier_index)
    from homotopy_groups import TodaPrimaryGroupZeroStatement
    from expression import ScalarSymbol
    from homotopy_groups import TodaPrimaryGroup
    from web_group_proof_common import _group_proof_statement_latex
    displayed_cyclic_math = set()
    from phase171_r20r12_verified_cyclic_narrative.projection import (
        verified_order_four_summary,
        suppress_exact_duplicate_body_lines,
    )
    order_summary = verified_order_four_summary(model) if not incomplete else None
    # A certified composite GeneratorImage incorporates its two verified
    # generator-suspension premises. Suppress their separate prose only when
    # they are uncited, used by that image alone, and its eta-square image
    # can actually be displayed. No ProofSteps or citations are discarded.
    if not incomplete:
        for image_index in order:
            image_step = model.steps[image_index]
            image = image_step.conclusion
            if (image_step.rule is not ProofRule.INFERENCE
                    or not isinstance(image, GeneratorImage)
                    or not isinstance(image.map, TodaSuspensionMap)
                    or len(image_step.premises) != 2
                    or element_tex(image.source_generator) is None
                    or element_tex(image.target_generator) is None
                    or not cited_general_ancestor_numbers(
                        image_step, TodaEtaFamilyGeneralDefinition
                    )
                    or not all(isinstance(parent.conclusion, GeneratorSuspension)
                               for parent in image_step.premises)):
                continue
            for parent in image_step.premises:
                parent_index = unique_step_index(parent)
                if (parent_index is not None and parent_index in order
                        and parent_index != model.root_index
                        and parent.rule is ProofRule.INFERENCE
                        and not model.step_citation_numbers[parent_index]
                        and only_consumed_by(parent, image_step)):
                    suppressed_body_indices.add(parent_index)
    # R10A: presentation-only projection of the already-verified E^r image chain.
    # The Proof Tree, its citations, and all original ProofSteps remain intact.
    from phase169_r10a_verified_stable_chain_projection.projection import (
        VerifiedStableImageChainDisplay,
        project_verified_stable_image_chain,
    )
    from phase169_r10a2_unified_one_stem.one_stem_projection import (
        project_verified_one_stem_notation_chain,
    )
    stable_chain_display = (
        (project_verified_stable_image_chain(model, order)
         or project_verified_one_stem_notation_chain(model, order))
        if not incomplete else None
    )
    if stable_chain_display is not None:
        suppressed_body_indices.update(stable_chain_display.hidden_indices)
    # R10EC: a complete, verified direct-sum proof may present the actual
    # E^r endpoints, while retaining all certified ProofSteps and citations.
    from phase169_r10ec_direct_sum_narrative_projection.projection import (
        project_verified_direct_sum_transport,
    )
    direct_sum_display = (
        project_verified_direct_sum_transport(model, order)
        if not incomplete else None
    )
    if direct_sum_display is not None:
        suppressed_body_indices.update(direct_sum_display.hidden_indices)
    for index in order:
        if order_summary is not None and index == model.root_index:
            lines.extend((order_summary, ""))
        if direct_sum_display is not None and index == direct_sum_display.root_index:
            lines.extend((direct_sum_display.statement, ""))
        if stable_chain_display is not None and index == stable_chain_display.root_index:
            source_tags = ", ".join(
                f"[R{number}]" for number in stable_chain_display.citation_numbers
            )
            compressed_statement = (
                rf"$E^{{{stable_chain_display.exponent}}}"
                rf"({stable_chain_display.source_tex})="
                rf"{stable_chain_display.target_tex}$"
            )
            if source_tags:
                prefix = f"{source_tags}より, "
            elif isinstance(stable_chain_display, VerifiedStableImageChainDisplay):
                prefix = "Definition より, "
            else:
                prefix = ""
            lines.extend((f"{prefix}{compressed_statement}.", ""))
        if index in suppressed_body_indices:
            continue
        step = model.steps[index]
        statement = step.conclusion
        if not incomplete:
            from phase169_r3k_narrative_projection import duplicate_group_relation_notice
            notice = duplicate_group_relation_notice(model, index, displayed_cyclic_math)
            if notice is not None:
                # The duplicate has already been displayed; its provenance
                # remains in Reference and the verified Proof Tree.
                if notice and order_summary is None:
                    lines.extend((notice, ""))
                continue
            from homotopy_groups import FiniteCyclicGroup
            if (isinstance(statement, Relation)
                    and statement.relation_type is RelationType.EQUALITY
                    and isinstance(statement.lhs, TodaPrimaryGroup)
                    and isinstance(statement.rhs, FiniteCyclicGroup)):
                latex, problem = _group_proof_statement_latex(statement)
                if latex is not None and problem is None:
                    displayed_cyclic_math.add(latex)
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
        # R3Z: general higher-eta clauses belong to Reference, not the proof body.
        # Hide one only when a directly dependent certified specialization is
        # retained in this display. The citation and both ProofSteps survive.
        if (step.rule is ProofRule.GIVEN
                and isinstance(statement, Relation)
                and model.step_citation_numbers[index]):
            from phase165_r57_r8_eta_specialization import _is_generic_eta_group_relation
            from phase165_r57_r20_general_specialization import specialize_typed_statement
            if (_is_generic_eta_group_relation(statement)
                    and any(
                        derived_index not in suppressed_body_indices
                        and derived_index != index
                        and derived.rule is ProofRule.INFERENCE
                        and isinstance(derived.conclusion, Relation)
                        and any(parent is step or parent == step
                                for parent in derived.premises)
                        and specialize_typed_statement(
                            statement, derived.conclusion
                        ) is not None
                        for derived_index in order
                        for derived in (model.steps[derived_index],)
                    )):
                continue
        # Only verbalize the certified stable-eta normalization already
        # represented by this step's source relation and cited definition.
        transition = (
        None
        if stable_chain_display is not None and index == stable_chain_display.root_index
        else project_stable_eta_notation_transition(model, index)
    )
        if transition is not None:
            lines.extend((transition, ""))
        body_line = body_by_step.get(index)
        sentence = typed_sentence(step.conclusion, step)
        if sentence is not None:
            # The certified kernel step already consumes the suppressed
            # exactness equality and a concrete Delta image. Compose only
            # the displayed equality, without re-running a proof rule.
            if (isinstance(statement, SuspensionKernelFreeCyclicStatement)
                    and any(
                        isinstance(parent.conclusion, EHPImageEqualsKernelStatement)
                        and unique_step_index(parent) in suppressed_body_indices
                        for parent in step.premises
                    )):
                generator = element_tex(statement.kernel_group.generator)
                if generator is not None:
                    sentence = (
                        rf"完全性より, $\ker E=\operatorname{{Im}}\Delta="
                        rf"\mathbb{{Z}}\{{{generator}\}}$."
                    )
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
                        if ((isinstance(statement, GeneratorSuspension)
                             and _eta_pair(statement) is not None)
                            or (isinstance(statement, GeneratorImage)
                                and isinstance(statement.map, TodaSuspensionMap)
                                and element_tex(statement.source_generator) is not None
                                and element_tex(statement.target_generator) is not None))
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
            # Cite the actual Proposition 4.4 GIVEN ancestor of a
            # proved injective map; no rule-name or locator guessing.
            from phase165_r14_r6_generic_iso import MapInjective
            from phase165_r52_r27_r5_literature import TodaProp44UniversalStatement
            if step.rule is ProofRule.INFERENCE and isinstance(statement, MapInjective):
                prop44_numbers = cited_general_ancestor_numbers(
                    step, TodaProp44UniversalStatement
                )
                if prop44_numbers:
                    prop44_tags = ", ".join(f"[R{number}]" for number in prop44_numbers)
                    if prop44_tags not in sentence:
                        sentence = f"{prop44_tags}より, " + sentence
                    # R4F: the source paragraph immediately BEFORE Prop. 4.4
                    # establishes the n=4 Hopf fibration.  Cite only the
                    # actually proved MapInjective step and its cited GIVEN.
                    # Do not invoke the later Lemma 5.4 naming nu_4.
                    from homotopy_groups import TodaSuspensionMap
                    mapping = statement.map
                    i = getattr(getattr(mapping, "target_group", None),
                                "group_dimension", None)
                    if (isinstance(mapping, TodaSuspensionMap)
                            and type(i) is int and i >= 4
                            and mapping.source_group == TodaPrimaryGroup(i - 1, 3)
                            and mapping.target_group == TodaPrimaryGroup(i, 4)
                            and len(step.premises) == 1
                            and step.premises[0].rule is ProofRule.GIVEN
                            and type(step.premises[0].conclusion)
                                is TodaProp44UniversalStatement
                            and step.premises[0].conclusion
                                == TodaProp44UniversalStatement()):
                        # Keep the R4E result sentence and its [R] tag intact.
                        # Add the source-order-safe applicability as separate prose.
                        application = (
                            r"$n=4$ の Hopf fibration $h:S^7\to S^4$ により, "
                            r"$\alpha=h\in\pi_7^4$, "
                            r"$H(\alpha)=\pm\iota_7$ と取れる. "
                            + f"{prop44_tags}を "
                            + rf"$(n,i)=(4,{i})$ に適用できる."
                        )
                        lines.extend((application, ""))
            if sentence.endswith("である."):
                sentence = sentence[:-4] + "."
            elif sentence.endswith("が成り立つ."):
                sentence = sentence[:-6] + "."
            lines.extend((sentence, ""))
        elif body_line is not None:
            tags = ", ".join(f"[R{number}]" for number in body_line.citation_numbers)
            if body_line.role == "given":
                prefix = f"{tags}より, " if tags else "前提として, "
            elif body_line.role == "root":
                prefix = f"{tags}を用いて, " if tags else "以上より, "
            else:
                if tags:
                    prefix = f"{tags}を用いて, "
                else:
                    sources = direct_given_premise_citation_numbers(step)
                    prefix = (
                        ", ".join(f"[R{number}]" for number in sources) + "より, "
                        if sources else ""
                    )
            statement_latex = body_line.statement_latex
            if isinstance(step.conclusion, TodaProp42ExactnessStatement):
                # An individual certified EHP window is sourced by the
                # actual universal Proposition 4.2 GIVEN proof ancestor.
                if not tags:
                    source_numbers = cited_general_ancestor_numbers(
                        step, TodaProp42GeneralExactnessStatement
                    )
                    if source_numbers:
                        prefix = ", ".join(
                            f"[R{number}]" for number in source_numbers
                        ) + "より, "
                statement_latex = statement_latex.replace(r" \text{ is exact}", "")
                lines.append(f"{prefix}${statement_latex}$ は完全.")
            else:
                from phase169_r3k_narrative_projection import project_proven_map_property
                projected = project_proven_map_property(step, statement_latex)
                lines.append(f"{prefix}{projected}" if projected is not None
                             else f"{prefix}${statement_latex}$.")
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
    if order_summary is not None:
        lines = suppress_exact_duplicate_body_lines(lines)
    if not incomplete:
        from phase171_r20r13_eta_sentence_layout.projection import (
            format_complete_proof_sentences,
        )
        lines = format_complete_proof_sentences(lines, model)
    return "\n".join(lines).rstrip() + "\n"

```

## 新規 projection.py 全文（import を含む）

```python
"""Source-bound presentation of adjacent eta equations and sentence boundaries.

This module never infers new mathematics. It combines only existing rendered
sentences whose exact content is backed by INFERENCE ProofSteps in the final
root ancestry and a cited general eta definition. Partial proofs are unchanged.
"""
from __future__ import annotations

from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
from phase165_r14_r14_diagonal_and_prop42 import GeneratorSuspension
from phase165_r14_r6_generic_iso import GeneratorImage
from phase168_r3_27_typed_statement_projection import element_tex, typed_sentence
from phase168_r3_3_proof_narrative_model import root_ancestor_step_indices
from homotopy_groups import TodaSuspensionMap
from proof import ProofRule


def verified_eta_display_sentences(model) -> dict[str, tuple[str, str]]:
    """Map existing source-tagged sentences to (same tag, existing math body).

    A line is eligible only if it is an exact rendering of a certified typed
    suspension step with an actually cited eta-definition GIVEN ancestor.
    """
    if model.root_index is None:
        return {}
    scope = root_ancestor_step_indices(model.steps, model.root_index)
    allowed: dict[str, tuple[str, str]] = {}
    for index in scope:
        step = model.steps[index]
        statement = step.conclusion
        if step.rule is not ProofRule.INFERENCE:
            continue
        if not isinstance(statement, (GeneratorSuspension, GeneratorImage)):
            continue
        if not isinstance(statement.map, TodaSuspensionMap):
            continue
        source = element_tex(statement.source_generator)
        target = element_tex(statement.target_generator)
        if source is None or target is None:
            continue
        if not (source.startswith(r"\eta_{") and target.startswith(r"\eta_{")):
            continue
        sentence = typed_sentence(statement, step)
        if sentence is None or not sentence.startswith("$E(") or not sentence.endswith("$."):
            continue
        cited: list[int] = []
        visited: set[int] = set()
        pending = [step]
        while pending:
            ancestor = pending.pop()
            if id(ancestor) in visited:
                continue
            visited.add(id(ancestor))
            if (ancestor.rule is ProofRule.GIVEN
                    and isinstance(ancestor.conclusion, TodaEtaFamilyGeneralDefinition)):
                for source_index, source_step in enumerate(model.steps):
                    if source_step is ancestor or source_step == ancestor:
                        for number in model.step_citation_numbers[source_index]:
                            if number not in cited:
                                cited.append(number)
                        break
            pending.extend(ancestor.premises)
        if not cited:
            continue
        tag = ", ".join(f"[R{number}]" for number in cited) + "より, "
        full_line = tag + sentence
        math_body = sentence[1:-2]  # take only existing TeX, excluding $ and period
        allowed[full_line] = (tag, math_body)
    return allowed


def combine_adjacent_verified_eta_sentences(lines: list[str], model) -> list[str]:
    """Combine neighboring printed certified equations sharing one citation.

    Empty Markdown separators between these equations may be crossed. Other
    mathematics, differently sourced results and nonadjacent lines are kept.
    """
    allowed = verified_eta_display_sentences(model)
    result: list[str] = []
    index = 0
    while index < len(lines):
        first = allowed.get(lines[index])
        if first is None:
            result.append(lines[index])
            index += 1
            continue
        tag, first_math = first
        terms = [first_math]
        cursor = index + 1
        while cursor < len(lines):
            # Standard narrative inserts precisely one empty line per sentence.
            has_separator = lines[cursor] == ""
            next_index = cursor + 1 if has_separator else cursor
            if next_index >= len(lines):
                break
            candidate = allowed.get(lines[next_index])
            if candidate is None or candidate[0] != tag:
                break
            terms.append(candidate[1])
            cursor = next_index + 1
        if len(terms) < 2:
            result.append(lines[index])
            index += 1
            continue
        result.append(tag + "$" + r",\quad ".join(terms) + "$.")
        index = cursor
    return result


def _split_outside_math_at_period(line: str) -> list[str]:
    """Split ASCII '. ' prose boundaries, not decimals or math expressions."""
    pieces: list[str] = []
    begin = 0
    math_mode = False
    index = 0
    while index < len(line):
        char = line[index]
        if char == "$" and (index == 0 or line[index - 1] != "\\"):
            math_mode = not math_mode
        if (not math_mode and char == "."
                and index + 1 < len(line) and line[index + 1] == " "
                and index > 0):
            # Dot is part of the sentence. Subsequent prose starts a new line.
            pieces.append(line[begin:index + 1].strip())
            begin = index + 2
        index += 1
    pieces.append(line[begin:].strip())
    return [piece for piece in pieces if piece]


def split_completed_proof_sentences(lines: list[str]) -> list[str]:
    """Use real Markdown paragraph breaks at periods only in the proof body.

    Do not touch citation locators (e.g. Proposition 5.6.), reference bodies,
    math notation, or an incomplete proof's diagnostic section.
    """
    result: list[str] = []
    in_body = False
    for line in lines:
        if line == "証明":
            in_body = True
            result.append(line)
            continue
        if not in_body or not line or line == "□":
            result.append(line)
            continue
        sentences = _split_outside_math_at_period(line)
        if len(sentences) < 2:
            result.append(line)
            continue
        for i, sentence in enumerate(sentences):
            if i:
                result.append("")
            result.append(sentence)
    return result


def format_complete_proof_sentences(lines: list[str], model) -> list[str]:
    """Keep the original tree/citations; alter only completed narrative prose."""
    return split_completed_proof_sentences(
        combine_adjacent_verified_eta_sentences(lines, model)
    )

```

## テスト全文

### test_install.py

```python
"""Installer guards and whole-function preservation (no live repository needed)."""
from __future__ import annotations

import ast

import pytest

from phase171_r20r13_eta_sentence_layout.install import OLD, NEW, transform


def test_replaces_exactly_one_complete_renderer_return():
    fixture = 'def renderer():\n' + OLD
    output = transform(fixture)
    assert NEW in output
    assert output.count("format_complete_proof_sentences") == 2
    assert len([x for x in ast.parse(output).body if isinstance(x, ast.FunctionDef)]) == 1


def test_refuses_unreviewed_source_and_duplicate_anchor():
    with pytest.raises(RuntimeError):
        transform("def unrelated():\n    return 1\n")
    with pytest.raises(RuntimeError):
        transform("def renderer():\n" + OLD + OLD)


def test_output_only_changes_renderer_tail():
    fixture = 'def renderer():\n    x = 1\n' + OLD
    changed = transform(fixture)
    assert changed.startswith('def renderer():\n    x = 1\n')
    assert changed.endswith(NEW)


def test_valid_python_source_and_no_proof_engine_patch():
    fixture = 'def renderer():\n' + OLD
    ast.parse(transform(fixture))
    assert "ProofStep(" not in NEW
    assert "GIVEN" not in NEW

```

### test_projection.py

```python
"""Sentence layout unit checks and canonical public-search integration."""
from __future__ import annotations

from types import SimpleNamespace

import pytest

from phase171_r20r13_eta_sentence_layout.projection import (
    _split_outside_math_at_period,
    combine_adjacent_verified_eta_sentences,
    format_complete_proof_sentences,
    split_completed_proof_sentences,
    verified_eta_display_sentences,
)


def test_periods_are_newlines_only_in_proof_body():
    lines = [
        "使用する結果", "", "[R1] Proposition 5.6.", "",
        "証明", "", "最初の理由. 次の理由. $E(\\eta_{2})=\\eta_{3}$.",
        "", "□",
    ]
    actual = split_completed_proof_sentences(lines)
    assert "[R1] Proposition 5.6." in actual
    assert "最初の理由." in actual
    assert "次の理由." in actual
    assert r"$E(\eta_{2})=\eta_{3}$." in actual
    assert "最初の理由. 次の理由." not in actual


def test_periods_inside_math_and_decimals_remain_intact():
    assert _split_outside_math_at_period(r"$x=1. 2$ を用いる. 次を示す.") == [
        r"$x=1. 2$ を用いる.", "次を示す."
    ]
    assert _split_outside_math_at_period("値は3.14である. 次を示す.") == [
        "値は3.14である.", "次を示す."
    ]
    assert _split_outside_math_at_period("位数は2. また群は有限.") == [
        "位数は2.", "また群は有限."
    ]


def test_uncertified_eta_lines_are_not_merged():
    model = SimpleNamespace(steps=(), root_index=None)
    lines = ["証明", "", r"[R3]より, $E(\eta_{2})=\eta_{3}$.", "",
             r"[R3]より, $E(\eta_{3}^{2})=\eta_{4}^{2}$."]
    assert combine_adjacent_verified_eta_sentences(lines, model) == lines
    assert format_complete_proof_sentences(lines, model) == lines


@pytest.fixture(scope="module")
def canonical_pi63():
    from phase165_r52_partial_proof import ProofSearchStatus
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
    from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
    from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative
    original = build_shared_typed_bridge()
    contexts = []
    result = search_group_from_registered_goal(
        n=3, k=3, bridge=original, context_sink=contexts.append,
    )
    assert result.status is ProofSearchStatus.COMPLETE
    assert not result.open_goals
    assert len(contexts) == 1
    citing = resolve_specialized_goal_citing_id(original, result.conclusion)
    assert citing is not None
    verify_proof_tree_for_narrative(result, contexts[0], citing_assertion_id=citing)
    return result, build_linked_proof_narrative_model(result, contexts[0])


def test_real_derived_eta_prose_has_verified_citation(canonical_pi63):
    _, model = canonical_pi63
    eligible = verified_eta_display_sentences(model)
    assert len(eligible) >= 3
    assert sum(line.startswith("[R3]より, $E(") for line in eligible) >= 3


def test_real_public_proof_joins_eta_and_retains_order_four(canonical_pi63):
    from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
    result, model = canonical_pi63
    markdown = render_model_backed_narrative_markdown(result, model)
    refs, body = markdown.split("\n証明\n", 1)
    eligible = verified_eta_display_sentences(model)
    assert len(model.citations) == 8
    assert "[R3] Chapter V, i)." in refs
    assert r"\operatorname{ord}" in body
    assert r"\neq0" in body
    assert r"\quad E(" in body
    assert any(source not in body for source in eligible if source.startswith("[R3]より,"))
    assert "による導出も同じ群構造を示す" not in body

```


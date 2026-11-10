# R55R3R2R1 変更後関数全文

## New common reference helper — insertion before project_reference_bodies

```python
def _project_certified_general_reference_body(assertion: object, registry: object,
                                         statement: object) -> str | None:
    """Show already-cited general laws when source identity and typed data agree."""
    from unified_statement_registry import (
        AssertionEntry, AssertionKind, AssertionOrigin, ReferenceKind,
        UnifiedStatementRegistry,
    )
    from phase174_r3_r7_r12_toda59_annihilator_source.source import (
        CitedFamilyAnnihilator, SOURCE_ANNIHILATOR_LOCATOR,
    )
    from phase174_r3_r7_r28_prop27_typed_literature_registration.registration import (
        Prop27UniversalLiteratureStatement,
    )

    if not isinstance(registry, UnifiedStatementRegistry) or not isinstance(assertion, AssertionEntry):
        return None
    try:
        if registry.assertion(assertion.assertion_id) is not assertion:
            return None
        reference = registry.reference(assertion.reference_id)
    except KeyError:
        return None
    if (assertion.kind is not AssertionKind.STATEMENT
            or assertion.origin is not AssertionOrigin.FIXED_STATEMENT
            or assertion.dependencies
            or assertion.content is not statement
            or not isinstance(reference.publication_position, int)
            or reference.publication_position <= 0):
        return None

    if type(statement) is CitedFamilyAnnihilator:
        if (statement != CitedFamilyAnnihilator(
                left_family_id=4, right_family_id=2,
                minimum_left_index=6, right_index_offset=3,
                citation_locator=SOURCE_ANNIHILATOR_LOCATOR,
            )
                or not assertion.assertion_id.endswith(
                    ':isolated:toda:(5.9):nu_eta_general:statement')
                or not assertion.reference_id.endswith(
                    ':isolated:toda:(5.9):nu_eta_general')
                or assertion.scope != 'nu_n composed eta_(n+3) = 0, n>=6'
                or reference.kind is not ReferenceKind.EQUATION
                or reference.locator != '(5.9)'
                or reference.source_id != (
                    'sources/toda/Toda_05_2.tex '
                    '(adopted; printed edition unchecked)'
                )):
            return None
        return r'$n\ge6$ に対して, $\nu_n\circ\eta_{n+3}=0$.'

    if type(statement) is Prop27UniversalLiteratureStatement:
        if (statement != Prop27UniversalLiteratureStatement()
                or not assertion.assertion_id.endswith(
                    ':typed_literature:assertion:toda:prop2.7')
                or not assertion.reference_id.endswith(
                    ':typed_literature:toda:prop2.7')
                or assertion.scope != ('n >= 2', 'n even', 'sign undetermined')
                or reference.kind is not ReferenceKind.PROPOSITION
                or reference.locator != 'Proposition 2.7'
                or reference.source_id != 'toda:tex:ch2:0018'):
            return None
        return (r'$n\ge2$ を偶数とすると, '
                r'$H(\Delta(\iota_{2n+1}))=\pm2\iota_{2n-1}$.')
    return None

```

## phase168_r3_37c_reference_projection.py — project_reference_bodies

```python
def project_reference_bodies(registry, assertion_ids):
    """Project only cited, typed source statements, including registered composite fields.

    Composite expansion follows the assertion's registered field scope. It does
    not read text from a literature catalog or create a new proof premise.
    """
    if registry is None:
        return ()
    from dataclasses import fields, is_dataclass
    from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
    from phase169_r10d2_general_family_definition.family_citation import (
        CitedStableFamilyDefinition, cited_family_reference_sentence,
    )
    from phase165_r12_r11_prop42_unified import TodaProp42GeneralExactnessStatement
    from phase165_r12_r15_toda51 import Toda51BelowDiagonalZeroStatement
    from phase165_r52_r27_r5_literature import Toda52UniversalStatement, TodaProp44UniversalStatement
    from phase174_r3_r6_r2_prop44_lemma54.source import (
        TodaPreProp44SplittingStatement,
    )
    from phase165_r57_r8_eta_specialization import _is_generic_eta_group_relation
    from toda_rules import Toda45IsomorphismStatement
    from expression import ScalarSymbol, ScalarSum, ScalarProduct
    from homotopy_groups import TodaIteratedSuspensionMap, TodaPrimaryGroupZeroStatement
    from proof import Relation
    from phase174_r3_r6_r4_common_reference.projection import (
        project_cited_universal_toda_reference_body,
    )

    result = []
    for assertion_id in assertion_ids:
        assertion = registry.assertion(assertion_id)
        content = assertion.content
        scope = getattr(assertion, "scope", ())
        statements = (content,)
        if (isinstance(scope, tuple) and len(scope) >= 2
                and scope[0] == "typed_composite_fields"):
            field_names = scope[1]
            if not isinstance(field_names, tuple) or len(field_names) < 2:
                raise ValueError("registered composite field scope is inconsistent")
            content_fields = (
                tuple(field.name for field in fields(content))
                if is_dataclass(content) and not isinstance(content, type) else ()
            )
            if content_fields == field_names:
                statements = tuple(getattr(content, field_name) for field_name in field_names)
            else:
                # The registered component bridge retains the parent's scope
                # on an atomic child. Validate the exact parent dependency and
                # field content instead of expanding this child a second time.
                dependencies = getattr(assertion, "dependencies", ())
                if not isinstance(dependencies, tuple) or len(dependencies) != 1:
                    raise ValueError("registered composite field scope is inconsistent")
                parent = registry.assertion(dependencies[0])
                parent_content = parent.content
                parent_fields = (
                    tuple(field.name for field in fields(parent_content))
                    if is_dataclass(parent_content) and not isinstance(parent_content, type)
                    else ()
                )
                if (parent.scope != scope
                        or parent_fields != field_names
                        or not any(
                            type(content) is type(getattr(parent_content, field_name))
                            and content == getattr(parent_content, field_name)
                            for field_name in field_names
                        )):
                    raise ValueError("registered composite field scope is inconsistent")

        for statement in statements:
            sentence = _verified_source_sentence(statement)
            if isinstance(statement, TodaEtaFamilyGeneralDefinition):
                if statement.lower_bound == 2:
                    sentence = r"$n\ge 2$ に対し, $\eta_n=E^{n-2}\eta_2$ と定義する."
            elif isinstance(statement, CitedStableFamilyDefinition):
                sentence = cited_family_reference_sentence(statement)
            elif (isinstance(statement, TodaPrimaryGroupZeroStatement)
                  and isinstance(statement.group.group_dimension, ScalarSymbol)
                  and statement.group.sphere_dimension == 1):
                sentence = r"$\pi_i^1=0\quad(i>1)$."
            elif isinstance(statement, Toda51BelowDiagonalZeroStatement):
                sentence = r"$\pi_i^n=0\quad(i<n)$."
            elif (type(statement) is TodaProp44UniversalStatement
                  and statement == TodaProp44UniversalStatement()):
                sentence = (
                    r"$\alpha\in\pi_{2n-1}^{n}$ で "
                    r"$H(\alpha)=\pm\iota_{2n-1}$ とする."
                    "\n"
                    r"このとき, 任意の $i$ に対して次の写像は同型である."
                    "\n"
                    r"$\pi_{i-1}^{n-1}\oplus\pi_i^{2n-1}"
                    r"\xrightarrow{\;\cong\;}\pi_i^n,\quad"
                    r"(\beta,\gamma)\longmapsto E\beta+\alpha\circ\gamma$."
                    "\n"
                    r"特に $E:\pi_{i-1}^{n-1}\to\pi_i^{n}$ は単射である."
                )
            elif (type(statement) is TodaPreProp44SplittingStatement
                  and statement == TodaPreProp44SplittingStatement()):
                sentence = (
                    r"$n=2,4,8$ では Hopf fibration $h:S^{2n-1}\to S^n$ "
                    r"が存在し, 任意の $i$ で "
                    r"$E+h_*:\pi_{i-1}^{n-1}\oplus\pi_i^{2n-1}"
                    r"\xrightarrow{\cong}\pi_i^n$ が成り立つ "
                    r"(Steenrod 1951 を引用)."
                )
            elif isinstance(statement, TodaProp42GeneralExactnessStatement):
                sentence = (
                    r"$\pi_i^n\xrightarrow{E}\pi_{i+1}^{n+1}"
                    r"\xrightarrow{H}\pi_{i+1}^{2n+1}"
                    r"\xrightarrow{\Delta}\pi_{i-1}^{n}"
                    r"\xrightarrow{E}\pi_i^{n+1}$ は完全."
                )
            elif isinstance(statement, Toda52UniversalStatement):
                if (statement.variable == "i" and statement.minimum_i == 3
                        and statement.map_formula == "alpha -> eta_2 o alpha"
                        and statement.source_group == "pi_i^3"
                        and statement.target_group == "pi_i^2"):
                    sentence = (
                        r"$i\ge 3$ に対し, "
                        r"$\eta_2\circ(-):\pi_i^3\xrightarrow{\cong}\pi_i^2$ は同型."
                    )
            elif isinstance(statement, Toda45IsomorphismStatement):
                mapping = statement.map
                n, m, k = ScalarSymbol("n"), ScalarSymbol("m"), ScalarSymbol("k")
                if (
                    isinstance(mapping, TodaIteratedSuspensionMap)
                    and mapping.exponent == ScalarSum(left=m, right=ScalarProduct(left=-1, right=n))
                    and mapping.source_group.sphere_dimension == n
                    and mapping.target_group.sphere_dimension == m
                    and mapping.source_group.group_dimension == ScalarSum(left=n, right=k)
                    and mapping.target_group.group_dimension == ScalarSum(left=m, right=k)
                ):
                    sentence = (
                        r"$n\ge k+2$, $m\ge n$, $k\ge0$ に対し, "
                        r"$E^{m-n}:\pi_{n+k}^{n}\xrightarrow{\cong}\pi_{m+k}^{m}$ "
                        r"が成り立つ."
                    )
            elif isinstance(statement, Relation) and _is_generic_eta_group_relation(statement):
                # The typed source schema, already guarded by the general
                # eta-group recognizer, has the documented n >= 4 range.
                variable = statement.lhs.sphere_dimension.name
                sentence = (
                    r"$\pi_{" + variable + r"+1}^{" + variable + r"}="
                    r"\mathbb{Z}/2\{\eta_{" + variable + r"}\}"
                    r"\quad(" + variable + r"\ge4)$."
                )
            if sentence is None:
                sentence = _project_certified_general_reference_body(
                    assertion, registry, statement,
                )
            if sentence is None:
                sentence = project_cited_universal_toda_reference_body(
                    assertion, registry, statement,
                )
            if sentence is None:
                sentence = typed_sentence(statement, None)
            if sentence is None:
                latex, fallback = _group_proof_statement_latex(statement)
                if latex is not None and fallback is None:
                    sentence = "$" + latex + "$."
            if (sentence is not None and r"\pi_{n}^{n}" in sentence
                    and r"\mathbb{Z}" in sentence and r"n\ge" not in sentence
                    and sentence.endswith("$.")):
                sentence = sentence[:-2] + r"\quad(n\ge 1)$."
            if sentence is not None and sentence not in result:
                result.append(sentence)
    return tuple(result)

```

## phase168_r3_5_model_renderer.py — render_model_backed_narrative_markdown

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

    if model.abstract_structure is not result.abstract_structure:
        raise ValueError("Narrative Model abstract certificate must match searched result")
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

    from phase172_r5_prior_reference_display.projection import (
        display_prior_reference_locator,
    )
    for citation in model.citations:
        locator = citation.reference.locator or citation.reference.label
        if not incomplete:
            displayed = display_prior_reference_locator(citation, model)
            if displayed is not None:
                locator = displayed
            from phase174_r3_r6_r3_common_narrative.projection import (
                display_cited_nu_family_locator,
            )
            family_locator = display_cited_nu_family_locator(citation, model)
            if family_locator is not None:
                locator = family_locator
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
    for chain_index, chain in enumerate(chains):
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
        prefix = (
            f"${group_tex(model.target)}$の群構造を決定するために, "
            if chain_index == 0 else "さらに, "
        )
        if exactness_numbers:
            tags = ", ".join(f"[R{number}]" for number in exactness_numbers)
            lines.append(f"{prefix}{tags}を用いて次の完全列を考える.")
        else:
            lines.append(f"{prefix}次の完全列を考える.")
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
    if not incomplete:
        from phase172_r2_suspension_relation_display.projection import (
            redundant_suspension_relation_indices,
        )
        suppressed_body_indices.update(
            redundant_suspension_relation_indices(
                model, order, suppressed_body_indices,
            )
        )
    hopf_display = None
    if not incomplete:
        from phase172_r3_hopf_chain_display.projection import (
            project_verified_hopf_chain,
        )
        hopf_display = project_verified_hopf_chain(
            model, order, suppressed_body_indices,
        )
        if hopf_display is not None:
            suppressed_body_indices.update(hopf_display.hidden_indices)
    if not incomplete:
        from phase172_r4_hopf_surjectivity_display.projection import (
            redundant_hopf_surjectivity_indices,
        )
        suppressed_body_indices.update(
            redundant_hopf_surjectivity_indices(
                model, order, suppressed_body_indices,
            )
        )
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
        if hopf_display is not None and index in (
            hopf_display.formula_index, hopf_display.image_index,
        ):
            latex, fallback = _group_proof_statement_latex(
                model.steps[index].conclusion,
            )
            if latex is None or fallback is not None:
                raise ValueError("verified Hopf line cannot be rendered")
            numbers = (
                hopf_display.formula_citations
                if index == hopf_display.formula_index
                else hopf_display.image_citations
            )
            source_tags = ", ".join(f"[R{number}]" for number in numbers)
            lines.extend((f"{source_tags}より, ${latex}$.", ""))
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
                    # Keep every verified ProofStep and its provenance in the
                    # unified Model, but never expose internal Python type names
                    # as a mathematical proof sentence. Unsupported statements
                    # remain part of the proof tree and of cited References.
                    latex, fallback = _group_proof_statement_latex(statement)
                    if latex is None or fallback is not None:
                        continue
                    statement_text = f"${latex}$"
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
        if index != model.root_index:
            from phase174_r3_r6_r3_common_narrative.projection import (
                project_verified_cyclic_extension_reason,
            )
            extension_reason = project_verified_cyclic_extension_reason(
                step.conclusion, step,
            )
            if extension_reason is not None:
                sentence = extension_reason
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
            for goal, count in project_typed_open_goal_displays(model.open_goals):
                if isinstance(goal, str):
                    shown = goal
                else:
                    latex, fallback = _group_proof_statement_latex(goal)
                    shown = (f"${latex}$" if latex is not None and fallback is None
                             else type(goal).__name__ + "（数式表示未対応）")
                # This is display grouping only. Every original typed pending
                # goal still exists in model.open_goals and in the search state.
                if count > 1:
                    shown += f"（同じ群構造の未解決 Goal {count} 件を表示上集約）"
                lines.append("- " + shown)
        if model.diagnostics:
            lines.extend(("", "## 探索診断", ""))
            for diagnostic in model.diagnostics:
                lines.append("- " + diagnostic)
        if model.abstract_structure is not None:
            from phase173_r4_r15r9_shared_abstract_renderer.projection import (
                render_certified_abstract_model_section,
            )
            lines.extend(("", render_certified_abstract_model_section(model)))
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

## phase168_r3_27_typed_statement_projection.py — typed_sentence

```python
def typed_sentence(statement, step):
    from phase174_r3_r6_r3_common_narrative.projection import (
        project_verified_index_two_statement,
    )
    index_two = project_verified_index_two_statement(statement, step)
    if index_two is not None:
        return index_two
    map_sentence = map_property_sentence(statement, step)
    if map_sentence is not None:
        return map_sentence
    # Only project the mathematical content already present in a typed claim.
    # These are shared statement formatters, not a proof-tree-specific narrative.
    from expression import Zero
    from proof import Relation, RelationType
    from phase165_r12_r2_quotient_rules import KernelMultipleStatement
    from phase174_r3_r7_r25_prop27_isolated_inference.rule import (
        Prop27TypedHopfDeltaStatement, typed_specialization,
    )
    if type(statement) is Prop27TypedHopfDeltaStatement:
        if (type(statement.n) is int and statement.n >= 2
                and statement.n % 2 == 0
                and statement == typed_specialization(statement.n)):
            sign = r"\pm" if statement.sign_undetermined else ""
            return (
                rf"$H(\Delta(\iota_{{{statement.source_iota_dimension}}}))="
                rf"{sign}{statement.absolute_coefficient}"
                rf"\iota_{{{statement.target_iota_dimension}}}$."
            )
        return None
    if type(statement) is KernelMultipleStatement:
        mapping = statement.map
        source = group_tex(getattr(mapping, "source_group", None))
        target = group_tex(getattr(mapping, "target_group", None))
        symbol = map_symbol_tex(mapping)
        generator = element_tex(statement.source_generator)
        if (source is not None and target is not None
                and symbol is not None and generator is not None
                and type(statement.multiple) is int
                and statement.multiple >= 1
                and statement.domain == mapping.source_group):
            return (
                rf"$\ker({symbol}:{source}\to {target})="
                rf"{statement.multiple}\mathbb{{Z}}\{{{generator}\}}$."
            )
        return None
    if (type(statement) is Relation
            and statement.relation_type is RelationType.EQUALITY
            and isinstance(statement.rhs, Zero)):
        from toda_conclusion_latex_renderer import (
            render_repository_conclusion_latex,
        )
        try:
            latex = render_repository_conclusion_latex(statement)
        except (TypeError, ValueError):
            return None
        return "$" + latex + "$."
    from toda_rules import Toda45IsomorphismStatement
    from homotopy_groups import TodaIteratedSuspensionMap
    if isinstance(statement, Toda45IsomorphismStatement):
        mapping = statement.map
        if isinstance(mapping, TodaIteratedSuspensionMap):
            source = group_tex(mapping.source_group)
            target = group_tex(mapping.target_group)
            if source is not None and target is not None and type(mapping.exponent) is int:
                symbol = 'E' if mapping.exponent == 1 else rf'E^{{{mapping.exponent}}}'
                evidence = toda45_specialization_evidence(step)
                if evidence is not None:
                    _, bindings = evidence
                    values = dict(bindings)
                    return (
                        rf'$(n,m,k)=({values["n"]},{values["m"]},{values["k"]})$ '
                        rf'に適用すると, ${symbol}: {source}\to {target}$ は同型である.'
                    )
                return rf'${symbol}: {source}\to {target}$ は同型である.'
    if isinstance(statement, GeneratorImage):
        x, y = element_tex(statement.source_generator), element_tex(statement.target_generator)
        symbol = map_symbol_tex(statement.map)
        if x is not None and y is not None and symbol is not None:
            return rf"${symbol}({x})={y}$."
    if isinstance(statement, EHPImageEqualsKernelStatement):
        window = statement.window
        if prop42_exactness_indices(TodaProp42ExactnessStatement(window)) is None:
            return None
        if window.first_map == EHP_DELTA_MAP and window.second_map == EHP_E_MAP:
            return r"完全性より, $\operatorname{Im}\Delta=\ker E$ が成り立つ."
        if window.first_map == EHP_E_MAP and window.second_map == EHP_H_MAP:
            return r"完全性より, $\operatorname{Im}E=\ker H$ が成り立つ."
    if isinstance(statement, TodaDeltaImageFreeCyclicStatement):
        if not isinstance(statement.map, TodaDeltaMap) or not isinstance(statement.image_group, FreeCyclicGroup):
            return None
        generator = element_tex(statement.image_group.generator)
        if generator is not None:
            return rf"これより, $\operatorname{{Im}}\Delta=\mathbb{{Z}}\{{{generator}\}}$."
    if isinstance(statement, SuspensionKernelFreeCyclicStatement):
        if not isinstance(statement.map, TodaSuspensionMap) or not isinstance(statement.kernel_group, FreeCyclicGroup):
            return None
        generator = element_tex(statement.kernel_group.generator)
        if generator is not None:
            return rf"完全性より, $\ker E=\mathbb{{Z}}\{{{generator}\}}$."
    if isinstance(statement, QuotientIsomorphismStatement):
        if not isinstance(statement.map, TodaSuspensionMap):
            return None
        domain, codomain = group_tex(statement.domain), group_tex(statement.codomain)
        generator = element_tex(statement.source_generator)
        if domain is not None and codomain is not None and generator is not None and type(statement.multiple) is int:
            multiple = statement.multiple
            return rf"全射性と核の決定から, 準同型定理より ${codomain}\cong {domain}/\mathbb{{Z}}\{{{multiple}{generator}\}}$."
    if isinstance(statement, GeneratorSuspension) and isinstance(statement.map, TodaSuspensionMap):
        x, y = element_tex(statement.source_generator), element_tex(statement.target_generator)
        if x is not None and y is not None:
            return rf"$E({x})={y}$."
    return None

```

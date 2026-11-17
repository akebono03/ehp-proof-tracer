# Phase 175 R3R11R4 — 変更コード・関連テスト全文

## 変更対象の一覧

- 既存コード変更：`phase175_r3r11_cited_hopf_narrative/projection.py::_verified_hopf_chain_lines()` のみ。
- 追加テスト：`tests/test_projection.py` の2関数（末尾に追加）。
- 識別子変更：`audit.py` の `GATE`、`_public_gate()`、`run()`、`main()`、`run.ps1`。
- 既存 `phase171_r20r13_eta_sentence_layout/projection.py` はコミット済みで変更不要。
- module-level の import は変更なし。変更した関数内の import は下記全文に含む。
- 数学的 GIVEN・推論規則・Proof Tree の変更なし。

実装前監査と数学的根拠は `AUDIT_PLAN_JA.md` を参照。次に掲げる Python / PowerShell コードはすべて実ファイル全文であり、省略部分はない。

## `projection.py`

変更モジュール全文。追加した関数内 import と変更関数 `_verified_hopf_chain_lines()` を省略せず収録。

```python
"""Source-bound reference and Hopf-chain display for a completed Proof Tree.

No goal, mathematical premise, rule, source registration, or ProofStep is added.
A presentation is modified only if exact cited GIVENs and a fully established
right-Hopf composition ancestry are present. Otherwise it remains untouched.
"""
from __future__ import annotations

import re

from expression import Composition, MapApplication, Suspension, Zero
from map_facts import EHP_H_MAP
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r52_partial_proof import ProofSearchStatus
from phase168_r3_3_proof_narrative_model import root_ancestor_step_indices
from phase168_r3_27_typed_statement_projection import typed_sentence
from proof import ProofRule, Relation, RelationType


def _completed_scope(model: object) -> frozenset[int] | None:
    """Use only steps belonging to one completed root; no synthetic ancestry."""
    if (getattr(model, "status", None) is not ProofSearchStatus.COMPLETE
            or getattr(model, "open_goals", ())):
        return None
    steps = getattr(model, "steps", None)
    numbers = getattr(model, "step_citation_numbers", None)
    root = getattr(model, "root_index", None)
    if (not isinstance(steps, tuple) or not isinstance(numbers, tuple)
            or len(steps) != len(numbers) or type(root) is not int):
        return None
    try:
        return root_ancestor_step_indices(steps, root)
    except ValueError:
        return None


def _source_citation(model, scope: frozenset[int], *, statement_type: type,
                     assertion_id: str, reference_id: str, locator: str,
                     allow_provenance_fallback: bool = False):
    """Bind a real cited GIVEN to a typed, used, source-screened proof leaf.

    Prefer the precise registry IDs. The historical Proposition 2.2 path can
    carry only the original ProofStep's attached LiteratureReference in the
    Narrative Model. Its fallback requires the exact proved source leaf,
    citation membership, and verified source-rule identity; a bare locator
    alone never supplies a fact.
    """
    citations = getattr(model, "citations", ())
    matches = []
    for citation in citations:
        if citation.reference.locator != locator:
            continue
        for i in citation.step_indices:
            if (i not in scope or type(model.steps[i].conclusion) is not statement_type
                    or model.steps[i].rule is not ProofRule.GIVEN
                    or model.steps[i].premises
                    or citation.number not in model.step_citation_numbers[i]):
                continue
            registered = (assertion_id in citation.assertion_ids
                          and reference_id in citation.reference_ids)
            if not registered and allow_provenance_fallback:
                source = model.steps[i].inference_rule
                reference = getattr(source, "literature_reference", None)
                registered = (
                    statement_type.__name__ == "TodaProp22RightFormula"
                    and getattr(source, "name", None)
                    == "Toda Proposition 2.2 right-Hopf source"
                    and getattr(reference, "locator", None) == locator
                    and locator == "Proposition 2.2"
                )
            if registered:
                matches.append((citation, i))
    return matches[0] if len(matches) == 1 else None


def _reference_body_lines(lines: list[str], model, scope: frozenset[int]):
    """Show the quoted part actually represented by each screened GIVEN."""
    from phase175_r3r9_lemma57_explicit_public.source import (
        ASSERTION_ID as LEMMA_ASSERTION,
        REFERENCE_ID as LEMMA_REFERENCE,
        PARTICULAR_CLAUSE,
        TodaLemma57ExplicitNuPrimeZero,
    )
    from phase171_r2h_prop22_cited_hopf.source import (
        ASSERTION_ID as PROP_ASSERTION,
        REFERENCE_ID as PROP_REFERENCE,
        RIGHT_FORMULA,
        TodaProp22RightFormula,
    )

    wanted = (
        (TodaLemma57ExplicitNuPrimeZero, LEMMA_ASSERTION, LEMMA_REFERENCE,
         "Lemma 5.7", "$" + PARTICULAR_CLAUSE.replace(r"\circ", "") + "$."),
        (TodaProp22RightFormula, PROP_ASSERTION, PROP_REFERENCE,
         "Proposition 2.2", "$" + re.sub(
             r" +", " ", RIGHT_FORMULA.replace(r"\circ", " ")
             .replace(r"\ =\ ", "=")) + "$."),
    )
    output = list(lines)
    try:
        proof_boundary = output.index("証明")
    except ValueError:
        return output
    if output.count("証明") != 1:
        return output
    for source_type, assertion, reference, locator, sentence in wanted:
        found = _source_citation(
            model, scope, statement_type=source_type,
            assertion_id=assertion, reference_id=reference, locator=locator,
            allow_provenance_fallback=(locator == "Proposition 2.2"),
        )
        if found is None:
            continue
        citation, _ = found
        # Already-projected reference bodies remain authoritative.
        if citation.statement_bodies:
            continue
        header = f"**[R{citation.number}] {locator}.**"
        indices = [i for i, text in enumerate(output[:proof_boundary]) if text == header]
        if len(indices) != 1:
            continue
        insert_at = indices[0] + 1
        if sentence not in output[indices[0]:proof_boundary]:
            output[insert_at:insert_at] = ["", sentence]
            proof_boundary += 2
    return output


def _normalized_zero_image(lines: list[str], model, scope: frozenset[int]):
    """Normalize a single cited composite-zero sentence to juxtaposition."""
    from phase175_r3r9_lemma57_explicit_public.source import (
        ASSERTION_ID, REFERENCE_ID, TodaLemma57ExplicitNuPrimeZero,
    )
    found = _source_citation(
        model, scope, statement_type=TodaLemma57ExplicitNuPrimeZero,
        assertion_id=ASSERTION_ID, reference_id=REFERENCE_ID, locator="Lemma 5.7",
    )
    if found is None:
        return list(lines)
    citation, source_index = found
    steps = model.steps
    candidates = (
        step for i, step in enumerate(steps)
        if i in scope and step.rule is ProofRule.INFERENCE
        and isinstance(step.conclusion, GeneratorImage)
        and isinstance(step.conclusion.target_generator, Zero)
        and isinstance(step.conclusion.source_generator, Composition)
        and len(step.premises) == 1
        and step.premises[0] is steps[source_index]
    )
    candidates = tuple(candidates)
    if len(candidates) != 1:
        return list(lines)
    sentence = typed_sentence(candidates[0].conclusion, candidates[0])
    if sentence is None or r"\circ" not in sentence:
        return list(lines)
    original = f"[R{citation.number}]より, " + sentence
    result = list(lines)
    try:
        proof_start = result.index("証明") + 1
    except ValueError:
        return result
    occurrences = [i for i in range(proof_start, len(result)) if result[i] == original]
    if len(occurrences) == 1:
        result[occurrences[0]] = original.replace(r"\circ ", "").replace(r"\circ", "")
    return result


def _unique_conclusion(model, scope: frozenset[int], conclusion, rule: ProofRule):
    matches = tuple(
        (i, step) for i, step in enumerate(model.steps)
        if i in scope and step.conclusion == conclusion and step.rule is rule
    )
    return matches[0] if len(matches) == 1 else None


def _ancestor_citation(model, scope: frozenset[int], step, expected_type: type):
    """Find one citation by reaching a typed GIVEN through actual premises."""
    seen: set[int] = set()
    stack = [step]
    source_numbers: set[int] = set()
    while stack:
        ancestor = stack.pop()
        identity = tuple(i for i in scope if model.steps[i] is ancestor)
        if len(identity) != 1:
            return None
        i = identity[0]
        if i in seen:
            continue
        seen.add(i)
        if ancestor.rule is ProofRule.GIVEN and type(ancestor.conclusion) is expected_type:
            source_numbers.update(model.step_citation_numbers[i])
        stack.extend(ancestor.premises)
    return next(iter(source_numbers)) if len(source_numbers) == 1 else None


def _rendered_sentence(step):
    """Reproduce a sentence only from the exact typed conclusion."""
    sentence = typed_sentence(step.conclusion, step)
    if sentence is not None:
        return sentence
    from web_group_proof_common import _group_proof_statement_latex
    latex, fallback = _group_proof_statement_latex(step.conclusion)
    if latex is None or fallback is not None:
        return None
    return f"${latex}$."


def _unique_display_index(lines: list[str], boundary: int, sentence: str):
    if not sentence:
        return None
    matches = [i for i in range(boundary, len(lines))
               if lines[i] == sentence or lines[i].endswith(sentence)]
    return matches[0] if len(matches) == 1 else None


def _verified_hopf_chain_lines(lines: list[str], model, scope: frozenset[int]):
    """Summarize only a verified right-Hopf chain actually used by the root.

    The final Hopf image and the specialized right-Hopf equation must each be
    distinct proved INFERENCE steps. Both must descend from the cited general
    Proposition 2.2, the separately cited H(alpha) value and the eta-family
    suspension witness. Only matching uncited intermediate proof equations
    are omitted. No new equality, citation, or proof step is constructed.
    """
    from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
    from phase171_r2h_prop22_cited_hopf.source import (
        ASSERTION_ID, REFERENCE_ID, TodaProp22RightFormula,
    )
    from phase171_r2i_eta_hopf_bridge.source import _make_chain
    from phase175_r3r9_lemma57_explicit_public.source import (
        ASSERTION_ID as LEMMA_ASSERTION_ID,
        REFERENCE_ID as LEMMA_REFERENCE_ID,
        TodaLemma57ExplicitNuPrimeZero,
    )

    result = list(lines)
    if result.count("証明") != 1:
        return result
    # Phase 172 already provides a compact Hopf chain for other complete
    # roots.  Do not collapse that previously approved presentation a second
    # time.  This additional single equation is only for a completed root
    # with the separately cited *and derived* Lemma 5.7 zero-image bridge.
    # No group dimensions, reference numbers or text-only labels are matched.
    lemma_source = _source_citation(
        model, scope, statement_type=TodaLemma57ExplicitNuPrimeZero,
        assertion_id=LEMMA_ASSERTION_ID, reference_id=LEMMA_REFERENCE_ID,
        locator="Lemma 5.7",
    )
    if lemma_source is None:
        return result
    _, lemma_index = lemma_source
    zero_bridges = tuple(
        step for i, step in enumerate(model.steps)
        if i in scope and step.rule is ProofRule.INFERENCE
        and isinstance(step.conclusion, GeneratorImage)
        and isinstance(step.conclusion.target_generator, Zero)
        and isinstance(step.conclusion.source_generator, Composition)
        and len(step.premises) == 1
        and step.premises[0] is model.steps[lemma_index]
    )
    if len(zero_bridges) != 1:
        return result
    boundary = result.index("証明") + 1
    prop_source = _source_citation(
        model, scope, statement_type=TodaProp22RightFormula,
        assertion_id=ASSERTION_ID, reference_id=REFERENCE_ID,
        locator="Proposition 2.2", allow_provenance_fallback=True,
    )
    if prop_source is None:
        return result
    prop_citation, prop_index = prop_source

    for given_index in sorted(scope):
        hopf_given = model.steps[given_index]
        if (hopf_given.rule is not ProofRule.GIVEN
                or not isinstance(hopf_given.conclusion, Relation)
                or hopf_given.conclusion.relation_type is not RelationType.EQUALITY):
            continue
        chain = _make_chain(hopf_given.conclusion)
        if chain is None:
            continue
        hopf_numbers = model.step_citation_numbers[given_index]
        if len(hopf_numbers) != 1:
            continue
        hopf_number = hopf_numbers[0]
        if not any(
            cite.number == hopf_number and given_index in cite.step_indices
            for cite in model.citations
        ):
            continue

        formula = Relation(
            lhs=chain.cited_hopf.lhs,
            rhs=Composition(
                MapApplication(EHP_H_MAP, chain.alpha), Suspension(chain.beta),
            ),
            relation_type=RelationType.EQUALITY,
        )
        witnesses = {
            "witness": chain.generator_suspension,
            "formula": formula,
            "conclusion": chain.conclusion,
        }
        located = {
            name: _unique_conclusion(model, scope, claim, ProofRule.INFERENCE)
            for name, claim in witnesses.items()
        }
        if any(item is None for item in located.values()):
            continue
        indices = {name: pair[0] for name, pair in located.items()}
        steps = {name: pair[1] for name, pair in located.items()}

        try:
            final_ancestry = root_ancestor_step_indices(
                model.steps, indices["conclusion"],
            )
            formula_ancestry = root_ancestor_step_indices(
                model.steps, indices["formula"],
            )
        except ValueError:
            continue
        # Verify real premise ownership. This also prevents independently
        # proven, similarly rendered equations from being silently conflated.
        if (not {given_index, prop_index, indices["witness"],
                 indices["formula"]}.issubset(final_ancestry)
                or prop_index not in formula_ancestry):
            continue
        eta_number = _ancestor_citation(
            model, scope, steps["witness"], TodaEtaFamilyGeneralDefinition,
        )
        if (eta_number is None
                or len({eta_number, prop_citation.number, hopf_number}) != 3):
            continue
        if any(model.step_citation_numbers[indices[name]]
               for name in ("formula", "conclusion")):
            continue

        anchors = {
            name: _unique_display_index(
                result, boundary, _rendered_sentence(steps[name]),
            )
            for name in ("witness", "formula", "conclusion")
        }
        hopf_anchor = _unique_display_index(
            result, boundary, _rendered_sentence(hopf_given),
        )
        if any(i is None for i in anchors.values()) or hopf_anchor is None:
            continue
        if not (anchors["witness"] < anchors["formula"] < hopf_anchor
                < anchors["conclusion"]):
            continue

        # An inline equality chain is legitimate only if every intermediate
        # equality actually occurs as an uncited derived step in this root.
        # It is not enough to reconstruct a plausible equation from labels.
        required_equalities = (
            chain.eta_forward, chain.eta_backward,
            chain.alpha_composition, chain.hopf_composition,
            chain.cited_hopf, chain.intermediate, chain.beta_composition,
        )
        required_indices = []
        for equality in required_equalities:
            found = _unique_conclusion(
                model, scope, equality, ProofRule.INFERENCE,
            )
            if (found is None or found[0] not in final_ancestry
                    or model.step_citation_numbers[found[0]]):
                break
            required_indices.append(found[0])
        if len(required_indices) != len(required_equalities):
            continue

        hidden_indices = []
        for name, claim in (
            ("forward", chain.eta_forward),
            ("backward", chain.eta_backward),
            ("alpha", chain.alpha_composition),
            ("hopf", chain.hopf_composition),
            ("cited", chain.cited_hopf),
            ("intermediate", chain.intermediate),
            ("beta", chain.beta_composition),
        ):
            located_step = _unique_conclusion(
                model, scope, claim, ProofRule.INFERENCE,
            )
            if located_step is None or located_step[0] not in final_ancestry:
                continue
            if model.step_citation_numbers[located_step[0]]:
                continue
            display_index = _unique_display_index(
                result, boundary, _rendered_sentence(located_step[1]),
            )
            if display_index is None or result[display_index].startswith("[R"):
                continue
            if not (anchors["witness"] < display_index
                    < anchors["conclusion"]):
                continue
            hidden_indices.append(display_index)
        if len(hidden_indices) != len(set(hidden_indices)):
            continue
        # Construct one displayed equality chain from the typed generator,
        # suspension and final proven image. The relation steps above certify
        # every link; the formatter only renders their already-proved values.
        from toda_human_readable_renderer import render_toda_expression_latex

        try:
            alpha = render_toda_expression_latex(chain.alpha)
            beta = render_toda_expression_latex(chain.beta)
            eta_next = render_toda_expression_latex(chain.eta_next)
            square = render_toda_expression_latex(chain.conclusion.rhs)
        except (TypeError, ValueError):
            continue
        if not all((alpha, beta, eta_next, square)):
            continue
        chain_math = (
            f"H({alpha}{eta_next})"
            f"=H({alpha}E{beta})"
            f"=H({alpha})E{beta}"
            f"={beta}E{beta}"
            f"={square}"
        )
        tags = ", ".join(f"[R{n}]" for n in (
            eta_number, prop_citation.number, hopf_number,
        ))
        summary = f"{tags}より, ${chain_math}$."
        omitted = set(hidden_indices)
        omitted.update((
            anchors["witness"], anchors["formula"], hopf_anchor,
        ))
        if anchors["conclusion"] in omitted:
            continue
        changed: list[str] = []
        for i, line in enumerate(result):
            if i in omitted:
                continue
            if i == anchors["conclusion"]:
                changed.append(summary)
            else:
                changed.append(line)
        # Suppressed equations can leave adjacent empty paragraphs. This is
        # presentation-only and applies only after verified compression.
        return [line for i, line in enumerate(changed)
                if line or i == 0 or changed[i - 1] != ""]
    return result


def project_verified_source_and_hopf_summary(lines: list[str], model) -> list[str]:
    """Single post-render presentation hook; all other searches pass unchanged."""
    scope = _completed_scope(model)
    if scope is None:
        return list(lines)
    with_sources = _reference_body_lines(lines, model, scope)
    normalized = _normalized_zero_image(with_sources, model, scope)
    return _verified_hopf_chain_lines(normalized, model, scope)
```

## `tests/test_projection.py`

変更済みテストファイル全文。2件の新規テストはファイル末尾に追加。

```python
"""End-to-end cited Proof Tree narration; no database-given group conclusions."""
from __future__ import annotations

from dataclasses import replace

import pytest

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative
from phase175_r3r11_cited_hopf_narrative.projection import (
    project_verified_source_and_hopf_summary,
)


@pytest.fixture(scope="module")
def pi73_verified():
    bridge = build_shared_typed_bridge()
    contexts = []
    result = search_group_from_registered_goal(
        n=3, k=4, bridge=bridge, context_sink=contexts.append,
    )
    assert result.status is ProofSearchStatus.COMPLETE
    assert not result.open_goals
    assert len(contexts) == 1
    cited = resolve_specialized_goal_citing_id(bridge, result.conclusion)
    verify_proof_tree_for_narrative(result, contexts[0], citing_assertion_id=cited)
    model = build_linked_proof_narrative_model(result, contexts[0])
    return result, model


def test_references_and_zero_composition_are_explicit(pi73_verified) -> None:
    result, model = pi73_verified
    content = render_model_backed_narrative_markdown(result, model)
    reference, body = content.split("\n証明\n", 1)
    assert "**[R2] Lemma 5.7.**" in reference
    assert r"$E(\eta_2\nu')=0$." in reference
    assert "特に, " not in reference
    assert "**[R6] Proposition 2.2.**" in reference
    assert r"$H(\alpha E\beta)=H(\alpha) E\beta$." in reference
    assert "右合成公式: " not in reference
    assert r"[R2]より, $E(\eta_{2}\nu')=0$." in body
    assert r"$E(\eta_{2}\circ " not in body
    assert len(model.citations) == 7


def test_hopf_chain_is_source_bound_and_compact(pi73_verified) -> None:
    result, model = pi73_verified
    before = tuple(id(step) for step in model.steps)
    content = render_model_backed_narrative_markdown(result, model)
    _, body = content.split("\n証明\n", 1)
    chain = (
        r"[R5], [R6], [R7]より, "
        r"$H(\nu'\eta_{6})=H(\nu'E\eta_{5})"
        r"=H(\nu')E\eta_{5}=\eta_{5}E\eta_{5}=\eta_{5}^{2}$."
    )
    assert body.count(chain) == 1, body
    assert r"[R5]より, $E(\eta_{5})=\eta_{6}$." not in body
    assert r"[R6]より, $H(\nu'E\eta_{5})" not in body
    assert r"[R7]より, $H(\nu')=\eta_{5}$." not in body
    assert "□" in body
    assert before == tuple(id(step) for step in model.steps)


def test_unscreened_or_incomplete_model_remains_unchanged(pi73_verified) -> None:
    _, model = pi73_verified
    lines = ["使用する結果", "", "証明", "", "元の数学的表示", "", "□"]
    assert project_verified_source_and_hopf_summary(
        lines, replace(model, status=ProofSearchStatus.PARTIAL),
    ) == lines
    assert project_verified_source_and_hopf_summary(
        lines, replace(model, citations=()),
    ) == lines
    assert project_verified_source_and_hopf_summary(
        lines, replace(model, root_index=None),
    ) == lines


def test_citation_identity_not_locator_text_controls_reference(pi73_verified) -> None:
    _, model = pi73_verified
    refs = tuple(replace(c, assertion_ids=()) if c.reference.locator == "Lemma 5.7"
                 else c for c in model.citations)
    lines = ["使用する結果", "", "**[R2] Lemma 5.7.**", "", "証明", "", "□"]
    changed = project_verified_source_and_hopf_summary(
        lines, replace(model, citations=refs),
    )
    assert r"$E(\eta_2\nu')=0$." not in changed


def test_proposition_22_citation_fallback_uses_actual_given(pi73_verified) -> None:
    """Legacy model links can omit IDs, never the source ProofStep itself."""
    from phase171_r2h_prop22_cited_hopf.source import (
        ASSERTION_ID, REFERENCE_ID, TodaProp22RightFormula,
    )
    from phase175_r3r11_cited_hopf_narrative.projection import (
        _completed_scope, _source_citation,
    )
    _, model = pi73_verified
    scope = _completed_scope(model)
    assert scope is not None
    citation_only = replace(model, citations=tuple(
        replace(cite, assertion_ids=(), reference_ids=())
        if cite.reference.locator == "Proposition 2.2" else cite
        for cite in model.citations
    ))
    source = _source_citation(
        citation_only, scope, statement_type=TodaProp22RightFormula,
        assertion_id=ASSERTION_ID, reference_id=REFERENCE_ID,
        locator="Proposition 2.2", allow_provenance_fallback=True,
    )
    assert source is not None
    source_citation, source_index = source
    assert source_citation.reference.locator == "Proposition 2.2"
    original = model.steps[source_index]
    assert original.inference_rule is not None
    spoofed = replace(original, inference_rule=replace(
        original.inference_rule, name="not the verified Proposition 2.2 source",
    ))
    damaged_steps = list(citation_only.steps)
    damaged_steps[source_index] = spoofed
    damaged = replace(citation_only, steps=tuple(damaged_steps))
    assert _source_citation(
        damaged, scope, statement_type=TodaProp22RightFormula,
        assertion_id=ASSERTION_ID, reference_id=REFERENCE_ID,
        locator="Proposition 2.2", allow_provenance_fallback=True,
    ) is None


def test_unverified_intermediate_cannot_be_collapsed(pi73_verified) -> None:
    from phase175_r3r11_cited_hopf_narrative.projection import (
        _completed_scope, _verified_hopf_chain_lines,
    )
    _, model = pi73_verified
    scope = _completed_scope(model)
    assert scope is not None
    # The absence of the actual proof-body formulas must never create them.
    lines = ["使用する結果", "", "証明", "", "元の数学的表示", "", "□"]
    assert _verified_hopf_chain_lines(lines, model, scope) == lines


def test_pi63_phase172_hopf_display_survives_second_projector() -> None:
    """The newer one-line Hopf summary must not erase Phase 172's cited prose."""
    bridge = build_shared_typed_bridge()
    contexts = []
    result = search_group_from_registered_goal(
        n=3, k=3, bridge=bridge, context_sink=contexts.append,
    )
    assert result.status is ProofSearchStatus.COMPLETE
    assert not result.open_goals
    assert len(contexts) == 1
    citing = resolve_specialized_goal_citing_id(bridge, result.conclusion)
    assert citing is not None
    verify_proof_tree_for_narrative(
        result, contexts[0], citing_assertion_id=citing,
    )
    model = build_linked_proof_narrative_model(result, contexts[0])
    markdown = render_model_backed_narrative_markdown(result, model)
    reference, body = markdown.split("\n証明\n", 1)
    assert "[R4] Proposition 2.2." in reference
    assert r"[R3]より, $E(\eta_{5})=\eta_{6}$." in body
    assert "[R4]より, " in body
    assert "[R3], [R4], [R5]より, " in body
    assert "□" in body


def test_hopf_summary_requires_actual_lemma57_zero_image(pi73_verified) -> None:
    """A mere Hopf formula cannot authorize R3R11's second compression."""
    from phase175_r3r11_cited_hopf_narrative.projection import (
        _completed_scope, _verified_hopf_chain_lines,
    )
    _, model = pi73_verified
    scope = _completed_scope(model)
    assert scope is not None
    lemma_citations = tuple(
        replace(citation, assertion_ids=(), reference_ids=())
        if citation.reference.locator == "Lemma 5.7" else citation
        for citation in model.citations
    )
    no_lemma = replace(model, citations=lemma_citations)
    lines = [
        "使用する結果", "", "証明", "",
        r"[R5]より, $E(\eta_{5})=\eta_{6}$.", "",
        r"[R6]より, $H(\nu'E\eta_{5})=H(\nu')E\eta_{5}$.", "",
        r"[R7]より, $H(\nu')=\eta_{5}$.", "",
        r"[R5], [R6], [R7]より, $H(\nu'\eta_{6})=\eta_{5}^{2}$.",
        "", "□",
    ]
    assert _verified_hopf_chain_lines(lines, no_lemma, scope) == lines
```

## `audit.py`

監査スクリプト全文。変更された `_public_gate()`・`run()`・`main()` および import を含む。

```python
"""R3R11 guarded read-only DryRun and completed cited-narrative Web gate."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import traceback

from phase175_r3r11_cited_hopf_narrative import install

GATE = "PASS_R3R11R4_SINGLE_EQUATION_AND_PRIOR_NARRATIVE"
TEST_PATHS = (
    "phase175_r3r11_cited_hopf_narrative/tests",
    "phase175_r3r10_generator_zero_narrative/tests/test_public.py",
    "phase175_r3r10_generator_zero_narrative/tests/test_projection.py",
    "phase175_r3r9_lemma57_explicit_public/tests/test_public_search.py",
    "phase171_r20r13_eta_sentence_layout/tests/test_projection.py",
    "phase172_r3_hopf_chain_display/tests/test_projection.py",
    # R70's historical installer-source-pin test expects the pre-R3R10
    # phase168 file. R3R10 legitimately changed that file. Retain the
    # independent R70 functional tests, without weakening its source guard.
    "phase174_r3_r7_r70_verified_narrative_projection/tests/test_projection.py::test_line_endings_source_guard_and_patch_idempotence",
    "phase174_r3_r7_r70_verified_narrative_projection/tests/test_projection.py::test_source_guard_rejects_unreviewed_change",
    "phase174_r3_r7_r70_verified_narrative_projection/tests/test_projection.py::test_rejects_mixed_eol_and_cr_only",
    "phase174_r3_r7_r70_verified_narrative_projection/tests/test_projection.py::test_body_line_search_does_not_match_reference_text",
    "phase174_r3_r7_r70_verified_narrative_projection/tests/test_projection.py::test_step_index_rejects_ambiguous_value_fallback",
    "phase174_r3_r7_r70_verified_narrative_projection/tests/test_projection.py::test_incomplete_model_has_no_composed_rewrite",
    "phase174_r3_r7_r70_verified_narrative_projection/tests/test_projection.py::test_git_sha_fixture",
)


def _read_git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=root, capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=False,
    )
    if result.returncode:
        raise RuntimeError("R3R11_GIT_READ_FAILED: " + " ".join(args))
    return result.stdout.strip()


def preflight(root: Path):
    if not (root / ".git").exists():
        raise RuntimeError("R3R11_GIT_REPOSITORY_REQUIRED")
    if _read_git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("R3R11_DEVELOP_REQUIRED")
    blob = _read_git(root, "rev-parse", "HEAD:" + install.TARGET.as_posix())
    if blob != install.REVIEWED_HEAD_BLOB:
        raise RuntimeError("R3R11_REVIEWED_BLOB_CHANGED")
    if not (root / "phase175_r3r10_generator_zero_narrative" / "run.ps1").is_file():
        raise RuntimeError("R3R11_R3R10_REQUIRED")
    if not (root / "phase175_r3r9_lemma57_explicit_public" / "route.py").is_file():
        raise RuntimeError("R3R11_R3R9_REQUIRED")
    r3r10 = (root / "phase168_r3_27_typed_statement_projection.py").read_text(
        encoding="utf-8",
    )
    if "if isinstance(statement.target_generator, Zero):" not in r3r10:
        raise RuntimeError("R3R11_R3R10_NOT_INSTALLED")
    plan = install.plan_patch(root)
    status = _read_git(root, "status", "--porcelain", "--", install.TARGET.as_posix())
    if plan.status == "PATCH_REQUIRED" and status:
        raise RuntimeError("R3R11_PREEXISTING_RENDERER_EDIT_REFUSED")
    return {"head": _read_git(root, "rev-parse", "HEAD"),
            "blob": blob, "plan": plan}


def _public_gate() -> dict[str, object]:
    """Require a cited single equation with the same verified proof and Web gate."""
    from phase175_r1_k4_audit.audit import inspect_one_group
    from phase175_r3r9_lemma57_explicit_public.audit import verify_public_result

    recorded = inspect_one_group(3, 4)
    proof = verify_public_result(recorded)
    markdown = recorded.get("markdown")
    if not isinstance(markdown, str) or markdown.count("\n証明\n") != 1:
        raise RuntimeError("R3R11R4_MODEL_NARRATIVE_NOT_AVAILABLE")
    reference, body = markdown.split("\n証明\n", 1)
    refs = recorded.get("references")
    if not isinstance(refs, list):
        raise RuntimeError("R3R11R4_MODEL_CITATIONS_MISSING")
    by_locator = {c["locator"]: c["number"] for c in refs}
    if not all(name in by_locator for name in
               ("Lemma 5.7", "Proposition 2.2", "Chapter V, i)", "(5.3)")):
        raise RuntimeError("R3R11R4_REQUIRED_TYPED_SOURCES_NOT_CITED")
    l57 = f"[R{by_locator['Lemma 5.7']}]"
    prop22 = f"[R{by_locator['Proposition 2.2']}]"
    eta = f"[R{by_locator['Chapter V, i)']}]"
    hopf = f"[R{by_locator['(5.3)']}]"
    if (r"$E(\eta_2\nu')=0$." not in reference
            or r"$H(\alpha E\beta)=H(\alpha) E\beta$." not in reference
            or "特に, " in reference or "右合成公式: " in reference):
        raise RuntimeError("R3R11R4_REFERENCE_BODY_CONTRACT_FAILED")
    if (f"{l57}より, " + r"$E(\eta_{2}\nu')=0$." not in body
            or r"$E(\eta_{2}\circ" in body):
        raise RuntimeError("R3R11R4_COMPOSITION_NOT_UNIFIED")
    summary = (
        f"{eta}, {prop22}, {hopf}より, "
        r"$H(\nu'\eta_{6})=H(\nu'E\eta_{5})"
        r"=H(\nu')E\eta_{5}=\eta_{5}E\eta_{5}=\eta_{5}^{2}$."
    )
    if body.count(summary) != 1:
        raise RuntimeError("R3R11R4_SINGLE_EQUATION_NOT_VERIFIED")
    if any(old in body for old in (
        r"[R5]より, $E(\eta_{5})=\eta_{6}$.",
        r"[R6]より, $H(\nu'E\eta_{5})",
        r"[R7]より, $H(\nu')=\eta_{5}$.",
    )):
        raise RuntimeError("R3R11R4_OLD_HOPF_LINES_STILL_VISIBLE")
    if (recorded.get("web_key") != "generic-complete-proof"
            or recorded.get("trust_verified") is not True
            or recorded.get("reference_count") != 7):
        raise RuntimeError("R3R11R4_PROOF_TRUST_OR_WEB_CHANGED")
    return {
        "search": proof["search_status"],
        "web": proof["web"],
        "trust": recorded.get("trust_verified"),
        "lemma54_used": proof["lemma54_used"],
        "reference_count": recorded.get("reference_count"),
        "lemma57_reference": l57,
        "prop22_reference": prop22,
        "single_equation_references": f"{eta}, {prop22}, {hopf}",
        "single_equation": summary,
        "markdown_sha256": sha256(markdown.encode("utf-8")).hexdigest(),
    }


def run(root: Path, dry_run: bool, timeout_seconds: int) -> int:
    root = root.resolve()
    checked = preflight(root)
    plan = checked["plan"]
    print("PHASE175_R3R11R4_BRANCH=develop")
    print("PHASE175_R3R11R4_HEAD=" + checked["head"])
    print("PHASE175_R3R11R4_REVIEWED_BLOB=" + checked["blob"])
    print("PHASE175_R3R11R4_PATCH_STATUS=" + plan.status)
    print("PHASE175_R3R11R4_NEW_GIVEN=0")
    print("PHASE175_R3R11R4_NEW_MATHEMATICAL_RULES=0")
    if dry_run:
        print("PHASE175_R3R11R4_GATE=PASS_R3R11R4_READ_ONLY_DRYRUN")
        return 0

    folder = (Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
              / "EHPProofTracerAudit" / "phase175_r3r11_cited_hopf_narrative")
    folder.mkdir(parents=True, exist_ok=True)
    target = root / install.TARGET
    if plan.status == "PATCH_REQUIRED":
        (folder / "renderer_backup.py").write_bytes(plan.old_bytes)
    try:
        install.apply_patch(root, plan)
        env = dict(os.environ)
        env.update(PYTHONUTF8="1", PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
        cmd = [sys.executable, "-B", "-m", "pytest", "-q", "--disable-warnings",
               "-p", "no:cacheprovider", "-o", "addopts=", "--import-mode=importlib",
               *TEST_PATHS]
        result = subprocess.run(
            cmd, cwd=root, env=env, capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=timeout_seconds, check=False,
        )
        (folder / "focused_pytest.txt").write_text(
            result.stdout + "\n" + result.stderr, encoding="utf-8",
        )
        print(result.stdout[-4000:])
        if result.returncode:
            raise RuntimeError("R3R11_FOCUSED_PYTEST_FAILED")
        print("PHASE175_R3R11R4_FOCUSED_PYTEST=PASS")
        certified = _public_gate()
        (folder / "report.json").write_text(json.dumps({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "gate": GATE,
            "head": checked["head"],
            "pre_sha256": sha256(plan.old_bytes).hexdigest(),
            "post_sha256": sha256(target.read_bytes()).hexdigest(),
            "public": certified,
        }, indent=2, ensure_ascii=False), encoding="utf-8")
        for key, value in certified.items():
            print("PHASE175_R3R11R4_" + key.upper() + "=" + str(value))
        print("PHASE175_R3R11R4_GATE=" + GATE)
        return 0
    except Exception:
        if plan.status == "PATCH_REQUIRED":
            if target.read_bytes() == plan.new_bytes:
                target.write_bytes(plan.old_bytes)
                print("PHASE175_R3R11R4_ROLLBACK=RESTORED")
            else:
                print("PHASE175_R3R11R4_ROLLBACK=MANUAL_INSPECTION_REQUIRED")
        raise


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--timeout-seconds", type=int, default=300)
    args = parser.parse_args()
    try:
        return run(args.root, args.dry_run, args.timeout_seconds)
    except Exception:
        traceback.print_exc()
        print("PHASE175_R3R11R4_GATE=FAIL")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
```

## `run.ps1`

PowerShell 実行コード全文。

```powershell
param(
    [switch]$DryRun,
    [int]$TimeoutSeconds = 300
)

$ErrorActionPreference = 'Stop'
$env:PYTHONUTF8 = '1'
$env:PYTHONIOENCODING = 'utf-8'
$env:PYTHONDONTWRITEBYTECODE = '1'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $root

if ($DryRun) {
    & python -B -m phase175_r3r11_cited_hopf_narrative.audit `
        --root $root --dry-run --timeout-seconds $TimeoutSeconds
    $code = $LASTEXITCODE
    Write-Output "PHASE175_R3R11R4_EXIT_CODE=$code"
    exit $code
}

& python -B -m phase175_r3r11_cited_hopf_narrative.audit `
    --root $root --timeout-seconds $TimeoutSeconds
$code = $LASTEXITCODE
Write-Output "PHASE175_R3R11R4_EXIT_CODE=$code"
exit $code
```

## `install.py`

固定済みインストーラー全文（R3R11R3 から変更なし）。

```python
"""Replace one pinned, complete renderer function with EOL-aware rollback support."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

TARGET = Path("phase171_r20r13_eta_sentence_layout/projection.py")
REVIEWED_HEAD_BLOB = "5deaa8886f36ec967d52b9fcd603d135ae290b39"
PACKAGE = Path(__file__).resolve().parent
BASE = (PACKAGE / "full_functions" /
        "format_complete_proof_sentences_BASE.py").read_text(encoding="utf-8")
FULL = (PACKAGE / "full_functions" /
        "format_complete_proof_sentences_FULL.py").read_text(encoding="utf-8")


@dataclass(frozen=True)
class PatchPlan:
    status: str
    old_bytes: bytes
    new_bytes: bytes


def _canonical(data: bytes) -> tuple[bytes, bytes]:
    if data.startswith(b"\xef\xbb\xbf"):
        raise RuntimeError("R3R11_UNEXPECTED_BOM")
    if b"\r\r\n" in data:
        raise RuntimeError("R3R11_DOUBLE_CRLF")
    rest = data.replace(b"\r\n", b"")
    if b"\r" in rest:
        raise RuntimeError("R3R11_UNEXPECTED_CR")
    if b"\r\n" in data and b"\n" in rest:
        raise RuntimeError("R3R11_MIXED_EOL")
    eol = b"\r\n" if b"\r\n" in data else b"\n"
    normalized = data.replace(b"\r\n", b"\n")
    return normalized, eol


def plan_patch(root: Path) -> PatchPlan:
    target = Path(root) / TARGET
    if not target.is_file():
        raise RuntimeError("R3R11_RENDERER_NOT_FOUND")
    original = target.read_bytes()
    normalized, eol = _canonical(original)
    before = BASE.encode("utf-8")
    after = FULL.encode("utf-8")
    if (normalized.count(b"def format_complete_proof_sentences(") != 1
            or not normalized.endswith(b"\n")
            or BASE == FULL):
        raise RuntimeError("R3R11_FUNCTION_BOUNDARY_NOT_UNIQUE")
    if normalized.endswith(after) and normalized.count(after) == 1:
        return PatchPlan("ALREADY_APPLIED", original, original)
    if not normalized.endswith(before) or normalized.count(before) != 1:
        raise RuntimeError("R3R11_REVIEWED_FORMATTER_MISMATCH")
    patched = normalized[:-len(before)] + after
    result = patched.replace(b"\n", eol)
    if eol == b"\r\n" and result.count(b"\n") != result.count(b"\r\n"):
        raise RuntimeError("R3R11_EOL_PRESERVATION_FAILED")
    return PatchPlan("PATCH_REQUIRED", original, result)


def apply_patch(root: Path, plan: PatchPlan) -> None:
    target = Path(root) / TARGET
    if plan.status not in ("PATCH_REQUIRED", "ALREADY_APPLIED"):
        raise RuntimeError("R3R11_UNKNOWN_PATCH_STATUS")
    if target.read_bytes() != plan.old_bytes:
        raise RuntimeError("R3R11_TARGET_CHANGED_SINCE_PREFLIGHT")
    if plan.status == "PATCH_REQUIRED":
        target.write_bytes(plan.new_bytes)
```

## `tests/test_install.py`

インストーラー関連テスト全文（変更なし）。

```python
"""Atomic function replacement and Windows CRLF boundary checks."""
from __future__ import annotations

from pathlib import Path

import pytest

from phase175_r3r11_cited_hopf_narrative import install


def _fixture(tmp_path: Path, *, eol: bytes = b"\n") -> Path:
    target = tmp_path / install.TARGET
    target.parent.mkdir(parents=True, exist_ok=True)
    text = b"# unrelated top-level declarations\n\n" + install.BASE.encode("utf-8")
    target.write_bytes(text.replace(b"\n", eol))
    return tmp_path


def test_full_function_is_only_changed_segment(tmp_path: Path) -> None:
    root = _fixture(tmp_path)
    plan = install.plan_patch(root)
    assert plan.status == "PATCH_REQUIRED"
    assert plan.new_bytes.startswith(b"# unrelated top-level declarations\n\n")
    assert plan.new_bytes.endswith(install.FULL.encode("utf-8"))
    install.apply_patch(root, plan)
    again = install.plan_patch(root)
    assert again.status == "ALREADY_APPLIED"
    assert again.old_bytes == again.new_bytes


def test_crlf_fixture_preserves_only_crlf(tmp_path: Path) -> None:
    root = _fixture(tmp_path, eol=b"\r\n")
    plan = install.plan_patch(root)
    install.apply_patch(root, plan)
    raw = (root / install.TARGET).read_bytes()
    assert plan.status == "PATCH_REQUIRED"
    assert b"\r\r\n" not in raw
    assert raw.count(b"\r\n") == raw.count(b"\n")
    assert raw.endswith(install.FULL.encode("utf-8").replace(b"\n", b"\r\n"))
    assert install.plan_patch(root).status == "ALREADY_APPLIED"


def test_rejects_unreviewed_formatter_and_mixed_eol(tmp_path: Path) -> None:
    root = _fixture(tmp_path)
    target = root / install.TARGET
    target.write_bytes(target.read_bytes().replace(b"Keep the original", b"Discard the original"))
    with pytest.raises(RuntimeError, match="REVIEWED_FORMATTER_MISMATCH"):
        install.plan_patch(root)
    root = _fixture(tmp_path)
    target.write_bytes(b"# first\r\n# second\n" + install.BASE.encode("utf-8"))
    with pytest.raises(RuntimeError, match="MIXED_EOL"):
        install.plan_patch(root)


def test_patch_is_stale_write_protected(tmp_path: Path) -> None:
    root = _fixture(tmp_path)
    plan = install.plan_patch(root)
    target = root / install.TARGET
    target.write_bytes(target.read_bytes() + b"# concurrent change\n")
    with pytest.raises(RuntimeError, match="TARGET_CHANGED_SINCE_PREFLIGHT"):
        install.apply_patch(root, plan)


def test_committed_r3r11r1_formatter_is_already_applied(tmp_path: Path) -> None:
    """The reviewed Git HEAD has the R3R11R1 formatter hook already."""
    root = _fixture(tmp_path)
    target = root / install.TARGET
    current = target.read_bytes().replace(install.BASE.encode("utf-8"),
                                          install.FULL.encode("utf-8"))
    target.write_bytes(current)
    plan = install.plan_patch(root)
    assert plan.status == "ALREADY_APPLIED"
    assert plan.old_bytes == plan.new_bytes == current


def test_reviewed_r3r11r1_git_blob_pin() -> None:
    assert install.REVIEWED_HEAD_BLOB == "5deaa8886f36ec967d52b9fcd603d135ae290b39"
```

## `full_functions/format_complete_proof_sentences_BASE.py`

既存 Renderer 関数の前版全文。

```python
def format_complete_proof_sentences(lines: list[str], model) -> list[str]:
    """Keep the original tree/citations; alter only completed narrative prose."""
    from phase174_r3_r7_r70_verified_narrative_projection.projection import (
        project_verified_general_narrative,
    )
    return split_completed_proof_sentences(
        project_verified_general_narrative(
            combine_adjacent_verified_eta_sentences(lines, model), model,
        )
    )
```

## `full_functions/format_complete_proof_sentences_FULL.py`

既存 Renderer 関数の現行全文。

```python
def format_complete_proof_sentences(lines: list[str], model) -> list[str]:
    """Keep the original tree/citations; alter only completed narrative prose."""
    from phase174_r3_r7_r70_verified_narrative_projection.projection import (
        project_verified_general_narrative,
    )
    from phase175_r3r11_cited_hopf_narrative.projection import (
        project_verified_source_and_hopf_summary,
    )
    combined = project_verified_general_narrative(
        combine_adjacent_verified_eta_sentences(lines, model), model,
    )
    cited = project_verified_source_and_hopf_summary(combined, model)
    return split_completed_proof_sentences(cited)
```

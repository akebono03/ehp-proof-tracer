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

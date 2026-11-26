from __future__ import annotations

import ast
import pytest

from phase178_r12r2_zero_composition_elision.installer import ANCHOR, HOOK, proposed_source
from phase178_r12r2_zero_composition_elision.projection import remove_owned_paragraphs, project_zero_composition_elision


def test_remove_only_owned_paragraphs():
    lines = ['ref', '証明', 'base', '', 'first', '', 'duplicate', '', 'second', '', '□']
    assert remove_owned_paragraphs(lines, 1, [2, 6]) == ['ref', '証明', 'first', '', 'second', '', '□']
    assert lines[2] == 'base' and lines[6] == 'duplicate'
    for invalid in ([0], [1], [10], [2, 2], [3], [2, 5]):
        assert remove_owned_paragraphs(lines, 1, invalid) == lines


def test_installer_preserves_r12r1_and_scopes_hook():
    source = 'import os\n\ndef render_model_backed_narrative_markdown(result, model):\n    if True:\n' + ANCHOR + '    return lines\n'
    revised = proposed_source(source)
    assert revised == source.replace(ANCHOR, HOOK)
    assert revised.count(ANCHOR) == 1
    ast.parse(revised)
    with pytest.raises(RuntimeError):
        proposed_source(revised)


def test_actual_typed_branch_and_guards():
    from dataclasses import replace
    from expression import Composition, GeneratorSymbol, HomotopyElement, Zero
    from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
    from phase165_r14_r6_generic_iso import GeneratorImage
    from phase165_r52_partial_proof import ProofSearchStatus
    from phase168_r3_3_proof_narrative_model import NarrativeCitation, ProofNarrativeModel
    from phase175_r3r9_lemma57_explicit_public.rule import lemma57_explicit_zero_rule
    from phase175_r3r9_lemma57_explicit_public.source import TodaLemma57ExplicitNuPrimeZero, ASSERTION_ID, REFERENCE_ID, PARTICULAR_CLAUSE
    from phase176_r3r10_right_zero_transport_isolated.rule import right_zero_transport_rule
    from phase178_r12r1_suspension_composition_display.projection import project_zero_suspension_composition
    from phase168_r3_27_typed_statement_projection import typed_sentence
    from proof import ProofRule, ProofStep, LiteratureReference, find_inference_matches_for_rule, apply_inference_match
    from toda_human_readable_renderer import render_toda_public_group_generator_latex

    from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
    prior = exact_prior_database_result(2, 4)
    assert prior is not None
    a, b = prior.rhs.generator.left, prior.rhs.generator.right
    c = HomotopyElement('η₆', 6, source=7, target=6, generator=GeneratorSymbol('η', 6))
    d = HomotopyElement('η₇', 7, source=8, target=7, generator=GeneratorSymbol('η', 7))
    def image(degree, expression):
        return GeneratorImage(TodaSuspensionMap(TodaPrimaryGroup(degree, 2), TodaPrimaryGroup(degree + 1, 3)), expression, Zero())
    def prove(rule, premise):
        match, = find_inference_matches_for_rule(rule, (premise,))
        return apply_inference_match(match)
    leaf = ProofStep(TodaLemma57ExplicitNuPrimeZero(), (), ProofRule.GIVEN)
    base_value = image(6, Composition(a, b))
    base = prove(lemma57_explicit_zero_rule(base_value), leaf)
    x = image(7, Composition(a, Composition(b, c)))
    y = image(7, Composition(Composition(a, b), c))
    z = image(8, Composition(a, Composition(b, Composition(c, d))))
    first = prove(right_zero_transport_rule(x, base_value), base)
    duplicate = prove(right_zero_transport_rule(y, base_value), base)
    child = prove(right_zero_transport_rule(z, y), duplicate)
    # Synthetic root only assembles the branches for projection testing.
    root = ProofStep('fixture root', (first, child), ProofRule.INFERENCE)
    steps = (leaf, base, first, duplicate, child, root)
    tag = '[R1]より, '
    formula = '$E(' + render_toda_public_group_generator_latex(base_value.source_generator) + ')=0$.'
    model = ProofNarrativeModel(steps, (NarrativeCitation(1, LiteratureReference(label='fixture', locator='Lemma 5.7'), (0,), (ASSERTION_ID,), (REFERENCE_ID,)),), ((1,), (), (), (), (), ()), 5, ProofSearchStatus.COMPLETE)
    old = ['**[R1] Lemma 5.7.**', '$' + PARTICULAR_CLAUSE.replace(r'\circ', '') + '$.', '', '証明', tag + formula, '', tag + typed_sentence(x, first), '', tag + typed_sentence(y, duplicate), '', tag + typed_sentence(z, child), '', '□']
    normalized = project_zero_suspension_composition(old, model)
    out, plan = project_zero_composition_elision(old, normalized, model)
    assert plan['retained_index'] == 2 and plan['duplicate_index'] == 3 and plan['consumer_index'] == 4
    assert plan['base_display_absorbed'] and len(plan['removed_positions']) == 2
    assert out == normalized[:4] + normalized[6:8] + normalized[10:]
    assert model.steps == steps
    assert project_zero_composition_elision(old, normalized, replace(model, status=ProofSearchStatus.PARTIAL)) == (normalized, {})
    for i in (2, 3, 4):
        assert project_zero_composition_elision(old, normalized, model, {i}) == (normalized, {})
    # Without the cited formula, retain the base in the body.
    bad_old, bad_normalized = list(old), list(normalized)
    bad_old[1] = bad_normalized[1] = 'other reference formula'
    out, plan = project_zero_composition_elision(bad_old, bad_normalized, model)
    assert not plan['base_display_absorbed'] and tag + formula in out[4:]
    # Duplicate body ownership cannot be guessed after normalization alone.
    assert project_zero_composition_elision(normalized, normalized, model) == (normalized, {})
    # A second consumer of the duplicate prevents suppression.
    extra = ProofStep('extra', (duplicate,), ProofRule.INFERENCE)
    shared = replace(model, steps=steps + (extra,), step_citation_numbers=model.step_citation_numbers + ((),))
    assert project_zero_composition_elision(old, normalized, shared) == (normalized, {})

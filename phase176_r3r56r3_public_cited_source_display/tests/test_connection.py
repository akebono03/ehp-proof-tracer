"""Exact replacements and real cited source guards."""
from dataclasses import replace

import pytest

from phase175_r3r9_lemma57_explicit_public.source import (
    ASSERTION_ID, REFERENCE_ID, TodaLemma57ExplicitNuPrimeZero,
)
from phase168_r3_3_proof_narrative_model import root_ancestor_step_indices
from phase176_r3r56r1_historical_source_audit.audit import load_tests
from phase176_r3r56_cited_source_display_isolated.projection import source_citation
from phase176_r3r56r3_public_cited_source_display.apply import (
    ROOT, PINS, baseline_source, updated_source,
)


@pytest.fixture(scope='module')
def verified():
    _, model = load_tests().pi73_verified.__wrapped__()
    scope = root_ancestor_step_indices(model.steps, model.root_index)
    index, = [i for i in scope if type(model.steps[i].conclusion) is TodaLemma57ExplicitNuPrimeZero]
    args = (scope, index, TodaLemma57ExplicitNuPrimeZero(), ASSERTION_ID, REFERENCE_ID, 'Lemma 5.7')
    citation = source_citation(model, *args)
    assert citation is not None
    return model, args, citation


def test_exact_and_same_namespace_pair(verified):
    model, args, citation = verified
    for assertions, references in [((ASSERTION_ID,), (REFERENCE_ID,)),
                                   (('shared:21:' + ASSERTION_ID,), ('shared:21:' + REFERENCE_ID,))]:
        good = replace(citation, assertion_ids=assertions, reference_ids=references)
        changed = replace(model, citations=tuple(good if c is citation else c for c in model.citations))
        assert source_citation(changed, *args) is good


def test_cross_namespace_missing_and_ambiguous_pairs_rejected(verified):
    model, args, citation = verified
    for assertions, references in [
        (('shared:21:' + ASSERTION_ID,), ('shared:22:' + REFERENCE_ID,)),
        ((ASSERTION_ID,), ('shared:21:' + REFERENCE_ID,)),
        ((), ('shared:21:' + REFERENCE_ID,)),
        (('shared:21:' + ASSERTION_ID,), ()),
        (('shared:x:' + ASSERTION_ID,), ('shared:x:' + REFERENCE_ID,)),
        (tuple('shared:' + n + ':' + ASSERTION_ID for n in ('21', '22')),
         tuple('shared:' + n + ':' + REFERENCE_ID for n in ('21', '22'))),
    ]:
        bad = replace(citation, assertion_ids=assertions, reference_ids=references)
        changed = replace(model, citations=tuple(bad if c is citation else c for c in model.citations))
        assert source_citation(changed, *args) is None
    assert source_citation(replace(model, citations=model.citations + (replace(citation),)), *args) is None


def test_scope_and_actual_leaf_required(verified):
    model, args, _ = verified
    scope, index, statement, assertion, reference, locator = args
    assert source_citation(model, scope - {index}, index, statement, assertion, reference, locator) is None
    assert source_citation(model, scope, None, statement, assertion, reference, locator) is None
    assert source_citation(model, scope, index, object(), assertion, reference, locator) is None
    numbers = list(model.step_citation_numbers)
    numbers[index] = ()
    assert source_citation(replace(model, step_citation_numbers=tuple(numbers)), *args) is None


def test_two_exact_replacements_are_idempotent():
    # The R56R3 patch is tested against its exact, inverse-verified stage.
    from phase176_r3r57r1_public_composite_hopf_display.apply import (
        LAYOUT, previous_source,
    )
    from phase176_r3r58r1_public_finite_cyclic_lift_display.apply import r57_stage_bytes
    for path in PINS:
        raw = (ROOT / path).read_bytes()
        if path == LAYOUT:
            raw = previous_source(path, r57_stage_bytes(path))
        assert updated_source(path, raw) == raw
        base, _ = baseline_source(path, raw)
        for eol in ('\n', '\r\n'):
            original = base.replace('\n', eol).encode('utf-8')
            changed = updated_source(path, original)
            assert baseline_source(path, changed)[0] == base
            assert updated_source(path, changed) == changed
        with pytest.raises(ValueError):
            updated_source(path, raw + b'\n# unknown edit\n')

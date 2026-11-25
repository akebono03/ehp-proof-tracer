"""Real cited model guards plus exact replacement regression checks."""
from dataclasses import replace

import pytest

from phase175_r3r9_lemma57_explicit_public.source import (
    ASSERTION_ID, REFERENCE_ID, TodaLemma57ExplicitNuPrimeZero,
)
from phase175_r3r11_cited_hopf_narrative.projection import _completed_scope, _source_citation
from phase176_r3r56r1_historical_source_audit.audit import load_tests
from phase176_r3r56r2_namespace_source_fix.apply import TARGET, baseline_source, updated_source
from proof import ProofRule


@pytest.fixture(scope='module')
def verified():
    result, model = load_tests().pi73_verified.__wrapped__()
    scope = _completed_scope(model)
    assert scope is not None
    args = dict(statement_type=TodaLemma57ExplicitNuPrimeZero, assertion_id=ASSERTION_ID,
                reference_id=REFERENCE_ID, locator='Lemma 5.7')
    return model, scope, args


def test_real_source_and_legacy_exact_pair(verified):
    model, scope, args = verified
    found = _source_citation(model, scope, **args)
    assert found is not None
    citation, index = found
    assert model.steps[index].rule is ProofRule.GIVEN
    assert citation.number in model.step_citation_numbers[index]
    direct = replace(citation, assertion_ids=(ASSERTION_ID,), reference_ids=(REFERENCE_ID,))
    changed = replace(model, citations=tuple(direct if c is citation else c for c in model.citations))
    assert _source_citation(changed, scope, **args) == (direct, index)


def test_namespace_pair_rejects_missing_mismatched_and_ambiguous_ids(verified):
    model, scope, args = verified
    citation, _ = _source_citation(model, scope, **args)
    pairs = [
        (('shared:21:' + ASSERTION_ID,), ('shared:22:' + REFERENCE_ID,)),
        (('shared:21:' + ASSERTION_ID,), ()),
        ((), ('shared:21:' + REFERENCE_ID,)),
        ((ASSERTION_ID,), ('shared:21:' + REFERENCE_ID,)),
        (('shared:x:' + ASSERTION_ID,), ('shared:x:' + REFERENCE_ID,)),
        (('shared:21:' + ASSERTION_ID + ':other',), ('shared:21:' + REFERENCE_ID,)),
        (tuple('shared:' + n + ':' + ASSERTION_ID for n in ('21', '22')),
         tuple('shared:' + n + ':' + REFERENCE_ID for n in ('21', '22'))),
    ]
    for assertions, references in pairs:
        bad = replace(citation, assertion_ids=assertions, reference_ids=references)
        changed = replace(model, citations=tuple(bad if c is citation else c for c in model.citations))
        assert _source_citation(changed, scope, **args) is None


def test_actual_source_scope_and_citation_membership_required(verified):
    model, scope, args = verified
    citation, index = _source_citation(model, scope, **args)
    assert _source_citation(model, scope - {index}, **args) is None
    numbers = list(model.step_citation_numbers)
    numbers[index] = ()
    assert _source_citation(replace(model, step_citation_numbers=tuple(numbers)), scope, **args) is None
    assert _source_citation(model, scope, **{**args, 'locator': 'Lemma 5.8'}) is None
    assert _source_citation(model, scope, **{**args, 'statement_type': object}) is None
    assert _source_citation(replace(model, citations=model.citations + (replace(citation),)), scope, **args) is None


def test_patch_is_idempotent_and_rejects_unknown_bytes():
    raw = TARGET.read_bytes()
    assert updated_source(raw) == raw
    base, _ = baseline_source(raw)
    for eol in ('\n', '\r\n'):
        before = base.replace('\n', eol).encode('utf-8')
        after = updated_source(before)
        assert updated_source(after) == after
        assert baseline_source(after)[0] == base
    with pytest.raises(ValueError):
        updated_source(raw + b'\n# unknown edit\n')

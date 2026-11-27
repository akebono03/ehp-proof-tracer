from dataclasses import replace
import re
from unittest.mock import patch

import pytest

from phase178_r26_n7_final_verified_proof_audit.audit import (
    EXPECTED_DISPLAY, validate_display, validate_summary,
)


def complete_summary():
    return dict(n=7, k=6, status='complete', trust_status='VERIFIED', open_goal_count=0,
                target_given_count=0, web_error=None, complete_invariants_hold=True,
                web_key='generic-complete-proof', proven_step_count=18, reference_count=0)


@pytest.mark.parametrize('count', [0, 5])
def test_complete_summary(count):
    validate_summary(dict(complete_summary(), reference_count=count))


@pytest.mark.parametrize('key,value', [('n', 6), ('status', 'partial'), ('trust_status', 'UNKNOWN'),
    ('open_goal_count', 1), ('target_given_count', 1), ('web_error', 'error'),
    ('complete_invariants_hold', False), ('web_key', 'generic-partial-proof'),
    ('proven_step_count', 17), ('reference_count', -1), ('reference_count', None),
    ('reference_count', True)])
def test_summary_rejects_regressions(key, value):
    row = complete_summary()
    row[key] = value
    with pytest.raises(RuntimeError):
        validate_summary(row)


def rendered(tex, suffix):
    return f'WebGroupProofRenderedLineView(statement_latex={tex!r}, suffix={suffix!r})'


def valid_lines():
    return [rendered(r'E: \pi_{12}^{6}\to \pi_{13}^{7}', ' は同型.'),
            rendered(r'E(\nu_{6}^{2})=\nu_{7}^{2}', '.')]


def test_display_accepts_single_composite_and_isomorphism():
    assert validate_display(valid_lines()) == EXPECTED_DISPLAY


@pytest.mark.parametrize('extra', [rendered(r'E(\nu_{6})=\nu_{7}', '.'),
    rendered(r'E(\nu_{9})=\nu_{10}', '.'), *valid_lines()])
def test_display_rejects_redundancy(extra):
    with pytest.raises(RuntimeError, match='N7_RENDERER_CONTRACT_CHANGED'):
        validate_display(valid_lines() + [extra])


@pytest.mark.parametrize('index', [0, 1])
def test_display_rejects_missing_required_line(index):
    lines = valid_lines()
    del lines[index]
    with pytest.raises(RuntimeError, match='N7_RENDERER_CONTRACT_CHANGED'):
        validate_display(lines)


def validate_model_citations(model):
    from phase168_r3_3_proof_narrative_model import root_ancestor_step_indices
    from proof import ProofRule

    scope = root_ancestor_step_indices(model.steps, model.root_index)
    assert len(scope) == len(model.steps) == 18
    givens = {i for i in scope if model.steps[i].rule is ProofRule.GIVEN}
    assert len(givens) == 5
    assert len(model.citations) == 5
    assert len(model.step_citation_numbers) == len(model.steps)
    assert tuple(c.number for c in model.citations) == (1, 2, 3, 4, 5)
    cited_givens = set()
    for citation in model.citations:
        assert citation.reference.locator or citation.reference.label
        indices = set(citation.step_indices)
        assert indices <= scope
        associated = indices & givens
        assert len(associated) == 1 and not (associated & cited_givens)
        cited_givens.update(associated)
        assert all(citation.number in model.step_citation_numbers[i] for i in indices)
        assert indices == {i for i, numbers in enumerate(model.step_citation_numbers)
                           if citation.number in numbers}
    assert cited_givens == givens
    assert all(set(numbers) <= {1, 2, 3, 4, 5}
               for numbers in model.step_citation_numbers)


def test_real_public_model_citations():
    import phase165_r52_r3_web_adapter as adapter
    from phase165_r52_partial_proof import ProofSearchStatus
    from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
    from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
    from web_group_proof import build_standard_web_group_proof_view

    actual = adapter.build_partial_web_group_proof_view
    captured = []

    def capture(result, **kwargs):
        view = actual(result, **kwargs)
        captured.append((result, kwargs.get('narrative_model'), view))
        return view

    with patch.object(adapter, 'build_partial_web_group_proof_view', capture):
        view = build_standard_web_group_proof_view(n=7, k=6, max_depth=2,
            mode='narrative', citation_source='model')
    assert len(captured) == 1
    result, model, rendered_view = captured[0]
    assert result.status is ProofSearchStatus.COMPLETE and not result.open_goals
    assert result.conclusion == exact_prior_database_result(7, 6)
    assert model is not None and model.status is ProofSearchStatus.COMPLETE
    assert model.steps[model.root_index].conclusion == result.conclusion
    assert view.key == rendered_view.key == 'generic-complete-proof'
    validate_model_citations(model)
    markdown = render_model_backed_narrative_markdown(result, model)
    headings = re.findall(r'^\*\*\[R(\d+)\] .+\.\*\*$', markdown, re.MULTILINE)
    assert headings == ['1', '2', '3', '4', '5']
    validate_display([str(line) for line in rendered_view.rendered_lines])
    with pytest.raises(AssertionError):
        validate_model_citations(replace(model, citations=model.citations[:-1]))
    first = replace(model.citations[0], step_indices=())
    with pytest.raises(AssertionError):
        validate_model_citations(replace(model, citations=(first,) + model.citations[1:]))
    print('PHASE178_R26_MODEL_CITATION_COUNT=' + str(len(model.citations)))
    print('PHASE178_R26_GIVEN_CITATION_BINDINGS=VERIFIED')
    print('PHASE178_R26_RENDERED_CITATION_HEADINGS=VERIFIED')

"""Exercise the public proof, exact premises, and guarded display-only elision."""
from dataclasses import replace
from unittest.mock import patch

import pytest

from phase165_r52_partial_proof import ProofSearchStatus
from phase168_r3_27_typed_statement_projection import typed_sentence
from phase168_r3_37c_reference_projection import _verified_source_sentence
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from phase177_r17r6r1_suspension_composition_display.projection import match_composition_branch
from phase178_r15_toda512_isolated.source import canonical_512
from phase178_r17_finite_cyclic_quotient_isolated.rule import RULE_NAME
from phase178_r17r2_cited_512_priority.audit import audit_actual
from phase178_r17r3_common_renderer.projection import (
    cited_512_reference_sentence, composition_display_plan,
    finite_cyclic_quotient_reason, project_composite_suspension_lines,
    project_finite_quotient_order,
)
from proof import ProofRule, ProofStep
from web_group_proof_common import _group_proof_statement_latex


@pytest.fixture(scope='module')
def actual(tmp_path_factory):
    import phase165_r52_r3_web_adapter as adapter
    real = adapter.build_partial_web_group_proof_view
    captures = []
    def capture(result, **kwargs):
        view = real(result, **kwargs)
        captures.append((result, kwargs.get('narrative_model'), view))
        return view
    folder = tmp_path_factory.mktemp('r17r3')
    with patch.object(adapter, 'build_partial_web_group_proof_view', capture):
        report = audit_actual(folder)
    assert len(captures) == 1
    result, model, view = captures[0]
    assert result.status is ProofSearchStatus.COMPLETE and not result.open_goals
    assert view.key == 'generic-complete-proof'
    assert len(result.proven_steps) == len(model.steps) == report['root_ancestor_count'] == 18
    assert report['model_reference_count'] == len(model.citations) == 6
    assert report['legacy_reference_count'] == 0
    q, = [i for i, s in enumerate(model.steps) if s.inference_rule is not None and s.inference_rule.name == RULE_NAME]
    image, = [i for i, s in enumerate(model.steps) if s is model.steps[q].premises[-1]]
    return result, model, q, image


@pytest.mark.parametrize('n', (4, 5, 6))
def test_canonical_512_reference(n):
    claim = canonical_512(n)
    sentence = cited_512_reference_sentence(claim)
    assert sentence == r'$\Delta:\pi_{n+7}^{2n+1}\to\pi_{n+5}^{n}$ は単射 $(n=4,5,6)$.'
    assert _verified_source_sentence(claim) == sentence
    assert cited_512_reference_sentence(replace(claim, n=7)) is None
    assert cited_512_reference_sentence(replace(claim, statement=canonical_512(5 if n == 4 else 4).statement)) is None
    assert cited_512_reference_sentence(replace(claim, locator='(5.13)')) is None


def test_actual_renderer(actual):
    result, model, q, image = actual
    before = (model.steps, model.citations, model.step_citation_numbers)
    reason = finite_cyclic_quotient_reason(model.steps[q].conclusion, model.steps[q])
    assert reason is not None and typed_sentence(model.steps[q].conclusion, model.steps[q]) == reason
    assert r'\ker E=\operatorname{Im}\Delta=\langle 2' in reason
    assert r'\cong \mathbb{Z}/8' in reason
    first, last = reason.split('. ', 1)
    branch, leaves, old = match_composition_branch(model, image)
    refs = sorted({n for i in leaves for n in model.step_citation_numbers[i]})
    step = model.steps[image]
    composite = ', '.join(f'[R{n}]' for n in refs) + 'より, ' + typed_sentence(step.conclusion, step)
    markdown = render_model_backed_narrative_markdown(result, model)
    reference, body = markdown.split('\n証明\n', 1)
    c, = [c for c in model.citations if c.reference.locator == '(5.12)']
    assert cited_512_reference_sentence(canonical_512(4)) in c.statement_bodies
    assert cited_512_reference_sentence(canonical_512(4)) in reference
    lines = body.splitlines()
    assert all(s not in lines for s in old), markdown
    assert lines.count(composite) == 1, markdown
    root, fallback = _group_proof_statement_latex(result.conclusion)
    assert root is not None and fallback is None
    assert body.count('$' + root + '$') == 1
    assert body.index(first + '.') < body.index(last) < body.index(composite) < body.index('$' + root + '$'), markdown
    assert before == (model.steps, model.citations, model.step_citation_numbers)
    print('PHASE178_R17R3_PUBLIC_PROVEN_STEP_COUNT=18')
    print('PHASE178_R17R3_MODEL_REFERENCE_COUNT=6')
    print('PHASE178_R17R3_COMPOSITION_ELISION=VERIFIED')
    print('PHASE178_R17R3_FINITE_QUOTIENT_REASON=VERIFIED')
    print('PHASE178_R17R3_CITED_512_REFERENCE=VERIFIED')
    print(markdown)


def test_quotient_rejects_missing_or_changed_premises(actual):
    _, model, q, _ = actual
    step = model.steps[q]
    for i in range(6):
        assert finite_cyclic_quotient_reason(step.conclusion, replace(step, premises=step.premises[:i] + step.premises[i+1:])) is None
    for i in range(2, 6):
        bad = list(step.premises)
        bad[i] = replace(bad[i], rule=ProofRule.INFERENCE if i == 2 else ProofRule.GIVEN)
        assert finite_cyclic_quotient_reason(step.conclusion, replace(step, premises=tuple(bad))) is None
    assert finite_cyclic_quotient_reason(step.conclusion, replace(step, rule=ProofRule.GIVEN)) is None
    assert finite_cyclic_quotient_reason(step.conclusion, replace(step, premises=tuple(reversed(step.premises)))) is None


def test_guarded_composition_projection(actual):
    result, model, q, image = actual
    branch, leaves, old = match_composition_branch(model, image)
    refs = sorted({n for i in leaves for n in model.step_citation_numbers[i]})
    composite = ', '.join(f'[R{n}]' for n in refs) + 'より, ' + typed_sentence(model.steps[image].conclusion, model.steps[image])
    lines = render_model_backed_narrative_markdown(result, model).splitlines()
    pos = lines.index(composite)
    original = lines[:pos] + [old[0], '', old[1], ''] + lines[pos:]
    assert composition_display_plan(original, model, image) is not None
    assert project_composite_suspension_lines(original, model) == lines
    assert project_composite_suspension_lines(lines, model) == lines
    for i in branch:
        assert composition_display_plan(original, model, image, {i}) is None
    assert project_composite_suspension_lines(original, replace(model, status=ProofSearchStatus.PARTIAL)) == original
    assert project_composite_suspension_lines(original, replace(model, open_goals=(model.steps[q].conclusion,))) == original
    duplicate = original[:pos] + [old[0], ''] + original[pos:]
    assert composition_display_plan(duplicate, model, image) is None
    extra_parent = model.steps[next(iter(branch - leaves - {image}))]
    extra = ProofStep(extra_parent.conclusion, (extra_parent,), ProofRule.INFERENCE)
    shared = replace(model, steps=model.steps + (extra,), step_citation_numbers=model.step_citation_numbers + ((),))
    assert composition_display_plan(original, shared, image) is None
    assert project_finite_quotient_order(lines, model) == lines

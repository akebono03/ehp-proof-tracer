from dataclasses import replace

import pytest

from expression import Composition, HomotopyElement, IteratedSuspension
from phase165_r52_partial_proof import ProofSearchStatus
from phase168_r3_3_proof_narrative_model import (
    NarrativeCitation, ProofNarrativeModel, root_ancestor_step_indices,
)
from phase168_r3_29_order_projection import project_narrative_order
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from phase175_r4r12r10r1_cited_511_public.provider import expand_cited_511
from phase175_r4r12r10r1_cited_511_public.source import CitedToda511, canonical_511
from phase176_r3r55_equality_display_isolated.projection import rendered_math
from phase177_r2_cited_511_reuse_audit.audit import capture
from phase177_r17r4r1_prop25_suspension_elision.tests.test_display import proved
from phase177_r17r5_duplicate_cited_equality.projection import (
    direct_source, omit_duplicate_cited_equality, same_equality,
)
from proof import LiteratureReference, ProofRule, ProofStep, Relation
from relation_rules import equality_symmetry_inference_rule


def model_for(leaf, first, second):
    # An isolated projection fixture. The actual integration test uses the
    # independently verified public tree, not this synthetic root.
    root = ProofStep(first.conclusion, (first, second), ProofRule.INFERENCE)
    return ProofNarrativeModel(
        (leaf, first, second, root),
        (NarrativeCitation(1, LiteratureReference(label='test source', locator='test'), (0, 1, 2)),),
        ((1,), (1,), (1,), ()), 3, ProofSearchStatus.COMPLETE,
    )


def line_for(step, number=1):
    latex = rendered_math(step.conclusion)
    assert latex
    return f'[R{number}]より, ${latex}$.'


@pytest.mark.parametrize('n', [3, 5, 8])
def test_equal_typed_direct_readings(n):
    a = HomotopyElement('a', n, n+1, n)
    b = HomotopyElement('b', n, n+1, n)
    leaf = ProofStep(Relation(b, a), (), ProofRule.GIVEN)
    goal = Relation(a, b)
    first = proved(equality_symmetry_inference_rule(), (leaf,), goal)
    second = proved(equality_symmetry_inference_rule(), (leaf,), goal)
    assert first is not second
    model = model_for(leaf, first, second)
    line = line_for(first)
    seen = {}
    assert not omit_duplicate_cited_equality(model, 1, line, seen)
    assert omit_duplicate_cited_equality(model, 2, line, seen)
    assert seen == {line: [1]}
    assert not omit_duplicate_cited_equality(model, 3, line, seen)
    assert not omit_duplicate_cited_equality(model, 1, line, {})
    assert not omit_duplicate_cited_equality(model, 2, line, seen, {2})
    assert not omit_duplicate_cited_equality(model, 2, line, seen, {1})
    assert not omit_duplicate_cited_equality(replace(model, status=ProofSearchStatus.PARTIAL), 2, line, seen)
    assert not omit_duplicate_cited_equality(replace(model, open_goals=(goal,)), 2, line, seen)
    assert not omit_duplicate_cited_equality(replace(model, step_citation_numbers=((1,), (1,), (2,), ())), 2, line, seen)
    assert not omit_duplicate_cited_equality(model, 2, line.replace('より,', 'を用いて,'), seen)
    assert not same_equality(goal, Relation(b, a))
    assert not same_equality(goal, Relation(a, replace(b, source=n+2)))


def test_registered_notation_direct_readings():
    canonical = canonical_511()
    variant = Relation(canonical.lhs, Composition(IteratedSuspension(canonical.rhs.left.expression, 1), canonical.rhs.right))
    assert canonical != variant and same_equality(canonical, variant)
    source = CitedToda511(canonical)
    leaf = ProofStep(source, (), ProofRule.GIVEN)
    one, = expand_cited_511(canonical, (source,))
    two, = expand_cited_511(variant, (source,))
    first = proved(one.rule, (leaf,), canonical)
    second = proved(two.rule, (leaf,), variant)
    model = model_for(leaf, first, second)
    line = line_for(first)
    assert line_for(second) == line
    seen = {}
    assert not omit_duplicate_cited_equality(model, 1, line, seen)
    assert omit_duplicate_cited_equality(model, 2, line, seen)
    wrong = Relation(canonical.lhs, Composition(canonical.rhs.left, replace(canonical.rhs.right, source=9)))
    assert not same_equality(canonical, wrong)


def test_actual_duplicate_display():
    invocation, result, calls, model, view = capture()
    assert result.status.value == 'complete' and not result.open_goals
    assert view.key == 'generic-complete-proof'
    assert len(result.proven_steps) == len(model.steps) == 43 and len(model.citations) == 8
    scope = root_ancestor_step_indices(model.steps, model.root_index)
    order = tuple(e.step_index for e in project_narrative_order(model) if e.step_index in scope)
    canonical = canonical_511()
    target = '[R4]より, $' + rendered_math(canonical) + '$.'
    seen, hidden, candidates = {}, [], []
    for i in order:
        step = model.steps[i]
        if rendered_math(step.conclusion) != rendered_math(canonical):
            continue
        if direct_source(model, i, target, scope) is None:
            continue
        candidates.append(i)
        if omit_duplicate_cited_equality(model, i, target, seen):
            hidden.append(i)
    assert len(candidates) == 2 and len(hidden) == 1, (candidates, hidden)
    before = (model.steps, model.citations, model.step_citation_numbers)
    markdown = render_model_backed_narrative_markdown(result, model)
    body = markdown.split('\n証明\n', 1)[1]
    assert body.splitlines().count(target) == 1, body
    assert body.index(target) < body.index(r'よって, $\Delta:\pi_{10}^{9}\to \pi_{8}^{4}$ は単射.')
    assert before == (model.steps, model.citations, model.step_citation_numbers)
    assert all(model.steps[i] in result.proven_steps for i in hidden)
    print('PHASE177_R17R5_CANDIDATE_INDICES='+str(candidates))
    print('PHASE177_R17R5_HIDDEN_PROOF_INDICES='+str(hidden))
    print('PHASE177_R17R5_DUPLICATE_COUNT=1')
    print('PHASE177_R17R5_ROOT_STEPS=43')
    print('PHASE177_R17R5_REFERENCE_COUNT=8')

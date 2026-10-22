from phase165_r52_partial_proof import ProofSearchStatus, make_partial_proof_result
from phase168_r3_3_proof_narrative_model import build_proof_narrative_model
from proof import InferenceRule, LiteratureReference, ProofRule, ProofStep
from unified_statement_registry import AssertionEntry, AssertionKind, LiteratureEntry, ProofStepLink, ReferenceKind, UnifiedStatementRegistry


def test_multiple_assertions_share_reference_id():
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry(reference_id='toda:51', kind=ReferenceKind.EQUATION, locator='(5.1)'))
    links = []
    steps = []
    for key in ('a', 'b'):
        registry.add_assertion(AssertionEntry(assertion_id=key, reference_id='toda:51', kind=AssertionKind.STATEMENT, content=key))
        step = ProofStep(conclusion=key, premises=(), rule=ProofRule.GIVEN)
        steps.append(step)
        links.append(ProofStepLink(assertion_id=key, step=step))
    result = make_partial_proof_result(n=2, k=1, status=ProofSearchStatus.COMPLETE, proven_steps=tuple(steps), conclusion='b')
    model = build_proof_narrative_model(result, registry=registry, proof_links=tuple(links))
    assert len(model.citations) == 1
    assert model.citations[0].reference_ids == ('toda:51',)
    assert model.citations[0].assertion_ids == ('a', 'b')
    assert model.citations[0].step_indices == (0, 1)


def test_inference_only_reference_has_no_registry_id():
    step = ProofStep(conclusion='goal', premises=(), rule=ProofRule.INFERENCE,
        inference_rule=InferenceRule(name='transport', literature_reference=LiteratureReference(label='Toda (5.2)', locator='(5.2)')))
    result = make_partial_proof_result(n=2, k=2, status=ProofSearchStatus.COMPLETE, proven_steps=(step,), conclusion='goal')
    model = build_proof_narrative_model(result)
    assert model.citations[0].reference_ids == ()
    assert model.citations[0].reference.locator == '(5.2)'


def test_distinct_registered_sources_remain_distinct():
    registry = UnifiedStatementRegistry()
    steps = []
    links = []
    for key, locator in (('eq', '(5.1)'), ('prop', 'Proposition 5.1')):
        registry.add_reference(LiteratureEntry(reference_id=key, kind=ReferenceKind.PROPOSITION, locator=locator))
        registry.add_assertion(AssertionEntry(assertion_id='a:'+key, reference_id=key, kind=AssertionKind.STATEMENT, content=key))
        step = ProofStep(conclusion=key, premises=(), rule=ProofRule.GIVEN)
        steps.append(step)
        links.append(ProofStepLink(assertion_id='a:'+key, step=step))
    result = make_partial_proof_result(n=2, k=1, status=ProofSearchStatus.COMPLETE, proven_steps=tuple(steps), conclusion='prop')
    model = build_proof_narrative_model(result, registry=registry, proof_links=tuple(links))
    assert [c.reference_ids for c in model.citations] == [('eq',), ('prop',)]


def test_rule_and_registry_matching_locator_do_not_duplicate():
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry(reference_id='registered', kind=ReferenceKind.PROPOSITION, locator='Proposition 5.1'))
    registry.add_assertion(AssertionEntry(assertion_id='a', reference_id='registered', kind=AssertionKind.STATEMENT, content='x'))
    step = ProofStep(conclusion='x', premises=(), rule=ProofRule.GIVEN,
        inference_rule=InferenceRule(name='given', literature_reference=LiteratureReference(label='Toda Proposition 5.1', locator='Proposition 5.1')))
    result = make_partial_proof_result(n=2, k=1, status=ProofSearchStatus.COMPLETE, proven_steps=(step,), conclusion='x')
    model = build_proof_narrative_model(result, registry=registry, proof_links=(ProofStepLink(assertion_id='a', step=step),))
    assert len(model.citations) == 1
    assert model.citations[0].reference_ids == ('registered',)

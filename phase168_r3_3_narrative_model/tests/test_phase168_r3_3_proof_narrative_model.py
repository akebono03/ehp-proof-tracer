from phase165_r52_partial_proof import ProofSearchStatus, make_partial_proof_result
from phase168_r3_3_proof_narrative_model import build_proof_narrative_model
from proof import InferenceRule, LiteratureReference, ProofRule, ProofStep
from unified_statement_registry import (
    AssertionEntry,
    AssertionKind,
    LiteratureEntry,
    ProofStepLink,
    ReferenceKind,
    UnifiedStatementRegistry,
)


def _result(steps, conclusion):
    return make_partial_proof_result(
        n=3, k=1, status=ProofSearchStatus.COMPLETE,
        proven_steps=steps, conclusion=conclusion,
    )


def test_root_inference_rule_reference_is_retained():
    ref = LiteratureReference(label="Toda (5.2)", locator="(5.2)")
    given = ProofStep(conclusion="premise", premises=(), rule=ProofRule.GIVEN)
    root = ProofStep(
        conclusion="derived", premises=(given,), rule=ProofRule.INFERENCE,
        inference_rule=InferenceRule(name="transport", literature_reference=ref),
    )
    model = build_proof_narrative_model(_result((given, root), "derived"))
    assert model.root_index == 1
    assert len(model.citations) == 1
    assert model.citations[0].reference == ref
    assert model.step_citation_numbers == ((), (1,))


def test_used_registered_given_and_root_rule_have_two_citations():
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry(
        reference_id="p51", kind=ReferenceKind.PROPOSITION,
        locator="Proposition 5.1", publication_position=7800,
    ))
    registry.add_assertion(AssertionEntry(
        assertion_id="pi43", reference_id="p51",
        kind=AssertionKind.STATEMENT, content="pi43-group",
    ))
    given = ProofStep(conclusion="pi43-group", premises=(), rule=ProofRule.GIVEN)
    rule_ref = LiteratureReference(label="Toda (5.2)", locator="(5.2)")
    root = ProofStep(
        conclusion="pi42-group", premises=(given,), rule=ProofRule.INFERENCE,
        inference_rule=InferenceRule(name="transport", literature_reference=rule_ref),
    )
    model = build_proof_narrative_model(
        _result((given, root), "pi42-group"), registry=registry,
        proof_links=(ProofStepLink(assertion_id="pi43", step=given),),
    )
    assert [citation.reference.locator for citation in model.citations] == [
        "Proposition 5.1", "(5.2)",
    ]
    assert model.step_citation_numbers == ((1,), (2,))


def test_unmatched_links_are_not_treated_as_proof_evidence():
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry(
        reference_id="p51", kind=ReferenceKind.PROPOSITION,
        locator="Proposition 5.1",
    ))
    registry.add_assertion(AssertionEntry(
        assertion_id="other", reference_id="p51",
        kind=AssertionKind.STATEMENT, content="other",
    ))
    given = ProofStep(conclusion="actual", premises=(), rule=ProofRule.GIVEN)
    model = build_proof_narrative_model(
        _result((given,), "actual"), registry=registry,
        proof_links=(ProofStepLink(
            assertion_id="other",
            step=ProofStep(conclusion="other", premises=(), rule=ProofRule.GIVEN),
        ),),
    )
    assert model.citations == ()
    assert model.step_citation_numbers == ((),)


def test_repeated_rule_reference_is_deduplicated():
    ref = LiteratureReference(label="Toda (5.2)", locator="(5.2)")
    rule = InferenceRule(name="transport", literature_reference=ref)
    first = ProofStep(conclusion="a", premises=(), rule=ProofRule.INFERENCE, inference_rule=rule)
    root = ProofStep(conclusion="b", premises=(first,), rule=ProofRule.INFERENCE, inference_rule=rule)
    model = build_proof_narrative_model(_result((first, root), "b"))
    assert len(model.citations) == 1
    assert model.citations[0].step_indices == (0, 1)
    assert model.step_citation_numbers == ((1,), (1,))

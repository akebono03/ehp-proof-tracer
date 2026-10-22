from phase165_r52_partial_proof import ProofSearchStatus, make_partial_proof_result
from phase168_r3_3_proof_narrative_model import build_proof_narrative_model
from proof import InferenceRule, LiteratureReference, ProofRule, ProofStep
from unified_statement_registry import (
    AssertionEntry, AssertionKind, LiteratureEntry, ProofStepLink,
    ReferenceKind, UnifiedStatementRegistry,
)


def _project(registered_locator: str, rule_locator: str, rule: ProofRule = ProofRule.GIVEN):
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry(
        reference_id="source", kind=ReferenceKind.DEFINITION,
        locator=registered_locator,
    ))
    registry.add_assertion(AssertionEntry(
        assertion_id="fact", reference_id="source",
        kind=AssertionKind.STATEMENT, content="x",
    ))
    step = ProofStep(
        conclusion="x", premises=(), rule=rule,
        inference_rule=InferenceRule(
            name="recorded rule", literature_reference=LiteratureReference(
                label="Toda " + rule_locator, locator=rule_locator,
            ),
        ),
    )
    result = make_partial_proof_result(
        n=3, k=1, status=ProofSearchStatus.COMPLETE,
        proven_steps=(step,), conclusion="x",
    )
    return build_proof_narrative_model(
        result, registry=registry,
        proof_links=(ProofStepLink(assertion_id="fact", step=step),),
    )


def test_descriptive_heading_on_same_given_uses_registered_source():
    model = _project(
        "Chapter V, i) The Groups pi^(n)_(n+1), eta-family notation",
        "Chapter V, i)",
    )
    assert len(model.citations) == 1
    assert model.citations[0].reference.locator == "Chapter V, i) The Groups pi^(n)_(n+1), eta-family notation"
    assert model.citations[0].assertion_ids == ("fact",)
    assert model.step_citation_numbers == ((1,),)


def test_different_locator_same_given_remains_separate():
    model = _project("Proposition 5.1", "(5.1)")
    assert len(model.citations) == 2
    assert model.step_citation_numbers == ((1, 2),)


def test_numbered_subsection_is_not_a_description_alias():
    model = _project("Proposition 5.1 (iii)", "Proposition 5.1")
    assert len(model.citations) == 2


def test_derived_inference_keeps_both_provenances():
    model = _project("Chapter V, i) The Groups pi^(n)_(n+1)", "Chapter V, i)", ProofRule.INFERENCE)
    assert len(model.citations) == 2

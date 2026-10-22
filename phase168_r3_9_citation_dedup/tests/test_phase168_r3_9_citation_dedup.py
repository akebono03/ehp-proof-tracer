from phase165_r52_partial_proof import ProofSearchStatus, make_partial_proof_result
from phase168_r3_3_proof_narrative_model import build_proof_narrative_model
from proof import InferenceRule, LiteratureReference, ProofRule, ProofStep
from unified_statement_registry import (
    AssertionEntry, AssertionKind, LiteratureEntry, ProofStepLink,
    ReferenceKind, UnifiedStatementRegistry,
)


def _make_model(link_locator, rule_locator, second_rule_locator=None):
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry(
        reference_id="ref", kind=ReferenceKind.PROPOSITION,
        locator=link_locator,
    ))
    registry.add_assertion(AssertionEntry(
        assertion_id="assertion", reference_id="ref",
        kind=AssertionKind.STATEMENT, content="fact",
    ))
    given = ProofStep(
        conclusion="fact", premises=(), rule=ProofRule.GIVEN,
        inference_rule=InferenceRule(
            name="documented given", literature_reference=LiteratureReference(
                label="Toda " + rule_locator, locator=rule_locator,
            ),
        ),
    )
    steps = (given,)
    if second_rule_locator is not None:
        root = ProofStep(
            conclusion="result", premises=(given,), rule=ProofRule.INFERENCE,
            inference_rule=InferenceRule(
                name="derived", literature_reference=LiteratureReference(
                    label="Toda " + second_rule_locator,
                    locator=second_rule_locator,
                ),
            ),
        )
        steps = (given, root)
    result = make_partial_proof_result(
        n=3, k=1, status=ProofSearchStatus.COMPLETE,
        proven_steps=steps, conclusion=steps[-1].conclusion,
    )
    return build_proof_narrative_model(
        result, registry=registry,
        proof_links=(ProofStepLink(assertion_id="assertion", step=given),),
    )


def test_same_step_link_and_rule_is_one_citation():
    model = _make_model("Proposition 5.1", "Proposition 5.1")
    assert len(model.citations) == 1
    assert model.citations[0].assertion_ids == ("assertion",)
    assert model.step_citation_numbers == ((1,),)


def test_distinct_source_on_same_step_is_not_removed():
    model = _make_model("Proposition 5.1", "(5.1)")
    assert [c.reference.locator for c in model.citations] == ["Proposition 5.1", "(5.1)"]
    assert model.step_citation_numbers == ((1, 2),)


def test_root_rule_provenance_survives():
    model = _make_model("Proposition 5.1", "Proposition 5.1", "(5.2)")
    assert [c.reference.locator for c in model.citations] == ["Proposition 5.1", "(5.2)"]
    assert model.step_citation_numbers == ((1,), (2,))


def test_same_locator_different_labels_dedupes_across_steps():
    first = ProofStep(conclusion="a", premises=(), rule=ProofRule.GIVEN,
        inference_rule=InferenceRule(name="one", literature_reference=LiteratureReference(label="Toda (5.1)", locator="(5.1)")))
    second = ProofStep(conclusion="b", premises=(first,), rule=ProofRule.INFERENCE,
        inference_rule=InferenceRule(name="two", literature_reference=LiteratureReference(label="(5.1)", locator="(5.1)")))
    result = make_partial_proof_result(n=3, k=1, status=ProofSearchStatus.COMPLETE,
        proven_steps=(first, second), conclusion="b")
    model = build_proof_narrative_model(result)
    assert len(model.citations) == 1
    assert model.citations[0].step_indices == (0, 1)

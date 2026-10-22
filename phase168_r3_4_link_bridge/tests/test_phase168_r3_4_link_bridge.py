import pytest

from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r52_partial_proof import ProofSearchStatus, make_partial_proof_result
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from proof import InferenceRule, LiteratureReference, ProofRule, ProofStep
from unified_statement_registry import (
    AssertionEntry, AssertionKind, LiteratureEntry, ProofStepLink,
    ReferenceKind, UnifiedStatementRegistry,
)


def _fixture():
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry(
        reference_id="prop51", kind=ReferenceKind.PROPOSITION,
        locator="Proposition 5.1", publication_position=7800,
    ))
    registry.add_assertion(AssertionEntry(
        assertion_id="pi43", reference_id="prop51",
        kind=AssertionKind.STATEMENT, content="pi43",
    ))
    given = ProofStep(conclusion="pi43", premises=(), rule=ProofRule.GIVEN)
    root = ProofStep(
        conclusion="pi42", premises=(given,), rule=ProofRule.INFERENCE,
        inference_rule=InferenceRule(
            name="toda52", literature_reference=LiteratureReference(
                label="Toda (5.2)", locator="(5.2)",
            ),
        ),
    )
    unused = ProofStep(conclusion="unused", premises=(), rule=ProofRule.GIVEN)
    bridge = RegistryBridgeResult(
        registry, (), (
            ProofStepLink(assertion_id="pi43", step=given),
            ProofStepLink(assertion_id="pi43", step=unused),
        ),
    )
    result = make_partial_proof_result(
        n=2, k=2, status=ProofSearchStatus.COMPLETE,
        proven_steps=(given, root), conclusion=root.conclusion,
    )
    return result, bridge


def test_only_used_given_and_root_rule_produce_two_references():
    result, bridge = _fixture()
    model = build_linked_proof_narrative_model(result, bridge)
    assert [citation.reference.locator for citation in model.citations] == [
        "Proposition 5.1", "(5.2)",
    ]
    assert model.step_citation_numbers == ((1,), (2,))
    assert model.root_index == 1


def test_adapter_does_not_mutate_search_or_registry():
    result, bridge = _fixture()
    links = bridge.proof_links
    steps = result.proven_steps
    first = build_linked_proof_narrative_model(result, bridge)
    second = build_linked_proof_narrative_model(result, bridge)
    assert first == second
    assert bridge.proof_links is links
    assert result.proven_steps is steps


def test_adapter_rejects_unrelated_bridge_type():
    result, _ = _fixture()
    with pytest.raises(TypeError, match="RegistryBridgeResult"):
        build_linked_proof_narrative_model(result, object())

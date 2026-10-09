import pytest

from unified_statement_registry import (
    AssertionEntry,
    AssertionInstantiation,
    AssertionKind,
    AssertionOrigin,
    LiteratureEntry,
    ProofStepLink,
    ReferenceKind,
    UnifiedStatementRegistry,
)


def test_multiple_assertions_share_one_reference():
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry("toda:5.3", ReferenceKind.EQUATION, "(5.3)"))
    registry.add_assertion(AssertionEntry("5.3:membership", "toda:5.3", AssertionKind.STATEMENT, "ν′ belongs to π₆³", component_position=1))
    registry.add_assertion(AssertionEntry("5.3:hopf", "toda:5.3", AssertionKind.STATEMENT, "H(ν′)=η₅", component_position=2))
    assert len(registry.assertions_for("toda:5.3")) == 2
    assert registry.assertion("5.3:hopf").component_position == 2


def test_definition_and_instantiation_are_distinct():
    definition = AssertionEntry("def:bracket", "toda:def", AssertionKind.DEFINITION, "Toda bracket construction", defined_symbol="{α,β,γ}", scope="composable triples")
    instance = AssertionInstantiation("def:bracket", "specific bracket", (("α", "η₃"),))
    assert definition.defined_symbol == "{α,β,γ}"
    assert instance.assertion_id == definition.assertion_id
    assert definition.content != instance.concrete_content


def test_proof_internal_and_availability_not_conflated():
    internal = AssertionEntry("lemma:internal", "toda:lemma", AssertionKind.STATEMENT, "intermediate", origin=AssertionOrigin.PROOF_INTERNAL, component_position=1)
    assert internal.available_after_position is None
    assert internal.origin is AssertionOrigin.PROOF_INTERNAL


def test_duplicate_ids_and_unknown_references_rejected():
    registry = UnifiedStatementRegistry()
    ref = LiteratureEntry("r", ReferenceKind.LEMMA, "Lemma 5.2")
    registry.add_reference(ref)
    with pytest.raises(ValueError):
        registry.add_reference(ref)
    with pytest.raises(ValueError):
        registry.add_assertion(AssertionEntry("a", "missing", AssertionKind.STATEMENT, 1))
    item = AssertionEntry("a", "r", AssertionKind.STATEMENT, 1)
    registry.add_assertion(item)
    with pytest.raises(ValueError):
        registry.add_assertion(item)


def test_invalid_dependency_and_position_rejected():
    with pytest.raises(ValueError):
        AssertionEntry("a", "r", AssertionKind.STATEMENT, 1, dependencies=("a",))
    with pytest.raises(ValueError):
        LiteratureEntry("r", ReferenceKind.EQUATION, "(5.3)", publication_position=0)


def test_proofstep_link_accepts_repository_key_without_mutation():
    link = ProofStepLink("a", repository_key="existing-entry")
    assert link.repository_key == "existing-entry"
    assert link.step is None

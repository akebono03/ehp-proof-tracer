import pytest

from unified_statement_registry import (
    AssertionEntry,
    AssertionKind,
    AssertionOrigin,
    LiteratureEntry,
    ReferenceKind,
    UnifiedStatementRegistry,
)
from phase163_r3_registry_validation import (
    CitationDecision,
    IdentityDecision,
    assess_citation,
    audit_dependencies,
    compare_assertion_identity,
)


def make_registry(source="toda", cited_available=1, citing_position=2):
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry("ref:a", ReferenceKind.PROPOSITION, "Proposition A", source_id=source, publication_position=1))
    registry.add_reference(LiteratureEntry("ref:b", ReferenceKind.LEMMA, "Lemma B", source_id=source, publication_position=citing_position))
    registry.add_assertion(AssertionEntry("a", "ref:a", AssertionKind.STATEMENT, "known", available_after_position=cited_available))
    registry.add_assertion(AssertionEntry("b", "ref:b", AssertionKind.STATEMENT, "target"))
    return registry


def test_identity_same_id_is_same():
    entry = AssertionEntry("a", "r", AssertionKind.STATEMENT, "X")
    assert compare_assertion_identity(entry, entry) is IdentityDecision.SAME


def test_identity_same_text_different_id_is_not_proven_equal():
    left = AssertionEntry("a", "r", AssertionKind.STATEMENT, "X")
    right = AssertionEntry("b", "r", AssertionKind.STATEMENT, "X")
    assert compare_assertion_identity(left, right) is IdentityDecision.UNKNOWN


def test_identity_structurally_different_content():
    left = AssertionEntry("a", "r", AssertionKind.STATEMENT, "X")
    right = AssertionEntry("b", "r", AssertionKind.STATEMENT, "Y")
    assert compare_assertion_identity(left, right) is IdentityDecision.DIFFERENT


def test_citation_allowed_with_explicit_completion_order():
    registry = make_registry()
    assert assess_citation(registry, "a", "b").decision is CitationDecision.ALLOWED


def test_citation_denied_if_completion_is_too_late():
    registry = make_registry(cited_available=2)
    assert assess_citation(registry, "a", "b").decision is CitationDecision.DENIED


def test_citation_unknown_without_completed_proof_position():
    registry = make_registry(cited_available=None)
    assert assess_citation(registry, "a", "b").decision is CitationDecision.UNKNOWN


def test_self_citation_and_proof_internal_denied():
    registry = make_registry()
    assert assess_citation(registry, "a", "a").decision is CitationDecision.DENIED
    registry.add_assertion(AssertionEntry("internal", "ref:a", AssertionKind.STATEMENT, "intermediate", origin=AssertionOrigin.PROOF_INTERNAL))
    assert assess_citation(registry, "internal", "b").decision is CitationDecision.DENIED


def test_dependency_cycle_detected_and_citation_not_allowed():
    registry = make_registry()
    registry2 = UnifiedStatementRegistry()
    for ref in (registry.reference("ref:a"), registry.reference("ref:b")):
        registry2.add_reference(ref)
    registry2.add_assertion(AssertionEntry("a", "ref:a", AssertionKind.STATEMENT, "known", available_after_position=1, dependencies=("b",)))
    registry2.add_assertion(AssertionEntry("b", "ref:b", AssertionKind.STATEMENT, "target", dependencies=("a",)))
    audit = audit_dependencies(registry2)
    assert audit.cycles == (("a", "b"),)
    assert assess_citation(registry2, "a", "b").decision is CitationDecision.UNKNOWN


def test_missing_dependencies_reported_without_inference():
    registry = make_registry()
    registry.add_assertion(AssertionEntry("c", "ref:a", AssertionKind.STATEMENT, "C", dependencies=("missing",)))
    assert audit_dependencies(registry).missing == (("c", "missing"),)


def test_citation_unknown_across_different_or_unknown_sources():
    registry = make_registry()
    other = UnifiedStatementRegistry()
    other.add_reference(registry.reference("ref:a"))
    other.add_reference(LiteratureEntry("ref:b", ReferenceKind.LEMMA, "Lemma B", source_id="other", publication_position=2))
    other.add_assertion(registry.assertion("a"))
    other.add_assertion(registry.assertion("b"))
    assert assess_citation(other, "a", "b").decision is CitationDecision.UNKNOWN


def test_invalid_input_rejected():
    with pytest.raises(TypeError):
        audit_dependencies(object())

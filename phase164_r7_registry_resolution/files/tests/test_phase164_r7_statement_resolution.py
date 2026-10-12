"""Phase 164 R7: synthetic identities only; no mathematical certification."""
from dataclasses import replace

import pytest

from phase163_r4_registry_bridge import MigrationRecord, MigrationStatus, RegistryBridgeResult
from phase164_r7_statement_resolution import resolve_registered_statement
from proof import ProofRule, ProofStep
from proof_repository import ProofRepository, ProofRepositoryEntry
from unified_statement_registry import (
    AssertionEntry, AssertionKind, AssertionOrigin, LiteratureEntry,
    ProofStepLink, ReferenceKind, UnifiedStatementRegistry,
)


def make_bridge(*, origin=AssertionOrigin.FIXED_STATEMENT, status=MigrationStatus.STRUCTURED):
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry("r", ReferenceKind.PROPOSITION, "Test source", publication_position=1))
    registry.add_reference(LiteratureEntry("goal", ReferenceKind.PROPOSITION, "Test goal", publication_position=2))
    registry.add_assertion(AssertionEntry(
        "a", "r", AssertionKind.STATEMENT, "statement", origin=origin,
        available_after_position=1,
    ))
    registry.add_assertion(AssertionEntry("b", "goal", AssertionKind.STATEMENT, "goal"))
    return RegistryBridgeResult(
        registry, (MigrationRecord("fixture", "a", "a", status, "fixture"),), (),
    )


def test_r7_lookup_keeps_identity_and_source():
    bridge = make_bridge()
    result = resolve_registered_statement(bridge, "a", expected_conclusion="statement")
    assert result.assertion is bridge.registry.assertion("a")
    assert result.reference is bridge.registry.reference("r")
    assert result.proof_link is None


def test_r7_fixed_citation_requires_independent_verification():
    bridge = make_bridge()
    with pytest.raises(ValueError, match="independent_verification_not_recorded"):
        resolve_registered_statement(bridge, "a", citing_assertion_id="b")
    found = resolve_registered_statement(
        bridge, "a", citing_assertion_id="b", verified_assertion_ids=("a",),
    )
    assert found.assertion.assertion_id == "a"


@pytest.mark.parametrize("origin,status", [
    (AssertionOrigin.SOURCE_ARCHIVE, MigrationStatus.STRUCTURED),
    (AssertionOrigin.FIXED_STATEMENT, MigrationStatus.METADATA_ONLY),
    (AssertionOrigin.FIXED_STATEMENT, MigrationStatus.UNRESOLVED_SOURCE),
])
def test_r7_unverified_sources_fail_closed(origin, status):
    with pytest.raises(ValueError):
        resolve_registered_statement(make_bridge(origin=origin, status=status), "a")


def test_r7_rejects_mismatched_statement_and_missing_record():
    bridge = make_bridge()
    with pytest.raises(ValueError, match="registered conclusion mismatch"):
        resolve_registered_statement(bridge, "a", expected_conclusion="different")
    with pytest.raises(ValueError, match="migration record missing"):
        resolve_registered_statement(replace(bridge, records=()), "a")


def test_r7_internal_repository_resolution_keeps_exact_step():
    bridge = make_bridge(origin=AssertionOrigin.PROOF_INTERNAL)
    step = ProofStep(conclusion="statement", rule=ProofRule.GIVEN)
    repository = ProofRepository()
    repository.register(ProofRepositoryEntry("entry", step))
    link = ProofStepLink("a", repository_key="entry", step=step)
    bridge = replace(bridge, proof_links=(link,))
    result = resolve_registered_statement(bridge, "a", proof_repository=repository)
    assert result.proof_link.step is step
    with pytest.raises(ValueError, match="proof_internal_not_external_reference"):
        resolve_registered_statement(
            bridge, "a", proof_repository=repository,
            citing_assertion_id="b", verified_assertion_ids=("a",),
        )


def test_r7_rejects_ambiguous_or_inconsistent_links():
    bridge = make_bridge(origin=AssertionOrigin.PROOF_INTERNAL)
    step = ProofStep(conclusion="statement", rule=ProofRule.GIVEN)
    bad = ProofStep(conclusion="different", rule=ProofRule.GIVEN)
    link = ProofStepLink("a", repository_key="entry", step=step)
    with pytest.raises(ValueError, match="ambiguous ProofStepLink"):
        resolve_registered_statement(replace(bridge, proof_links=(link, link)), "a")
    repository = ProofRepository()
    repository.register(ProofRepositoryEntry("entry", bad))
    with pytest.raises(ValueError, match="identity mismatch"):
        resolve_registered_statement(
            replace(bridge, proof_links=(link,)), "a", proof_repository=repository,
        )

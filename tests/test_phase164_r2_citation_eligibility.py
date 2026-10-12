from dataclasses import replace

import pytest

from phase163_r4_registry_bridge import (
    MigrationRecord,
    MigrationStatus,
    RegistryBridgeResult,
)
from phase164_r2_citation_eligibility import (
    EligibilityStatus,
    assess_phase164_r2_citation,
)
from unified_statement_registry import (
    AssertionEntry,
    AssertionKind,
    AssertionOrigin,
    LiteratureEntry,
    ReferenceKind,
    UnifiedStatementRegistry,
)


def make_bridge(*, origin=AssertionOrigin.FIXED_STATEMENT,
                migration=MigrationStatus.STRUCTURED,
                cited_available=1, citing_position=2, verified=True,
                dependencies=()):
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry(
        "ref:source", ReferenceKind.EQUATION, "(5.2)",
        source_id="Toda", publication_position=1,
    ))
    registry.add_reference(LiteratureEntry(
        "ref:target", ReferenceKind.PROPOSITION, "Proposition target",
        source_id="Toda", publication_position=citing_position,
    ))
    registry.add_assertion(AssertionEntry(
        "source", "ref:source", AssertionKind.STATEMENT, "typed mathematical claim",
        origin=origin, available_after_position=cited_available,
        dependencies=dependencies,
    ))
    registry.add_assertion(AssertionEntry(
        "target", "ref:target", AssertionKind.STATEMENT, "goal",
    ))
    records = (
        MigrationRecord("theorem_fact", "source", "source", migration, "fixture"),
    )
    bridge = RegistryBridgeResult(registry, records, ())
    approved = ("source",) if verified else ()
    return bridge, approved


def test_reviewed_structured_earlier_statement_is_allowed():
    bridge, approved = make_bridge()
    result = assess_phase164_r2_citation(
        bridge, "source", "target", verified_assertion_ids=approved,
    )
    assert result.status is EligibilityStatus.ALLOWED
    assert result.usable


def test_registration_is_not_verification():
    bridge, _ = make_bridge()
    result = assess_phase164_r2_citation(bridge, "source", "target")
    assert result.status is EligibilityStatus.UNKNOWN
    assert result.reason == "independent_verification_not_recorded"
    assert not result.usable


@pytest.mark.parametrize("origin,reason", [
    (AssertionOrigin.SOURCE_ARCHIVE, "source_archive_not_verified"),
    (AssertionOrigin.PROOF_INTERNAL, "proof_internal_not_external_reference"),
])
def test_non_external_origins_denied_even_when_allowlisted(origin, reason):
    bridge, approved = make_bridge(origin=origin)
    result = assess_phase164_r2_citation(
        bridge, "source", "target", verified_assertion_ids=approved,
    )
    assert result.status is EligibilityStatus.DENIED
    assert result.reason == reason


def test_boundary_metadata_denied_even_when_allowlisted():
    bridge, approved = make_bridge(migration=MigrationStatus.METADATA_ONLY)
    result = assess_phase164_r2_citation(
        bridge, "source", "target", verified_assertion_ids=approved,
    )
    assert result.status is EligibilityStatus.DENIED
    assert result.reason == "metadata_only"


def test_self_citation_denied():
    bridge, approved = make_bridge()
    result = assess_phase164_r2_citation(
        bridge, "source", "source", verified_assertion_ids=approved,
    )
    assert result.status is EligibilityStatus.DENIED


def test_later_or_simultaneous_completion_denied():
    bridge, approved = make_bridge(cited_available=2)
    result = assess_phase164_r2_citation(
        bridge, "source", "target", verified_assertion_ids=approved,
    )
    assert result.status is EligibilityStatus.DENIED
    assert result.reason == "not_available_before_citing_entry"


def test_unknown_order_fails_closed():
    bridge, approved = make_bridge(cited_available=None)
    result = assess_phase164_r2_citation(
        bridge, "source", "target", verified_assertion_ids=approved,
    )
    assert result.status is EligibilityStatus.UNKNOWN
    assert not result.usable


def test_missing_migration_record_fails_closed():
    bridge, approved = make_bridge()
    bridge = replace(bridge, records=())
    result = assess_phase164_r2_citation(
        bridge, "source", "target", verified_assertion_ids=approved,
    )
    assert result.status is EligibilityStatus.UNKNOWN


def test_unresolved_record_fails_closed():
    bridge, approved = make_bridge(migration=MigrationStatus.UNRESOLVED_SOURCE)
    result = assess_phase164_r2_citation(
        bridge, "source", "target", verified_assertion_ids=approved,
    )
    assert result.status is EligibilityStatus.UNKNOWN


def test_back_reference_dependency_denied():
    bridge, approved = make_bridge(dependencies=("target",))
    result = assess_phase164_r2_citation(
        bridge, "source", "target", verified_assertion_ids=approved,
    )
    assert result.status is EligibilityStatus.DENIED
    assert result.reason == "depends_on_citing_assertion"


def test_missing_dependency_fails_closed():
    bridge, approved = make_bridge(dependencies=("absent",))
    result = assess_phase164_r2_citation(
        bridge, "source", "target", verified_assertion_ids=approved,
    )
    assert result.status is EligibilityStatus.UNKNOWN
    assert result.reason == "dependency_graph_unverified"


def test_unreviewed_dependency_fails_closed():
    bridge, approved = make_bridge(dependencies=("support",))
    bridge.registry.add_assertion(AssertionEntry(
        "support", "ref:source", AssertionKind.STATEMENT, "support",
    ))
    result = assess_phase164_r2_citation(
        bridge, "source", "target", verified_assertion_ids=approved,
    )
    assert result.status is EligibilityStatus.UNKNOWN
    assert result.reason == "dependency_not_verified"


def test_unstructured_dependency_fails_closed_even_when_reviewed():
    bridge, approved = make_bridge(dependencies=("support",))
    bridge.registry.add_assertion(AssertionEntry(
        "support", "ref:source", AssertionKind.STATEMENT, "support",
    ))
    result = assess_phase164_r2_citation(
        bridge, "source", "target",
        verified_assertion_ids=approved + ("support",),
    )
    assert result.status is EligibilityStatus.UNKNOWN
    assert result.reason == "dependency_not_structured"


def test_invalid_parameters_rejected():
    bridge, _ = make_bridge()
    with pytest.raises(TypeError):
        assess_phase164_r2_citation(object(), "source", "target")
    with pytest.raises(TypeError):
        assess_phase164_r2_citation(
            bridge, "source", "target", verified_assertion_ids=["source"],
        )

from phase163_r4_registry_bridge import MigrationRecord, MigrationStatus, RegistryBridgeResult
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from unified_statement_registry import UnifiedStatementRegistry, LiteratureEntry, ReferenceKind, AssertionEntry, AssertionKind


def test_unresolved_migration_record_without_assertion_id_is_retained():
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry("source:ref", ReferenceKind.PROPOSITION, "Proposition source"))
    registry.add_assertion(AssertionEntry("source:assertion", "source:ref", AssertionKind.STATEMENT, "fact"))
    source = RegistryBridgeResult(registry, (
        MigrationRecord("fixture", "missing", None, MigrationStatus.UNRESOLVED_SOURCE, "unresolved"),
        MigrationRecord("fixture", "known", "source:assertion", MigrationStatus.STRUCTURED, "typed"),
    ), ())
    merged = build_shared_typed_bridge(sources=(source,))
    assert merged.records[0].assertion_id is None
    assert merged.records[0].status is MigrationStatus.UNRESOLVED_SOURCE
    assert merged.records[1].assertion_id == "shared:0:source:assertion"
    assert merged.registry.assertion("shared:0:source:assertion").content == "fact"


def test_nullable_migration_records_do_not_become_proof_links():
    registry = UnifiedStatementRegistry()
    source = RegistryBridgeResult(registry, (
        MigrationRecord("fixture", "unresolved", None, MigrationStatus.UNRESOLVED_SOURCE, "no claim"),
    ), ())
    merged = build_shared_typed_bridge(sources=(source,))
    assert merged.proof_links == ()
    assert len(merged.records) == 1
    assert merged.records[0].assertion_id is None

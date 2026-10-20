"""Focused source-ID order binding checks; no complete-proof replay."""
from dataclasses import replace
import pytest
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase166_r3l_reference_order import connect_all_reference_orders
from unified_statement_registry import LiteratureEntry, ReferenceKind, UnifiedStatementRegistry
from phase163_r4_registry_bridge import RegistryBridgeResult


def test_all_typed_references_are_audited():
    bridge=build_shared_typed_bridge()
    _, report=connect_all_reference_orders(bridge)
    assert report.total == len(bridge.registry._references)
    assert report.connected + report.previously_connected + len(report.unresolved) == report.total


def test_known_typed_references_keep_canonical_positions():
    bridge=build_shared_typed_bridge()
    for reference_id, position in (
        ('shared:4:typed_literature:toda:tex:ch4:0006',69),
        ('shared:3:adopted:toda51:diagonal',77),
        ('shared:2:adopted:toda:adopted:prop5.1:finite_dimensional',78),
    ):
        assert bridge.registry.reference(reference_id).publication_position == position


def test_no_locator_only_matching():
    registry=UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry('unknown:r3l:alias',ReferenceKind.EQUATION,'(5.1)'))
    connected,report=connect_all_reference_orders(RegistryBridgeResult(registry,(),()))
    assert connected.registry.reference('unknown:r3l:alias').publication_position is None
    assert report.unresolved == ('unknown:r3l:alias',)


def test_no_proof_or_assertion_modification():
    bridge=build_shared_typed_bridge()
    bound,_=connect_all_reference_orders(bridge)
    assert bound.proof_links is bridge.proof_links
    assert bound.records is bridge.records
    for key in bridge.registry._assertions:
        assert bound.registry.assertion(key) is bridge.registry.assertion(key)


def test_conflicting_position_is_error():
    bridge=build_shared_typed_bridge()
    key='shared:3:adopted:toda51:diagonal'
    bridge.registry._references[key]=replace(bridge.registry.reference(key),publication_position=78)
    with pytest.raises(ValueError,match='conflicting'):
        connect_all_reference_orders(bridge)

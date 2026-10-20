"""Focused R3-C tests; no full-suite or fabricated publication positions."""
from pathlib import Path

from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from unified_statement_registry import (
    AssertionEntry, AssertionKind, LiteratureEntry, ReferenceKind,
    UnifiedStatementRegistry,
)


def _source():
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry('toda:(5.1)', ReferenceKind.EQUATION, '(5.1)', source_id='Toda'))
    registry.add_reference(LiteratureEntry('custom:unknown', ReferenceKind.EQUATION, 'unknown', source_id='Toda'))
    registry.add_assertion(AssertionEntry('a', 'toda:(5.1)', AssertionKind.STATEMENT, 'source'))
    registry.add_assertion(AssertionEntry('b', 'custom:unknown', AssertionKind.STATEMENT, 'other'))
    return RegistryBridgeResult(registry, (), ())


def test_manifest_order_survives_shared_namespacing():
    merged = build_shared_typed_bridge(sources=(_source(),))
    assert merged.registry.reference('shared:0:toda:(5.1)').publication_position == 77


def test_unknown_reference_stays_without_position():
    merged = build_shared_typed_bridge(sources=(_source(),))
    assert merged.registry.reference('shared:0:custom:unknown').publication_position is None


def test_shared_assertions_keep_their_origins_and_contents():
    merged = build_shared_typed_bridge(sources=(_source(),))
    entry = merged.registry.assertion('shared:0:a')
    assert entry.content == 'source'
    assert entry.dependencies == ()
    assert entry.component_position is None


def test_production_search_does_not_use_fake_target_order():
    source = Path(__file__).resolve().parents[2].joinpath('phase165_r52_r9_shared_math.py').read_text(encoding='utf-8-sig')
    assert 'context_id = citing_assertion_id or assertions[0].assertion_id' in source
    assert 'lookup_mode="typed_reference"' in source

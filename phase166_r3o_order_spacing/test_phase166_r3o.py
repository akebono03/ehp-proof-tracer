"""Limited regression tests for Phase 166 R3-O."""
from __future__ import annotations

import json

from phase165_r5_manifest_bridge import DEFAULT_MANIFEST
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase166_r3b_publication_order_binding.phase166_r3b_publication_order_binding import (
    _load_manifest_reference_order,
)


def test_100_spaced_manifest_preserves_108_unique_reference_ranks():
    positions, _, manifest = _load_manifest_reference_order(DEFAULT_MANIFEST)
    assert len(positions) == 108
    assert sorted(set(positions.values())) == list(range(100, 10900, 100))
    assert len(manifest['assertions']) == 117


def test_important_reference_positions():
    positions, _, _ = _load_manifest_reference_order(DEFAULT_MANIFEST)
    assert positions['toda:Proposition 4.2'] == 6800
    assert positions['toda:(4.5)'] == 6900
    assert positions['toda:(5.1)'] == 7700
    assert positions['toda:Proposition 5.1'] == 7800


def test_manifest_component_positions_are_spaced():
    manifest = json.loads(DEFAULT_MANIFEST.read_text(encoding='utf-8-sig'))
    assert all(row['component_position'] is None or row['component_position'] % 100 == 0
               for row in manifest['assertions'])


def test_shared_registry_inherits_spaced_positions_without_losing_sources():
    bridge = build_shared_typed_bridge()
    selected = [(ref.reference_id, ref.publication_position)
                for ref in bridge.registry._references.values()]
    assert ('shared:0:toda:(5.1)', 7700) in selected
    assert ('shared:0:toda:Proposition 5.1', 7800) in selected
    a = bridge.registry.assertion('shared:2:toda:adopted:prop5.1:eta2_hopf_relation')
    b = bridge.registry.assertion('shared:2:toda:adopted:prop5.1:pi3_2_group_relation')
    c = bridge.registry.assertion('shared:2:toda:adopted:prop5.1:pi4_3')
    assert (a.component_position, b.component_position, c.component_position) == (100, 200, 400)


def test_existing_proof_unchanged_by_ranking_change():
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase165_r52_partial_proof import ProofSearchStatus
    result = search_group_from_registered_goal(n=2, k=1)
    assert result.status is ProofSearchStatus.COMPLETE

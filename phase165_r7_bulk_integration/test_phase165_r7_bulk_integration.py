from pathlib import Path
from types import SimpleNamespace

import pytest

from phase163_r4_registry_bridge import build_registry_bridge
from phase165_r7_bulk_integration import build_bulk_integration
from proof import ProofRule, ProofStep


MANIFEST = Path('phase163_r4_r94_output/manifest.json')


def test_full_archive_scanned_without_promoting():
    result = build_bulk_integration(MANIFEST)
    assert result.source_count == 117
    assert len(result.candidate_pairs) + len(result.ambiguous_ids) + len(result.unmatched_ids) == 117
    assert result.eligible_source_ids == ()
    assert result.verified_source_ids == ()
    assert result.rule_expansion_provider_connected is False


def test_repository_roots_remain_internal_and_preserve_identity():
    step = ProofStep('A', (), ProofRule.INFERENCE)
    repo = SimpleNamespace(entries=lambda: (SimpleNamespace(key='sample', step=step),))
    result = build_bulk_integration(MANIFEST, proof_repository=repo)
    assert result.repository_roots == ('repository:sample:conclusion',)
    assert result.bridge.proof_links[0].step is step
    assert result.eligible_source_ids == ()


def test_reject_conflicting_inputs():
    bridge = build_registry_bridge(components_by_reference={}, theorem_facts=SimpleNamespace(entries=()))
    with pytest.raises(ValueError, match='either'):
        build_bulk_integration(MANIFEST, proof_repository=object(), base_bridge=bridge)


def test_corrupted_manifest_fails_closed(tmp_path):
    path = tmp_path / 'manifest.json'
    path.write_text('{"assertions": []}', encoding='utf-8')
    with pytest.raises(ValueError, match='manifest'):
        build_bulk_integration(path)

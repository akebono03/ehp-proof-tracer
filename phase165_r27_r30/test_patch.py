"""Targeted R27-R30 tests (no full regression suite)."""
import importlib.util
from pathlib import Path

import pytest

SPEC = importlib.util.spec_from_file_location('phase165_r27_r30_installer', Path(__file__).with_name('apply.py'))
module = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(module)


def fixture_repo(tmp_path):
    (tmp_path / 'phase163_r4_r12_stable_bases.py').write_text(
        'class StableBaseRegistration: pass\n'
        'def existing_stable_minimal_registration() -> StableBaseRegistration:\n'
        '    from toda_upstream_bootstrap import build_old\n'
        '    return build_old()\n', encoding='utf-8')
    (tmp_path / 'phase163_r4_r13_inventory.py').write_text(
        'class InventoryReport: pass\n'
        'def existing_phase163_r4_r13_inventory() -> InventoryReport:\n'
        '    from toda_upstream_bootstrap import build_old\n'
        '    return build_old()\n', encoding='utf-8')
    (tmp_path / 'toda_upstream_bootstrap.py').write_text('def build_old(): return None\n', encoding='utf-8')
    (tmp_path / 'toda_other_bootstrap.py').write_text('from toda_upstream_bootstrap import build_old\n', encoding='utf-8')
    (tmp_path / 'proof_repository.py').write_text('class ProofRepository: pass\n', encoding='utf-8')
    return tmp_path


def test_bulk_deletes_mutually_referencing_legacy_bootstraps(tmp_path):
    repo = fixture_repo(tmp_path)
    result = module.apply(repo)
    assert sorted(result['deleted']) == ['toda_other_bootstrap.py', 'toda_upstream_bootstrap.py']
    assert not (repo / 'toda_upstream_bootstrap.py').exists()
    assert (repo / 'proof_repository.py').exists()


def test_historical_registry_helpers_replaced_not_registration_module(tmp_path):
    repo = fixture_repo(tmp_path)
    module.apply(repo)
    for filename in module.PATCHES:
        text = (repo / filename).read_text(encoding='utf-8')
        assert 'raise RuntimeError(' in text
        assert 'from toda_upstream_bootstrap import' not in text


def test_external_import_keeps_its_bootstrap(tmp_path):
    repo = fixture_repo(tmp_path)
    (repo / 'live.py').write_text('from toda_other_bootstrap import run\n', encoding='utf-8')
    with pytest.raises(RuntimeError, match='Upstream bootstrap still referenced'):
        module.apply(repo)
    assert (repo / 'toda_upstream_bootstrap.py').exists()
    assert (repo / 'phase163_r4_r13_inventory.py').exists()


def test_explicit_legacy_import_causes_safe_stop(tmp_path):
    repo = fixture_repo(tmp_path)
    (repo / 'live.py').write_text('def run():\n    from toda_upstream_bootstrap import build_old\n', encoding='utf-8')
    with pytest.raises(RuntimeError, match='Upstream bootstrap still referenced'):
        module.apply(repo)
    assert (repo / 'toda_upstream_bootstrap.py').exists()


def test_idempotent_second_run(tmp_path):
    repo = fixture_repo(tmp_path)
    module.apply(repo)
    result = module.apply(repo)
    assert result['deleted'] == []


def test_backup_is_restorable(tmp_path):
    repo = fixture_repo(tmp_path)
    module.apply(repo)
    assert (repo / 'phase165_r27_r30_removed_backup' / 'toda_upstream_bootstrap.py').is_file()
    assert (repo / 'phase165_r27_r30_removed_backup' / 'phase163_r4_r13_inventory.py').is_file()


def test_already_retired_helper_unchanged(tmp_path):
    repo = fixture_repo(tmp_path)
    module.apply(repo)
    assert module.plan(repo)['replacements'] == {}


def test_phase_protects_typed_core_modules():
    assert 'unified_statement_registry.py' in module.PROTECTED
    assert 'phase165_r52_r5_auto_search.py' in module.PROTECTED
    assert 'toda_rules.py' in module.PROTECTED

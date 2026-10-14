import json
from pathlib import Path

from apply import apply, dependency_edges, plan


def test_import_edges():
    assert dependency_edges('import repository_alpha\nfrom repository_beta import x\n') == {'repository_alpha', 'repository_beta'}


def test_literal_dynamic_import():
    assert 'repository_alpha' in dependency_edges('from importlib import import_module\nimport_module("repository_alpha")')


def test_orphan_only(tmp_path: Path):
    (tmp_path / 'main.py').write_text('import repository_active\n')
    (tmp_path / 'repository_active.py').write_text('import repository_nested\n')
    (tmp_path / 'repository_nested.py').write_text('')
    (tmp_path / 'repository_orphan.py').write_text('')
    audit = plan(tmp_path)
    assert audit['orphan_modules'] == ['repository_orphan']
    assert audit['remaining_legacy_modules'] == ['repository_active', 'repository_nested']


def test_apply_preserves_active(tmp_path: Path):
    (tmp_path / 'main.py').write_text('import repository_active\n')
    (tmp_path / 'repository_active.py').write_text('')
    (tmp_path / 'repository_orphan.py').write_text('ORIGINAL = 1\n')
    report = apply(tmp_path)
    assert report['removed_legacy_modules'] == ['repository_orphan']
    assert (tmp_path / 'repository_active.py').exists()
    assert not (tmp_path / 'repository_orphan.py').exists()
    assert (tmp_path / 'phase165_r27_r47_backup/repository_orphan.py').read_text() == 'ORIGINAL = 1\n'


def test_idempotence(tmp_path: Path):
    (tmp_path / 'main.py').write_text('')
    (tmp_path / 'repository_orphan.py').write_text('')
    apply(tmp_path)
    assert apply(tmp_path)['status'] == 'NO_SAFE_CHANGES'


def test_backup_conflict_fails_without_deletion(tmp_path: Path):
    (tmp_path / 'main.py').write_text('')
    (tmp_path / 'repository_orphan.py').write_text('ORIGINAL = 1')
    backup = tmp_path / 'phase165_r27_r47_backup'
    backup.mkdir()
    (backup / 'repository_orphan.py').write_text('DIFFERENT = 2')
    try:
        apply(tmp_path)
    except RuntimeError as error:
        assert 'Backup conflict' in str(error)
    else:
        assert False
    assert (tmp_path / 'repository_orphan.py').exists()


def test_critical_deps_reported(tmp_path: Path):
    (tmp_path / 'toda_calculation.py').write_text('import repository_scope\n')
    (tmp_path / 'repository_scope.py').write_text('')
    assert plan(tmp_path)['critical_migration_pending']['toda_calculation'] == ['repository_scope']

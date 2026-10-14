from pathlib import Path
import pytest
from apply import apply, imports_of, plan


def write(root, **modules):
    for name, body in modules.items():
        (root / (name + '.py')).write_text(body, encoding='utf-8')


def test_imports_in_functions_detected():
    assert 'repository_keep' in imports_of('def f():\n  from repository_keep import x\n')


def test_unused_repository_chain_deleted_together(tmp_path):
    write(tmp_path, main='from repository_keep import go\n', repository_keep='def go(): pass\n', repository_a='from repository_b import run\n', repository_b='def run(): pass\n')
    result = apply(tmp_path)
    assert result['deletable'] == ['repository_a', 'repository_b']
    assert (tmp_path / 'repository_keep.py').exists()
    assert (tmp_path / 'phase165_r27_r31_removed_backup' / 'repository_a.py').exists()


def test_indirect_dependency_is_kept(tmp_path):
    write(tmp_path, main='from repository_a import go\n', repository_a='from repository_b import run\n', repository_b='def run(): pass\n')
    assert plan(tmp_path)['deletable'] == []


def test_core_import_retains_old_module(tmp_path):
    write(tmp_path, phase165_r4_production_connection='from repository_bridge import x\n', repository_bridge='x = 3\n')
    assert plan(tmp_path)['deletable'] == []


def test_rerun_safe(tmp_path):
    write(tmp_path, main='pass\n', repository_dead='pass\n')
    assert apply(tmp_path)['deletable'] == ['repository_dead']
    assert apply(tmp_path)['deletable'] == []


def test_backup_conflict_blocks_deletion(tmp_path):
    write(tmp_path, main='pass\n', repository_dead='pass\n')
    (tmp_path / 'phase165_r27_r31_removed_backup').mkdir()
    (tmp_path / 'phase165_r27_r31_removed_backup' / 'repository_dead.py').write_text('different')
    with pytest.raises(RuntimeError, match='Backup conflict'):
        apply(tmp_path)
    assert (tmp_path / 'repository_dead.py').exists()

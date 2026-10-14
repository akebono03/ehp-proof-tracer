import ast
from pathlib import Path
from apply import apply, plan, prune_unused_legacy_imports


def test_prunes_only_unused_legacy_imports():
    source = 'from repository_a import foo, bar\nfrom os import path\nprint(foo)\n'
    out, removed = prune_unused_legacy_imports(source)
    assert 'from repository_a import foo\n' in out
    assert 'bar' not in out
    assert 'from os import path' in out
    assert removed == ('repository_a.bar',)


def test_retains_used_legacy_imports_inside_functions():
    source = 'from repository_a import foo\ndef invoke():\n    return foo()\n'
    out, removed = prune_unused_legacy_imports(source)
    assert out == source
    assert not removed


def test_prunes_multiline_unused_imports():
    source = 'from repository_old import (\n  missing,\n  unused,\n)\nanswer = 1\n'
    out, removed = prune_unused_legacy_imports(source)
    assert 'repository_old' not in out
    assert len(removed) == 2
    ast.parse(out)


def test_batch_deletes_unreachable_scc(tmp_path):
    (tmp_path / 'main.py').write_text('x = 1\n')
    (tmp_path / 'repository_a.py').write_text('from repository_b import foo\n')
    (tmp_path / 'repository_b.py').write_text('from repository_a import bar\n')
    assert plan(tmp_path)['deletable'] == ['repository_a', 'repository_b']
    result = apply(root=tmp_path)
    assert result['deletable'] == ['repository_a', 'repository_b']
    assert not (tmp_path / 'repository_a.py').exists()
    assert (tmp_path / 'phase165_r27_r32_backup/repository_a.py').exists()


def test_reachable_old_dependencies_kept(tmp_path):
    (tmp_path / 'main.py').write_text('from repository_a import foo\nprint(foo)\n')
    (tmp_path / 'repository_a.py').write_text('from repository_b import bar\nfoo = bar\n')
    (tmp_path / 'repository_b.py').write_text('bar = 2\n')
    result = apply(root=tmp_path)
    assert result['deletable'] == []
    assert (tmp_path / 'repository_b.py').exists()


def test_repeated_run_is_safe(tmp_path):
    (tmp_path / 'main.py').write_text('from repository_unused import foo\nx = 1\n')
    (tmp_path / 'repository_unused.py').write_text('foo = 3\n')
    first = apply(root=tmp_path)
    second = apply(root=tmp_path)
    assert first['deletable'] == ['repository_unused']
    assert second['status'] == 'NO_SAFE_CHANGES'


def test_conflicting_backup_blocks_writes(tmp_path):
    (tmp_path / 'main.py').write_text('from repository_unused import foo\nx = 1\n')
    (tmp_path / 'repository_unused.py').write_text('foo = 3\n')
    backup = tmp_path / 'phase165_r27_r32_backup'
    backup.mkdir()
    (backup / 'main.py').write_text('conflict')
    import pytest
    with pytest.raises(RuntimeError, match='Backup conflict'):
        apply(root=tmp_path)
    assert (tmp_path / 'repository_unused.py').exists()
    assert 'from repository_unused import foo' in (tmp_path / 'main.py').read_text()

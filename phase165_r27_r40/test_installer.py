from pathlib import Path
import importlib.util
import pytest

spec = importlib.util.spec_from_file_location('r40_installer', Path(__file__).with_name('apply.py'))
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


def test_remove_orphan_helper():
    src = 'from repository_old import Thing\n\ndef _legacy():\n    return Thing()\n\ndef public():\n    return 7\n'
    out, removed = installer.remove_orphan_helpers(src, ('_legacy',))
    assert removed == ('_legacy',)
    assert 'def public()' in out
    assert '_legacy' not in out
    clean, imports = installer.prune_imports(out)
    assert 'repository_old' not in clean
    assert imports == ('repository_old.Thing',)


def test_protect_referenced_private_helper():
    src = 'def _legacy():\n    return 1\n\ndef public():\n    return _legacy()\n'
    with pytest.raises(RuntimeError, match='referenced'):
        installer.remove_orphan_helpers(src, ('_legacy',))


def test_signature_guard():
    with pytest.raises(RuntimeError, match='signatures'):
        installer.remove_orphan_helpers('def public():\n    pass\n', ('_legacy',))


def test_prune_preserves_live_import():
    src = 'from repository_old import Alive, Dead\nresult = Alive()\n'
    out, imports = installer.prune_imports(src)
    assert 'from repository_old import Alive' in out
    assert imports == ('repository_old.Dead',)


def test_reachability_removes_orphan_cycle(tmp_path):
    (tmp_path / 'main.py').write_text('import repository_active\n', encoding='utf-8')
    (tmp_path / 'repository_active.py').write_text('VALUE = 1\n', encoding='utf-8')
    (tmp_path / 'repository_unused_a.py').write_text('import repository_unused_b\n', encoding='utf-8')
    (tmp_path / 'repository_unused_b.py').write_text('import repository_unused_a\n', encoding='utf-8')
    report = installer.plan(tmp_path, {})
    assert report['deletable'] == ['repository_unused_a', 'repository_unused_b']
    assert report['retained_repository_modules'] == ['repository_active']


def test_protect_imports_after_helper_removed():
    src = 'from repository_old import Legacy, Alive\n\ndef _private():\n    return Legacy()\n\ndef public():\n    return Alive()\n'
    out, _ = installer.remove_orphan_helpers(src, ('_private',))
    clean, unused = installer.prune_imports(out)
    assert 'Alive' in clean
    assert 'Legacy' not in clean
    assert unused == ('repository_old.Legacy',)

import importlib.util
import json
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / 'retire_tests.py'
SPEC = importlib.util.spec_from_file_location('phase165_r6_8_4_retire', SCRIPT)
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)

def make_fixture(tmp_path):
    (tmp_path / 'tests').mkdir()
    folder = tmp_path / 'phase165_r6_audit_results' / 'collection_close'
    folder.mkdir(parents=True)
    names = [f'tests/test_legacy_{i:03}.py' for i in range(105)]
    (folder / 'r6_8_dependency_chains.json').write_text(json.dumps({'test_dependencies':[{'test_path':p} for p in names]}))
    for name in names:
        (tmp_path / name).write_text('def test_obsolete():\n    assert True\n')
    for p in module.ROOTS:
        (tmp_path / p).write_text('value = 1\n')
    return names

def test_archives_exact_cohort(tmp_path):
    paths = make_fixture(tmp_path)
    result = module.execute(tmp_path, True)
    assert result['archived'] == 105
    assert result['action'] == 'archived_legacy_cohort'
    assert all(not (tmp_path / p).exists() for p in paths)
    from zipfile import ZipFile
    with ZipFile(result['backup']) as archive:
        assert set(archive.namelist()) == set(paths)

def test_refuses_production_reachable_test(tmp_path):
    paths = make_fixture(tmp_path)
    (tmp_path / 'web_app.py').write_text('import tests.test_legacy_000\n')
    result = module.execute(tmp_path, True)
    assert result['action'] == 'blocked_production_dependency'
    assert all((tmp_path / p).exists() for p in paths)

def test_rejects_unexpected_baseline(tmp_path):
    make_fixture(tmp_path)
    path = tmp_path / module.BASELINE
    path.write_text(json.dumps({'test_dependencies':[{'test_path':'tests/test_other.py'}]}))
    import pytest
    with pytest.raises(RuntimeError, match='Unexpected baseline size'):
        module.execute(tmp_path, True)

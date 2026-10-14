import json
from pathlib import Path
from apply import imports_of, references_of, plan, apply


def test_ast_imports_and_local_imports():
    assert imports_of('from repository_proof_scope import f\ndef f():\n from toda_calculation import g\n') == {'repository_proof_scope', 'toda_calculation'}


def test_literal_dynamic_import_is_detected():
    assert 'repository_proof_scope' in references_of('from importlib import import_module\nimport_module("repository_proof_scope")')


def test_no_false_danger_from_string():
    assert not references_of('value = "repository_proof_scope"')


def test_production_blocker_detected(tmp_path):
    (tmp_path / 'repository_proof_scope.py').write_text('x=1')
    (tmp_path / 'toda_calculation.py').write_text('from repository_proof_scope import x')
    (tmp_path / 'toda_typed_group_facade.py').write_text('x=1')
    (tmp_path / 'phase165_r52_r5_auto_search.py').write_text('x=2')
    r = plan(tmp_path)
    assert r['status'] == 'RETIREMENT_BLOCKED'
    assert r['deleted_files'] == []
    assert 'toda_calculation.py' in r['production_legacy_importers']


def test_test_import_reported_separately(tmp_path):
    (tmp_path / 'repository_proof_scope.py').write_text('x=1')
    (tmp_path / 'toda_typed_group_facade.py').write_text('x=1')
    (tmp_path / 'phase165_r52_r5_auto_search.py').write_text('x=2')
    (tmp_path / 'tests').mkdir()
    (tmp_path / 'tests' / 'test_old.py').write_text('import repository_proof_scope')
    result = plan(tmp_path)
    assert result['deletion_ready_by_static_imports'] is True
    assert 'tests/test_old.py' in result['test_legacy_importers']


def test_missing_typed_entry_is_blocker(tmp_path):
    (tmp_path / 'repository_proof_scope.py').write_text('x=1')
    assert plan(tmp_path)['deletion_ready_by_static_imports'] is False


def test_audit_does_not_modify_modules(tmp_path):
    p = tmp_path / 'repository_proof_scope.py'
    p.write_text('x=1')
    first = apply(tmp_path)
    second = apply(tmp_path)
    assert first == second
    assert p.read_text() == 'x=1'
    assert json.loads((tmp_path/'phase165_r27_r57_audit.json').read_text()) == first

import importlib.util
from pathlib import Path

import pytest

SPEC = importlib.util.spec_from_file_location('r59_installer', Path(__file__).with_name('apply.py'))
r59 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(r59)

FAC = '''from toda_typed_group_facade import build_standard_toda_partial_result\n\ndef build_toda_report(repository, n, k):\n    return object()\n\ndef build_standard_toda_report(n, k):\n    return object()\n\ndef build_standard_toda_partial_result(n, k):\n    return build_standard_toda_partial_result(n, k)\n'''


def fixture_root(tmp_path):
    (tmp_path/'toda_calculation_facade.py').write_text(FAC)
    (tmp_path/'toda_typed_group_facade.py').write_text('def build_standard_toda_partial_result(n,k): return None\n')
    (tmp_path/'phase165_r52_r5_auto_search.py').write_text('def search_group_structure_automatically(): return None\n')
    (tmp_path/'toda_calculation.py').write_text('VALUE=1\n')
    return tmp_path


def test_api_removed():
    result = r59.remove_legacy_facade_api(FAC)
    assert 'def build_toda_report' not in result
    assert 'def build_standard_toda_report' not in result
    assert 'def build_standard_toda_partial_result' in result


def test_gate_blocks_protected_caller(tmp_path):
    root = fixture_root(tmp_path)
    (root/'cli.py').write_text('from toda_calculation import build_toda_calculation_result\n')
    assert r59.apply(root)['status'] == 'BLOCKED'
    assert (root/'toda_calculation.py').exists()


def test_gate_blocks_historical_script(tmp_path):
    root = fixture_root(tmp_path)
    (root/'audit_legacy.py').write_text('from toda_calculation import build_toda_calculation_result\n')
    assert r59.apply(root)['status'] == 'CHANGED'
    assert not (root/'audit_legacy.py').exists()


def test_retire_with_backup_and_tests(tmp_path):
    root = fixture_root(tmp_path)
    (root/'tests').mkdir()
    oldtest = root/'tests'/'test_old.py'
    oldtest.write_text('from toda_calculation import build_toda_calculation_result\n')
    result = r59.apply(root)
    assert result['status'] == 'CHANGED'
    assert not oldtest.exists()
    assert not (root/'toda_calculation.py').exists()
    assert (root/'phase165_r27_r59_r1_retirement_backup.zip').exists()
    assert result['archived_tests'] == ['tests/test_old.py']
    assert r59.apply(root)['status'] == 'ALREADY_RETIRED'


def test_no_fallback_to_old_api(tmp_path):
    root = fixture_root(tmp_path)
    (root/'toda_typed_group_facade.py').write_text('from toda_calculation_facade import build_toda_report\n')
    assert r59.plan(root)['status'] == 'BLOCKED'


def test_half_deleted_api_refused():
    with pytest.raises(RuntimeError):
        r59.remove_legacy_facade_api(FAC.replace('def build_toda_report', 'def previously_deleted'))


def test_retirement_blocks_imported_audit(tmp_path):
    root = fixture_root(tmp_path)
    (root/'audit_legacy.py').write_text('from toda_calculation import build_toda_calculation_result\n')
    (root/'active_feature.py').write_text('import audit_legacy\n')
    result = r59.apply(root)
    assert result['status'] == 'BLOCKED'
    assert (root/'audit_legacy.py').exists()


def test_transitive_test_archive(tmp_path):
    root = fixture_root(tmp_path)
    tests = root/'tests'
    tests.mkdir()
    (tests/'test_old.py').write_text('from toda_calculation import build_toda_calculation_result\n')
    (tests/'test_dependent.py').write_text('from test_old import helper\n')
    result = r59.apply(root)
    assert result['status'] == 'CHANGED'
    assert len(result['archived_tests']) == 2

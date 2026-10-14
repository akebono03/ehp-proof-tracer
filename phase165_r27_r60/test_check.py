import importlib.util
from pathlib import Path
import pytest

spec = importlib.util.spec_from_file_location('r60_check', Path(__file__).with_name('check.py'))
r60 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r60)


def test_parses_direct_imports():
    assert r60.imported_modules('from toda_calculation import f\nimport repository_proof_scope as ps\n') == {'toda_calculation', 'repository_proof_scope'}


def test_static_detects_old_module(tmp_path):
    for name in r60.PUBLIC:
        (tmp_path / name).write_text('def build_standard_toda_partial_result(n,k): return None\nbuild_standard_toda_partial_result\n')
    (tmp_path / 'repository_proof_scope.py').write_text('VALUE = 1\n')
    check = r60.check_static(tmp_path)
    assert not check['conditions']['old_modules_absent']
    assert 'repository_proof_scope' in check['remaining_old_modules']


def test_static_detects_entry_import(tmp_path):
    for name in r60.PUBLIC:
        (tmp_path / name).write_text('def build_standard_toda_partial_result(n,k): return None\nbuild_standard_toda_partial_result\n')
    (tmp_path / 'cli.py').write_text('from toda_calculation import build_toda_calculation_result\nbuild_standard_toda_partial_result\n')
    assert not r60.check_static(tmp_path)['conditions']['public_direct_legacy_imports_absent']


def test_group_targets():
    assert r60.GROUPS == ((2, 1), (3, 1), (3, 2))


def test_timeout_is_fail_closed(tmp_path, monkeypatch):
    def timeout(*args, **kwargs):
        raise r60.subprocess.TimeoutExpired('python', 1)
    monkeypatch.setattr(r60.subprocess, 'run', timeout)
    assert r60.probe(tmp_path,2,1,timeout=1)['execution'] == 'TIMEOUT'


def test_probe_records_errors(tmp_path, monkeypatch):
    class Process:
        returncode = 2
        stdout = ''
        stderr = 'ImportError: missing module'
    monkeypatch.setattr(r60.subprocess, 'run', lambda *args, **kwargs: Process())
    assert r60.probe(tmp_path,2,1)['execution'] == 'ERROR'

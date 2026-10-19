import importlib.util
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1] / 'cleanup.py'
spec = importlib.util.spec_from_file_location('phase165_graph_cleanup', SOURCE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

def test_parse_pytest_error_headers():
    log = '____ ERROR collecting tests/test_phase90_a.py ____\nNo module named repository_inference\n1 error in 0.50s\n'
    assert list(mod.get_errors(log)) == ['tests/test_phase90_a.py']

def test_keep_test_imported_by_modern_test(tmp_path):
    tests = tmp_path / 'tests'
    tests.mkdir()
    (tests/'test_phase80_old.py').write_text('from repository_inference import f\n')
    (tests/'test_phase160_new.py').write_text('from test_phase80_old import f\n')
    log = '____ ERROR collecting tests/test_phase80_old.py ____\nModuleNotFoundError: No module named \'repository_inference\'\n1 error in 0.50s\n'
    p = mod.build_plan(tmp_path, log)
    assert p['remove_count'] == 0

def test_remove_closed_old_group(tmp_path):
    tests = tmp_path/'tests'
    tests.mkdir()
    (tests/'test_phase80_old.py').write_text('from repository_inference import f\n')
    (tests/'test_phase81_old.py').write_text('from test_phase80_old import f\n')
    log = ('____ ERROR collecting tests/test_phase80_old.py ____\nNo module named \'repository_inference\'\n'
           '____ ERROR collecting tests/test_phase81_old.py ____\nNo module named \'repository_inference\'\n2 errors in 0.50s\n')
    p = mod.build_plan(tmp_path, log)
    assert p['remove_count'] == 2

def test_never_delete_modern(tmp_path):
    t = tmp_path/'tests'
    t.mkdir()
    (t/'test_phase159_modern.py').write_text('from repository_inference import f\n')
    log = '____ ERROR collecting tests/test_phase159_modern.py ____\nNo module named \'repository_inference\'\n1 error in 0.50s\n'
    assert mod.build_plan(tmp_path, log)['remove_count'] == 0

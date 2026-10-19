from pathlib import Path
from check import imported_names, scan

def test_import_parser():
    result = imported_names('import probes.probe_phase55_capabilities\nfrom tests.test_phase59_n3_ehp_chain import x\n')
    assert 'probes.probe_phase55_capabilities' in result
    assert 'tests.test_phase59_n3_ehp_chain' in result

def test_scan_flags_deleted_import(tmp_path: Path):
    folder = tmp_path / 'tests'
    folder.mkdir()
    (folder / 'test_old.py').write_text('from probes.probe_phase55_capabilities import old\n', encoding='utf-8')
    result = scan(tmp_path)
    assert result['remaining_test_files'] == 1
    assert result['direct_retired_imports']['test_old.py'] == ['probes.probe_phase55_capabilities']

def test_scan_clean(tmp_path: Path):
    folder = tmp_path / 'tests'
    folder.mkdir()
    (folder / 'test_good.py').write_text('import math\n', encoding='utf-8')
    assert scan(tmp_path)['direct_retired_imports'] == {}

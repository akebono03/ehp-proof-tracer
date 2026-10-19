from pathlib import Path
from apply import dependency_audit, retire


def test_external_import_blocks_retirement(tmp_path: Path):
    target = tmp_path / 'tests' / 'test_phase49_probe.py'
    target.parent.mkdir(parents=True)
    target.write_text('def test_old():\n    assert True\n', encoding='utf-8')
    (tmp_path / 'test_current.py').write_text('from test_phase49_probe import test_old\n', encoding='utf-8')
    result = retire(tmp_path)
    assert result['status'] == 'BLOCKED'
    assert target.exists()
    assert result['external_test_import_blockers']


def test_retirement_backups_and_preserves_probes(tmp_path: Path):
    p = tmp_path / 'tests' / 'test_phase49_probe.py'
    p.parent.mkdir(parents=True)
    p.write_text('def test_old():\n    assert True\n', encoding='utf-8')
    probe = tmp_path / 'probes' / 'probe_phase49_capabilities.py'
    probe.parent.mkdir(parents=True)
    probe.write_text('def print_separator():\n    print("=")\n', encoding='utf-8')
    result = retire(tmp_path)
    assert result['status'] == 'RETIRED_TEST_FILES'
    assert not p.exists()
    assert probe.exists()
    assert (Path(result['backup']) / 'tests' / 'test_phase49_probe.py').exists()
    assert result['probes_retired'] is False

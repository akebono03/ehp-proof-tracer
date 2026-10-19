from pathlib import Path

from phase165_r6_8_3_retire_legacy.retire import check_consumers


def test_guard_finds_external_import(tmp_path: Path):
    (tmp_path / 'probes').mkdir()
    (tmp_path / 'tests').mkdir()
    (tmp_path / 'main.py').write_text('from probes.probe_phase55_capabilities import build_phase55_representative_result\n', encoding='utf-8')
    blockers = check_consumers(tmp_path)
    assert 'probes/probe_phase55_capabilities.py' in blockers
    assert any('main.py:1' in entry for entry in blockers['probes/probe_phase55_capabilities.py'])


def test_guard_allows_isolated_candidates(tmp_path: Path):
    (tmp_path / 'probes').mkdir()
    (tmp_path / 'tests').mkdir()
    (tmp_path / 'main.py').write_text('def unrelated():\n    return 42\n', encoding='utf-8')
    assert check_consumers(tmp_path) == {}

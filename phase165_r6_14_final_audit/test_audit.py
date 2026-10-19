from pathlib import Path
from audit import active_sources, scan


def test_active_sources_excludes_archived_phase_folders(tmp_path: Path):
    (tmp_path / 'tests').mkdir()
    (tmp_path / 'probes').mkdir()
    (tmp_path / 'phase_old').mkdir()
    (tmp_path / 'tests' / 'test_a.py').write_text('x=1\n', encoding='utf-8')
    (tmp_path / 'phase_old' / 'bad.py').write_text('this is invalid (\n', encoding='utf-8')
    assert [p.relative_to(tmp_path).as_posix() for p in active_sources(tmp_path)] == ['tests/test_a.py']


def test_scan_catches_legacy_imports_and_calls(tmp_path: Path):
    (tmp_path / 'tests').mkdir()
    (tmp_path / 'tests' / 'test_a.py').write_text('from probes.probe_phase49_capabilities import build_phase49_representative_result\nbuild_phase49_representative_result()\n', encoding='utf-8')
    result = scan(tmp_path)
    assert {x['kind'] for x in result['legacy_references']} == {'import_from', 'legacy_builder_call'}
    assert all(x['path'] == 'tests/test_a.py' for x in result['legacy_references'])


def test_scan_shared_entry(tmp_path: Path):
    (tmp_path / 'phase165_r55_nk_only_goal.py').write_text('def search_group_from_registered_goal():\n    return None\n', encoding='utf-8')
    (tmp_path / 'phase165_r52_r9_shared_math.py').write_text('', encoding='utf-8')
    (tmp_path / 'probes').mkdir()
    (tmp_path / 'probes' / 'probe_phase58_capabilities.py').write_text('', encoding='utf-8')
    result = scan(tmp_path)
    assert result['shared_entry_function_present'] is True
    assert result['missing_required_modules'] == []

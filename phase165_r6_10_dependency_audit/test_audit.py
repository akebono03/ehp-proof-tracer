from audit import scan


def test_scan_detects_phase49_import_and_retains_current_test(tmp_path):
    (tmp_path / 'tests').mkdir()
    (tmp_path / 'probes').mkdir()
    (tmp_path / 'tests' / 'test_phase49_probe.py').write_text('from probes.probe_phase49_capabilities import build_phase49_representative_result\n', encoding='utf-8')
    (tmp_path / 'tests' / 'test_current.py').write_text('from probes.probe_phase49_capabilities import print_separator\n', encoding='utf-8')
    report = scan(tmp_path)
    assert report['candidate_named_tests'] == ['tests/test_phase49_probe.py']
    assert 'tests/test_current.py' in report['direct_legacy_importers_outside_named_tests']
    assert report['parse_errors'] == []


def test_scan_is_read_only(tmp_path):
    (tmp_path / 'tests').mkdir()
    path = tmp_path / 'tests' / 'test_phase56_probe.py'
    path.write_text('def test_old():\n    assert True\n', encoding='utf-8')
    before = path.read_bytes()
    report = scan(tmp_path)
    assert path.read_bytes() == before
    assert report['candidate_named_tests'] == ['tests/test_phase56_probe.py']

import json
from pathlib import Path

import pytest

from phase165_r6_recollect_parser_fix.repair import extract_summary_error_count, parse_errors, repair_report


def test_parse_underlined_and_bare_headers() -> None:
    log = '_____ ERROR collecting tests/test_a.py ______\n_ ERROR collecting tests/test_b.py _\nERROR collecting tests/test_a.py\n'
    assert parse_errors(log) == ['tests/test_a.py', 'tests/test_b.py']


def test_summary_counter() -> None:
    assert extract_summary_error_count('=== 4223 tests collected, 380 errors in 52.45s ===') == 380
    assert extract_summary_error_count('collection incomplete') is None


def test_repair_report_preserves_original(tmp_path: Path) -> None:
    folder = tmp_path / 'phase165_r6_audit_results' / 'recollection'
    folder.mkdir(parents=True)
    (folder / 'collection.log').write_text('_ ERROR collecting tests/test_a.py _\nERROR collecting tests/test_b.py\n=== 2 errors in 1.4s ===\n')
    (folder / 'report.json').write_text(json.dumps({'exit_code': 1, 'error_file_count': 0, 'scope': ['tests']}))
    result = repair_report(tmp_path)
    actual = json.loads((folder / 'report.json').read_text())
    assert result['error_file_count'] == 2
    assert actual['scope'] == ['tests']
    assert actual['error_files'] == ['tests/test_a.py', 'tests/test_b.py']
    assert json.loads(Path(result['backup']).read_text())['error_file_count'] == 0


def test_mismatched_summary_does_not_modify_report(tmp_path: Path) -> None:
    folder = tmp_path / 'phase165_r6_audit_results' / 'recollection'
    folder.mkdir(parents=True)
    (folder / 'collection.log').write_text('_ ERROR collecting tests/test_a.py _\n=== 2 errors in 1s ===\n')
    report = folder / 'report.json'
    report.write_text('{"exit_code": 1}')
    with pytest.raises(ValueError, match='Header count'):
        repair_report(tmp_path)
    assert report.read_text() == '{"exit_code": 1}'

from pathlib import Path

from audit import analyze_source


def test_calls_distinguished_from_definitions(tmp_path: Path) -> None:
    file = tmp_path / 'sample.py'
    file.write_text('def build_standard_toda_report():\n    return 1\n\nvalue = build_standard_toda_report()\n', encoding='utf-8')
    assert analyze_source(file)['references'] == [
        {'symbol': 'build_standard_toda_report', 'line': 4, 'kind': 'call'}
    ]


def test_import_is_detected(tmp_path: Path) -> None:
    file = tmp_path / 'sample.py'
    file.write_text('from facade import build_standard_toda_report\n', encoding='utf-8')
    assert analyze_source(file)['references'] == [
        {'symbol': 'build_standard_toda_report', 'line': 1, 'kind': 'import'}
    ]

"""Targeted tests for the read-only dependency inventory."""
from pathlib import Path

from audit import FILES, PROTECTED, SYMBOLS, audit


def test_audit_reports_legacy_and_shared_view_symbols(tmp_path):
    for name in FILES:
        (tmp_path / name).write_text('', encoding='utf-8')
    (tmp_path / 'web_group_proof.py').write_text(
        'class WebGroupProofView: pass\n'
        'def build_standard_web_group_proof_view():\n'
        '    return build_standard_toda_report()\n', encoding='utf-8'
    )
    outcome = audit(tmp_path)
    entries = next(x for x in outcome['references'] if x['path'] == 'web_group_proof.py')['references']
    assert {'kind': 'definition', 'line': 1, 'symbol': 'WebGroupProofView'} in entries
    assert any(x['kind'] == 'call' and x['symbol'] == 'build_standard_toda_report' for x in entries)
    assert outcome['deletion_authorized'] is False


def test_audit_does_not_modify_protected_files(tmp_path):
    for name in FILES + PROTECTED:
        (tmp_path / name).write_text('# unchanged\n', encoding='utf-8')
    before = {name: (tmp_path / name).read_bytes() for name in PROTECTED}
    outcome = audit(tmp_path)
    assert outcome['missing_paths'] == []
    assert all((tmp_path / name).read_bytes() == before[name] for name in PROTECTED)
    assert 'build_standard_production_proof_repository' in SYMBOLS

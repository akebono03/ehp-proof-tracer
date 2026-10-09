import csv
import json
from pathlib import Path

from audit import audit


def test_r1f_reports_unresolved_gate(tmp_path: Path) -> None:
    source = tmp_path / 'phase163_r1e_output'
    source.mkdir()
    with (source / 'entry_review.csv').open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=['constructor', 'key_literal'])
        writer.writeheader()
        writer.writerow({'constructor': 'ProofRepositoryEntry', 'key_literal': 'standard.toda.prop56'})
        writer.writerow({'constructor': 'TheoremFactEntry', 'key_literal': ''})
    result = audit(tmp_path)
    assert result['status'] == 'PROVISIONAL_NOT_COMPLETE'
    assert result['explicit_key_sites'] == 1
    assert result['sites_without_explicit_key'] == 1
    assert result['mathematical_statement_total'] is None
    saved = json.loads((tmp_path / 'phase163_r1f_output' / 'summary.json').read_text(encoding='utf-8'))
    assert saved['unresolved_gate_count'] == 6


def test_r1f_rejects_missing_evidence(tmp_path: Path) -> None:
    try:
        audit(tmp_path)
    except FileNotFoundError as error:
        assert 'entry_review.csv' in str(error)
    else:
        raise AssertionError('Missing R1E evidence must be rejected')

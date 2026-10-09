from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from audit import collect, report


def test_collect_detects_registration_sites_without_execution(tmp_path):
    source = tmp_path / 'repo.py'
    source.write_text("from somewhere import ProofRepositoryEntry\nentry = ProofRepositoryEntry(key='a', theorem='T')\nrepo.register(entry)\n", encoding='utf-8')
    records, errors, definitions = collect(tmp_path)
    assert not errors
    assert not definitions
    assert [r['kind'] for r in records] == ['entry_constructor', 'registration_call']
    assert records[0]['key_literal'] == 'a'


def test_duplicate_literal_keys_are_candidates_not_statement_counts(tmp_path):
    source = tmp_path / 'repo.py'
    source.write_text("a = ProofRepositoryEntry(key='same')\nb = ProofRepositoryEntry(key='same')\n",encoding='utf-8')
    summary = report(tmp_path, tmp_path/'reports')
    assert summary['duplicate_literal_key_candidates'] == 1
    assert summary['literal_entry_keys'] == 1
    assert (tmp_path/'reports'/'duplicate_key_candidates.csv').exists()

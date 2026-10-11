from pathlib import Path
import pytest

from phase163_r4_r17_statement_registration.register import register, run


@pytest.fixture
def source() -> Path:
    return Path(__file__).resolve().parents[1] / 'Toda_01.tex'


def test_named_statement_order(source):
    entries = register(source)['entries']
    assert len(entries) == 9
    assert [e['locator'] for e in entries] == ['Lemma 1.1'] + [f'Proposition 1.{i}' for i in range(2, 10)]


def test_immutable_identity_and_independent_order(source):
    entries = register(source)['entries']
    assert [e['statement_id'] for e in entries] == [f'TODA-S{i:06d}' for i in range(1, 10)]
    assert [e['order_key'] for e in entries] == [str(i) for i in range(1, 10)]


def test_named_claim_body_is_not_proof(source):
    entries = register(source)['entries']
    assert 'double coset' in entries[0]['source_statement_tex']
    assert '\\begin{enumerate}' in entries[1]['source_statement_tex']
    assert len(entries[1]['internal_clause_markers']) == 5


def test_unverified_statements_never_search_enabled(source):
    entries = register(source)['entries']
    assert all(e['source_status'] == 'unchecked' and e['search_status'] == 'unconnected' for e in entries)
    assert all(e['legacy_identity_status'] == 'unverified' for e in entries)


def test_output_and_source_change_gate(source, tmp_path):
    assert run(source, tmp_path)['named_statements_registered'] == 9
    assert (tmp_path / 'named_statements.json').exists()
    altered = tmp_path / 'modified.tex'
    altered.write_text(source.read_text(encoding='utf-8').replace('prop:1-9', 'prop:1-10'), encoding='utf-8')
    with pytest.raises(ValueError, match='manual re-review'):
        register(altered)

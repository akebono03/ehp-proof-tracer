from pathlib import Path
from fractions import Fraction

import pytest

from phase163_r4_r18_prose_registry.integrate import CURATED, integrate, run

SOURCE = Path(__file__).resolve().parents[1] / 'Toda_01.tex'


def test_preserves_named_identity_and_order():
    entries = integrate(SOURCE)['entries']
    named = [e for e in entries if e['entry_scope'] == 'named_statement']
    assert [e['statement_id'] for e in named] == [f'TODA-S{i:06d}' for i in range(1, 10)]
    assert [e['order_key'] for e in named] == [str(i) for i in range(1, 10)]


def test_curated_items_have_unique_ids_and_positions():
    entries = integrate(SOURCE)['entries']
    assert len(entries) == 9 + len(CURATED)
    assert len({e['statement_id'] for e in entries}) == len(entries)
    positions = [Fraction(e['order_key']) for e in entries]
    assert positions == sorted(set(positions))


def test_secondary_composition_precedes_lemma():
    entries = integrate(SOURCE)['entries']
    definition = next(e for e in entries if 'secondary composition（' in e.get('summary_ja', ''))
    lemma = next(e for e in entries if e['locator'] == 'Lemma 1.1')
    assert Fraction(definition['order_key']) < Fraction(lemma['order_key'])


def test_no_proof_search_or_printed_verification():
    entries = integrate(SOURCE)['entries']
    assert all(e['search_status'] == 'unconnected' for e in entries)
    assert all(e['source_status'] == 'unchecked' for e in entries)
    assert all(e['legacy_identity_status'] == 'unverified' for e in entries)


def test_anchor_change_requires_manual_review(tmp_path):
    altered = tmp_path / 'changed.tex'
    altered.write_text(SOURCE.read_text(encoding='utf-8').replace(CURATED[0][0], 'INVALID'), encoding='utf-8')
    with pytest.raises(ValueError, match='Anchor changed'):
        integrate(altered)


def test_outputs(tmp_path):
    summary = run(SOURCE, tmp_path)
    assert summary['named_statements_preserved'] == 9
    assert summary['new_explicit_items_reserved'] == len(CURATED)
    assert (tmp_path / 'chapter1_integrated.json').exists()
    assert (tmp_path / 'report.md').exists()

from pathlib import Path

import pytest

from phase163_r4_r19_equation_audit.audit import audit, run


SOURCE = Path(__file__).resolve().parents[1] / 'Toda_01.tex'


def test_r19_all_candidates_preserved():
    rows, summary = audit(SOURCE)
    assert len(rows) == 102
    assert summary['existing_integrated_records'] == 24
    assert len({r['candidate_no'] for r in rows}) == 102


def test_r19_reserved_ids_not_changed():
    rows, summary = audit(SOURCE)
    assert summary['existing_ids_modified'] == 0
    assert summary['new_statement_ids_assigned'] == 0
    assert all(not r['new_statement_id'] for r in rows)


def test_r19_named_statements_keep_prior_reservations():
    rows, _ = audit(SOURCE)
    named = [r for r in rows if r['review_status'] == 'EXISTING_NAMED']
    assert len(named) == 9
    assert {r['linked_reserved_id'] for r in named} == {
        f'TODA-S{i:06d}' for i in range(1, 10)
    }


def test_r19_selected_math_review_status():
    rows, _ = audit(SOURCE)
    by_line = {r['start_line']: r for r in rows}
    assert by_line[211]['review_status'] == 'INDEPENDENT_CANDIDATE'
    assert by_line[450]['linked_reserved_id'] == 'TODA-S000018'
    assert by_line[1115]['review_status'] == 'INDEPENDENT_CANDIDATE'


def test_r19_unknown_math_remains_unverified():
    rows, summary = audit(SOURCE)
    assert summary['unresolved_candidates'] > 0
    assert any(r['review_status'] == 'NEEDS_FULL_TEXT_REVIEW' for r in rows)
    assert summary['exhaustive_semantic_review'] is False


def test_r19_source_change_fails_closed(tmp_path):
    target = tmp_path / 'changed.tex'
    target.write_text(SOURCE.read_text(encoding='utf-8').replace('\\section*{CHAPTER I', '\\section*{CHAPTER X', 1), encoding='utf-8')
    with pytest.raises(ValueError):
        audit(target)


def test_r19_export(tmp_path):
    summary = run(SOURCE, tmp_path)
    assert (tmp_path / 'equation_review.csv').is_file()
    assert (tmp_path / 'summary.json').is_file()
    assert (tmp_path / 'report.md').is_file()
    assert summary['search_connected'] == 0

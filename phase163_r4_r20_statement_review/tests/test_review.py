from pathlib import Path

import pytest

from phase163_r4_r20_statement_review.review import CLAIMS, review, run


SOURCE = Path(__file__).resolve().parents[2] / 'phase163_r4_r19_equation_audit' / 'Toda_01.tex'


def test_all_fourteen_have_mathematical_hypotheses():
    result, pending = review(SOURCE)
    assert len(result['claims']) == 14
    assert all(row['hypotheses_ja'] for row in result['claims'])
    assert len(pending) == 65


def test_original_ids_are_preserved():
    result, _ = review(SOURCE)
    entries = result['reserved_catalog']['entries']
    assert len(entries) == 24
    assert {e['statement_id'] for e in entries} == {f'TODA-S{i:06d}' for i in range(1,25)}
    assert all(not row['statement_id'] for row in result['claims'])


def test_dimensional_conflict_is_not_verified():
    result, _ = review(SOURCE)
    item = next(row for row in result['claims'] if row['source_line'] == 211)
    assert item['review_class'] == 'needs_mathematical_correction'
    assert item['printed_source_status'] == 'UNVERIFIED'
    assert 'smash product' in item['verification_issue_ja']


def test_no_unverified_proof_search_connection():
    result, _ = review(SOURCE)
    assert result['summary']['proof_search_connected'] == 0
    assert result['summary']['legacy_equivalence_verified'] == 0
    assert all(x['search_status'] == 'UNCONNECTED' for x in result['claims'])


def test_pending_queue_keeps_source_context():
    _, pending = review(SOURCE)
    assert all(row['semantic_decision'] == 'PENDING_MANUAL_REVIEW' for row in pending)
    assert all('preceding_context' in row and 'following_context' in row for row in pending)


def test_reports_are_written(tmp_path):
    summary = run(SOURCE, tmp_path)
    assert summary['remaining_semantic_pending'] == 65
    assert (tmp_path/'statement_review.json').exists()
    assert (tmp_path/'pending_65.csv').exists()
    assert (tmp_path/'report.md').exists()

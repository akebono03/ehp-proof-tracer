"""Focused audit contracts; these tests do not prove any group."""
from types import SimpleNamespace

import pytest

from phase177_r1_k5_completion_status_audit import audit


def test_inventory_keeps_distinct_summands_and_ignores_separator(tmp_path):
    path = tmp_path / 'sphere.csv'
    path.write_text('k,n,id,orders,generator\n5,4,0,2,a\n5,4,1,2,b\n5,,,,\n4,3,0,2,c\n5,2,0,2,d\n', encoding='utf-8')
    groups = audit.inventory(path)
    assert tuple(groups) == ((2, 5), (4, 5))
    assert [row['generator'] for row in groups[(4, 5)]] == ['a', 'b']


def test_inventory_requires_k5(tmp_path):
    path = tmp_path / 'sphere.csv'
    path.write_text('k,n,id,orders,generator\n4,2,0,2,a\n', encoding='utf-8')
    with pytest.raises(RuntimeError, match='NO_K5_GROUPS'):
        audit.inventory(path)


def test_frontier_distinguishes_not_reached_empty_and_candidates():
    option = SimpleNamespace(rule=SimpleNamespace(name='rule-a'), subgoals=('child',))
    result = audit.frontier(('x', 'y', 'z'), [('y', ()), ('z', (option,))])
    assert [r['classification'] for r in result] == ['NOT_REACHED', 'NO_CANDIDATES', 'CANDIDATES_NOT_PROVED']
    assert result[2]['candidate_batches'] == [[{'rule': 'rule-a', 'subgoals': [repr('child')]}]]


def sample_rows():
    return [{'n': n, 'k': k, 'status': 'partial' if n == 4 else 'search_failed' if n == 5 else 'complete',
             'integrity_ok': True, 'web_ok': True, 'verified_complete_tree': n not in (4, 5)}
            for n, k in audit.EXPECTED_PAIRS]


def test_summary_separates_unfinished_from_worker_error():
    result = audit.summarize(sample_rows())
    assert result['gate'].startswith('PASS_')
    assert result['counts'] == {'complete': 4, 'partial': 1, 'search_failed': 1}
    assert result['pending_n'] == [4, 5]
    assert result['next_target_candidate_n'] == 4


def test_summary_fails_for_regression():
    rows = sample_rows()
    rows[1].update(status='partial', verified_complete_tree=False)
    result = audit.summarize(rows)
    assert result['regressions'] == [[3, 5]]
    assert result['gate'].startswith('FAIL_')
    assert result['next_target_candidate_n'] is None


@pytest.mark.parametrize('change', [{'status': 'worker_timeout'}, {'web_ok': False}, {'integrity_ok': False}, {'status': 'not_searched'}])
def test_summary_fails_closed(change):
    rows = sample_rows()
    rows[2].update(change)
    assert audit.summarize(rows)['gate'].startswith('FAIL_')


def test_summary_rejects_missing_or_duplicate_inventory():
    rows = sample_rows()
    assert audit.summarize(rows[:-1])['gate'].startswith('FAIL_')
    assert audit.summarize(rows + [rows[-1]])['gate'].startswith('FAIL_')

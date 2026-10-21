from pathlib import Path

from phase166_r3ai_112_goal_audit.audit import audit


def test_all_112_pairs_classified():
    root = Path(__file__).resolve().parents[2]
    result = audit(root)
    assert result['read_only'] is True
    assert result['count'] == 112
    assert len({(x['n'], x['k']) for x in result['records']}) == 112
    assert result['source_counts'].get('missing', 0) == 0


def test_zero_groups_not_misclassified_as_finite_cyclic():
    result = audit(Path(__file__).resolve().parents[2])
    for item in result['records']:
        if item['orders'] and all(x == '0' for x in item['orders']):
            assert item['conversion'] != 'typed_goal' or item['goal_type'] != 'FiniteCyclicGroup'


def test_pi32_goal_is_not_regressed():
    result = audit(Path(__file__).resolve().parents[2])
    row = next(x for x in result['records'] if (x['n'], x['k']) == (2, 1))
    assert row['conversion'] == 'typed_goal'
    assert row['goal_type'] == 'FreeCyclicGroup'

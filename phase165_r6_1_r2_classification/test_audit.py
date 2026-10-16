from pathlib import Path
from tempfile import TemporaryDirectory

from audit import classify


def test_active_adapter_and_generic_connection_are_distinguished():
    with TemporaryDirectory() as d:
        root = Path(d)
        (root / 'phase165_r52_r9_shared_math.py').write_text(
            'from phase165_r52_r23_existing_rule_adapter import expand_existing_pi43_rules\n'
            'def shared_expansion_provider(goal):\n'
            '    providers = (expand_existing_pi43_rules,)\n'
            '    return generic_provider(goal)\n', encoding='utf-8')
        (root / 'phase165_r52_r23_existing_rule_adapter.py').write_text(
            'def expand_existing_pi43_rules(goal):\n'
            '    if goal == TodaPrimaryGroup(4, 3):\n'
            '        return ()\n'
            '    return ()\n', encoding='utf-8')
        report = classify(root)
        assert all(report['checks'].values())
        assert any(row['category'] == 'ACTIVE_GROUP_SPECIFIC_ADAPTER' for row in report['records'])


def test_unrelated_named_group_branch_is_not_claimed_active():
    with TemporaryDirectory() as d:
        root = Path(d)
        (root / 'phase165_goal_only_search.py').write_text(
            'def search(goal):\n    return ()\n', encoding='utf-8')
        (root / 'historical_backward.py').write_text(
            'def search(goal):\n    if pi43 == goal:\n        return ()\n    return ()\n', encoding='utf-8')
        report = classify(root)
        found = next(x for x in report['records'] if x['file'] == 'historical_backward.py')
        assert found['category'] == 'NAMED_GROUP_BRANCH_REVIEW'
        assert not found['reachable_by_imports']
        assert report['mode'] == 'READ_ONLY'


def test_group_type_branch_does_not_imply_hardcoded_group():
    with TemporaryDirectory() as d:
        root = Path(d)
        (root / 'phase165_r3_recursive_search.py').write_text(
            'def reconstruct_goal(goal):\n'
            '    if isinstance(goal, TodaPrimaryGroup):\n'
            '        return goal\n'
            '    return None\n', encoding='utf-8')
        report = classify(root)
        found = next(x for x in report['records'] if x['function'] == 'reconstruct_goal')
        assert found['category'] == 'GROUP_TYPE_BRANCH_REVIEW'


def test_many_branches_remain_bounded_and_identified():
    with TemporaryDirectory() as d:
        root = Path(d)
        lines = ['def reconstruct_goal(goal):']
        for index in range(1000):
            lines.extend((f'    if goal == pi43_{index}:', '        return goal'))
        lines.append('    return None')
        (root / 'phase165_r3_recursive_search.py').write_text('\n'.join(lines) + '\n', encoding='utf-8')
        report = classify(root)
        found = next(x for x in report['records'] if x['function'] == 'reconstruct_goal')
        assert found['category'] == 'NAMED_GROUP_BRANCH_REVIEW'
        assert len(found['conditions']) == 1000

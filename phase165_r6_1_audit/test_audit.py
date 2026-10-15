from pathlib import Path
from tempfile import TemporaryDirectory

from audit import scan


def test_detects_group_specific_adapter_and_generic_connection():
    with TemporaryDirectory() as directory:
        root = Path(directory)
        (root / 'phase165_r52_r9_shared_math.py').write_text(
            'from phase165_r52_r23_existing_rule_adapter import expand_existing_pi43_rules\n'
            'def shared_expansion_provider():\n'
            '    expand_existing_pi43_rules,\n'
            '    return generic_provider(goal)\n', encoding='utf-8')
        (root / 'phase165_r52_r23_existing_rule_adapter.py').write_text(
            'def expand_existing_pi43_rules(goal):\n'
            '    return TodaPrimaryGroup(4, 3)\n', encoding='utf-8')
        (root / 'phase165_r57_r26_generic_search_connection.py').write_text(
            'def build_generic_backward_expansion_provider():\n'
            '    return discover_explicit_goal_candidates(rules, goal)\n', encoding='utf-8')
        found = scan(root)['connection_checks']
        assert all(found.values())


def test_no_fabrication_from_unrelated_group_symbols():
    with TemporaryDirectory() as directory:
        root = Path(directory)
        (root / 'phase165_r52_r9_shared_math.py').write_text('def search(goal):\n    return ()\n', encoding='utf-8')
        found = scan(root)
        assert found['connection_checks']['shared_calls_pi43_adapter'] is False
        assert found['mode'] == 'READ_ONLY'
        assert any(row['category'] == 'MISSING_CORE_FILE' for row in found['candidates'])

import ast
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).parent))
from apply import FUNCTIONS, apply, transform

ORIGINAL = '''from toda_group_query import TodaGroupQuery\n\ndef build_toda_report(repository, n, k):\n    return repository\n\ndef build_standard_toda_report(n, k):\n    return n, k\n'''


def test_install_adds_both_new_functions_without_removing_old_api():
    result, changed = transform(ORIGINAL)
    assert changed
    nodes = {n.name for n in ast.parse(result).body if isinstance(n, ast.FunctionDef)}
    assert {'build_toda_report', 'build_standard_toda_report', 'build_toda_partial_result', 'build_standard_toda_partial_result'} <= nodes


def test_idempotence():
    result, _ = transform(ORIGINAL)
    assert transform(result) == (result, False)


def test_reject_partial_installation():
    one = ast.parse(FUNCTIONS).body[0]
    source = ORIGINAL + ast.get_source_segment(FUNCTIONS, one) + '\n'
    with pytest.raises(RuntimeError, match='partial'):
        transform(source)


def test_reject_unknown_existing_function():
    bad = ORIGINAL + '\ndef build_toda_partial_result(query):\n    return None\n' + FUNCTIONS.split('def build_standard_toda_partial_result')[1].join(['def build_standard_toda_partial_result',''])
    with pytest.raises((RuntimeError, SyntaxError)):
        transform(bad)


def test_fail_without_known_facade():
    with pytest.raises(RuntimeError, match='unknown facade'):
        transform('from toda_group_query import TodaGroupQuery\n')


def test_legacy_methods_remain_exactly_unmodified():
    old = ast.parse(ORIGINAL)
    new = ast.parse(transform(ORIGINAL)[0])
    for before in old.body:
        if isinstance(before, ast.FunctionDef):
            after = next(n for n in new.body if isinstance(n, ast.FunctionDef) and n.name == before.name)
            assert ast.dump(before, include_attributes=False) == ast.dump(after, include_attributes=False)


def test_apply_and_reinstall(tmp_path):
    file = tmp_path / 'toda_calculation_facade.py'
    file.write_text(ORIGINAL, encoding='utf-8')
    assert apply(tmp_path)['status'] == 'CHANGED'
    assert (tmp_path / 'phase165_r27_r50_backup' / file.name).read_text() == ORIGINAL
    assert apply(tmp_path)['status'] == 'ALREADY_INSTALLED'

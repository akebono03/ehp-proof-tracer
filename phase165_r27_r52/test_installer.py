import ast
from pathlib import Path
import pytest
from apply import NEW_FILE, transform_facade, apply


OLD = '''from toda_group_query import TodaGroupQuery

def build_toda_partial_result(query: TodaGroupQuery):
    if not isinstance(query, TodaGroupQuery):
        raise TypeError("query must be a TodaGroupQuery")
    from phase165_r52_r5_auto_search import search_group_structure_automatically
    return search_group_structure_automatically(n=query.n, k=query.k)

def build_standard_toda_partial_result(n: int, k: int):
    return build_toda_partial_result(TodaGroupQuery(n=n, k=k))
'''


def test_new_module_is_independent():
    s = NEW_FILE.read_text(encoding='utf-8')
    t = ast.parse(s)
    names = [n.module for n in ast.walk(t) if isinstance(n, ast.ImportFrom)]
    assert 'toda_calculation_facade' not in names
    assert 'proof_repository' not in names
    assert not any((name or '').startswith('repository_') for name in names)


def test_old_facade_is_replaced():
    result, changed = transform_facade(OLD)
    assert changed
    assert result.count('from toda_typed_group_facade import') == 2


def test_repeated_install_is_idempotent():
    result, changed = transform_facade(OLD)
    again, changed_again = transform_facade(result)
    assert not changed_again
    assert again == result


def test_unknown_implementation_is_rejected():
    src = OLD.replace('return search_group_structure_automatically(n=query.n, k=query.k)', 'return other_implementation(query)')
    with pytest.raises(RuntimeError):
        transform_facade(src)


def test_missing_functions_rejected():
    with pytest.raises(RuntimeError):
        transform_facade('def test(): pass')


def test_apply_creates_and_repeats(tmp_path):
    (tmp_path / 'toda_calculation_facade.py').write_text(OLD, encoding='utf-8')
    (tmp_path / 'phase165_r52_r5_auto_search.py').write_text('', encoding='utf-8')
    (tmp_path / 'toda_group_query.py').write_text('', encoding='utf-8')
    first = apply(tmp_path)
    assert first['status'] == 'CHANGED'
    second = apply(tmp_path)
    assert second['status'] == 'ALREADY_INSTALLED'


def test_target_conflict_is_safe(tmp_path):
    (tmp_path / 'toda_calculation_facade.py').write_text(OLD, encoding='utf-8')
    (tmp_path / 'phase165_r52_r5_auto_search.py').write_text('', encoding='utf-8')
    (tmp_path / 'toda_group_query.py').write_text('', encoding='utf-8')
    (tmp_path / 'toda_typed_group_facade.py').write_text('different', encoding='utf-8')
    with pytest.raises(RuntimeError):
        apply(tmp_path)

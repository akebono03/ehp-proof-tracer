from __future__ import annotations

import ast
from pathlib import Path
import pytest

from phase165_r27_r49.apply import transform, apply, MARKER


OLD = '''def search_group_structure_automatically(*, n, k, discovery=None):
    make_partial_proof_result(n=n, k=k)
    group = object()
    if discovery is None:
        from toda_calculation_facade import build_standard_toda_report
        from phase165_r52_r9_shared_math import search_shared_group_goal
        report = build_standard_toda_report(n=n, k=k)
        if report:
            return search_shared_group_goal(n=n, k=k)
        from phase165_r9_production_wiring import discover_goal_search_inputs
        discovery = discover_goal_search_inputs()
    return discovery
'''


def test_remove_legacy_presearch():
    result = transform(OLD)
    assert MARKER in result
    ast.parse(result)
    assert 'from toda_calculation_facade import' not in result
    assert 'search_shared_group_goal(' not in result
    assert 'discovery = discover_goal_search_inputs()' in result


def test_idempotent():
    assert transform(transform(OLD)) == transform(OLD)


def test_other_function_remains():
    source = 'def helper():\n    return 42\n\n' + OLD
    assert 'def helper():\n    return 42' in transform(source)


def test_guard_on_unrecognized():
    with pytest.raises(RuntimeError):
        transform('def search_group_structure_automatically(*, discovery=None):\n    if discovery is None:\n        discovery = object()\n')


def test_guard_on_missing_function():
    with pytest.raises(RuntimeError):
        transform('def other():\n    pass\n')


def test_install_and_reinstall(tmp_path: Path):
    (tmp_path / 'phase165_r52_r5_auto_search.py').write_text(OLD, encoding='utf-8')
    (tmp_path / 'phase165_r9_production_wiring.py').write_text('', encoding='utf-8')
    first = apply(tmp_path)
    second = apply(tmp_path)
    assert first['status'] == 'CHANGED'
    assert second['status'] == 'ALREADY_INSTALLED'
    assert (tmp_path / 'phase165_r27_r49_backup' / 'phase165_r52_r5_auto_search.py').is_file()


def test_does_not_delete_old_modules(tmp_path: Path):
    (tmp_path / 'phase165_r52_r5_auto_search.py').write_text(OLD, encoding='utf-8')
    (tmp_path / 'phase165_r9_production_wiring.py').write_text('', encoding='utf-8')
    old = tmp_path / 'repository_proof_scope.py'
    old.write_text('# preserved pending migration\n', encoding='utf-8')
    assert 'repository_proof_scope' in apply(tmp_path)['remaining_legacy_modules']
    assert old.exists()

"""R27-R49-R1: adapt legacy-seeded group search without source-text equality checks."""
from __future__ import annotations

import ast
import json
import shutil
from pathlib import Path

PHASE = '165 R27-R49-R1'
MARKER = '# Phase 165 R27-R49: registry-only default search'
TARGET = 'phase165_r52_r5_auto_search.py'
REPLACEMENT = '''if discovery is None:
        # Phase 165 R27-R49: registry-only default search
        # No legacy group result may supply the answer or premises.
        from phase165_r9_production_wiring import discover_goal_search_inputs
        discovery = discover_goal_search_inputs()'''


def _bounds(source: str, node: ast.AST) -> tuple[int, int]:
    lines = source.splitlines(keepends=True)
    return sum(map(len, lines[:node.lineno - 1])) + node.col_offset, sum(map(len, lines[:node.end_lineno]))


def _is_none_guard(node: ast.AST) -> bool:
    return (isinstance(node, ast.If) and isinstance(node.test, ast.Compare)
            and isinstance(node.test.left, ast.Name)
            and node.test.left.id == 'discovery' and len(node.test.ops) == 1
            and isinstance(node.test.ops[0], ast.Is) and len(node.test.comparators) == 1
            and isinstance(node.test.comparators[0], ast.Constant)
            and node.test.comparators[0].value is None)


def _called_names(node: ast.AST) -> set[str]:
    return {call.func.id for call in ast.walk(node)
            if isinstance(call, ast.Call) and isinstance(call.func, ast.Name)}


def transform(source: str) -> str:
    tree = ast.parse(source)
    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)
                 and node.name == 'search_group_structure_automatically']
    if len(functions) != 1:
        raise RuntimeError('Expected one canonical group search entry')
    function = functions[0]
    defaults = [node for node in function.body if _is_none_guard(node)]
    if len(defaults) != 1:
        raise RuntimeError('Expected one discovery-is-None guard')
    guard = defaults[0]
    called = _called_names(guard)
    legacy = {'build_standard_toda_report', 'search_shared_group_goal'}
    if not legacy.intersection(called):
        # Accept only the canonical registry-only branch, not arbitrary code.
        statements = guard.body
        if (len(statements) == 2 and isinstance(statements[0], ast.ImportFrom)
                and statements[0].module == 'phase165_r9_production_wiring'
                and [a.name for a in statements[0].names] == ['discover_goal_search_inputs']
                and isinstance(statements[1], ast.Assign)
                and len(statements[1].targets) == 1
                and isinstance(statements[1].targets[0], ast.Name)
                and statements[1].targets[0].id == 'discovery'
                and isinstance(statements[1].value, ast.Call)
                and isinstance(statements[1].value.func, ast.Name)
                and statements[1].value.func.id == 'discover_goal_search_inputs'
                and not statements[1].value.args and not statements[1].value.keywords):
            return source
        raise RuntimeError('Unknown default search branch; refusing overwrite')
    # Only rewrite the bootstrap if the legacy calls are confined to that branch.
    remainder = [n for n in ast.walk(function) if isinstance(n, ast.Call)
                 and isinstance(n.func, ast.Name) and n.func.id in legacy
                 and not any(n is inner for inner in ast.walk(guard))]
    if remainder:
        raise RuntimeError('Legacy calls outside discovery bootstrap; refusing overwrite')
    if 'discover_goal_search_inputs' not in called:
        raise RuntimeError('No verified registry discovery path; refusing overwrite')
    start, end = _bounds(source, guard)
    indentation = ' ' * guard.col_offset
    replacement = REPLACEMENT.replace('\n', '\n' + indentation)
    updated = source[:start] + replacement + '\n' + source[end:]
    ast.parse(updated)
    return updated


def apply(root: Path) -> dict:
    file = root / TARGET
    if not file.is_file() or not (root / 'phase165_r9_production_wiring.py').is_file():
        raise RuntimeError('Required production files missing')
    original = file.read_text(encoding='utf-8')
    updated = transform(original)
    changed = original != updated
    if changed:
        backup = root / 'phase165_r27_r49_r1_backup' / TARGET
        backup.parent.mkdir(parents=True, exist_ok=True)
        if not backup.exists():
            shutil.copy2(file, backup)
        file.write_text(updated, encoding='utf-8')
    audit = {
        'phase': PHASE,
        'status': 'CHANGED' if changed else 'ALREADY_INSTALLED',
        'modified_files': [TARGET] if changed else [],
        'canonical_group_search_uses_legacy_calculation_seed': False,
        'default_source': 'unified_registry_and_backward_search',
        'legacy_toda_calculation_api_unchanged': True,
        'remaining_legacy_modules': sorted(p.stem for p in root.glob('repository_*.py')),
        'full_pytest_run': False,
    }
    (root / 'phase165_r27_r49_r1_audit.json').write_text(
        json.dumps(audit, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    return audit


if __name__ == '__main__':
    print(json.dumps(apply(Path(__file__).resolve().parent.parent), indent=2, ensure_ascii=False))

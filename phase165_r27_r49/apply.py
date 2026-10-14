"""R27-R49: remove legacy TodaCalculation seed from canonical group search."""
from __future__ import annotations

import ast
import json
import shutil
from pathlib import Path

PHASE = '165 R27-R49'
MARKER = '# Phase 165 R27-R49: registry-only default search'
TARGET = 'phase165_r52_r5_auto_search.py'


def _bounds(source: str, node: ast.AST) -> tuple[int, int]:
    lines = source.splitlines(keepends=True)
    return sum(map(len, lines[:node.lineno - 1])), sum(map(len, lines[:node.end_lineno]))


def transform(source: str) -> str:
    tree = ast.parse(source)
    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)
                 and node.name == 'search_group_structure_automatically']
    if len(functions) != 1:
        raise RuntimeError('Expected one canonical group search entry')
    function = functions[0]
    defaults = [node for node in function.body if isinstance(node, ast.If)
                and isinstance(node.test, ast.Compare)
                and isinstance(node.test.left, ast.Name)
                and node.test.left.id == 'discovery'
                and len(node.test.ops) == 1
                and isinstance(node.test.ops[0], ast.Is)
                and len(node.test.comparators) == 1
                and isinstance(node.test.comparators[0], ast.Constant)
                and node.test.comparators[0].value is None]
    if len(defaults) != 1:
        raise RuntimeError('Expected one discovery-is-None guard')
    guard = defaults[0]
    body = ast.get_source_segment(source, guard) or ''
    if MARKER in body:
        return source
    if ('build_standard_toda_report' not in body or
            'search_shared_group_goal' not in body or
            'discover_goal_search_inputs' not in body):
        raise RuntimeError('Unrecognized default search; refusing overwrite')
    replacement = '''if discovery is None:
        # Phase 165 R27-R49: registry-only default search
        # Group structure is a goal; legacy calculation is not evidence.
        from phase165_r9_production_wiring import discover_goal_search_inputs
        discovery = discover_goal_search_inputs()'''
    start, end = _bounds(source, guard)
    indentation = ' ' * guard.col_offset
    updated = source[:start] + indentation + replacement.replace('\n', '\n' + indentation) + '\n' + source[end:]
    tree = ast.parse(updated)
    function = next(n for n in tree.body if isinstance(n, ast.FunctionDef)
                    and n.name == 'search_group_structure_automatically')
    if any(isinstance(n, ast.Name) and n.id in ('build_standard_toda_report', 'search_shared_group_goal')
           for n in ast.walk(function)):
        raise RuntimeError('Legacy calculation reference remains in group search')
    return updated


def apply(root: Path) -> dict:
    file = root / TARGET
    if not file.is_file() or not (root / 'phase165_r9_production_wiring.py').is_file():
        raise RuntimeError('Required production files missing')
    original = file.read_text(encoding='utf-8')
    updated = transform(original)
    changed = original != updated
    if changed:
        backup = root / 'phase165_r27_r49_backup' / TARGET
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
    (root / 'phase165_r27_r49_audit.json').write_text(
        json.dumps(audit, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    return audit


if __name__ == '__main__':
    print(json.dumps(apply(Path(__file__).resolve().parent.parent), indent=2, ensure_ascii=False))

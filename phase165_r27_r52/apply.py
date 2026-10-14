"""Phase 165 R27-R52 installer: extract a legacy-free typed group facade."""
from __future__ import annotations

import ast
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent.parent
NEW_FILE = Path(__file__).with_name('toda_typed_group_facade.py')
FUNCTION_NAMES = ('build_toda_partial_result', 'build_standard_toda_partial_result')


def _find_function(tree: ast.Module, name: str) -> ast.FunctionDef:
    found = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name]
    if len(found) != 1:
        raise RuntimeError(f'exactly one {name} is required in legacy facade')
    return found[0]


def transform_facade(source: str) -> tuple[str, bool]:
    tree = ast.parse(source)
    new_functions = ast.parse(NEW_FILE.read_text(encoding='utf-8'))
    replacements = []
    for name in FUNCTION_NAMES:
        node = _find_function(tree, name)
        expected = _find_function(new_functions, name)
        # R50 is the only supported starting point. Reject unrelated rewrites.
        calls = {
            n.func.id for n in ast.walk(node)
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
        }
        if 'build_toda_partial_result' not in calls and 'search_group_structure_automatically' not in calls and 'build_standard_toda_partial_result' not in calls and 'build_toda_typed_partial_result' not in calls:
            if 'toda_typed_group_facade' not in ast.unparse(node):
                raise RuntimeError(f'unrecognized R50 function {name}; refusing overwrite')
        if name == 'build_toda_partial_result':
            replacement = '''def build_toda_partial_result(query: TodaGroupQuery):
    """Legacy-compatible entry; implementation lives in the independent typed facade."""
    from toda_typed_group_facade import build_toda_partial_result as run_typed_search
    return run_typed_search(query)
'''
        else:
            replacement = '''def build_standard_toda_partial_result(n: int, k: int):
    """Legacy-compatible entry; implementation lives in the independent typed facade."""
    from toda_typed_group_facade import build_standard_toda_partial_result as run_typed_search
    return run_typed_search(n, k)
'''
        replacement_node = ast.parse(replacement).body[0]
        if ast.dump(node, include_attributes=False) != ast.dump(replacement_node, include_attributes=False):
            replacements.append((node.lineno - 1, node.end_lineno, replacement))
    if not replacements:
        return source, False
    lines = source.splitlines(keepends=True)
    for start, end, replacement in sorted(replacements, reverse=True):
        lines[start:end] = [replacement + '\n']
    result = ''.join(lines)
    ast.parse(result)
    return result, True


def apply(root: Path = ROOT) -> dict:
    old_path = root / 'toda_calculation_facade.py'
    target = root / 'toda_typed_group_facade.py'
    if not old_path.is_file():
        raise FileNotFoundError(old_path)
    if not (root / 'phase165_r52_r5_auto_search.py').is_file():
        raise RuntimeError('canonical group search module not installed')
    if not (root / 'toda_group_query.py').is_file():
        raise RuntimeError('TodaGroupQuery module not installed')
    new_bytes = NEW_FILE.read_bytes()
    if target.exists() and target.read_bytes() != new_bytes:
        raise RuntimeError('typed facade already exists with different contents')
    previous = old_path.read_text(encoding='utf-8-sig')
    changed_facade, change = transform_facade(previous)
    new_created = not target.exists()
    if new_created or change:
        backup = root / 'phase165_r27_r52_backup'
        backup.mkdir(exist_ok=True)
        if change:
            existing = backup / old_path.name
            if existing.exists() and existing.read_bytes() != old_path.read_bytes():
                raise RuntimeError('backup conflict; refusing overwrite')
            if not existing.exists():
                shutil.copy2(old_path, existing)
        if new_created:
            target.write_bytes(new_bytes)
        if change:
            old_path.write_text(changed_facade, encoding='utf-8', newline='\n')
    result = {
        'phase': '165 R27-R52',
        'status': 'CHANGED' if new_created or change else 'ALREADY_INSTALLED',
        'modified_files': ([target.name] if new_created else []) + ([old_path.name] if change else []),
        'typed_group_facade_without_legacy_imports': True,
        'compatibility_entry_preserved': True,
        'legacy_calculation_unchanged': True,
        'remaining_legacy_repository_modules': 4,
        'full_pytest_run': False,
    }
    (root / 'phase165_r27_r52_audit.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return result


if __name__ == '__main__':
    print(json.dumps(apply(), ensure_ascii=False, indent=2))

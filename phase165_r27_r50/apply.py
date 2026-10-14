"""Phase 165 R27-R50: additive typed group-calculation public facade."""
from __future__ import annotations
import ast
import json
from pathlib import Path
import shutil

FUNCTIONS = '''\n\ndef build_toda_partial_result(query: TodaGroupQuery):\n    """Search a group using the registry-backed prover, never legacy calculation."""\n    if not isinstance(query, TodaGroupQuery):\n        raise TypeError("query must be a TodaGroupQuery")\n    from phase165_r52_r5_auto_search import search_group_structure_automatically\n    return search_group_structure_automatically(n=query.n, k=query.k)\n\n\ndef build_standard_toda_partial_result(n: int, k: int):\n    """Canonical partial-proof entry for public group-calculation callers."""\n    return build_toda_partial_result(TodaGroupQuery(n=n, k=k))\n'''


def transform(src: str) -> tuple[str, bool]:
    tree = ast.parse(src)
    defs = {n.name: n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}
    if not {'build_toda_report', 'build_standard_toda_report'} <= defs.keys():
        raise RuntimeError('unknown facade API; refusing change')
    if not any(isinstance(n, ast.ImportFrom) and n.module == 'toda_group_query' and
               any(a.name == 'TodaGroupQuery' for a in n.names) for n in tree.body):
        raise RuntimeError('missing TodaGroupQuery import; refusing change')
    names = ('build_toda_partial_result', 'build_standard_toda_partial_result')
    found = [n in defs for n in names]
    if all(found):
        for name in names:
            node = defs[name]
            expected = next(n for n in ast.parse(FUNCTIONS).body if isinstance(n, ast.FunctionDef) and n.name == name)
            if ast.dump(node, include_attributes=False) != ast.dump(expected, include_attributes=False):
                raise RuntimeError(f'existing {name} differs; refusing overwrite')
        return src, False
    if any(found):
        raise RuntimeError('partial R50 installation detected; refusing overwrite')
    return src.rstrip('\r\n') + FUNCTIONS + '\n', True


def apply(root: Path) -> dict:
    path = root / 'toda_calculation_facade.py'
    if not path.is_file():
        raise FileNotFoundError(path)
    old = path.read_text(encoding='utf-8-sig')
    new, changed = transform(old)
    if changed:
        backup = root / 'phase165_r27_r50_backup'
        backup.mkdir(exist_ok=True)
        shutil.copy2(path, backup / path.name)
        path.write_text(new, encoding='utf-8', newline='\n')
    result = {
        'phase': '165 R27-R50', 'status': 'CHANGED' if changed else 'ALREADY_INSTALLED',
        'modified_files': [path.name] if changed else [],
        'new_api': ['build_toda_partial_result', 'build_standard_toda_partial_result'],
        'canonical_search': 'search_group_structure_automatically',
        'legacy_group_calculation_preserved': True,
        'remaining_legacy_modules': [
            'repository_foundational_group_specialization', 'repository_proof_scope',
            'repository_symbolic_sigma_specialization', 'repository_symbolic_stable_group_specialization'],
        'full_pytest_run': False,
    }
    (root / 'phase165_r27_r50_audit.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n',encoding='utf-8')
    return result


if __name__ == '__main__':
    print(json.dumps(apply(Path(__file__).resolve().parent.parent), ensure_ascii=False, indent=2))

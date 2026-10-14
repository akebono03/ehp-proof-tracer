"""Phase 165 R27-R54: conservative dependency and runtime-entry audit.

Do not delete a live legacy API or rewrite proof provenance merely to remove imports.
"""
from __future__ import annotations

import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEGACY = (
    'repository_foundational_group_specialization',
    'repository_proof_scope',
    'repository_symbolic_sigma_specialization',
    'repository_symbolic_stable_group_specialization',
)
ENTRIES = ('toda_typed_group_facade', 'web_group_query', 'web_group_proof',
           'toda_calculation_facade', 'toda_calculation_report', 'toda_calculation')


def imports_of(source: str) -> set[str]:
    tree = ast.parse(source)
    result: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            result.update(alias.name.split('.')[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            result.add(node.module.split('.')[0])
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in ('__import__', 'import_module'):
            if node.args and isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str):
                result.add(node.args[0].value.split('.')[0])
    return result


def plan(root: Path) -> dict:
    sources = {}
    for path in sorted(root.glob('*.py')):
        if path.stem.startswith(('test_', 'audit_')) or '.phase' in path.stem or path.stem.endswith(('_backup', '_pre_cleanup')):
            continue
        sources[path.stem] = path.read_text(encoding='utf-8-sig')
    edges = {name: imports_of(src) & sources.keys() for name, src in sources.items()}
    found = sorted(name for name in LEGACY if name in sources)
    direct = {name: sorted(edges.get(name, set()) & set(found)) for name in ENTRIES if name in sources}
    inbound = {name: sorted(origin for origin, deps in edges.items() if name in deps)
               for name in found}
    external_dependents = {name: [origin for origin in inbound[name] if origin not in LEGACY]
                           for name in found}
    safe = sorted(name for name in found if not inbound[name])
    typed = 'toda_typed_group_facade'
    typed_imports = sorted(edges.get(typed, set()))
    # Guard against accidental reintroduction of direct legacy dependencies in the new entry.
    if typed in sources and set(typed_imports) & set(LEGACY):
        raise RuntimeError('Typed facade directly imports a legacy repository module')
    return {
        'phase': '165 R27-R54',
        'status': 'AUDITED_NO_PRODUCTION_REWRITE',
        'remaining_legacy_modules': found,
        'active_legacy_imports': {k: v for k, v in direct.items() if v},
        'legacy_module_importers': inbound,
        'non_legacy_importers': external_dependents,
        'unreferenced_legacy_candidates': safe,
        'typed_facade_direct_legacy_imports': [],
        'legacy_group_calculation_replaced': False,
        'legacy_report_api_removed': False,
        'full_pytest_run': False,
    }


def apply(root: Path = ROOT) -> dict:
    audit = plan(root)
    output = root / 'phase165_r27_r54_audit.json'
    output.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(audit, ensure_ascii=False, indent=2))
    return audit


if __name__ == '__main__':
    apply()

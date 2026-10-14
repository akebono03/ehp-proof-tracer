"""R27-R57: fail-closed retirement gate for the final four repository modules."""
from __future__ import annotations
import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEGACY = frozenset({
    'repository_foundational_group_specialization',
    'repository_proof_scope',
    'repository_symbolic_sigma_specialization',
    'repository_symbolic_stable_group_specialization',
})
OLD_CALC = frozenset({'toda_calculation', 'toda_calculation_report', 'toda_calculation_facade'})
NEW_ENTRY = frozenset({'toda_typed_group_facade', 'phase165_r52_r5_auto_search'})


def imports_of(source: str) -> set[str]:
    tree = ast.parse(source)
    modules = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            modules.add(node.module.split('.')[0])
        elif isinstance(node, ast.Import):
            modules.update(alias.name.split('.')[0] for alias in node.names)
    return modules


def references_of(source: str) -> set[str]:
    """Find literal dynamic imports as well as import statements."""
    tree = ast.parse(source)
    refs = imports_of(source)
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or not node.args:
            continue
        func = node.func
        if not (isinstance(func, ast.Name) and func.id in {'__import__', 'import_module'} or
                isinstance(func, ast.Attribute) and func.attr == 'import_module'):
            continue
        arg = node.args[0]
        if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
            refs.add(arg.value.split('.')[0])
    return refs


def relative_source_files(root: Path):
    """Only live root modules and tests; do not count archived phase source copies."""
    yield from sorted(root.glob('*.py'))
    tests = root / 'tests'
    if tests.is_dir():
        yield from sorted(tests.rglob('test_*.py'))


def plan(root: Path) -> dict:
    root = Path(root)
    remaining = sorted(module for module in LEGACY if (root / (module + '.py')).is_file())
    production = {}
    tests = {}
    dynamic_unknown = []
    for path in relative_source_files(root):
        if path.stem in LEGACY:
            continue
        src = path.read_text(encoding='utf-8-sig')
        deps = sorted(references_of(src) & (LEGACY | OLD_CALC))
        rel = str(path.relative_to(root)).replace('\\', '/')
        if deps:
            (tests if rel.startswith('tests/') else production)[rel] = deps
        if 'import_module(' in src or '__import__(' in src:
            dynamic_unknown.append(rel)
    typed = {}
    for name in NEW_ENTRY:
        path = root / (name + '.py')
        if not path.is_file():
            typed[name] = 'MISSING'
        else:
            typed[name] = sorted(references_of(path.read_text(encoding='utf-8-sig')) & (LEGACY | OLD_CALC))
    blockers = {path: deps for path, deps in production.items() if set(deps) & LEGACY}
    can_delete = bool(remaining) and not blockers and not any(v == 'MISSING' or v for v in typed.values())
    return {
        'phase': '165 R27-R57',
        'status': 'RETIREMENT_BLOCKED' if not can_delete else 'STATIC_GATE_READY_REVIEW_REQUIRED',
        'remaining_legacy_modules': remaining,
        'production_legacy_importers': production,
        'test_legacy_importers': tests,
        'typed_entry_legacy_imports': typed,
        'literal_dynamic_import_locations': dynamic_unknown,
        'deletion_ready_by_static_imports': can_delete,
        'deleted_files': [],
        'production_files_modified': [],
        'full_pytest_run': False,
    }


def apply(root: Path = ROOT) -> dict:
    result = plan(root)
    (Path(root) / 'phase165_r27_r57_audit.json').write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8'
    )
    return result


if __name__ == '__main__':
    print(json.dumps(apply(), ensure_ascii=False, indent=2))

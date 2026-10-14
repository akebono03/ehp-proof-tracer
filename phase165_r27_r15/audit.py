"""Phase 165 R27-R15: read-only, targeted legacy consumer boundary audit."""
from __future__ import annotations
import ast
import json
from pathlib import Path

TARGETS = {
    'repository_operation_query_facade.py': ('query_standard_repository_operation_input',),
    'repository_element_facade.py': ('explore_standard_repository_generator_input',),
    'standard_production_repository.py': ('build_standard_production_proof_repository',),
}
LEGACY = {'build_standard_production_proof_repository', 'build_standard_proof_repository', 'build_toda_prop515_upper_bootstrap'}
ENTRY_FILES = ('main.py', 'cli.py', 'web_operation_query.py', 'web_generator_exploration.py', 'web_operation_query_proof.py')
PROTECTED = ('proof.py', 'theorem_facts.py', 'toda_rules.py', 'unified_statement_registry.py', 'phase163_r4_registry_bridge.py', 'phase165_r52_r2_search_adapter.py')


def _name(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    return None


def inspect(root: Path) -> dict:
    absent = [p for p in (*TARGETS, *ENTRY_FILES) if not (root / p).is_file()]
    if absent:
        raise FileNotFoundError('Required source missing: ' + ', '.join(absent))
    records = []
    for file in (*TARGETS, *ENTRY_FILES):
        tree = ast.parse((root / file).read_text(encoding='utf-8-sig'), filename=file)
        imported = []
        functions = []
        for node in tree.body:
            if isinstance(node, ast.ImportFrom):
                imported.extend((node.module, alias.name) for alias in node.names)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                calls = sorted({name for child in ast.walk(node) if isinstance(child, ast.Call) if (name := _name(child.func)) is not None})
                functions.append({'function': node.name, 'line': node.lineno, 'calls': calls, 'legacy_calls': sorted(LEGACY.intersection(calls))})
        records.append({'path': file, 'legacy_imports': [{'module': mod, 'symbol': sym} for mod, sym in imported if sym in LEGACY], 'functions': functions})
    by_path = {r['path']: r for r in records}
    asserted = []
    for file, names in TARGETS.items():
        for name in names:
            hits = [f for f in by_path[file]['functions'] if f['function'] == name]
            if len(hits) != 1:
                raise RuntimeError(f'{file}: expected exactly one {name}, found {len(hits)}')
            asserted.append({'path': file, 'function': name, 'calls': hits[0]['calls'], 'legacy_calls': hits[0]['legacy_calls']})
    test_samples = {str(p.relative_to(root)).replace('\\', '/'): True for p in sorted((root / 'tests').glob('test_*repository*'))[:30]} if (root / 'tests').is_dir() else {}
    return {
        'phase': '165 R27-R15',
        'mode': 'READ_ONLY_PUBLIC_CONSUMER_FUNCTION_BOUNDARY',
        'production_files_modified': False,
        'full_pytest_run': False,
        'deletion_authorized': False,
        'next_phase_deletion_start': '165 R27-R16',
        'public_function_boundaries': asserted,
        'entry_files': list(ENTRY_FILES),
        'test_samples': list(test_samples),
        'protected_files': list(PROTECTED),
        'records': records,
        'runtime_reachability_verified': False,
        'r16_scope': 'Migrate individual live public consumers before removing legacy factories; delete only proven-unreferenced functions',
    }


def main() -> int:
    report = inspect(Path.cwd())
    output = Path(__file__).resolve().parent / 'audit_report.json'
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    summary = {key: report[key] for key in ('phase', 'mode', 'production_files_modified', 'full_pytest_run', 'deletion_authorized', 'next_phase_deletion_start', 'public_function_boundaries', 'runtime_reachability_verified')}
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print('Report:', output)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

"""Phase 165 R27-R9: read-only inventory of legacy builder dependencies."""
from __future__ import annotations

import ast
import json
from pathlib import Path

FILES = (
    'web_group_proof.py',
    'phase165_r52_r3_web_adapter.py',
    'phase165_r52_r4_flask_bridge.py',
    'web_app.py',
    'web_group_query.py',
    'main.py',
    'standard_production_repository.py',
    'standard_repository.py',
    'toda_calculation_facade.py',
    'toda_prop515_upper_bootstrap.py',
    'phase165_r9_production_wiring.py',
    'phase165_r4_production_connection.py',
)
PROTECTED = (
    'unified_statement_registry.py',
    'phase163_r4_registry_bridge.py',
    'phase165_r52_r2_search_adapter.py',
)
SYMBOLS = (
    'build_standard_web_group_proof_view',
    'build_standard_toda_report',
    'build_standard_production_proof_repository',
    'build_standard_proof_repository',
    'build_toda_group_result_proof_replay',
    'build_toda_prop515_upper_bootstrap',
    'WebGroupProofView',
    'WebGroupProofStepView',
    '_build_group_proof_rendered_lines',
    '_group_proof_rule_name',
    '_group_proof_statement_latex',
)


def audit(root: Path) -> dict:
    references = []
    missing = []
    for name in FILES:
        path = root / name
        if not path.is_file():
            missing.append(name)
            continue
        tree = ast.parse(path.read_text(encoding='utf-8-sig'), filename=name)
        entries = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    if alias.name in SYMBOLS:
                        entries.append({'line': node.lineno, 'kind': 'import', 'symbol': alias.name, 'module': node.module})
            elif isinstance(node, ast.Call):
                fn = node.func
                symbol = fn.id if isinstance(fn, ast.Name) else fn.attr if isinstance(fn, ast.Attribute) else None
                if symbol in SYMBOLS:
                    entries.append({'line': node.lineno, 'kind': 'call', 'symbol': symbol})
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and node.name in SYMBOLS:
                entries.append({'line': node.lineno, 'kind': 'definition', 'symbol': node.name})
        references.append({'path': name, 'references': sorted(entries, key=lambda x: (x['line'], x['kind']))})
    tests = []
    for path in sorted(set(root.glob('test_*.py')) | set((root / 'tests').glob('test_*.py'))):
        try:
            tree = ast.parse(path.read_text(encoding='utf-8-sig'), filename=str(path))
        except (SyntaxError, UnicodeError):
            continue
        mentioned = sorted({node.id for node in ast.walk(tree) if isinstance(node, ast.Name) and node.id in SYMBOLS} |
                           {node.attr for node in ast.walk(tree) if isinstance(node, ast.Attribute) and node.attr in SYMBOLS})
        if mentioned:
            tests.append({'path': str(path.relative_to(root)), 'symbols': mentioned})
    return {
        'phase': '165 R27-R9',
        'mode': 'READ_ONLY_FUNCTION_LEVEL_DEPENDENCY_AUDIT',
        'production_files_modified': False,
        'full_pytest_run': False,
        'scanned_paths': len(FILES),
        'missing_paths': missing,
        'references': references,
        'related_tests': tests,
        'protected_files_excluded': list(PROTECTED),
        'deletion_authorized': False,
        'next_action': 'Separate common Web view/formatting APIs from legacy report/replay before deleting bootstrap or repository builders.',
    }


def main() -> int:
    root = Path.cwd()
    result = audit(root)
    output = Path(__file__).resolve().parent / 'audit_report.json'
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items() if k not in ('references', 'related_tests')}, ensure_ascii=False, indent=2))
    print('Reference file entries:', sum(len(x['references']) for x in result['references']))
    print('Related test files:', len(result['related_tests']))
    print('Full report:', output)
    return 0 if not result['missing_paths'] else 1


if __name__ == '__main__':
    raise SystemExit(main())

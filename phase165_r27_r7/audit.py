"""Phase 165 R27-R7: read-only inventory of legacy production calls."""
from __future__ import annotations

import ast
import json
from pathlib import Path

ROOT_FILES = (
    'phase165_r52_r5_auto_search.py',
    'phase165_r52_r4_flask_bridge.py',
    'web_app.py',
    'web_group_query.py',
    'web_group_proof.py',
    'toda_calculation_facade.py',
    'main.py',
    'standard_production_repository.py',
    'standard_repository.py',
    'phase165_r9_production_wiring.py',
)
LEGACY_SYMBOLS = (
    'build_standard_toda_report',
    'build_standard_web_group_proof_view',
    'build_standard_production_proof_repository',
    'build_standard_proof_repository',
    'build_toda_group_result_proof_replay',
    'build_standard_web_group_query_view',
)
PROTECTED_MODULES = (
    'unified_statement_registry.py',
    'phase163_r4_registry_bridge.py',
    'phase165_r52_r2_search_adapter.py',
)


def analyze_source(path: Path) -> dict:
    source = path.read_text(encoding='utf-8-sig')
    tree = ast.parse(source, filename=str(path))
    references = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            f = node.func
            name = f.id if isinstance(f, ast.Name) else f.attr if isinstance(f, ast.Attribute) else None
            if name in LEGACY_SYMBOLS:
                references.append({'symbol': name, 'line': node.lineno, 'kind': 'call'})
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                if alias.name in LEGACY_SYMBOLS:
                    references.append({'symbol': alias.name, 'line': node.lineno, 'kind': 'import'})
    return {'path': path.name, 'references': sorted(references, key=lambda x: (x['line'], x['kind']))}


def audit(root: Path) -> dict:
    missing = [p for p in ROOT_FILES if not (root / p).is_file()]
    if missing:
        raise FileNotFoundError('Missing production sources: ' + ', '.join(missing))
    found = [analyze_source(root / p) for p in ROOT_FILES]
    return {
        'phase': '165 R27-R7',
        'mode': 'READ_ONLY_LEGACY_DEPENDENCY_AUDIT',
        'production_files_modified': False,
        'full_pytest_run': False,
        'scanned_files': len(found),
        'references': [r for r in found if r['references']],
        'legacy_report_called_by_auto_search': any(
            x['symbol'] == 'build_standard_toda_report' and x['kind'] == 'call'
            for x in next(y['references'] for y in found if y['path'] == 'phase165_r52_r5_auto_search.py')
        ),
        'protected_files_excluded': list(PROTECTED_MODULES),
        'next_action': 'Replace legacy Group query and CLI callers without promoting unproved results to FOUND; then remove orphaned legacy proof builders.',
    }


def main() -> None:
    root = Path.cwd()
    report = audit(root)
    output = Path(__file__).resolve().parent / 'audit_report.json'
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2, ensure_ascii=False))
    if report['legacy_report_called_by_auto_search']:
        raise SystemExit('R27-R6 regression: auto search still calls legacy report')


if __name__ == '__main__':
    main()

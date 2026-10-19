"""R6-8 read-only audit of legacy probe output consumers."""
from __future__ import annotations

import ast
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'phase165_r6_audit_results' / 'r6_8_consumer_contract'
TARGETS = (
    'probes/probe_phase50_capabilities.py',
    'probes/probe_phase52_capabilities.py',
    'probes/probe_phase53_capabilities.py',
    'probes/probe_phase54_capabilities.py',
    'probes/probe_phase55_capabilities.py',
    'probes/probe_phase58_capabilities.py',
    'tests/test_phase59_n3_ehp_chain.py',
    'tests/test_phase164_r3_registry_search_connection.py',
)


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    report = {'phase': '165 R6-8', 'mode': 'read_only', 'files': {}, 'missing': [],
              'source_changed': False, 'pytest_executed': False}
    for relative in TARGETS:
        path = ROOT / relative
        if not path.is_file():
            report['missing'].append(relative)
            continue
        data = path.read_text(encoding='utf-8-sig')
        tree = ast.parse(data, filename=relative)
        imports = []
        accessed = defaultdict(set)
        builders = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                if node.module.startswith('probes.') or node.module.startswith('tests.'):
                    imports.append({'module': node.module, 'names': [alias.name for alias in node.names]})
            elif isinstance(node, ast.Subscript) and isinstance(node.value, ast.Name):
                value = node.slice
                if isinstance(value, ast.Constant) and isinstance(value.value, str):
                    accessed[node.value.id].add(value.value)
            elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                if node.func.id.startswith('build_phase'):
                    builders.append(node.func.id)
        report['files'][relative] = {
            'legacy_imports': imports,
            'dictionary_field_access': {key: sorted(value) for key, value in sorted(accessed.items())},
            'builder_calls': sorted(set(builders)),
        }
    output = OUT / 'report.json'
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('R6-8 legacy consumer contract audit')
    for path, details in report['files'].items():
        print('FILE:', path)
        print('  Probe imports:', ', '.join(x['module'] for x in details['legacy_imports']) or '(none)')
        for symbol, fields in details['dictionary_field_access'].items():
            if symbol.startswith('phase') or symbol in ('data', 'leaves'):
                print('  ', symbol, 'fields:', ', '.join(fields))
    print('Missing files:', len(report['missing']))
    print('Report:', output)
    print('Read-only; full pytest NOT run.')
    return 1 if report['missing'] else 0


if __name__ == '__main__':
    raise SystemExit(main())

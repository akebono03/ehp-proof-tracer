import ast
import json
from pathlib import Path

LEGACY = {'probes.probe_phase49_capabilities', 'probes.probe_phase56_capabilities'}
LEGACY_BUILDERS = {'build_phase49_representative_result', 'build_phase56_representative_result'}


def module_name(relative):
    return relative.with_suffix('').as_posix().replace('/', '.')


def scan(root):
    root = Path(root)
    files = sorted(p for folder in ('tests', 'probes') if (root / folder).is_dir() for p in (root / folder).rglob('*.py'))
    files += sorted(p for p in root.glob('*.py') if p.name != 'audit.py')
    records = []
    errors = []
    for path in files:
        rel = path.relative_to(root)
        try:
            tree = ast.parse(path.read_text(encoding='utf-8-sig'), filename=str(rel))
        except (SyntaxError, UnicodeError) as error:
            errors.append({'path': str(rel), 'error': str(error)})
            continue
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module in LEGACY:
                imports.append({'line': node.lineno, 'module': node.module, 'names': [alias.name for alias in node.names]})
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name in LEGACY:
                        imports.append({'line': node.lineno, 'module': alias.name, 'names': ['*']})
        calls = sorted(set(node.func.id for node in ast.walk(tree) if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in LEGACY_BUILDERS))
        if imports or calls or (rel.parts[0] == 'tests' and ('phase49' in rel.name or 'phase56' in rel.name)) or module_name(rel) in LEGACY:
            records.append({'path': rel.as_posix(), 'imports': imports, 'builder_calls': calls,
                            'legacy_named_test': rel.parts[0] == 'tests' and ('phase49' in rel.name or 'phase56' in rel.name),
                            'legacy_probe': module_name(rel) in LEGACY})
    return {'phase': '165 R6-10', 'mode': 'read_only', 'scanned_python_files': len(files),
            'records': records, 'parse_errors': errors,
            'direct_legacy_importers_outside_named_tests': [r['path'] for r in records if r['imports'] and not r['legacy_named_test'] and not r['legacy_probe']],
            'candidate_named_tests': [r['path'] for r in records if r['legacy_named_test']],
            'required_next_step': 'Review dependencies before any retirement; no source files changed.'}


def main():
    root = Path(__file__).resolve().parent.parent
    output = root / 'phase165_r6_audit_results' / 'r6_10_dependency_audit'
    output.mkdir(parents=True, exist_ok=True)
    report = scan(root)
    (output / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    lines = ['# Phase 165 R6-10 dependency audit', '', 'Read-only. No test or Probe has been retired.', '',
             f"Scanned Python files: {report['scanned_python_files']}",
             f"Phase 49/56 named test files: {len(report['candidate_named_tests'])}",
             f"Other direct legacy importers: {len(report['direct_legacy_importers_outside_named_tests'])}",
             f"AST parse errors: {len(report['parse_errors'])}", '', '## Candidate tests']
    lines += ['- ' + item for item in report['candidate_named_tests']]
    lines += ['', '## Other direct legacy importers']
    lines += ['- ' + item for item in report['direct_legacy_importers_outside_named_tests']]
    lines += ['', '## Caution', 'Do not retire a Probe until all active imports and call sites are resolved.']
    (output / 'report.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(json.dumps({'status': 'AUDITED_NO_CHANGES', 'report': str(output / 'report.json'),
                      'candidate_named_tests': len(report['candidate_named_tests']),
                      'other_direct_importers': len(report['direct_legacy_importers_outside_named_tests']),
                      'parse_errors': len(report['parse_errors']), 'full_pytest_run': False}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()

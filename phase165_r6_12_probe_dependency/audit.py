from __future__ import annotations

import ast
import json
from pathlib import Path

LEGACY = {"probes.probe_phase49_capabilities", "probes.probe_phase56_capabilities"}


def active_python_sources(root: Path):
    for path in sorted(root.glob('*.py')):
        yield path
    for folder in ('tests', 'probes'):
        directory = root / folder
        if directory.is_dir():
            for path in sorted(directory.rglob('*.py')):
                if '__pycache__' not in path.parts:
                    yield path


def audit(root: Path):
    references = []
    errors = []
    files = list(active_python_sources(root))
    for path in files:
        relative = path.relative_to(root).as_posix()
        try:
            tree = ast.parse(path.read_text(encoding='utf-8-sig'), filename=relative)
        except (SyntaxError, UnicodeError) as error:
            errors.append({'path': relative, 'error': str(error)})
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module in LEGACY:
                references.append({'path': relative, 'line': node.lineno, 'module': node.module, 'names': [a.name for a in node.names], 'kind': 'from_import'})
            elif isinstance(node, ast.Import):
                for item in node.names:
                    if item.name in LEGACY:
                        references.append({'path': relative, 'line': node.lineno, 'module': item.name, 'names': [], 'kind': 'import'})
    return {'phase': '165 R6-12', 'status': 'AUDITED_NO_CHANGES', 'active_files_scanned': len(files), 'references': references, 'parse_errors': errors, 'retirement_performed': False, 'full_pytest_run': False}


def main():
    root = Path(__file__).resolve().parent.parent
    result = audit(root)
    output = root / 'phase165_r6_audit_results' / 'r6_12_probe_dependency'
    output.mkdir(parents=True, exist_ok=True)
    (output / 'report.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({**result, 'report': str(output / 'report.json')}, ensure_ascii=False, indent=2))
    if result['parse_errors']:
        raise SystemExit(2)


if __name__ == '__main__':
    main()

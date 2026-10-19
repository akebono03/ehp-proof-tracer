"""R6-8(4) read-only post-retirement verification; no test bodies run."""
from __future__ import annotations
import ast
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

RETIRED = {
    'probes.probe_phase53_capabilities', 'probes.probe_phase54_capabilities',
    'probes.probe_phase55_capabilities', 'probes.probe_phase57_capabilities',
    'phase162_ehp_leaf_inputs', 'phase162_pi5_3_web_replay',
    'tests.test_phase59_n3_ehp_chain',
    'tests.test_phase55_prop51_phase52_phase54_dependency',
    'test_phase59_n3_ehp_chain', 'test_phase55_prop51_phase52_phase54_dependency',
}

def imported_names(source: str) -> set[str]:
    tree = ast.parse(source)
    result = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            result.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            result.add(node.module)
    return result

def scan(root: Path) -> dict:
    tests = sorted((root / 'tests').glob('test_*.py'))
    hits = {}
    errors = {}
    for path in tests:
        try:
            names = imported_names(path.read_text(encoding='utf-8-sig'))
        except (SyntaxError, UnicodeError) as exc:
            errors[path.name] = str(exc)
            continue
        found = sorted(x for x in names if any(x == old or x.startswith(old + '.') for old in RETIRED))
        if found:
            hits[path.name] = found
    return {'remaining_test_files': len(tests), 'direct_retired_imports': hits, 'parse_errors': errors}

def main() -> int:
    root = Path(__file__).resolve().parent.parent
    out = root / 'phase165_r6_audit_results' / 'r6_8_4_close'
    out.mkdir(parents=True, exist_ok=True)
    data = scan(root)
    cohort = sorted((root / 'tests').glob('test_phase165*.py'))
    # Collection only; no execution of test functions. No entire-suite collection.
    command = [sys.executable, '-m', 'pytest', '--collect-only', '-q',
               '--continue-on-collection-errors', '--tb=short', '-o', 'addopts=']
    command += [str(p.relative_to(root)) for p in cohort]
    data.update({'phase': '165 R6-8(4) closure', 'utc': datetime.now(timezone.utc).isoformat(),
                 'phase165_test_files': len(cohort), 'collection_command': command,
                 'full_pytest_executed': False, 'test_bodies_executed': False,
                 'source_modified': False,
                 'mathematical_coverage_verified': False})
    if cohort:
        try:
            result = subprocess.run(command, cwd=root, capture_output=True, text=True,
                                    errors='replace', timeout=240)
            transcript = result.stdout + '\n' + result.stderr
            data['collection_returncode'] = result.returncode
            data['collection_error_files'] = re.findall(r'^ERROR\s+([^\r\n]+)', transcript, re.M)
            data['collection_summary'] = [s.strip() for s in transcript.splitlines() if 'error' in s.lower() or 'collected' in s.lower()][-12:]
        except subprocess.TimeoutExpired:
            transcript = 'Collection timed out after 240 seconds.'
            data['collection_returncode'] = 'TIMEOUT'
    else:
        transcript = 'No tests/test_phase165*.py found; no collection attempted.'
        data['collection_returncode'] = 'NO_PHASE165_TESTS'
    (out / 'collection.txt').write_text(transcript, encoding='utf-8')
    (out / 'report.json').write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({k:v for k,v in data.items() if k not in ('collection_command',)}, ensure_ascii=False, indent=2))
    print('REPORT:', out / 'report.json')
    return 0 if data['collection_returncode'] == 0 and not data['direct_retired_imports'] else 1

if __name__ == '__main__':
    raise SystemExit(main())

from __future__ import annotations

import ast
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

CANDIDATES = (
    'tests/test_phase49_concrete_pi3_2_compatibility.py',
    'tests/test_phase49_delta_hopf_surjectivity.py',
    'tests/test_phase49_hopf_injectivity.py',
    'tests/test_phase49_hopf_isomorphism.py',
    'tests/test_phase49_low_dimensional_facts.py',
    'tests/test_phase49_probe.py',
    'tests/test_phase55_prop51_phase49_dependency.py',
    'tests/test_phase56_pi_i_minus_1_1_zero.py',
    'tests/test_phase56_probe.py',
    'tests/test_phase56_prop44_composition_compatibility.py',
    'tests/test_phase56_prop44_eta2_specialization.py',
    'tests/test_phase56_prop44_second_summand_restriction.py',
    'tests/test_phase56_toda52_composition_isomorphism.py',
)
EXCLUDE_DIRS = {'.git', '.venv', 'venv', '__pycache__', 'phase165_r6_audit_results', '.pytest_cache'}

def python_sources(root: Path):
    for p in root.rglob('*.py'):
        rel = p.relative_to(root)
        if any(x in EXCLUDE_DIRS or x.startswith('.phase') for x in rel.parts):
            continue
        if p.is_file():
            yield p, rel.as_posix()

def dependency_audit(root: Path, candidates=CANDIDATES):
    candidate_set = set(candidates)
    names = {Path(p).stem: p for p in candidates}
    blockers = []
    parse_errors = []
    for path, rel in python_sources(root):
        if rel in candidate_set:
            continue
        try:
            tree = ast.parse(path.read_text(encoding='utf-8-sig'), filename=rel)
        except (SyntaxError, UnicodeError) as exc:
            parse_errors.append({'path': rel, 'error': str(exc)})
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    parts = alias.name.split('.')
                    if parts[-1] in names:
                        blockers.append({'path': rel, 'line': node.lineno, 'module': alias.name, 'candidate': names[parts[-1]]})
            elif isinstance(node, ast.ImportFrom) and node.module:
                parts = node.module.split('.')
                if parts[-1] in names:
                    blockers.append({'path': rel, 'line': node.lineno, 'module': node.module, 'candidate': names[parts[-1]]})
    return blockers, parse_errors

def retire(root: Path):
    root = root.resolve()
    targets = [root / item for item in CANDIDATES]
    existing = [(relative, path) for relative, path in zip(CANDIDATES, targets) if path.is_file()]
    blockers, parse_errors = dependency_audit(root)
    out = root / 'phase165_r6_audit_results' / 'r6_11_legacy_tests_retirement'
    out.mkdir(parents=True, exist_ok=True)
    report = {'phase': '165 R6-11', 'status': 'BLOCKED', 'candidates': list(CANDIDATES), 'present': [rel for rel, _ in existing], 'missing': [rel for rel, p in zip(CANDIDATES, targets) if not p.is_file()], 'external_test_import_blockers': blockers, 'parse_errors': parse_errors, 'probes_retired': False, 'full_pytest_run': False}
    if blockers or parse_errors:
        (out / 'report.json').write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding='utf-8')
        return report
    if not existing:
        report['status'] = 'ALREADY_RETIRED'
        (out / 'report.json').write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding='utf-8')
        return report
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    dest = out / ('backup_' + stamp)
    manifest = []
    for relative, path in existing:
        payload = path.read_bytes()
        target = dest / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(payload)
        if target.read_bytes() != payload:
            raise OSError(f'Backup verification failed: {relative}')
        manifest.append({'path': relative, 'sha256': hashlib.sha256(payload).hexdigest()})
    (dest / 'manifest.json').write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding='utf-8')
    for relative, path in existing:
        path.unlink()
    report.update({'status': 'RETIRED_TEST_FILES', 'retired': len(existing), 'backup': str(dest), 'manifest': manifest})
    (out / 'report.json').write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding='utf-8')
    return report

if __name__ == '__main__':
    import sys
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    result = retire(root)
    print(json.dumps({k:v for k,v in result.items() if k != 'manifest'}, indent=2, ensure_ascii=False))
    if result['status'] == 'BLOCKED':
        sys.exit(2)

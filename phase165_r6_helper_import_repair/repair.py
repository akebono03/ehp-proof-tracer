from __future__ import annotations
import ast
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
import subprocess
import sys

TARGET = Path('tests/test_phase143_19_method_evidence.py')
PROBES = ('tests/test_phase143_22_exactness_components.py', 'tests/test_phase159_pi4_3_exactness_reason_unification.py')
OLD_SYMBOL = 'build_standard_toda_report'
OLD_MODULE = 'toda_calculation_facade'


def command(argv: list[str], root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(argv, cwd=root, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace', check=False)


def extract_candidate(root: Path) -> tuple[str, str] | None:
    history = command(['git', 'log', '--all', '--format=%H', '--', TARGET.as_posix()], root)
    revisions = ['HEAD'] + history.stdout.splitlines()[:30] if history.returncode == 0 else ['HEAD']
    for revision in dict.fromkeys(revisions):
        source = command(['git', 'show', f'{revision}:{TARGET.as_posix()}'], root)
        if source.returncode == 0:
            return revision, source.stdout
    for p in (root / 'phase165_r6_audit_results').rglob(TARGET.name):
        if p.is_file() and not p.is_symlink():
            return str(p), p.read_text(encoding='utf-8-sig')
    return None


def analyze_candidate(source: str) -> dict:
    tree = ast.parse(source)
    imported = []
    called = []
    references = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module == OLD_MODULE:
            imported.extend((a.name, a.asname or a.name, node.lineno, node.end_lineno) for a in node.names)
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id == OLD_SYMBOL:
                called.append(node.lineno)
            if isinstance(node.func, ast.Attribute) and node.func.attr == OLD_SYMBOL:
                called.append(node.lineno)
        if isinstance(node, ast.Name) and node.id == OLD_SYMBOL and isinstance(node.ctx, ast.Load):
            references.append(node.lineno)
    return {'old_imports': imported, 'old_calls': called, 'old_references': references,
            'helper_exists': any(isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == '_method_evidence_data' for n in tree.body)}


def remove_unused_import(source: str) -> tuple[str | None, str]:
    tree = ast.parse(source)
    imports = [n for n in ast.walk(tree) if isinstance(n, ast.ImportFrom) and n.module == OLD_MODULE and any(a.name == OLD_SYMBOL for a in n.names)]
    if len(imports) != 1:
        return None, 'old import not uniquely located'
    node = imports[0]
    names = {a.asname or a.name for a in node.names if a.name == OLD_SYMBOL}
    if any(isinstance(n, ast.Name) and n.id in names and isinstance(n.ctx, ast.Load) for n in ast.walk(tree)):
        return None, 'old function is actively referenced; cannot replace based on names alone'
    if len(node.names) != 1 or node.end_lineno is None:
        return None, 'mixed imports; requires manual inspection'
    lines = source.splitlines(keepends=True)
    new_source = ''.join(lines[:node.lineno - 1] + lines[node.end_lineno:])
    ast.parse(new_source)
    return new_source, 'removed one provably unused retired import'


def main() -> int:
    root = Path.cwd().resolve()
    output = root / 'phase165_r6_audit_results' / 'helper_import_repair' / datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    output.mkdir(parents=True, exist_ok=True)
    report = {'status': 'NO_CHANGE', 'target': str(TARGET), 'production_code_modified': False, 'full_pytest_run': False}
    if (root / TARGET).exists():
        report['status'] = 'TARGET_ALREADY_EXISTS_NO_CHANGE'
    else:
        candidate = extract_candidate(root)
        if candidate is None:
            report['status'] = 'CANDIDATE_NOT_FOUND'
        else:
            revision, source = candidate
            report['candidate_source'] = revision
            report['sha256'] = hashlib.sha256(source.encode('utf-8')).hexdigest()
            report['analysis'] = analyze_candidate(source)
            modified, reason = remove_unused_import(source)
            report['decision'] = reason
            # Keep exact historic source in the audit folder, not in project tests, for review.
            (output / 'historical_helper_candidate.py.txt').write_text(source, encoding='utf-8')
            if modified is None:
                report['status'] = 'ACTIVE_OLD_API_BLOCKED_NO_CHANGE'
            else:
                destination = root / TARGET
                destination.parent.mkdir(exist_ok=True)
                try:
                    destination.write_text(modified, encoding='utf-8')
                    targeted = command([sys.executable, '-m', 'pytest', '-q', *PROBES], root)
                    (output / 'targeted_pytest.log').write_text(targeted.stdout, encoding='utf-8')
                    report['targeted_pytest_returncode'] = targeted.returncode
                    if targeted.returncode == 0:
                        report['status'] = 'HELPER_RESTORED_TARGETED_PASS'
                    else:
                        report['status'] = 'TARGETED_FAILED_REVERTED'
                finally:
                    if report.get('status') != 'HELPER_RESTORED_TARGETED_PASS':
                        destination.unlink(missing_ok=True)
    (output / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'status': report['status'], 'decision': report.get('decision'), 'analysis': report.get('analysis'), 'report': str(output / 'report.json'), 'full_pytest_run': False}, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

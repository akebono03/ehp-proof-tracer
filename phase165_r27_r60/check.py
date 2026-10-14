"""Phase 165 R27-R60: typed-only regression checks, no production changes."""
from __future__ import annotations
import argparse
import ast
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OLD_MODULES = ('toda_calculation', 'toda_calculation_report', 'repository_foundational_group_specialization', 'repository_proof_scope', 'repository_symbolic_sigma_specialization', 'repository_symbolic_stable_group_specialization')
PUBLIC = ('cli.py', 'web_group_query.py', 'web_group_proof.py', 'toda_typed_group_facade.py', 'phase165_r52_r5_auto_search.py')
GROUPS = ((2, 1), (3, 1), (3, 2))


def imported_modules(source: str) -> set[str]:
    result = set()
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.ImportFrom) and node.module:
            result.add(node.module.split('.')[0])
        elif isinstance(node, ast.Import):
            result.update(alias.name.split('.')[0] for alias in node.names)
    return result


def check_static(root: Path) -> dict:
    missing = [name for name in PUBLIC if not (root / name).is_file()]
    lingering = [name for name in OLD_MODULES if (root / (name + '.py')).exists()]
    entry_deps = {}
    for name in PUBLIC:
        path = root / name
        if path.exists():
            try:
                entry_deps[name] = sorted(imported_modules(path.read_text(encoding='utf-8-sig')) & set(OLD_MODULES))
            except (SyntaxError, UnicodeError) as error:
                entry_deps[name] = ['SYNTAX_ERROR: ' + str(error)]
    cli_src = (root / 'cli.py').read_text(encoding='utf-8-sig') if (root / 'cli.py').exists() else ''
    typed_src = (root / 'toda_typed_group_facade.py').read_text(encoding='utf-8-sig') if (root / 'toda_typed_group_facade.py').exists() else ''
    conditions = {
        'public_files_exist': not missing,
        'old_modules_absent': not lingering,
        'public_direct_legacy_imports_absent': not any(entry_deps.values()),
        'cli_uses_typed_partial': 'build_standard_toda_partial_result' in cli_src,
        'typed_facade_has_public_entry': 'def build_standard_toda_partial_result' in typed_src,
    }
    return {'conditions': conditions, 'missing_public_files': missing, 'remaining_old_modules': lingering, 'entry_legacy_dependencies': entry_deps}


def probe(root: Path, n: int, k: int, timeout: int = 90) -> dict:
    source = '''import json\nfrom toda_typed_group_facade import build_standard_toda_partial_result\nr = build_standard_toda_partial_result(n=%d,k=%d)\npayload = {"n": %d, "k": %d, "result_type": type(r).__name__, "status": str(getattr(getattr(r,"status",None),"value",getattr(r,"status",None))), "structure_status": str(getattr(getattr(r,"structure_status",None),"value",getattr(r,"structure_status",None))), "proven_steps_count": len(getattr(r,"proven_steps",()) or ()), "open_goals_count": len(getattr(r,"open_goals",()) or ()), "has_conclusion": getattr(r,"conclusion",None) is not None}\nprint("R60_RESULT_JSON="+json.dumps(payload,ensure_ascii=False))\n''' % (n,k,n,k)
    try:
        process = subprocess.run([sys.executable, '-c', source], cwd=root, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return {'n': n, 'k': k, 'execution': 'TIMEOUT', 'timeout_seconds': timeout}
    lines = [line.partition('R60_RESULT_JSON=')[2] for line in process.stdout.splitlines() if line.startswith('R60_RESULT_JSON=')]
    if process.returncode or not lines:
        return {'n': n, 'k': k, 'execution': 'ERROR', 'returncode': process.returncode, 'stderr_tail': process.stderr[-2500:], 'stdout_tail': process.stdout[-1000:]}
    try:
        details = json.loads(lines[-1])
    except json.JSONDecodeError as error:
        return {'n': n, 'k': k, 'execution': 'INVALID_JSON', 'message': str(error)}
    details['execution'] = 'OK'
    details['verified_mathematical_proof'] = False
    return details


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--static-only', action='store_true')
    args = parser.parse_args()
    result = {'phase': '165 R27-R60', 'mode': 'REGRESSION_NO_PRODUCTION_REWRITE', 'static': check_static(ROOT), 'representative_groups': [], 'full_pytest_run': False}
    static_pass = all(result['static']['conditions'].values())
    if static_pass and not args.static_only:
        for n,k in GROUPS:
            result['representative_groups'].append(probe(ROOT,n,k))
    result['status'] = 'STATIC_BLOCKED' if not static_pass else ('STATIC_PASS' if args.static_only else 'CHECKED')
    (ROOT / 'phase165_r27_r60_results.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if static_pass else 1

if __name__ == '__main__':
    sys.exit(main())

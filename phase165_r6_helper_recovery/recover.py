"""Recover only an authentic, previously tracked shared test fixture."""
from __future__ import annotations
import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from datetime import datetime, timezone

TARGET = Path('tests/test_phase143_19_method_evidence.py')
BANNED = ('probes.', 'repository_inference', 'repository_element_facade', 'toda_pi4_3_delta_image_free_cyclic_inference_rule', 'toda_group_proof_generic_narrative_renderer')
PROBES = (
    'tests/test_phase143_22_exactness_components.py',
    'tests/test_phase159_pi4_3_exactness_reason_unification.py',
)

def run_cmd(argv: list[str], root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(argv, cwd=root, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8', errors='replace', check=False)

def safe_source(data: bytes) -> tuple[bool, str]:
    try:
        source = data.decode('utf-8-sig')
        tree = ast.parse(source)
    except (UnicodeDecodeError, SyntaxError) as exc:
        return False, f'cannot parse: {exc}'
    symbols = {node.name for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))}
    if '_method_evidence_data' not in symbols:
        return False, 'no _method_evidence_data definition'
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules = [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            modules = [node.module or '']
        else:
            continue
        for module in modules:
            if any(module == bad.rstrip('.') or module.startswith(bad) for bad in BANNED):
                return False, f'retired dependency: {module}'
    if any(bad in source for bad in BANNED):
        return False, 'retired implementation mention in source'
    return True, 'valid self-contained shared test helper source'

def candidate_sources(root: Path):
    # Only exact canonical Git paths and exact-name archival copies, never generated facsimiles.
    if shutil.which('git'):
        cmd = run_cmd(['git', 'show', f'HEAD:{TARGET.as_posix()}'], root)
        if cmd.returncode == 0:
            yield 'git:HEAD', cmd.stdout.encode('utf-8')
        history = run_cmd(['git', 'log', '--all', '--format=%H', '--', TARGET.as_posix()], root)
        if history.returncode == 0:
            for sha in history.stdout.splitlines()[:20]:
                recovered = run_cmd(['git', 'show', f'{sha}:{TARGET.as_posix()}'], root)
                if recovered.returncode == 0:
                    yield f'git:{sha}', recovered.stdout.encode('utf-8')
    folder = root / 'phase165_r6_audit_results'
    if folder.exists():
        for file in folder.rglob(TARGET.name):
            if file.is_file() and not file.is_symlink():
                yield f'backup:{file.relative_to(root)}', file.read_bytes()

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=Path.cwd())
    args = parser.parse_args()
    root = args.root.resolve()
    destination = root / TARGET
    output = root / 'phase165_r6_audit_results' / 'helper_recovery' / datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    output.mkdir(parents=True, exist_ok=True)
    result: dict = {'status': 'PENDING', 'target': str(TARGET), 'candidates': [], 'full_pytest_run': False}
    if destination.exists():
        result['status'] = 'ALREADY_EXISTS_NO_CHANGE'
    elif not all((root / path).is_file() for path in PROBES):
        result['status'] = 'TARGETED_TEST_MISSING_NO_CHANGE'
    else:
        for label, data in candidate_sources(root):
            valid, detail = safe_source(data)
            item = {'source': label, 'sha256': hashlib.sha256(data).hexdigest(), 'eligible': valid, 'reason': detail}
            result['candidates'].append(item)
            if not valid:
                continue
            destination.parent.mkdir(exist_ok=True)
            try:
                destination.write_bytes(data)
                targeted = run_cmd([sys.executable, '-m', 'pytest', '-q', *PROBES], root)
                (output / 'targeted_pytest.log').write_text(targeted.stdout, encoding='utf-8')
                item['targeted_test_returncode'] = targeted.returncode
                if targeted.returncode == 0:
                    result['status'] = 'RESTORED_TARGETED_TESTS_PASS'
                    result['source'] = label
                    break
                result['status'] = 'CANDIDATE_FAILED_REVERTED'
            finally:
                if result['status'] != 'RESTORED_TARGETED_TESTS_PASS':
                    destination.unlink(missing_ok=True)
        if result['status'] == 'PENDING':
            result['status'] = 'NO_VALID_HISTORICAL_SOURCE_NO_CHANGE'
    (output / 'report.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'status': result['status'], 'candidates': len(result['candidates']), 'report': str(output / 'report.json'), 'full_pytest_run': False}, ensure_ascii=False, indent=2))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())

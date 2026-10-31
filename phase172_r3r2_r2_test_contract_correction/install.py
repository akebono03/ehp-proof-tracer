"""Guarded R3 test-contract correction followed by the existing R3 runner.

This Phase 172 repair changes only one existing R2 test function. The canonical
R3 runner owns the production renderer installation and its rollback.
"""
from __future__ import annotations

import argparse
import ast
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent
TEST_FILE = Path('phase172_r2_suspension_relation_display/tests/test_projection.py')
RENDERER = Path('phase168_r3_5_model_renderer.py')
R3_INSTALL = Path('phase172_r3_hopf_chain_display/install.py')
R3_PROJECTION = Path('phase172_r3_hopf_chain_display/projection.py')
R3_TEST = Path('phase172_r3_hopf_chain_display/tests/test_projection.py')
REVIEWED_RENDERER_BLOB = 'bb267bc669bdcaa5b9dcc24bdf7dc8b2ac4e7c95'
REVIEWED_R2_TEST_BLOB = '0656bbd9c1b02c757927ab36b8df52cee8c1f45b'
REVIEWED_R3_INSTALL_SHA256 = 'ee16868581a8496acbb76873d8c3ff39587b5b3297e7fa23040effd594ea6c8a'
REVIEWED_R3_PROJECTION_SHA256 = 'fae04a1f9e5c0a2408e8cc29180bfe64c14b8376186ba78b168db270e2e55413'
REVIEWED_R3_TEST_SHA256 = '843f889791b3a447051edfd1c22d58208cbe78e481d048c0e998443f12e8e9b6'
OLD_ASSERTION = r'''    assert r"$\nu'\eta_{6} = \nu'E\eta_{5}$." in body'''
NEW_ASSERTIONS = (
    '    assert "[R4] Proposition 2.2." in references\n'
    '    assert "[R5] (5.3)." in references'
)
TARGET_TEST_NAME = 'test_real_complete_narrative_retains_cited_source_and_hopf_conclusion'


def run_command(*args: str, timeout: int = 45) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args, cwd=ROOT, capture_output=True, text=True, encoding='utf-8',
        errors='replace', check=False, timeout=timeout,
    )


def checked(*args: str) -> str:
    proc = run_command(*args)
    if proc.returncode:
        raise RuntimeError('command failed: ' + repr(args) + ': ' + proc.stderr[-900:])
    return proc.stdout.strip()


def normalize(data: bytes) -> str:
    content = data.decode('utf-8-sig')
    if '\r' in content.replace('\r\n', ''):
        raise RuntimeError('mixed newlines in checked source')
    return content.replace('\r\n', '\n')


def unique_function(source: str, name: str) -> ast.FunctionDef:
    tree = ast.parse(source)
    functions = [node for node in tree.body
                 if isinstance(node, ast.FunctionDef) and node.name == name]
    if len(functions) != 1:
        raise RuntimeError('target test function not found uniquely')
    return functions[0]


def transform_test(data: bytes) -> bytes:
    source = normalize(data)
    if source.count(OLD_ASSERTION) != 1 or NEW_ASSERTIONS in source:
        raise RuntimeError('reviewed R2 test assertion is not present exactly once')
    node = unique_function(source, TARGET_TEST_NAME)
    original_lines = source.splitlines()
    if OLD_ASSERTION not in '\n'.join(original_lines[node.lineno - 1:node.end_lineno]):
        raise RuntimeError('target assertion is outside the reviewed R2 test function')
    result = source.replace(OLD_ASSERTION, NEW_ASSERTIONS, 1)
    unique_function(result, TARGET_TEST_NAME)
    ending = '\r\n' if b'\r\n' in data else '\n'
    return result.replace('\n', ending).encode('utf-8')


def function_text(data: bytes) -> str:
    source = normalize(data)
    node = unique_function(source, TARGET_TEST_NAME)
    return '\n'.join(source.splitlines()[node.lineno-1:node.end_lineno]) + '\n'


def preflight() -> dict[str, str | None]:
    if checked('git', 'branch', '--show-current') != 'develop':
        raise RuntimeError('develop branch is required')
    head = checked('git', 'rev-parse', 'HEAD')
    if checked('git', 'rev-parse', 'HEAD:' + TEST_FILE.as_posix()) != REVIEWED_R2_TEST_BLOB:
        raise RuntimeError('committed R2 test differs from reviewed version')
    if checked('git', 'rev-parse', 'HEAD:' + RENDERER.as_posix()) != REVIEWED_RENDERER_BLOB:
        raise RuntimeError('committed Renderer differs from reviewed R2 version')
    for path in (TEST_FILE, RENDERER):
        if checked('git', 'status', '--porcelain=v1', '--', path.as_posix()):
            raise RuntimeError('tracked path has local changes: ' + str(path))
        committed = subprocess.run(
            ['git', 'show', 'HEAD:' + path.as_posix()], cwd=ROOT,
            check=True, capture_output=True,
        ).stdout
        if normalize(committed) != normalize((ROOT / path).read_bytes()):
            raise RuntimeError('worktree bytes differ from committed source: ' + str(path))
    for path, sha in (
        (R3_INSTALL, REVIEWED_R3_INSTALL_SHA256),
        (R3_PROJECTION, REVIEWED_R3_PROJECTION_SHA256),
        (R3_TEST, REVIEWED_R3_TEST_SHA256),
    ):
        if not (ROOT / path).is_file():
            raise RuntimeError('R3 prerequisite missing: ' + str(path))
        if hashlib.sha256((ROOT / path).read_bytes()).hexdigest() != sha:
            raise RuntimeError('R3 prerequisite changed: ' + str(path))
    existing = (ROOT / TEST_FILE).read_bytes()
    corrected = transform_test(existing)
    expected = PACKAGE / 'payload/test_projection.py'
    if normalize(corrected) != normalize(expected.read_bytes()):
        raise RuntimeError('corrected full test differs from reviewed payload')
    remote = run_command('git', 'ls-remote', 'origin', 'refs/heads/develop', timeout=25)
    remote_head = remote.stdout.split()[0] if remote.returncode == 0 and remote.stdout.strip() else None
    if remote_head is not None and remote_head != head:
        raise RuntimeError('origin/develop changed; re-review HEAD before patch')
    return {'branch': 'develop', 'head': head, 'remote': remote_head,
            'test_blob': REVIEWED_R2_TEST_BLOB,
            'renderer_blob': REVIEWED_RENDERER_BLOB,
            'corrected_test_sha256': hashlib.sha256(corrected).hexdigest()}


def output_directory() -> Path:
    base = Path(os.environ.get('LOCALAPPDATA') or Path.home()) / 'EHPProofTracerRecovery'
    directory = base / ('phase172_r3r2_' + datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%fZ'))
    directory.mkdir(parents=True, exist_ok=False)
    return directory


def local_tests(output: Path) -> None:
    env = os.environ.copy()
    env['PYTHONUTF8'] = '1'
    env['PYTHONIOENCODING'] = 'utf-8'
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    env['PYTHONPATH'] = str(ROOT) + os.pathsep + env.get('PYTHONPATH', '')
    run = subprocess.run(
        [sys.executable, '-B', '-m', 'pytest', '-q', '--tb=short', '-p', 'no:cacheprovider',
         'phase172_r3r2_r2_test_contract_correction/tests/test_install.py'],
        cwd=ROOT, env=env, text=True, capture_output=True, encoding='utf-8',
        errors='replace', check=False, timeout=120,
    )
    log = run.stdout + '\n' + run.stderr
    (output / 'correction_tests.log').write_text(log, encoding='utf-8')
    print('PHASE172_R3R2_GUARD_TESTS=' + ('PASS' if run.returncode == 0 else 'FAIL'), flush=True)
    if run.returncode:
        raise RuntimeError('correction tests failed: ' + log[-2500:])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--run-focused-tests', action='store_true')
    args = parser.parse_args()
    state = preflight()
    output = output_directory()
    old_test = (ROOT / TEST_FILE).read_bytes()
    new_test = transform_test(old_test)
    old_renderer = (ROOT / RENDERER).read_bytes()
    (output / 'test_real_complete_narrative_FULL.py').write_text(
        function_text(new_test), encoding='utf-8',
    )
    (output / 'test_projection_FULL.py').write_bytes(new_test)
    print('PHASE172_R3R2_HEAD=' + state['head'], flush=True)
    print('PHASE172_R3R2_SOURCE_GUARD=PASS', flush=True)
    print('PHASE172_R3R2_REPORT=' + str(output), flush=True)
    if args.dry_run:
        print('PHASE172_R3R2_DRY_RUN=PASS', flush=True)
        print('PHASE172_R3R2_SOURCE_CHANGES=0', flush=True)
        return 0
    if not args.run_focused_tests:
        raise RuntimeError('apply requires --run-focused-tests')
    report = {'phase': '172-R3R2', 'state': state,
              'proof_tree_modified': False, 'math_rules_modified': False,
              'full_pytest_executed': False}
    try:
        (ROOT / TEST_FILE).write_bytes(new_test)
        local_tests(output)
        env = os.environ.copy()
        env['PYTHONUTF8'] = '1'
        env['PYTHONIOENCODING'] = 'utf-8'
        env['PYTHONDONTWRITEBYTECODE'] = '1'
        env['PYTHONPATH'] = str(ROOT) + os.pathsep + env.get('PYTHONPATH', '')
        proc = subprocess.run(
            [sys.executable, '-B', '-m', 'phase172_r3_hopf_chain_display.install',
             '--run-focused-tests'],
            cwd=ROOT, env=env, capture_output=True, text=True, encoding='utf-8',
            errors='replace', check=False, timeout=1100,
        )
        (output / 'r3_run.log').write_text(proc.stdout + '\n' + proc.stderr, encoding='utf-8')
        if proc.stdout:
            print(proc.stdout.rstrip(), flush=True)
        if proc.returncode:
            raise RuntimeError('R3 runner failed: ' + proc.stderr[-3000:])
        if 'PHASE172_R3_RESULT=PASS_R3_HOPF_DISPLAY_ONLY' not in proc.stdout:
            raise RuntimeError('R3 runner returned no completion marker')
        report['result'] = 'PASS_R3R2_AND_R3'
        report['r3_result'] = 'PASS_R3_HOPF_DISPLAY_ONLY'
    except BaseException as error:
        (ROOT / TEST_FILE).write_bytes(old_test)
        (ROOT / RENDERER).write_bytes(old_renderer)
        report['result'] = 'FAILED_RESTORED'
        report['diagnostic'] = repr(error)
        (output / 'result.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print('PHASE172_R3R2_RESTORED=PASS', flush=True)
        raise
    (output / 'result.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('PHASE172_R3R2_SOURCE_CHANGES=2', flush=True)
    print('PHASE172_R3R2_RESULT=PASS_R3R2_AND_R3', flush=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())

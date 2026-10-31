"""Guarded Phase 172 R4 presentation-only patch with focused tests/rollback."""
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

from phase172_r3_hopf_chain_display import install as r3_installer

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent
TARGET = Path('phase168_r3_5_model_renderer.py')
PROJECTION = Path('phase172_r4_hopf_surjectivity_display/projection.py')
TESTS = Path('phase172_r4_hopf_surjectivity_display/tests/test_projection.py')
BASE_R2_BLOB = 'bb267bc669bdcaa5b9dcc24bdf7dc8b2ac4e7c95'
R3_PROJECTION_SHA256 = 'fae04a1f9e5c0a2408e8cc29180bfe64c14b8376186ba78b168db270e2e55413'
R3_TEST_SHA256 = '843f889791b3a447051edfd1c22d58208cbe78e481d048c0e998443f12e8e9b6'
R3_INSTALL_SHA256 = 'ee16868581a8496acbb76873d8c3ff39587b5b3297e7fa23040effd594ea6c8a'
OLD = (
    '        if hopf_display is not None:\n'
    '            suppressed_body_indices.update(hopf_display.hidden_indices)\n'
    '    for index in order:\n'
)
NEW = (
    '        if hopf_display is not None:\n'
    '            suppressed_body_indices.update(hopf_display.hidden_indices)\n'
    '    if not incomplete:\n'
    '        from phase172_r4_hopf_surjectivity_display.projection import (\n'
    '            redundant_hopf_surjectivity_indices,\n'
    '        )\n'
    '        suppressed_body_indices.update(\n'
    '            redundant_hopf_surjectivity_indices(\n'
    '                model, order, suppressed_body_indices,\n'
    '            )\n'
    '        )\n'
    '    for index in order:\n'
)
TEST_GROUPS = (
    ('phase172_r4_hopf_surjectivity_display/tests/test_projection.py',),
    ('phase172_r3_hopf_chain_display/tests/test_projection.py',),
    ('phase172_r2_suspension_relation_display/tests/test_projection.py',),
    ('phase171_r20r13_eta_sentence_layout/tests/test_projection.py',),
    ('phase171_r20r12_verified_cyclic_narrative/tests/test_projection.py',),
    ('phase169_r4d_pi64_narrative_audit/tests/test_r4d_narrative_audit.py',),
)


def run_command(args: list[str], *, timeout: int = 45) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args, cwd=ROOT, capture_output=True, text=True,
        encoding='utf-8', errors='replace', check=False, timeout=timeout,
    )


def checked(*args: str) -> str:
    process = run_command(list(args))
    if process.returncode:
        raise RuntimeError('command failed: ' + repr(args) + ' ' + process.stderr[-1000:])
    return process.stdout.strip()


def normalized(raw: bytes) -> str:
    result = raw.decode('utf-8-sig')
    if '\r' in result.replace('\r\n', ''):
        raise RuntimeError('mixed newline convention in guarded source')
    return result.replace('\r\n', '\n')


def updated_renderer(raw: bytes) -> bytes:
    old = normalized(raw)
    if old.count(OLD) != 1 or NEW in old:
        raise RuntimeError('R3 Renderer insertion anchor changed')
    new = old.replace(OLD, NEW, 1)
    tree = ast.parse(new)
    matches = [node for node in tree.body
               if isinstance(node, ast.FunctionDef)
               and node.name == 'render_model_backed_narrative_markdown']
    if len(matches) != 1:
        raise RuntimeError('Renderer function identity changed')
    newline = '\r\n' if b'\r\n' in raw else '\n'
    return new.replace('\n', newline).encode('utf-8')


def full_renderer_function(raw: bytes) -> str:
    source = normalized(raw)
    tree = ast.parse(source)
    matches = [node for node in tree.body
               if isinstance(node, ast.FunctionDef)
               and node.name == 'render_model_backed_narrative_markdown']
    if len(matches) != 1:
        raise RuntimeError('Renderer function not uniquely present')
    node = matches[0]
    return '\n'.join(source.splitlines()[node.lineno - 1:node.end_lineno]) + '\n'


def preflight() -> dict[str, str | None]:
    branch = checked('git', 'branch', '--show-current')
    head = checked('git', 'rev-parse', 'HEAD')
    if branch != 'develop':
        raise RuntimeError('R4 requires develop')
    original = subprocess.run(
        ['git', 'cat-file', 'blob', BASE_R2_BLOB], cwd=ROOT,
        capture_output=True, check=True,
    ).stdout
    if r3_installer.REVIEWED_GIT_BLOB != BASE_R2_BLOB:
        raise RuntimeError('R3 reviewed baseline changed')
    expected_r3 = r3_installer.transformed(original)
    current = (ROOT / TARGET).read_bytes()
    if normalized(current) != normalized(expected_r3):
        raise RuntimeError('R3 applied Renderer differs from the reviewed R2->R3 transformation')
    committed = subprocess.run(
        ['git', 'show', 'HEAD:' + TARGET.as_posix()], cwd=ROOT,
        capture_output=True, check=True,
    ).stdout
    if normalized(committed) == normalized(expected_r3):
        renderer_state = 'R3_COMMITTED'
    elif normalized(committed) == normalized(original):
        renderer_state = 'R3_UNCOMMITTED'
    else:
        raise RuntimeError('committed Renderer is neither reviewed R2 nor R3')
    for path, expected in (
        (Path('phase172_r3_hopf_chain_display/projection.py'), R3_PROJECTION_SHA256),
        (Path('phase172_r3_hopf_chain_display/tests/test_projection.py'), R3_TEST_SHA256),
        (Path('phase172_r3_hopf_chain_display/install.py'), R3_INSTALL_SHA256),
    ):
        if not (ROOT / path).is_file():
            raise RuntimeError('missing R3 prerequisite: ' + str(path))
        if hashlib.sha256((ROOT / path).read_bytes()).hexdigest() != expected:
            raise RuntimeError('R3 prerequisite payload differs: ' + str(path))
    r2_test = ROOT / 'phase172_r2_suspension_relation_display/tests/test_projection.py'
    if not r2_test.is_file():
        raise RuntimeError('missing R2 regression test')
    updated_r2_test = normalized(r2_test.read_bytes())
    if (r'''    assert r"$\nu'\eta_{6} = \nu'E\eta_{5}$." in body''' in updated_r2_test
            or 'assert "[R4] Proposition 2.2." in references' not in updated_r2_test
            or 'assert "[R5] (5.3)." in references' not in updated_r2_test):
        raise RuntimeError('R3R2 corrected R2 test contract is absent')
    for path in (PROJECTION, TESTS):
        if not (ROOT / path).is_file():
            raise RuntimeError('R4 payload is missing: ' + str(path))
    updated_renderer(current)
    remote = run_command(['git', 'ls-remote', 'origin', 'refs/heads/develop'], timeout=25)
    remote_head = remote.stdout.split()[0] if remote.returncode == 0 and remote.stdout.strip() else None
    if remote_head is not None and remote_head != head:
        raise RuntimeError('local HEAD differs from origin/develop')
    return {'branch': branch, 'head': head, 'remote_head': remote_head,
            'renderer_state': renderer_state,
            'before_sha256': hashlib.sha256(current).hexdigest()}


def report_directory() -> Path:
    base = Path(os.environ.get('LOCALAPPDATA') or Path.home()) / 'EHPProofTracerRecovery'
    result = base / ('phase172_r4_' + datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%fZ'))
    result.mkdir(parents=True, exist_ok=False)
    return result


def focused_tests(destination: Path) -> list[dict[str, object]]:
    env = os.environ.copy()
    env['PYTHONUTF8'] = '1'
    env['PYTHONIOENCODING'] = 'utf-8'
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    env['PYTHONPATH'] = str(ROOT) + os.pathsep + env.get('PYTHONPATH', '')
    reports = []
    for number, paths in enumerate(TEST_GROUPS, 1):
        process = subprocess.run(
            [sys.executable, '-B', '-m', 'pytest', '-q', '--tb=short',
             '-p', 'no:cacheprovider', *paths],
            cwd=ROOT, capture_output=True, text=True,
            encoding='utf-8', errors='replace', env=env, timeout=240,
        )
        content = process.stdout + '\n' + process.stderr
        (destination / f'focused_{number}.log').write_text(content, encoding='utf-8')
        reports.append({'group': number, 'paths': list(paths),
                        'exit_code': process.returncode})
        print(f'PHASE172_R4_FOCUSED_{number}=' +
              ('PASS' if process.returncode == 0 else 'FAIL'), flush=True)
        if process.returncode != 0:
            raise RuntimeError(f'focused pytest group {number} failed:\n' + content[-2500:])
    return reports


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--run-focused-tests', action='store_true')
    options = parser.parse_args()
    if not options.dry_run and not options.run_focused_tests:
        raise RuntimeError('R4 application requires --run-focused-tests')
    state = preflight()
    print('PHASE172_R4_BRANCH=' + state['branch'], flush=True)
    print('PHASE172_R4_HEAD=' + state['head'], flush=True)
    print('PHASE172_R4_R3_RENDERER_STATE=' + state['renderer_state'], flush=True)
    print('PHASE172_R4_REVIEWED_CONTENT=PASS', flush=True)
    before = (ROOT / TARGET).read_bytes()
    after = updated_renderer(before)
    output = report_directory()
    (output / 'render_model_backed_narrative_markdown_FULL.py').write_text(
        full_renderer_function(after), encoding='utf-8',
    )
    (output / 'phase168_r3_5_model_renderer_FULL.py').write_bytes(after)
    if options.dry_run:
        print('PHASE172_R4_DRY_RUN=PASS', flush=True)
        print('PHASE172_R4_FULL_FUNCTION=' + str(output), flush=True)
        print('PHASE172_R4_SOURCE_CHANGES=0', flush=True)
        return 0
    (output / 'renderer_before.py').write_bytes(before)
    report = {'phase': '172-R4', 'mode': 'PRESENTATION_ONLY',
              'state': state, 'full_pytest_executed': False,
              'proof_tree_modified': False, 'mathematical_rules_modified': False,
              'focused_tests': []}
    try:
        (ROOT / TARGET).write_bytes(after)
        report['focused_tests'] = focused_tests(output)
        report['result'] = 'PASS_R4_SURJECTIVITY_DISPLAY_ONLY'
    except BaseException as exc:
        (ROOT / TARGET).write_bytes(before)
        report['result'] = 'FAIL_RESTORED_SOURCE'
        report['exception'] = repr(exc)
        (output / 'result.json').write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8',
        )
        print('PHASE172_R4_RESTORED=PASS', flush=True)
        print('PHASE172_R4_REPORT=' + str(output), flush=True)
        raise
    (output / 'result.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8',
    )
    print('PHASE172_R4_REPORT=' + str(output), flush=True)
    print('PHASE172_R4_SOURCE_CHANGES=1', flush=True)
    print('PHASE172_R4_RESULT=PASS_R4_SURJECTIVITY_DISPLAY_ONLY', flush=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())

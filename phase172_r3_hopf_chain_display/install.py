"""Phase 172 R3: guarded, reversible single-function presentation update."""
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

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
TARGET = Path('phase168_r3_5_model_renderer.py')
PROJECTION = Path('phase172_r3_hopf_chain_display/projection.py')
TEST = Path('phase172_r3_hopf_chain_display/tests/test_projection.py')
REVIEWED_GIT_BLOB = 'bb267bc669bdcaa5b9dcc24bdf7dc8b2ac4e7c95'
R2_GIT_BLOB = 'bba6280a36ca1c094be1b2a65d94ba0d2582c7a1'
REVIEWED_PROJECTION_SHA256 = 'fae04a1f9e5c0a2408e8cc29180bfe64c14b8376186ba78b168db270e2e55413'
REVIEWED_TEST_SHA256 = '843f889791b3a447051edfd1c22d58208cbe78e481d048c0e998443f12e8e9b6'
OLD_BEFORE_LOOP = (
    '    if not incomplete:\n'
    '        from phase172_r2_suspension_relation_display.projection import (\n'
    '            redundant_suspension_relation_indices,\n'
    '        )\n'
    '        suppressed_body_indices.update(\n'
    '            redundant_suspension_relation_indices(\n'
    '                model, order, suppressed_body_indices,\n'
    '            )\n'
    '        )\n'
    '    for index in order:\n'
)
NEW_BEFORE_LOOP = (
    '    if not incomplete:\n'
    '        from phase172_r2_suspension_relation_display.projection import (\n'
    '            redundant_suspension_relation_indices,\n'
    '        )\n'
    '        suppressed_body_indices.update(\n'
    '            redundant_suspension_relation_indices(\n'
    '                model, order, suppressed_body_indices,\n'
    '            )\n'
    '        )\n'
    '    hopf_display = None\n'
    '    if not incomplete:\n'
    '        from phase172_r3_hopf_chain_display.projection import (\n'
    '            project_verified_hopf_chain,\n'
    '        )\n'
    '        hopf_display = project_verified_hopf_chain(\n'
    '            model, order, suppressed_body_indices,\n'
    '        )\n'
    '        if hopf_display is not None:\n'
    '            suppressed_body_indices.update(hopf_display.hidden_indices)\n'
    '    for index in order:\n'
)
OLD_IN_LOOP = (
    '        if index in suppressed_body_indices:\n'
    '            continue\n'
    '        step = model.steps[index]\n'
)
NEW_IN_LOOP = (
    '        if index in suppressed_body_indices:\n'
    '            continue\n'
    '        if hopf_display is not None and index in (\n'
    '            hopf_display.formula_index, hopf_display.image_index,\n'
    '        ):\n'
    '            latex, fallback = _group_proof_statement_latex(\n'
    '                model.steps[index].conclusion,\n'
    '            )\n'
    '            if latex is None or fallback is not None:\n'
    '                raise ValueError("verified Hopf line cannot be rendered")\n'
    '            numbers = (\n'
    '                hopf_display.formula_citations\n'
    '                if index == hopf_display.formula_index\n'
    '                else hopf_display.image_citations\n'
    '            )\n'
    '            source_tags = ", ".join(f"[R{number}]" for number in numbers)\n'
    '            lines.extend((f"{source_tags}より, ${latex}$.", ""))\n'
    '            continue\n'
    '        step = model.steps[index]\n'
)
TEST_GROUPS = (
    ('phase172_r3_hopf_chain_display/tests/test_projection.py',),
    ('phase172_r2_suspension_relation_display/tests/test_projection.py',),
    ('phase171_r20r13_eta_sentence_layout/tests/test_projection.py',),
    ('phase171_r20r12_verified_cyclic_narrative/tests/test_projection.py',),
    ('phase169_r4d_pi64_narrative_audit/tests/test_r4d_narrative_audit.py',),
)


def command(args: list[str], *, timeout: int = 60) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args, cwd=ROOT, capture_output=True, text=True, encoding='utf-8',
        errors='replace', check=False, timeout=timeout,
    )


def checked(args: list[str]) -> str:
    result = command(args)
    if result.returncode:
        raise RuntimeError('command failed: ' + repr(args) + ' ' + result.stderr[-900:])
    return result.stdout.strip()


def normalized(raw: bytes) -> str:
    data = raw.decode('utf-8-sig')
    if '\r' in data.replace('\r\n', ''):
        raise RuntimeError('mixed newlines are unsupported')
    return data.replace('\r\n', '\n')


def git_blob(raw: bytes) -> str:
    header = b'blob ' + str(len(raw)).encode('ascii') + b'\0'
    return hashlib.sha1(header + raw).hexdigest()


def transformed(raw: bytes) -> bytes:
    source = normalized(raw)
    if (source.count(OLD_BEFORE_LOOP) != 1
            or source.count(OLD_IN_LOOP) != 1
            or NEW_BEFORE_LOOP in source
            or NEW_IN_LOOP in source):
        raise RuntimeError('reviewed R2 Renderer anchors are not unique')
    replaced = source.replace(OLD_BEFORE_LOOP, NEW_BEFORE_LOOP, 1)
    replaced = replaced.replace(OLD_IN_LOOP, NEW_IN_LOOP, 1)
    tree = ast.parse(replaced)
    functions = [node for node in tree.body
                 if isinstance(node, ast.FunctionDef)
                 and node.name == 'render_model_backed_narrative_markdown']
    if len(functions) != 1:
        raise RuntimeError('expected exactly one Renderer function')
    ending = '\r\n' if b'\r\n' in raw else '\n'
    return replaced.replace('\n', ending).encode('utf-8')


def full_function(raw: bytes) -> str:
    source = normalized(raw)
    tree = ast.parse(source)
    functions = [node for node in tree.body
                 if isinstance(node, ast.FunctionDef)
                 and node.name == 'render_model_backed_narrative_markdown']
    if len(functions) != 1:
        raise RuntimeError('Renderer function missing/ambiguous')
    node = functions[0]
    return '\n'.join(source.splitlines()[node.lineno-1:node.end_lineno]) + '\n'


def preflight() -> dict[str, str | None]:
    branch = checked(['git', 'branch', '--show-current'])
    head = checked(['git', 'rev-parse', 'HEAD'])
    if branch != 'develop':
        raise RuntimeError('R3 requires develop')
    blob = checked(['git', 'rev-parse', 'HEAD:' + TARGET.as_posix()])
    if blob != REVIEWED_GIT_BLOB:
        raise RuntimeError('committed Renderer differs from reviewed R2 source')
    r2_blob = checked(['git', 'rev-parse', 'HEAD:phase172_r2_suspension_relation_display/projection.py'])
    if r2_blob != R2_GIT_BLOB:
        raise RuntimeError('committed R2 typed comparison differs from reviewed source')
    work_status = checked(['git', 'status', '--porcelain=v1', '--', TARGET.as_posix()])
    if work_status:
        raise RuntimeError('Renderer has local changes; not overwriting')
    tracked = subprocess.run(
        ['git', 'show', 'HEAD:' + TARGET.as_posix()], cwd=ROOT,
        check=True, capture_output=True,
    ).stdout
    actual = (ROOT / TARGET).read_bytes()
    if normalized(tracked) != normalized(actual):
        raise RuntimeError('worktree Renderer differs from HEAD')
    for path, expected_sha in (
        (PROJECTION, REVIEWED_PROJECTION_SHA256),
        (TEST, REVIEWED_TEST_SHA256),
    ):
        if not (ROOT / path).is_file():
            raise RuntimeError('R3 package file missing: ' + str(path))
        if hashlib.sha256((ROOT / path).read_bytes()).hexdigest() != expected_sha:
            raise RuntimeError('R3 package payload differs from reviewed content: ' + str(path))
    remote = command(['git', 'ls-remote', 'origin', 'refs/heads/develop'], timeout=25)
    remote_head = remote.stdout.split()[0] if remote.returncode == 0 and remote.stdout.strip() else None
    if remote_head is not None and remote_head != head:
        raise RuntimeError('origin/develop changed; review updated HEAD first')
    transformed(actual)
    return {
        'branch': branch, 'head': head, 'remote_develop': remote_head,
        'head_renderer_blob': blob, 'r2_projection_blob': r2_blob,
        'worktree_renderer_sha256': hashlib.sha256(actual).hexdigest(),
    }


def report_dir() -> Path:
    base = Path(os.environ.get('LOCALAPPDATA') or Path.home()) / 'EHPProofTracerRecovery'
    stamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%fZ')
    path = base / ('phase172_r3_' + stamp)
    path.mkdir(parents=True, exist_ok=False)
    return path


def run_focused(output: Path) -> list[dict[str, object]]:
    env = os.environ.copy()
    env['PYTHONUTF8'] = '1'
    env['PYTHONIOENCODING'] = 'utf-8'
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    env['PYTHONPATH'] = str(ROOT) + os.pathsep + env.get('PYTHONPATH', '')
    tested = []
    for number, paths in enumerate(TEST_GROUPS, 1):
        run = subprocess.run(
            [sys.executable, '-B', '-m', 'pytest', '-q', '--tb=short',
             '-p', 'no:cacheprovider', *paths],
            cwd=ROOT, env=env, capture_output=True, text=True,
            encoding='utf-8', errors='replace', check=False, timeout=200,
        )
        log = run.stdout + '\n' + run.stderr
        (output / f'focused_{number}.log').write_text(log, encoding='utf-8')
        tested.append({'number': number, 'paths': list(paths),
                       'exit_code': run.returncode,
                       'last_lines': log.splitlines()[-15:]})
        print(f'PHASE172_R3_FOCUSED_{number}=' +
              ('PASS' if run.returncode == 0 else 'FAIL'), flush=True)
        if run.returncode:
            raise RuntimeError('focused pytest failed: ' + str(number) + '\n' + log[-2200:])
    return tested


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--run-focused-tests', action='store_true')
    args = parser.parse_args()
    state = preflight()
    print('PHASE172_R3_BRANCH=' + str(state['branch']), flush=True)
    print('PHASE172_R3_HEAD=' + str(state['head']), flush=True)
    print('PHASE172_R3_REVIEWED_SOURCE=PASS', flush=True)
    before = (ROOT / TARGET).read_bytes()
    after = transformed(before)
    output = report_dir()
    (output / 'render_model_backed_narrative_markdown_FULL.py').write_text(
        full_function(after), encoding='utf-8',
    )
    (output / 'phase168_r3_5_model_renderer_FULL.py').write_bytes(after)
    if args.dry_run:
        print('PHASE172_R3_DRY_RUN=PASS', flush=True)
        print('PHASE172_R3_FULL_FUNCTION=' + str(output), flush=True)
        print('PHASE172_R3_SOURCE_CHANGES=0', flush=True)
        return 0
    (output / 'renderer_before.py').write_bytes(before)
    report: dict[str, object] = {
        'phase': '172-R3', 'mode': 'GUARDED_PRESENTATION_ONLY',
        'state': state, 'full_pytest_executed': False,
        'proof_tree_modified': False, 'mathematical_rules_modified': False,
        'focused': [],
    }
    try:
        (ROOT / TARGET).write_bytes(after)
        if args.run_focused_tests:
            report['focused'] = run_focused(output)
        report['result'] = 'PASS_R3_HOPF_DISPLAY_ONLY'
    except BaseException as error:
        (ROOT / TARGET).write_bytes(before)
        report['result'] = 'FAILED_RESTORED_SOURCE'
        report['diagnostic'] = repr(error)
        (output / 'result.json').write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8',
        )
        print('PHASE172_R3_RESTORED=PASS', flush=True)
        print('PHASE172_R3_REPORT=' + str(output), flush=True)
        raise
    (output / 'result.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8',
    )
    print('PHASE172_R3_REPORT=' + str(output), flush=True)
    print('PHASE172_R3_SOURCE_CHANGES=1', flush=True)
    print('PHASE172_R3_RESULT=PASS_R3_HOPF_DISPLAY_ONLY', flush=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())

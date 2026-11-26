"""Install a single reviewed complete-renderer hook and export full source."""
from __future__ import annotations

import ast
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BASE = 'd04df08c5bef102da7d6a7e23ddade18395e61a0'
TARGET = 'phase168_r3_5_model_renderer.py'
ANCHOR = '        lines, _ = project_suspension_composition_display(lines, model, protected_equalities)\n'
HOOK = ('        from phase178_r12r1_suspension_composition_display.projection import (\n'
        '            project_zero_suspension_composition,\n'
        '        )\n'
        '        lines = project_zero_suspension_composition(lines, model, protected_equalities)\n')


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def gt(*args):
    return git(*args).decode('utf-8').strip()


def normalize(raw):
    return raw.decode('utf-8-sig').replace('\r\n', '\n')


def proposed_source(source):
    tree = ast.parse(source)
    function, = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'render_model_backed_narrative_markdown']
    lines = source.splitlines(keepends=True)
    body = ''.join(lines[function.lineno - 1:function.end_lineno])
    require(body.count(ANCHOR) == 1 and HOOK not in source, 'RENDERER_ANCHOR_MISMATCH')
    updated = ''.join(lines[:function.lineno - 1]) + body.replace(ANCHOR, ANCHOR + HOOK, 1) + ''.join(lines[function.end_lineno:])
    ast.parse(updated)
    return updated


def full_review_source(source):
    lines = source.splitlines(keepends=True)
    nodes = [n for n in ast.parse(source).body if isinstance(n, (ast.Import, ast.ImportFrom)) or (isinstance(n, ast.FunctionDef) and n.name == 'render_model_backed_narrative_markdown')]
    return '\n'.join(''.join(lines[n.lineno - 1:n.end_lineno]) for n in nodes) + '\n'


def preflight():
    require(Path(gt('rev-parse', '--show-toplevel')).resolve() == ROOT, 'WRONG_ROOT')
    head = gt('rev-parse', 'HEAD')
    require(gt('branch', '--show-current') == 'develop' and head == BASE == gt('rev-parse', 'origin/develop'), 'REVIEWED_HEAD_REQUIRED')
    require(not gt('diff', '--cached', '--name-only'), 'STAGED_CHANGES_REFUSED')
    require(not set(gt('diff', '--name-only', 'HEAD').splitlines()) - {TARGET}, 'UNRELATED_TRACKED_CHANGES')
    require(not os.environ.get('PYTEST_ADDOPTS', '').strip(), 'PYTEST_ADDOPTS_REQUIRES_REVIEW')
    require(gt('rev-parse', 'HEAD:' + TARGET) == '9afd21ed344beea80699f49cba16ddd68197198b', 'RENDERER_BLOB_CHANGED')
    original = normalize(git('show', 'HEAD:' + TARGET))
    revised = proposed_source(original)
    current = (ROOT / TARGET).read_bytes()
    require(normalize(current) in (original, revised), 'UNREVIEWED_RENDERER_CHANGE')
    rest = current.replace(b'\r\n', b'')
    require(b'\r' not in rest and not (b'\r\n' in current and b'\n' in rest), 'MIXED_EOL')
    eol = '\r\n' if b'\r\n' in current else '\n'
    encoding = 'utf-8-sig' if current.startswith(b'\xef\xbb\xbf') else 'utf-8'
    return head, current, revised.replace('\n', eol).encode(encoding), revised

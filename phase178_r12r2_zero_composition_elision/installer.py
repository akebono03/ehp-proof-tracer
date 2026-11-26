"""Install a minimal post-normalization display-only hook."""
from __future__ import annotations

import ast
import os
from pathlib import Path
from phase178_r12r1_suspension_composition_display.installer import (
    ROOT, TARGET, git, gt, normalize, require, full_review_source,
)

BASE = 'd796ba7a9a8a32d458163f261cd8e19e60f5b949'
ANCHOR = '        lines = project_zero_suspension_composition(lines, model, protected_equalities)\n'
HOOK = ('        before_zero_composition = list(lines)\n' + ANCHOR
        + '        from phase178_r12r2_zero_composition_elision.projection import project_zero_composition_elision\n'
        + '        lines, _ = project_zero_composition_elision(before_zero_composition, lines, model, protected_equalities)\n')


def proposed_source(source):
    lines = source.splitlines(keepends=True)
    function, = [n for n in ast.parse(source).body if isinstance(n, ast.FunctionDef) and n.name == 'render_model_backed_narrative_markdown']
    body = ''.join(lines[function.lineno - 1:function.end_lineno])
    require(body.count(ANCHOR) == 1 and 'project_zero_composition_elision' not in source, 'RENDERER_ANCHOR_MISMATCH')
    revised = ''.join(lines[:function.lineno - 1]) + body.replace(ANCHOR, HOOK, 1) + ''.join(lines[function.end_lineno:])
    ast.parse(revised)
    return revised


def preflight():
    require(Path(gt('rev-parse', '--show-toplevel')).resolve() == ROOT, 'WRONG_ROOT')
    head = gt('rev-parse', 'HEAD')
    require(gt('branch', '--show-current') == 'develop' and head == gt('rev-parse', 'origin/develop'), 'HEAD_OR_BRANCH_MISMATCH')
    require(gt('merge-base', BASE, head) == BASE and not gt('diff', '--name-only', BASE, head), 'REVIEWED_TREE_REQUIRED')
    require(not gt('diff', '--cached', '--name-only'), 'STAGED_CHANGES_REFUSED')
    require(not set(gt('diff', '--name-only', 'HEAD').splitlines()) - {TARGET}, 'UNRELATED_TRACKED_CHANGES')
    require(not os.environ.get('PYTEST_ADDOPTS', '').strip(), 'PYTEST_ADDOPTS_REQUIRES_REVIEW')
    require(gt('rev-parse', 'HEAD:' + TARGET) == 'cb9026fb04c0f85983d14c757eec1de706e02d1b', 'RENDERER_BLOB_CHANGED')
    original = normalize(git('show', 'HEAD:' + TARGET))
    revised = proposed_source(original)
    current = (ROOT / TARGET).read_bytes()
    require(normalize(current) in (original, revised), 'UNREVIEWED_RENDERER_CHANGE')
    rest = current.replace(b'\r\n', b'')
    require(b'\r' not in rest and not (b'\r\n' in current and b'\n' in rest), 'MIXED_EOL')
    eol = '\r\n' if b'\r\n' in current else '\n'
    encoding = 'utf-8-sig' if current.startswith(b'\xef\xbb\xbf') else 'utf-8'
    return head, current, revised.replace('\n', eol).encode(encoding), revised

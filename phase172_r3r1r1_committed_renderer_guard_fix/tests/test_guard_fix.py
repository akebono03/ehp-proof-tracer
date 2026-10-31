"""Independent focused checks of the reviewed R3R1 renderer-state guard."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase172_r2_suspension_relation_display.install import transformed

ROOT = Path(__file__).resolve().parents[2]
REVIEWED_ORIGINAL = '94996b403f1c01f81319824565db422463714f02'
REVIEWED_COMMITTED = 'bb267bc669bdcaa5b9dcc24bdf7dc8b2ac4e7c95'


def guard():
    path = ROOT / 'phase172_r3r1r1_committed_renderer_guard_fix/corrected_audit_FULL.py'
    tree = ast.parse(path.read_text(encoding='utf-8'))
    nodes = [node for node in tree.body if isinstance(node, ast.FunctionDef)
             and node.name in ('normalize', 'reviewed_renderer_installation')]
    assert len(nodes) == 2
    space = {
        'EXPECTED_HEAD_RENDERER_BLOB': REVIEWED_ORIGINAL,
        'EXPECTED_COMMITTED_R2_RENDERER_BLOB': REVIEWED_COMMITTED,
    }
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(path), 'exec'), space)
    return space['reviewed_renderer_installation']


def original():
    return (
        'def render_model_backed_narrative_markdown():\n'
        '    if direct_sum_display is not None:\n'
        '        suppressed_body_indices.update(direct_sum_display.hidden_indices)\n'
        '    for index in order:\n'
        '        pass\n'
    ).encode('utf-8')


def test_committed_r2_content_is_accepted_only_as_exact_match():
    before = original()
    after = transformed(before)
    assert guard()(REVIEWED_COMMITTED, after, after) == 'COMMITTED_R2_PATCH'


def test_uncommitted_r2_content_is_accepted_when_patched():
    before = original()
    after = transformed(before)
    assert guard()(REVIEWED_ORIGINAL, before, after) == 'UNCOMMITTED_R2_PATCH'


def test_worktree_change_is_rejected_even_if_r2_committed():
    after = transformed(original())
    with pytest.raises(RuntimeError, match='worktree differs'):
        guard()(REVIEWED_COMMITTED, after, after + b'# unrelated\n')


def test_missing_r2_hook_is_rejected_for_committed_case():
    before = original()
    with pytest.raises(RuntimeError, match='missing the reviewed display hook'):
        guard()(REVIEWED_COMMITTED, before, before)


def test_unknown_committed_blob_is_rejected():
    after = transformed(original())
    with pytest.raises(RuntimeError, match='neither reviewed baseline'):
        guard()('0000000000000000000000000000000000000000', after, after)


def test_windows_crlf_worktree_is_accepted_for_committed_case():
    after = transformed(original())
    assert guard()(REVIEWED_COMMITTED, after, after.replace(b'\n', b'\r\n')) == 'COMMITTED_R2_PATCH'

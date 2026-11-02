"""Offline tests: patch preflight remains fail-closed without repository imports."""
from __future__ import annotations

from hashlib import sha1
from pathlib import Path
import ast

import pytest

from phase173_r4_r1_diagonal_inference_fix.install import (
    EXPECTED_BLOB, EXPECTED_PATCH_SHA256,
    blob_hash,
    normalize_line_endings,
    proposed_bytes,
)


def test_blob_hash_uses_git_encoding() -> None:
    raw = b'abc'
    assert blob_hash(raw) == sha1(b'blob 3\x00abc').hexdigest()


def test_original_reviewed_blob_is_pinned() -> None:
    assert EXPECTED_BLOB == 'e05ada41cbcf53e8b755428afd245ba2da619fa8'


def test_newline_normalization() -> None:
    assert normalize_line_endings(b'a\r\nb\r\n') == b'a\nb\n'


def test_patch_file_is_complete_and_scoped() -> None:
    root = Path(__file__).resolve().parents[2]
    content = proposed_bytes(root)
    tree = ast.parse(content.decode('utf8'))
    functions = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
    assert 'expand_source_bound_toda56' in functions
    assert 'source_bound_toda56_rule' in functions
    assert content.count(b'SourceBoundGoal(diagonal, diagonal_source)') == 1
    from hashlib import sha256
    assert sha256(content).hexdigest() == EXPECTED_PATCH_SHA256


def test_missing_payload_fails_closed(tmp_path: Path) -> None:
    with pytest.raises(RuntimeError, match='missing'):
        proposed_bytes(tmp_path)


def test_non_scoped_payload_fails_closed(tmp_path: Path) -> None:
    file = tmp_path / 'phase173_r4_r1_diagonal_inference_fix' / 'replacement_rule.py'
    file.parent.mkdir()
    file.write_text('def missing(): return 1\n', encoding='utf8')
    with pytest.raises(RuntimeError, match='scoped diagonal'):
        proposed_bytes(tmp_path)


def test_altered_but_similarly_named_payload_is_rejected(tmp_path: Path) -> None:
    file = tmp_path / 'phase173_r4_r1_diagonal_inference_fix' / 'replacement_rule.py'
    file.parent.mkdir()
    file.write_text('SourceBoundGoal(diagonal, diagonal_source)\n', encoding='utf8')
    with pytest.raises(RuntimeError, match='differs from the reviewed patch'):
        proposed_bytes(tmp_path)

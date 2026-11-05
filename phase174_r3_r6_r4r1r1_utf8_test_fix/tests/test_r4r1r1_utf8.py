"""Isolated guard tests for the UTF-8-only regression fix."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase174_r3_r6_r4r1r1_utf8_test_fix.patch import (
    AFTER_SHA256,
    BEFORE_SHA256,
    PACKAGE,
    digest,
    restore_format,
    review_patch,
)


def _baseline() -> bytes:
    reviewed = PACKAGE.parent / "phase174_r3_r6_r4r1_cited_reference_link_fix"
    return (reviewed / "tests" / "test_r4r1_guard.py").read_bytes()


def test_only_implicit_encoding_reads_changed_in_one_function() -> None:
    original = (PACKAGE / "output" / "test_r4r1_guard_FULL.py").read_text(encoding="utf-8")
    tree = ast.parse(original)
    functions = {node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)}
    assert "test_source_formula_is_shared_between_two_reviewed_reference_paths" in functions
    assert original.count('.read_text(encoding="utf-8")') == 4
    assert ".read_text()" not in original


def test_reviewed_hash_and_idempotency() -> None:
    candidate = (PACKAGE / "output" / "test_r4r1_guard_FULL.py").read_bytes()
    assert digest(candidate) == AFTER_SHA256
    assert review_patch(candidate) == candidate
    assert AFTER_SHA256 != BEFORE_SHA256


def test_rejects_unreviewed_edited_test() -> None:
    candidate = (PACKAGE / "output" / "test_r4r1_guard_FULL.py").read_bytes()
    with pytest.raises(ValueError, match="Unreviewed test content"):
        review_patch(candidate + b"# unreviewed local note\n")


def test_retains_windows_crlf_bom() -> None:
    sample = b"\xef\xbb\xbf" + b"first\r\nsecond\r\n"
    assert restore_format(sample, b"first\nthird\n") == b"\xef\xbb\xbffirst\r\nthird\r\n"


def test_imported_test_module_uses_explicit_utf8_only() -> None:
    target = (PACKAGE / "output" / "test_r4r1_guard_FULL.py").read_text(encoding="utf-8")
    tree = ast.parse(target)
    fn = next(node for node in tree.body if isinstance(node, ast.FunctionDef)
              and node.name == "test_source_formula_is_shared_between_two_reviewed_reference_paths")
    segment = "\n".join(target.splitlines()[fn.lineno - 1:fn.end_lineno])
    assert segment.count('.read_text(encoding="utf-8")') == 2
    assert '.read_text()' not in segment

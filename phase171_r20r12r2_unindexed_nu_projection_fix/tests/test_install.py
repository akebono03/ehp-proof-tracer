"""Content guard and line-ending preservation for the single-file correction."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase171_r20r12r2_unindexed_nu_projection_fix.install import (
    EXPECTED_ORIGINAL_SHA256, corrected_source, sha256,
)


def _old_bytes() -> bytes:
    package = Path(__file__).resolve().parent.parent
    return (package / "original_projection.py.reviewed").read_bytes()


def test_reviewed_original_projection_digest():
    assert sha256(_old_bytes()) == EXPECTED_ORIGINAL_SHA256


def test_single_line_change_and_parse():
    before = _old_bytes().decode("utf-8")
    after = corrected_source(_old_bytes()).decode("utf-8")
    ast.parse(after)
    assert before.count("    element = element_tex(order.element)\n") == 1
    assert after.count("    element = render_toda_expression_latex(order.element)\n") == 1
    assert "from phase168_r3_27_typed_statement_projection import element_tex, group_tex" not in after
    assert "from phase168_r3_27_typed_statement_projection import group_tex" in after
    assert len(after.splitlines()) == len(before.splitlines())


def test_crlf_repair_preserves_crlf_and_utf8_bom():
    old = b"\xef\xbb\xbf" + _old_bytes().replace(b"\n", b"\r\n")
    updated = corrected_source(old)
    assert updated.startswith(b"\xef\xbb\xbf")
    assert b"\r\n" in updated
    assert b"\n" not in updated.replace(b"\r\n", b"")


def test_unknown_or_double_patch_fails_closed():
    with pytest.raises(RuntimeError):
        corrected_source(_old_bytes().replace(b"element_tex(order.element)", b"other(order.element)"))
    with pytest.raises(RuntimeError):
        corrected_source(corrected_source(_old_bytes()))

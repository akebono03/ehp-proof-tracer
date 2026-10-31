"""Guarded patch and source export unit checks, independent of remote checkout."""
from __future__ import annotations

import ast

import pytest

from phase171_r20r12_verified_cyclic_narrative.install import (
    ANCHOR_NOTICE, ANCHOR_PREPARE, ANCHOR_RETURN, ANCHOR_ROOT,
    EXPECTED_BLOB, git_blob_sha, matches_reviewed_blob, preserve_format,
    transform_source,
)


def fixture_renderer() -> str:
    return (
        "def render_model_backed_narrative_markdown(model):\n"
        + ANCHOR_PREPARE
        + ANCHOR_ROOT
        + "            pass\n"
        + ANCHOR_NOTICE
        + ANCHOR_RETURN
    )


def test_guard_recognizes_only_reviewed_bytes_across_newline_conventions():
    assert len(EXPECTED_BLOB) == 40
    assert git_blob_sha(b"x") != git_blob_sha(b"y")
    assert not matches_reviewed_blob(b"unrelated production source")


def test_transform_replaces_each_anchor_once_without_touching_other_functions():
    source = fixture_renderer() + "\ndef unrelated():\n    return 25\n"
    result = transform_source(source)
    ast.parse(result)
    assert "verified_order_four_summary(model)" in result
    assert "suppress_exact_duplicate_body_lines(lines)" in result
    assert "def unrelated():\n    return 25" in result
    assert result.count("order_summary =") == 1


def test_transform_rejects_an_unreviewed_or_double_patch():
    source = fixture_renderer()
    with pytest.raises(RuntimeError):
        transform_source(source.replace("    displayed_cyclic_math = set()", "    bad = True"))
    with pytest.raises(RuntimeError):
        transform_source(transform_source(source))


def test_patch_preserves_crlf_and_utf8_bom():
    source = fixture_renderer().encode("utf-8")
    data = b"\xef\xbb\xbf" + source.replace(b"\n", b"\r\n")
    edited = transform_source(data.decode("utf-8-sig").replace("\r\n", "\n"))
    saved = preserve_format(data, edited)
    assert saved.startswith(b"\xef\xbb\xbf")
    assert b"\r\n" in saved
    assert b"\n" not in saved.replace(b"\r\n", b"")

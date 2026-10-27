"""Offline guarded patch tests: no project-level imports required."""
from __future__ import annotations

import ast

import pytest

from phase169_r10ec_direct_sum_narrative_projection.patch import (
    ANCHOR, REPLACEMENT, _decode_and_style, prepare_patch, transform,
)


def _example() -> str:
    return (
        "def render_model_backed_narrative_markdown(result, model):\n"
        "    incomplete = False\n"
        "    lines = []\n"
        "    order = (0,)\n"
        "    stable_chain_display = None\n"
        "    suppressed_body_indices = set()\n"
        + ANCHOR
        + "            pass\n"
        + "    return '\\n'.join(lines)\n"
    )


def test_r10ec_patch_replaces_exactly_one_whole_renderer():
    before = _example()
    updated, fn = transform(before)
    ast.parse(updated)
    assert ANCHOR in before
    assert REPLACEMENT in fn
    assert "project_verified_direct_sum_transport" in updated
    with pytest.raises(RuntimeError, match="anchor"):
        transform(updated)


@pytest.mark.parametrize("style", ["LF", "CRLF"])
def test_r10ec_newline_decoder(style):
    original = b"def f():\n    return 3\n"
    if style == "CRLF":
        original = original.replace(b"\n", b"\r\n")
    text, observed = _decode_and_style(original)
    assert observed == style
    assert text == "def f():\n    return 3\n"


def test_r10ec_rejects_unreviewed_source_and_mixed_newlines():
    with pytest.raises(RuntimeError, match="blob mismatch"):
        prepare_patch(_example().encode("utf-8"))
    with pytest.raises(RuntimeError, match="mixed newline"):
        _decode_and_style(b"a\r\nb\n")

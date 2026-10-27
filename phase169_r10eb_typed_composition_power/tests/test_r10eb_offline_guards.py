"""Portable source-patch safety checks that do not require EHP runtime imports."""
from __future__ import annotations

import pytest

from phase169_r10eb_typed_composition_power.patch import (
    NARRATIVE_ANCHOR, PUBLIC_ANCHOR, _style_and_source, transform,
)


@pytest.mark.parametrize("path,source", [
    (
        "phase168_r3_27_typed_statement_projection.py",
        "def element_tex(value):\n" + NARRATIVE_ANCHOR
        + ":\n        return None\n    return None\n",
    ),
    (
        "toda_human_readable_renderer.py",
        "def render_toda_expression_latex(expression):\n"
        + PUBLIC_ANCHOR + "\n    return None\n",
    ),
])
def test_r10eb_full_function_patch_is_unique_and_single_use(path, source):
    patched, function = transform(path, source)
    assert "typed_stable_composition_power_latex" in function
    assert patched != source
    with pytest.raises(RuntimeError, match="anchor changed"):
        transform(path, patched)


def test_r10eb_source_newline_styles_and_mixed_rejection():
    assert _style_and_source(b"a\nb\n") == ("a\nb\n", "LF")
    assert _style_and_source(b"a\r\nb\r\n") == ("a\nb\n", "CRLF")
    with pytest.raises(RuntimeError, match="mixed"):
        _style_and_source(b"a\r\nb\n")
    with pytest.raises(RuntimeError, match="CR-only"):
        _style_and_source(b"a\rb\r")


def test_r10eb_unreviewed_source_function_and_path_fail_closed():
    with pytest.raises(RuntimeError, match="anchor changed"):
        transform("phase168_r3_27_typed_statement_projection.py",
                  "def element_tex(value):\n    return None\n")
    with pytest.raises(RuntimeError, match="unreviewed patch destination"):
        transform("unrelated.py", "def f():\n    return None\n")

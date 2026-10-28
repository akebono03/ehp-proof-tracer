"""Pure source-replacement checks, runnable without the full repository."""
from __future__ import annotations

import ast
from pathlib import Path

from phase169_r10eo_r3_reviewed_definition_bridge.patch import (
    HERE,
    _INSERT_ANCHOR,
    _INSERT_NEW,
    function_span,
    replace_complete_function,
)


def test_r10eo_r3_three_full_functions_have_no_elisions():
    for name in ("canonical_member", "cited_family_reference_sentence",
                 "build_shared_typed_bridge"):
        source = (HERE / "full_functions" / (name + ".py")).read_text(
            encoding="utf-8",
        )
        ast.parse(source)
        assert source.startswith("def " + name + "(")
        assert function_span(source, name) == (0, len(source))
        assert not any(isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and node.value.value is Ellipsis for node in ast.walk(ast.parse(source)))


def test_r10eo_r3_shared_bridge_adds_only_reviewed_definition_source():
    full = (HERE / "full_functions" / "build_shared_typed_bridge.py").read_text(
        encoding="utf-8",
    )
    assert full.count(_INSERT_ANCHOR) == 1
    assert full.count(_INSERT_NEW) == 1
    assert full.index(_INSERT_ANCHOR) < full.index(_INSERT_NEW)


def test_r10eo_r3_function_replacement_preserves_unrelated_code():
    before = "x = 1\n\ndef f():\n    return 1\n\ny = 2\n"
    after = replace_complete_function(before, "f", "def f():\n    return 2\n")
    assert after == "x = 1\n\ndef f():\n    return 2\n\ny = 2\n"

"""Isolated-only release checks; no user code or published reference overwritten."""
from __future__ import annotations

import ast
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]


def test_new_code_is_complete_python_without_placeholder() -> None:
    for filename in ("rule.py", "audit.py"):
        content = (PACKAGE / filename).read_text(encoding="utf-8")
        ast.parse(content)
        assert not any(
            isinstance(node, ast.Expr)
            and isinstance(node.value, ast.Constant)
            and node.value.value is Ellipsis
            for node in ast.walk(ast.parse(content))
        )


def test_no_production_patch_or_direct_source_steps() -> None:
    contents = (PACKAGE / "rule.py").read_text(encoding="utf-8")
    assert "class Prop27TypedHopfDeltaStatement" not in contents
    assert "ProofStep(" not in contents
    assert "ProofRule.GIVEN" not in contents
    assert "build_shared_typed_bridge" not in contents


def test_one_rule_one_backward_expansion() -> None:
    node = ast.parse((PACKAGE / "rule.py").read_text(encoding="utf-8"))
    names = {x.name for x in node.body if isinstance(x, ast.FunctionDef)}
    assert names == {
        "upper_delta_surjectivity_inputs",
        "upper_delta_surjectivity_rule",
        "expand_upper_delta_surjectivity",
    }

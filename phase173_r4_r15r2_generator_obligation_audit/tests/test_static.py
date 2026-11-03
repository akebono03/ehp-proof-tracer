"""Offline safety and parser tests that do not need project imports."""
from __future__ import annotations

import ast
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]


def _module(name: str) -> ast.Module:
    return ast.parse((HERE / name).read_text(encoding="utf-8"))


def test_audit_source_is_parseable() -> None:
    _module("audit.py")


def test_preflight_source_is_parseable() -> None:
    _module("preflight.py")


def test_audit_has_no_proof_step_constructor() -> None:
    module = _module("audit.py")
    imported = [
        alias.name for node in ast.walk(module)
        if isinstance(node, ast.ImportFrom) for alias in node.names
    ]
    assert "ProofStep" not in imported
    assert "GoalExpansion" not in imported
    assert "InferenceRule" not in imported
    assert "LiteratureReference" not in imported


def test_main_does_not_select_single_stem() -> None:
    module = _module("audit.py")
    functions = {node.name: node for node in module.body if isinstance(node, ast.FunctionDef)}
    assert "inspect_k" in functions
    inspect = functions["inspect_k"]
    assert not any(
        isinstance(node, ast.Compare)
        and any(isinstance(comp, ast.Constant) and comp.value == 31 for comp in node.comparators)
        for node in ast.walk(inspect)
    )


def test_preflight_is_read_only() -> None:
    source = (HERE / "preflight.py").read_text(encoding="utf-8")
    assert '"git", "show"' in source
    assert '"git", "reset"' not in source
    assert '"git", "checkout"' not in source
    assert "write_bytes(" not in source


def test_audit_status_explicitly_is_not_complete() -> None:
    source = (HERE / "audit.py").read_text(encoding="utf-8")
    assert '"proof_completed_by_this_audit": False' in source
    assert '"new_proof_steps": 0' in source
    assert '"new_given_assertions": 0' in source

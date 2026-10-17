"""R12-R23 runtime path regression checks."""
from __future__ import annotations

import ast
from pathlib import Path


def test_r22_audit_resolves_from_project_root():
    module = Path(__file__).resolve().parents[1] / "phase165_r12_r23_public_narrative.py"
    project_root = module.parent.parent
    assert (project_root / "phase165_r12_r22_quotient_closure" / "audit.py").is_file()
    code = module.read_text(encoding="utf-8")
    ast.parse(code)
    assert "Path(__file__).resolve().parent / 'phase165_r12_r22_quotient_closure' / 'audit.py'" in code
    assert ".with_name('phase165_r12_r22_quotient_closure')" not in code


def test_r22_audit_function_exists():
    path = Path(__file__).resolve().parents[2] / "phase165_r12_r22_quotient_closure" / "audit.py"
    tree = ast.parse(path.read_text(encoding="utf-8"))
    assert any(isinstance(node, ast.FunctionDef) and node.name == "perform_audit" for node in tree.body)

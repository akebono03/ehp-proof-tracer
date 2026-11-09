"""Source-only structural tests independent of the deployed application."""
from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def parsed_module(name: str) -> ast.Module:
    return ast.parse((ROOT / name).read_text(encoding="utf-8"))


def test_no_direct_proofstep_creation_in_inference_rule():
    tree = parsed_module("rule.py")
    names = {node.func.id for node in ast.walk(tree)
             if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)}
    assert "ProofStep" not in names
    assert "KernelMultipleStatement" not in names


def test_single_generic_rule_without_dimension_literals():
    tree = parsed_module("rule.py")
    functions = {n.name for n in tree.body if isinstance(n, ast.FunctionDef)}
    assert functions == {
        "expression_coordinates", "conditional_inputs", "cyclic_delta_kernel_rule",
        "expand_cyclic_delta_kernel",
    }
    source = (ROOT / "rule.py").read_text(encoding="utf-8")
    assert "π_12" not in source
    assert "pi12" not in source


def test_audit_never_claims_public_proof():
    source = (ROOT / "audit.py").read_text(encoding="utf-8")
    assert '"kernel_proof_certified_by_audit": False' in source
    assert '"shared_provider_connected_in_r35": False' in source
    assert '"root_complete": False' in source


def test_full_runner_exists():
    text = (ROOT / "run.ps1").read_text(encoding="utf-8")
    assert "--dry-run" in text
    assert "R35_RULE" in text
    assert "FULL_PYTEST=False" in text

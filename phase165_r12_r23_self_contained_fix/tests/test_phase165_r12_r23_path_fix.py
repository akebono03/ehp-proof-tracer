"""R23 must recreate real proofs without importing an external audit script."""
from __future__ import annotations
import ast
from pathlib import Path


def test_narrative_builder_does_not_require_r22_audit_file():
    path = Path(__file__).resolve().parents[1] / "phase165_r12_r23_public_narrative.py"
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    assert "R12-R22 audit script is unavailable" not in source
    assert "spec_from_file_location" not in source
    function = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "build_verified_pi43_narrative")
    calls = [n.func.id for n in ast.walk(function) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)]
    assert "close_quotient_from_verified_steps" in calls
    assert "proof_ancestors" in calls
    assert "render_partial_proof_markdown" in calls


def test_narrative_builder_checks_all_four_proof_ancestors():
    path = Path(__file__).resolve().parents[1] / "phase165_r12_r23_public_narrative.py"
    source = path.read_text(encoding="utf-8")
    assert "proof_ancestors(root, (pstep, kernel.proof, onto.proof, source_root))" in source
    assert "root.conclusion != goal" in source

"""R3I2: the complete R3H replacement retains imports required by unchanged tests."""
from __future__ import annotations

import ast
from pathlib import Path


def test_r3i2_updated_r3h_test_imports_proof_search_status():
    package = Path(__file__).resolve().parents[1]
    replacement = package / "full_tests" / "test_phase169_r3h_toda53_hopf_source.py"
    tree = ast.parse(replacement.read_text(encoding="utf-8"))
    imported = any(
        isinstance(node, ast.ImportFrom)
        and node.module == "phase165_r52_partial_proof"
        and any(alias.name == "ProofSearchStatus" for alias in node.names)
        for node in tree.body
    )
    assert imported
    target = next(
        node for node in tree.body
        if isinstance(node, ast.FunctionDef)
        and node.name == "test_r3h_pi4_2_remains_complete"
    )
    assert any(
        isinstance(node, ast.Name) and node.id == "ProofSearchStatus"
        for node in ast.walk(target)
    )


def test_r3i2_legacy_test_replacement_changes_import_only_from_r3i1():
    package = Path(__file__).resolve().parents[1]
    old = package / "reviewed_r3h" / "test_phase169_r3h_toda53_hopf_source.py"
    new = package / "full_tests" / "test_phase169_r3h_toda53_hopf_source.py"
    original = old.read_text(encoding="utf-8")
    revised = new.read_text(encoding="utf-8")
    assert "from phase165_r52_partial_proof import ProofSearchStatus" in original
    assert "from phase165_r52_partial_proof import ProofSearchStatus" in revised
    assert original.count("def test_r3h_pi4_2_remains_complete():") == 1
    assert revised.count("def test_r3h_pi4_2_remains_complete():") == 1

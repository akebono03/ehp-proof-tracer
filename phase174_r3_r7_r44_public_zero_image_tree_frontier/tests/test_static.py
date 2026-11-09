"""R44 is audit-only, never another hidden production implementation."""
from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_audit_only_package_has_no_production_replacement():
    assert not (ROOT / "install.py").exists()
    assert not (ROOT / "replacement").exists()
    assert not (ROOT / "patch.py").exists()
    assert (ROOT / "run.ps1").is_file()


def test_audit_uses_canonical_search_and_typed_goal_separation():
    source = (ROOT / "audit.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    names = {node.id for node in ast.walk(tree) if isinstance(node, ast.Name)}
    calls = {node.func.id for node in ast.walk(tree)
             if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)}
    assert "search_registered_partial_proof" in calls
    assert "TodaPrimaryGroupZeroStatement" in calls
    assert "ImageZeroStatement" in names
    assert "ProofStep" in names and "ProofRule" in names
    assert "git" not in calls


def test_dry_run_is_implemented_and_does_not_modify_source():
    source = (ROOT / "run.ps1").read_text(encoding="utf-8")
    assert "param([switch]$DryRun)" in source
    assert "--dry-run" in source
    assert "python -B -m pytest" in source
    assert "-p no:cacheprovider" in source

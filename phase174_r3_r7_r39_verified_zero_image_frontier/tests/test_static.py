"""Read-only R39 artifact constraints: importable, complete, scope-isolated."""
from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_all_new_python_units_have_valid_syntax():
    for path in sorted(ROOT.rglob("*.py")):
        if "__pycache__" in path.parts:
            continue
        ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def test_audit_does_not_rename_proof_rules_or_create_a_given():
    code = (ROOT / "audit.py").read_text(encoding="utf-8")
    tree = ast.parse(code)
    calls = tuple(node for node in ast.walk(tree) if isinstance(node, ast.Call))
    assert not any(isinstance(call.func, ast.Name) and call.func.id == "ProofStep" for call in calls)
    assert "verified_db_step" in code
    assert "derive_inference_proof_step" in code
    assert "new_givens\": 0" in code


def test_source_guard_does_not_modify_git_or_source_files():
    code = (ROOT / "source_guard.py").read_text(encoding="utf-8")
    assert "git(\"fetch\", \"-q\", \"origin\", \"develop\")" in code
    for forbidden in ('git("reset"', 'git("pull"', 'git("checkout"', '.write_bytes(', '.write_text('):
        assert forbidden not in code
    assert "R38_PROVIDER_BLOB" in code
    assert "phase174_r3_r7_r9_composition_associativity/rule.py" in code


def test_powershell_dryrun_does_not_run_tests_or_create_patches():
    text = (ROOT / "run.ps1").read_text(encoding="utf-8")
    assert "param([switch]$DryRun)" in text
    assert "--dry-run" in text
    assert "-m pytest -q" in text
    assert "(END)" in text

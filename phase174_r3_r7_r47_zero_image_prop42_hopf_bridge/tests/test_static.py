"""Only independent audit files are added in R47, without changing math."""
from __future__ import annotations

import ast
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]


def test_python_sources_are_complete_and_parsable():
    for relative in (
        "__init__.py", "source_guard.py", "audit.py",
        "tests/test_guard.py", "tests/test_frontier.py", "tests/test_static.py",
    ):
        tree = ast.parse((PACKAGE / relative).read_text(encoding="utf-8"))
        assert not any(
            isinstance(node, ast.Constant) and node.value is Ellipsis
            for node in ast.walk(tree)
        )


def test_r47_never_installs_a_proof_or_modifies_production():
    code = (PACKAGE / "audit.py").read_text(encoding="utf-8")
    run = (PACKAGE / "run.ps1").read_text(encoding="utf-8")
    assert "search_registered_partial_proof" in code
    assert "shared_expansion_provider" in code
    assert "ProofStep(" not in code
    assert "build_shared_typed_bridge" in code
    assert "expand_generator_zero_from_composite" in code
    assert "full_pytest" in code
    assert "[switch]$DryRun" in run
    assert "--import-mode=$ImportMode" in run
    assert "git clean" not in run and "git reset" not in run
    assert "FULL_PYTEST=False" in run


def test_r47_includes_complete_code_and_japanese_audit_plan():
    for relative in (
        "README.md", "AUDIT_PLAN_JA.md", "CODE_FULL_JA.md",
        "TEST_RESULTS_JA.md", "run.ps1", "tests/test_frontier.py",
    ):
        assert (PACKAGE / relative).is_file()

"""R46 remains a standalone audit-only ZIP with no production patch."""
from __future__ import annotations

import ast
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]


def test_r46_source_has_no_ellipsis_expressions():
    for relative in (
        "__init__.py", "source_guard.py", "audit.py",
        "tests/test_audit.py", "tests/test_guard.py", "tests/test_static.py",
    ):
        source = (PACKAGE / relative).read_text(encoding="utf-8")
        tree = ast.parse(source)
        assert not any(
            isinstance(node, ast.Constant) and node.value is Ellipsis
            for node in ast.walk(tree)
        )


def test_r46_does_not_install_a_proof_or_modify_production():
    audit = (PACKAGE / "audit.py").read_text(encoding="utf-8")
    runner = (PACKAGE / "run.ps1").read_text(encoding="utf-8")
    assert "reconstruct_registered_goal" in audit
    assert "search_registered_partial_proof" in audit
    assert "ProofStep(" not in audit
    assert "expansion_provider=bounded_r45" in audit
    assert "git reset" not in runner and "git clean" not in runner
    assert "install.py" not in runner
    assert "FULL_PYTEST=False" in runner
    assert "[switch]$DryRun" in runner


def test_documentation_and_test_files_exist():
    for relative in (
        "README.md", "AUDIT_PLAN_JA.md", "CODE_FULL_JA.md",
        "TEST_RESULTS_JA.md", "run.ps1", "tests/test_audit.py",
    ):
        assert (PACKAGE / relative).is_file()

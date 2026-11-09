"""R48 only adds an auditable scoped proof-search procedure."""
from __future__ import annotations

import ast
from pathlib import Path

PKG = Path(__file__).resolve().parents[1]


def test_new_python_source_parses_without_placeholders() -> None:
    for path in (PKG / "audit.py", PKG / "source_guard.py", PKG / "tests/test_static.py", PKG / "tests/test_frontier.py", PKG / "tests/test_guard.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        assert not any(isinstance(node, ast.Constant) and node.value is Ellipsis for node in ast.walk(tree))


def test_runner_is_read_only_and_runs_only_focused_pytest() -> None:
    script = (PKG / "run.ps1").read_text(encoding="utf-8")
    assert "--dry-run" in script
    assert "--import-mode=$ImportMode" in script
    assert "R36_CITED_KERNEL_REGRESSION" in script
    assert "R47_FRONTIER_REGRESSION" in script
    assert "FULL_PYTEST=False" in script
    assert "git reset" not in script
    assert "git clean" not in script
    assert "install.py" not in script


def test_no_direct_proof_or_new_source_is_installed() -> None:
    source = (PKG / "audit.py").read_text(encoding="utf-8")
    assert "ProofStep(" not in source
    assert "checked_prior_statements()" in source
    assert "search_registered_partial_proof(" in source
    assert "isolated_proof_steps_injected" in source
    assert "R35/R36" in source

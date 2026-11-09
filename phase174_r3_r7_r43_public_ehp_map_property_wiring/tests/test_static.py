"""R43 scope and package integrity; no production math rewrite."""
from __future__ import annotations

import ast
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]


def test_all_new_modules_parse_without_ellipsis():
    for name in ("__init__.py", "source_guard.py", "install.py", "audit.py"):
        tree = ast.parse((PACKAGE / name).read_text(encoding="utf-8"))
        assert not any(
            isinstance(x, ast.Expr)
            and isinstance(x.value, ast.Constant)
            and x.value.value is Ellipsis
            for x in ast.walk(tree)
        )


def test_r43_wires_only_historical_r5_and_r37_rules():
    from phase174_r3_r7_r43_public_ehp_map_property_wiring.source_guard import INSERT
    assert "expand_hopf_injective_from_zero_image" in INSERT
    assert "expand_upper_delta_surjectivity" in INSERT
    assert "extra_providers" in INSERT
    assert "given_step" not in INSERT
    assert "ProofStep(" not in INSERT
    assert "if n ==" not in INSERT and "if k ==" not in INSERT


def test_runner_supports_dry_run_and_only_focused_tests():
    script = (PACKAGE / "run.ps1").read_text(encoding="utf-8")
    assert "[switch]$DryRun" in script
    assert "--dry-run" in script
    assert "pytest -q --import-mode=importlib" in script
    assert "git reset" not in script and "git clean" not in script
    assert "FULL_PYTEST=False" in script


def test_documentation_and_install_are_present():
    for name in ("README.md", "AUDIT_PLAN_JA.md", "CODE_FULL_JA.md", "TEST_RESULTS_JA.md"):
        assert (PACKAGE / name).is_file()
    assert (PACKAGE / "install.py").is_file()

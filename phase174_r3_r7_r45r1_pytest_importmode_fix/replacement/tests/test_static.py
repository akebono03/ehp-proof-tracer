"""R45 is a self-contained non-invasive audit-only ZIP."""
from __future__ import annotations

import ast
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]


def test_r45_python_modules_are_complete_and_parse():
    targets = (
        "__init__.py", "source_guard.py", "audit.py",
        "tests/test_frontier.py", "tests/test_source_guard.py",
        "tests/test_static.py",
    )
    for filename in targets:
        source = (PACKAGE / filename).read_text(encoding="utf-8")
        tree = ast.parse(source)
        assert not any(
            isinstance(node, ast.Constant) and node.value is Ellipsis
            for node in ast.walk(tree)
        )


def test_runner_performs_no_install_or_full_test_suite():
    source = (PACKAGE / "run.ps1").read_text(encoding="utf-8")
    assert "[switch]$DryRun" in source
    assert "--dry-run" in source
    assert "$ImportMode = 'importlib'" in source
    assert "git reset" not in source
    assert "git clean" not in source
    assert "install.py" not in source
    assert "FULL_PYTEST=False" in source


def test_prop42_regressions_use_prepend_to_avoid_same_name_module_shadowing():
    source = (PACKAGE / "run.ps1").read_text(encoding="utf-8")
    assert "$ImportMode = 'importlib'" in source
    assert "'PROP42_SPECIALIZATION_REGRESSION', 'PROP42_CONSEQUENCE_REGRESSION'" in source
    assert "$ImportMode = 'prepend'" in source
    assert '"--import-mode=$ImportMode"' in source
    assert "R45_FRONTIER" in source


def test_no_derived_theorem_is_installed_or_given():
    source = (PACKAGE / "audit.py").read_text(encoding="utf-8")
    assert "ProofStep(" not in source
    assert "ProofRule.GIVEN" in source
    assert "source_guard" in source
    assert "expand_provider=" not in source
    assert "expansion_provider=scoped" in source

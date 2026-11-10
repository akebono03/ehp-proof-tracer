"""R52 does not install a source, mathematics, or display override."""
from __future__ import annotations

import ast
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]


def test_r52_sources_parse_and_have_no_ellipsis() -> None:
    for path in (PACKAGE / "audit.py", PACKAGE / "source_guard.py", PACKAGE / "probe.py", *sorted((PACKAGE / "tests").glob("test_*.py"))):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        assert not any(isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant)
                       and node.value.value is Ellipsis for node in ast.walk(tree))


def test_production_is_unchanged_and_probe_is_not_goal_specific() -> None:
    code = (PACKAGE / "probe.py").read_text(encoding="utf-8")
    assert "ProofStep(" not in code
    assert "n=7" not in code and "k=5" not in code
    assert "SourceBoundGoal(conclusion=domain, source=source)" in code
    assert "return tuple(bound) + original" in code
    assert "find_inference_matches_for_rule(option.rule, (step,))" in code


def test_runner_stops_on_failures_and_has_no_global_pytest() -> None:
    code = (PACKAGE / "run.ps1").read_text(encoding="utf-8")
    assert "--dry-run" in code
    assert "--import-mode=importlib" in code
    assert "FULL_PYTEST=False" in code
    assert "git reset" not in code and "git clean" not in code
    assert "install.py" not in code

"""R53 prevents accidental scope creep in the public zero-branch wiring."""
from __future__ import annotations

import ast
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]


def test_all_r53_python_files_parse_without_ellipsis() -> None:
    for file in ("provider.py", "source_guard.py", "install.py", "audit.py",
                 "CHANGED_FUNCTIONS_FULL.py", "tests/test_static.py",
                 "tests/test_guard.py", "tests/test_public.py"):
        tree = ast.parse((PACKAGE / file).read_text(encoding="utf-8"), feature_version=(3, 10))
        assert not any(isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant)
                       and node.value.value is Ellipsis for node in ast.walk(tree))


def test_only_zero_public_branch_receives_generic_source_bound_provider() -> None:
    tree = ast.parse((PACKAGE / "CHANGED_FUNCTIONS_FULL.py").read_text(encoding="utf-8"))
    functions = tuple(x for x in tree.body if isinstance(x, ast.FunctionDef))
    assert len(functions) == 1
    assert functions[0].name == "search_group_from_registered_goal"
    text = (PACKAGE / "CHANGED_FUNCTIONS_FULL.py").read_text(encoding="utf-8")
    assert text.count("build_public_source_bound_kernel_provider(provider, screened)") == 1
    assert "if isinstance(candidate, TodaPrimaryGroupZeroStatement):" in text
    assert "return search_registered_partial_proof(" in text
    assert "if proof_order_catalog is None:" in text
    assert "def registered_group_goal_candidates(" not in text


def test_provider_only_reuses_a_reviewed_general_mathematical_rule() -> None:
    text = (PACKAGE / "provider.py").read_text(encoding="utf-8")
    assert "find_inference_matches_for_rule" in text
    assert "SourceBoundGoal(conclusion=domain, source=source)" in text
    assert "return tuple(bound) + original" in text
    assert "ProofStep(" not in text
    assert "n == 7" not in text and "k == 5" not in text
    script = (PACKAGE / "run.ps1").read_text(encoding="utf-8")
    assert "param([switch]$DryRun)" in script and "--dry-run" in script
    assert "FULL_PYTEST=False" in script
    assert "--import-mode=importlib" in script
    assert "git reset" not in script and "git clean" not in script

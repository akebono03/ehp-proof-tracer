"""R43R2 exact edited-function and fail-closed contract tests."""
from __future__ import annotations

import ast
from pathlib import Path

from phase174_r3_r7_r43r2_reviewed_tracked_change_guard.repair import (
    reviewed_contract,
)

ROOT = Path(__file__).resolve().parents[1]


def test_only_verify_checkout_changed():
    original, edited = reviewed_contract()
    before = ast.parse(original.decode("utf-8"))
    after = ast.parse(edited.decode("utf-8"))
    old = {node.name: ast.dump(node) for node in before.body
           if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))}
    new = {node.name: ast.dump(node) for node in after.body
           if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))}
    assert old.keys() == new.keys()
    assert old["verify_checkout"] != new["verify_checkout"]
    for name in old:
        if name != "verify_checkout":
            assert old[name] == new[name]


def test_staged_changes_are_never_admitted():
    _, edited = reviewed_contract()
    code = edited.decode("utf-8")
    assert 'git("diff", "--cached", "--name-only")' in code
    assert "if staged:" in code
    assert "Staged changes require independent review" in code


def test_only_exact_r43_public_target_is_whitelisted():
    _, edited = reviewed_contract()
    code = edited.decode("utf-8")
    assert 'reviewed_target = "phase165_r52_r9_shared_math.py"' in code
    assert "modified != (reviewed_target,)" in code
    assert "expected_replacement(baseline_output)" in code
    assert "if actual != expected:" in code
    assert "Unreviewed tracked changes; no files modified" in code


def test_source_pins_and_r43r1_contract_unchanged():
    original, edited = reviewed_contract()
    for literal in (
        b"REVIEWED_EHP_SOURCE_BLOB",
        b"PREVIOUS_PINS",
        b"reviewed_source_blob",
        b"replacement_contract",
        b"EXPECTED_HEAD",
    ):
        assert literal in original and literal in edited


def test_run_always_runs_prior_guard_and_focused_tests():
    run = (ROOT / "run.ps1").read_text(encoding="utf-8")
    assert "[switch]$DryRun" in run
    assert "R43R1 DryRun failed" in run
    assert "R43R1/R43 audit failed" in run
    assert "pytest -q --import-mode=importlib" in run
    assert "git reset" not in run
    assert "git clean" not in run
    assert "FULL_PYTEST=False" in run


def test_repair_does_not_touch_production_or_fabricate_source():
    code = (ROOT / "repair.py").read_text(encoding="utf-8")
    assert 'TARGET = PREVIOUS / "install.py"' in code
    assert "os.replace(temporary, TARGET)" in code
    assert "R43 target differs from the exact reviewed patch" in code
    assert "Staged changes require review" in code
    assert "Unreviewed tracked changes" in code

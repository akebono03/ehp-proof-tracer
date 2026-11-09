"""Focused R43R1 regression: SHA pin only, strict guards preserved."""
from __future__ import annotations

import ast
from pathlib import Path

from phase174_r3_r7_r43r1_r3_sha_pin_fix.install import (
    CORRECT_SHA, WRONG_SHA, replacement_contract, verify_checkout,
)

PACKAGE = Path(__file__).resolve().parents[1]


def test_single_reviewed_source_sha_correction():
    original, replacement = replacement_contract()
    assert len(WRONG_SHA) == 35
    assert len(CORRECT_SHA) == 40
    assert original.count((chr(34) + WRONG_SHA + chr(34)).encode()) == 1
    assert replacement == original.replace(
        (chr(34) + WRONG_SHA + chr(34)).encode(),
        (chr(34) + CORRECT_SHA + chr(34)).encode(),
        1,
    )


def test_all_r43_verification_functions_are_identical():
    original, replacement = replacement_contract()
    first = ast.parse(original.decode("utf-8"))
    second = ast.parse(replacement.decode("utf-8"))
    functions = lambda tree: {
        node.name: ast.dump(node)
        for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    assert functions(first) == functions(second)


def test_strict_source_guard_not_weakened():
    _, replacement = replacement_contract()
    code = replacement.decode("utf-8")
    assert "def verify_checkout()" in code
    assert '"git", "diff"' not in code  # keep the known git() helper, no invented bypass
    assert 'git("diff", "--cached", "--name-only")' in code
    assert 'matches_blob(p.read_bytes(), sha)' in code
    assert "len(expected) == 40" in code
    assert "REVIEWED_R42_HEAD" in code


def test_patch_runner_and_no_full_pytest():
    code = (PACKAGE / "run.ps1").read_text(encoding="utf-8")
    assert "[switch]$DryRun" in code
    assert "Original R43 audit failed" in code
    assert "pytest -q --import-mode=importlib" in code
    assert "FULL_PYTEST=False" in code
    assert "git reset" not in code and "git clean" not in code


def test_corrected_pin_is_pinned_in_exact_original_structure():
    _, replacement = replacement_contract()
    content = replacement.decode("utf-8")
    assert content.count(CORRECT_SHA) == 1
    assert WRONG_SHA not in content
    assert '"phase174_r3_r7_r3_ehp_zero_rule/rule.py": "' + CORRECT_SHA + '"' in content

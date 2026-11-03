"""Standalone regression and fail-closed content constraints."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase173_r4_r15r6_abstract_toda44_rule.preflight import (
    is_allowed_committed,
    sha256_normalized,
)

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("filename", ("abstract_rule.py", "audit.py", "preflight.py"))
def test_source_is_parsable_and_has_no_ellipsis(filename: str) -> None:
    source = (ROOT / filename).read_text(encoding="utf-8")
    tree = ast.parse(source)
    assert not any(isinstance(node, ast.Expr)
                   and isinstance(node.value, ast.Constant)
                   and node.value.value is Ellipsis
                   for node in ast.walk(tree))
    assert "eval(" not in source
    assert "exec(" not in source


def test_only_prior_audit_commit_paths_allowed() -> None:
    assert is_allowed_committed("phase173_r4_r15r5_family_source_frontier/audit.py")
    assert is_allowed_committed(".pytest_cache/v/cache/nodeids")
    assert not is_allowed_committed("phase173_r4_r10_general_toda56_core/core.py")
    assert not is_allowed_committed("sources/toda/Toda_06_2.tex")
    assert not is_allowed_committed("phase173_r4_r15r6_abstract_toda44_rule/audit.py")


def test_source_identity_is_line_ending_tolerant_only(tmp_path: Path) -> None:
    path = tmp_path / "test.py"
    path.write_bytes(b"a=1\nb=2\n")
    digest = sha256_normalized(path)
    path.write_bytes(b"a=1\r\nb=2\r\n")
    assert sha256_normalized(path) == digest
    path.write_bytes(b"a=1\r\nb=3\r\n")
    assert sha256_normalized(path) != digest


def test_no_public_proof_or_given_is_created() -> None:
    source = (ROOT / "audit.py").read_text(encoding="utf-8")
    assert '"public_completion": False' in source
    assert '"new_given": 0' in source
    rule = (ROOT / "abstract_rule.py").read_text(encoding="utf-8")
    assert "conclusion_pattern=statement" in rule
    assert "verified_db_step(first_step" in rule
    assert "verified_db_step(second_step" in rule
    assert "checked_abstract_inputs(proof_target)" in rule


def test_runner_uses_only_focused_pytest() -> None:
    s = (ROOT / "run.ps1").read_text(encoding="utf-8")
    assert "-DryRun" not in s
    assert "pytest -q" in s
    assert "phase173_r4_r10_general_toda56_core/tests/test_core.py" in s
    assert "git reset" not in s
    assert "git checkout" not in s

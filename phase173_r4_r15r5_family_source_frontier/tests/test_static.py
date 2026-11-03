"""Static source, safety and HEAD lineage constraints for R15R5."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase173_r4_r15r5_family_source_frontier.preflight import (
    ALLOWED_PYTEST_CACHE,
    is_allowed_committed,
    normalized_sha256,
)


ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("filename", ("source_scan.py", "audit.py", "preflight.py"))
def test_new_code_parses_without_elision(filename: str) -> None:
    text = (ROOT / filename).read_text(encoding="utf-8")
    tree = ast.parse(text)
    assert not any(isinstance(node, ast.Expr)
                   and isinstance(node.value, ast.Constant)
                   and node.value.value is Ellipsis
                   for node in ast.walk(tree))
    assert "eval(" not in text
    assert "exec(" not in text


def test_prior_math_code_is_not_modified_by_runner() -> None:
    runner = (ROOT / "run.ps1").read_text(encoding="utf-8")
    assert "phase173_r4_r15r5_family_source_frontier.audit" in runner
    assert "PHASE173_R4_R15R5_FOCUSED_PYTEST=PASS" in runner
    assert "--DryRun" not in runner
    assert "git reset" not in runner
    assert "git checkout" not in runner


def test_public_proof_not_promoted() -> None:
    text = (ROOT / "audit.py").read_text(encoding="utf-8")
    assert '"public_completion": False' in text
    assert '"new_given_created": False' in text
    assert '"new_proof_steps_created": False' in text


def test_only_expected_prior_commit_paths_allowed() -> None:
    assert is_allowed_committed(ALLOWED_PYTEST_CACHE)
    assert is_allowed_committed("phase173_r4_r15r4_cited_composition_image/audit.py")
    assert not is_allowed_committed("phase173_r4_r10_general_toda56_core/core.py")
    assert not is_allowed_committed("sources/toda/Toda_06_2.tex")
    assert not is_allowed_committed("phase173_r4_r15r5_family_source_frontier/audit.py")


def test_line_ending_hash_normalization(tmp_path: Path) -> None:
    source = tmp_path / "source.py"
    source.write_bytes(b"x=1\ny=2\n")
    first = normalized_sha256(source)
    source.write_bytes(b"x=1\r\ny=2\r\n")
    assert normalized_sha256(source) == first
    source.write_bytes(b"x=1\r\ny=3\r\n")
    assert normalized_sha256(source) != first

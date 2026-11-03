"""Standalone fail-closed/static tests; no live repository source required."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase173_r4_r15r7_source_first_abstract_certificate.preflight import (
    allowed_committed,
    normalized_sha256,
)

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize(
    "filename", ("source.py", "search.py", "audit.py", "preflight.py"),
)
def test_new_source_is_valid_python_without_ellipsis(filename: str) -> None:
    text = (ROOT / filename).read_text(encoding="utf-8")
    tree = ast.parse(text)
    assert not any(
        isinstance(node, ast.Expr)
        and isinstance(node.value, ast.Constant)
        and node.value.value is Ellipsis
        for node in ast.walk(tree)
    )
    assert "eval(" not in text
    assert "exec(" not in text


def test_only_prior_package_commits_permitted() -> None:
    assert allowed_committed("phase173_r4_r15r6_abstract_toda44_rule/audit.py")
    assert allowed_committed(".pytest_cache/v/cache/nodeids")
    assert not allowed_committed("phase173_r4_r10_general_toda56_core/core.py")
    assert not allowed_committed("phase173_r4_r15r7_source_first_abstract_certificate/search.py")


def test_previous_package_is_content_pinned(tmp_path: Path) -> None:
    path = tmp_path / "source.py"
    path.write_bytes(b"key = 10\n")
    digest = normalized_sha256(path)
    path.write_bytes(b"key = 10\r\n")
    assert normalized_sha256(path) == digest
    path.write_bytes(b"key = 11\r\n")
    assert normalized_sha256(path) != digest


def test_named_web_promotion_is_explicitly_forbidden() -> None:
    text = (ROOT / "search.py").read_text(encoding="utf-8")
    assert "def public_group_complete(self) -> bool:" in text
    assert "return False" in text
    assert "named_generator_shape_matched" in text
    assert "verified_db_step" in text
    assert "reconstruct_registered_goal" in text
    assert "derive_inference_proof_step" in text


def test_runner_only_runs_focused_tests_and_keeps_production_sources() -> None:
    script = (ROOT / "run.ps1").read_text(encoding="utf-8")
    assert "pytest -q" in script
    assert "phase173_r4_r10_general_toda56_core/tests/test_core.py" in script
    assert "git reset" not in script
    assert "git checkout" not in script
    assert "PHASE173_R4_R15R7_PHASE_COMPLETED=False" in script

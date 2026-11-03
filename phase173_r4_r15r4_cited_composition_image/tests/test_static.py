"""Source boundary and structural security assertions; no live repo needed."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("name", ("bridge.py", "replay.py", "audit.py", "preflight.py"))
def test_syntax_and_no_ellipsis(name: str) -> None:
    source = (ROOT / name).read_text(encoding="utf-8")
    tree = ast.parse(source)
    assert not any(
        isinstance(node, ast.Expr)
        and isinstance(node.value, ast.Constant)
        and node.value.value is Ellipsis
        for node in ast.walk(tree)
    )
    assert "eval(" not in source
    assert "exec(" not in source


def test_no_old_production_code_or_public_completion_change() -> None:
    assert (ROOT / "run.ps1").is_file()
    source = (ROOT / "audit.py").read_text(encoding="utf-8")
    assert '"public_completion": False' in source
    assert '"new_source_given": False' in source
    assert "replay_named_image" in source
    assert "proof_tree_steps" in source


def test_generic_composition_has_required_premises() -> None:
    source = (ROOT / "bridge.py").read_text(encoding="utf-8")
    assert "PremisePattern(" in source
    assert "proof_rule=ProofRule.INFERENCE" in source
    assert "return (GoalExpansion(rule, factors),)" in source
    assert "factor_image_goals(goal) == factors" in source


def test_replay_requires_checked_cited_fixed_sources() -> None:
    source = (ROOT / "replay.py").read_text(encoding="utf-8")
    assert "build_cited_stable_family_definitions()" in source
    assert "build_cited_chapter_vi_family_definitions()" in source
    assert "assertion.origin is AssertionOrigin.FIXED_STATEMENT" in source
    assert "find_inference_matches_for_rule" in source
    assert "apply_inference_match" in source


def test_commit_lineage_guard_is_not_blanket_disabled() -> None:
    source = (ROOT / "preflight.py").read_text(encoding="utf-8")
    assert "merge-base" in source
    assert "REVIEWED_BLOBS" in source
    assert "LOCAL_PINNED" in source
    assert "ALLOWED_COMMITTED" in source
    assert "head != remote" in source

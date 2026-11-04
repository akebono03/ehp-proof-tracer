"""Stand-alone review of fail-closed source rewrites."""
from __future__ import annotations

import ast

import pytest

from phase173_r4_r15r17_unified_model.patches import (
    EXPECTED_BLOBS,
    MODEL,
    NEW_STEPS_HELPER,
    replace_once,
)


def test_source_guard_has_all_five_explicit_production_blobs() -> None:
    assert len(EXPECTED_BLOBS) == 5
    assert MODEL in EXPECTED_BLOBS
    assert all(len(blob) == 40 for blob in EXPECTED_BLOBS.values())


def test_repeated_or_missing_anchor_is_rejected() -> None:
    assert replace_once("A\n", "A\n", "B\n", "fixture") == "B\n"
    with pytest.raises(RuntimeError, match="unreviewed or already patched"):
        replace_once("B\n", "A\n", "B\n", "fixture")
    with pytest.raises(RuntimeError, match="unreviewed or already patched"):
        replace_once("A\nA\n", "A\n", "B\n", "fixture")


def test_new_step_merger_has_no_dimension_or_named_generator_cases() -> None:
    tree = ast.parse(NEW_STEPS_HELPER)
    assert any(isinstance(node, ast.FunctionDef)
               and node.name == "verified_narrative_steps" for node in tree.body)
    assert "verified_tree_postorder" in NEW_STEPS_HELPER
    assert "result.proven_steps" in NEW_STEPS_HELPER
    assert "result.abstract_structure" in NEW_STEPS_HELPER
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            assert "\\nu" not in node.value
            assert "\\varepsilon" not in node.value

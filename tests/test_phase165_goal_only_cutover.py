"""Targeted, deterministic cutover checks."""
import ast
from pathlib import Path

import pytest

from phase165_goal_only_search import (
    GoalSearchIncompleteError,
    construct_registered_group_proof,
)
from phase164_r5_web_registry_connection import build_phase164_r5_web_pi5_3_proof


def test_goal_only_search_fails_closed_without_premise_discovery():
    with pytest.raises(GoalSearchIncompleteError, match="legacy proof selection is disabled"):
        construct_registered_group_proof(n=3, k=2)


def test_public_web_route_does_not_fallback_to_legacy():
    with pytest.raises(GoalSearchIncompleteError, match="legacy proof selection is disabled"):
        build_phase164_r5_web_pi5_3_proof(max_depth=2)


def test_web_route_excludes_specific_selection_imports():
    module = Path(__file__).resolve().parents[1] / "phase164_r5_web_registry_connection.py"
    tree = ast.parse(module.read_text(encoding="utf-8"))
    imports = {
        item.module
        for item in ast.walk(tree)
        if isinstance(item, ast.ImportFrom)
    }
    assert "phase162_pi5_3_web_replay" not in imports
    assert "phase162_web_narrative_integration" not in imports
    assert "phase164_r4_r8_registry_reconstruction" not in imports
    assert "phase165_goal_only_search" in imports

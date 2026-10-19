"""Read-only architecture contract for Phase 165 public group-proof path."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]


def _source(name: str) -> str:
    return (ROOT / name).read_text(encoding="utf-8-sig")


def _function(module: str, name: str) -> ast.FunctionDef:
    functions = [node for node in ast.parse(_source(module)).body
                 if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == name]
    assert len(functions) == 1, (module, name, "expected one public implementation")
    return functions[0]


def _calls(node: ast.AST) -> set[str]:
    return {call.func.id for call in ast.walk(node)
            if isinstance(call, ast.Call) and isinstance(call.func, ast.Name)}


def test_public_flask_bridge_uses_registered_search_and_shared_web_adapter() -> None:
    source = _function("phase165_r52_r4_flask_bridge.py", "build_group_proof_progress_view")
    calls = _calls(source)
    assert "search_group_from_registered_goal" in calls
    assert "search_registered_partial_proof" in calls
    assert "build_partial_web_group_proof_view" in calls
    assert len([call for call in ast.walk(source) if isinstance(call, ast.Call)
                and isinstance(call.func, ast.Name)
                and call.func.id == "build_partial_web_group_proof_view"]) == 1


def test_web_adapter_routes_narrative_through_shared_markdown() -> None:
    source = _function("phase165_r52_r3_web_adapter.py", "build_partial_web_group_proof_view")
    calls = _calls(source)
    assert "render_partial_proof_markdown" in calls
    assert "_build_group_proof_rendered_lines" in calls
    assert "WebGroupProofView" in calls
    assert "WebGroupProofStepView" in calls


def test_completed_adapter_preserves_replay_presentation_and_canonical_renderer() -> None:
    source = _function("phase165_r56_presentation_adapter.py", "render_completed_shared_narrative")
    calls = _calls(source)
    assert "build_complete_toda_group_result_proof_replay" in calls
    assert "build_toda_group_proof_presentation" in calls
    assert "render_toda_group_proof_narrative_markdown" in calls
    # Historical conditional proofstep rendering is known and explicitly tracked,
    # not silently treated as a newly introduced path.
    assert "render_completed_from_proofsteps" in calls


def test_completed_route_starts_from_registered_goal_and_uses_one_public_dispatch() -> None:
    source = _function("phase165_r52_partial_proof.py", "render_partial_proof_markdown")
    assert "render_completed_shared_narrative" in _calls(source)
    result = _function("phase165_r55_nk_only_goal.py", "search_group_from_registered_goal")
    assert "search_shared_group_goal" in _calls(result)


def test_no_group_specific_branch_added_to_public_adapter() -> None:
    for path, fn in (
        ("phase165_r52_r4_flask_bridge.py", "build_group_proof_progress_view"),
        ("phase165_r52_r3_web_adapter.py", "build_partial_web_group_proof_view"),
        ("phase165_r56_presentation_adapter.py", "render_completed_shared_narrative"),
    ):
        source = _function(path, fn)
        # These are routing contracts, not a prohibition on mathematically
        # justified group distinctions deeper in the established renderer.
        text = _source(path)
        for forbidden in ("pi3_2", "pi4_3", "pi_3_2", "pi_4_3"):
            # Historical documentation strings are not executable dispatch.
            executable = [n for n in ast.walk(source) if isinstance(n, ast.Compare)]
            for expression in executable:
                part = ast.get_source_segment(text, expression) or ""
                assert forbidden not in part, (path, forbidden)

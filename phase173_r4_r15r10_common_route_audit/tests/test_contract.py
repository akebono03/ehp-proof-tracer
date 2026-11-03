"""Small regression checks for shared Web Adapter contracts; no source edits."""
from __future__ import annotations

import ast
from pathlib import Path

from phase165_r52_partial_proof import ProofSearchStatus, make_partial_proof_result
from phase165_r52_r3_web_adapter import build_partial_web_group_proof_view
from phase168_r3_3_proof_narrative_model import build_proof_narrative_model
from phase173_r4_r15r10_common_route_audit.audit import specialized_dimensions


ROOT = Path(__file__).resolve().parents[2]


def test_shared_adapter_contains_single_abstract_projection_hook() -> None:
    path = ROOT / "phase165_r52_r3_web_adapter.py"
    tree = ast.parse(path.read_text(encoding="utf-8-sig"))
    calls = tuple(
        node for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "render_certified_abstract_section"
    )
    assert len(calls) == 1
    assert specialized_dimensions(tree) == ()


def test_abstract_projection_has_no_n_or_k_literal_branches() -> None:
    path = (ROOT / "phase173_r4_r15r9_shared_abstract_renderer" / "projection.py")
    tree = ast.parse(path.read_text(encoding="utf-8-sig"))
    assert specialized_dimensions(tree) == ()


def test_bare_partial_result_keeps_unresolved_goal_and_original_key() -> None:
    result = make_partial_proof_result(
        n=4, k=8, status=ProofSearchStatus.SEARCH_FAILED,
        open_goals=("unresolved named-generator relation",),
        diagnostics=("no registered proof",),
    )
    model = build_proof_narrative_model(result)
    view = build_partial_web_group_proof_view(
        result, mode="narrative", narrative_model=model,
    )
    assert view.key == "generic-partial-proof"
    assert view.partial_result is True
    assert result.conclusion is None
    assert result.open_goals == model.open_goals
    assert not any(
        line.kind == "heading" and line.prefix == "証明済みの抽象群構造"
        for line in view.rendered_lines
    )
    assert any(
        line.kind == "heading" and line.prefix == "未解決 Goal"
        for line in view.rendered_lines
    )


def test_trace_mode_does_not_inject_any_abstract_narrative() -> None:
    result = make_partial_proof_result(
        n=4, k=8, status=ProofSearchStatus.PARTIAL,
        open_goals=("pending",), diagnostics=("awaiting source",),
    )
    view = build_partial_web_group_proof_view(result, mode="trace")
    assert view.key == "generic-partial-proof"
    assert view.partial_result is True
    assert view.rendered_lines == ()

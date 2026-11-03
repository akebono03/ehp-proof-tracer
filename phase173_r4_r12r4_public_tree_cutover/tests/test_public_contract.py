"""Live source-owned public narrative tests for the five completed n=4 groups."""
from __future__ import annotations

import ast
from pathlib import Path
import re

import pytest

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase168_r3_3_proof_narrative_model import root_ancestor_step_indices
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from web_group_proof import build_standard_web_group_proof_view
from web_group_proof_common import _build_group_proof_rendered_lines


@pytest.mark.parametrize("dimension", (7, 8, 9, 10, 11))
def test_public_matches_common_renderer_and_certified_root(dimension: int) -> None:
    contexts = []
    result = search_group_from_registered_goal(
        n=4, k=dimension - 4, bridge=build_shared_typed_bridge(),
        context_sink=contexts.append,
    )
    assert result.status is ProofSearchStatus.COMPLETE
    assert result.open_goals == ()
    assert len(contexts) == 1
    model = build_linked_proof_narrative_model(result, contexts[0])
    assert model.root_index is not None
    root = model.steps[model.root_index]
    assert root.conclusion == result.conclusion
    assert root.inference_rule.match_guard(root.premises, {})
    ancestors = root_ancestor_step_indices(model.steps, model.root_index)
    assert len(model.citations) == 4
    for citation in model.citations:
        assert set(citation.step_indices).issubset(ancestors)
        assert citation.number >= 1
    rendered = render_model_backed_narrative_markdown(result, model)
    view = build_standard_web_group_proof_view(
        n=4, k=dimension - 4, mode="narrative", citation_source="model",
    )
    assert "先行データベース結果" in rendered or "DB prior: sphere.csv" in rendered
    assert view.key == "generic-complete-proof"
    assert view.partial_result is False
    assert "\\pi_" in view.conclusion_latex
    assert view.rendered_lines == _build_group_proof_rendered_lines(rendered)
    for citation in model.citations:
        assert f"[R{citation.number}]" in rendered


def test_active_web_adapter_cannot_depend_on_pi_specific_narrative() -> None:
    source = Path("phase165_r52_r3_web_adapter.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    functions = tuple(node for node in tree.body if isinstance(node, ast.FunctionDef)
                      and node.name == "build_partial_web_group_proof_view")
    assert len(functions) == 1
    assert "project_verified_toda56_narrative" not in source
    assert "project_verified_pi74_narrative" not in source
    assert "render_model_backed_narrative_markdown(result, narrative_model)" in source
    function = functions[0]
    for node in ast.walk(function):
        if isinstance(node, ast.ImportFrom):
            assert not re.search(r"pi[0-9]+.*narrative", node.module or "")
            for name in node.names:
                assert not re.search(r"pi[0-9]+.*narrative", name.name)
        if isinstance(node, ast.Assign):
            if any(isinstance(target, ast.Name) and target.id == "markdown"
                   for target in node.targets):
                if isinstance(node.value, ast.Call):
                    called = node.value.func
                    assert isinstance(called, ast.Name)
                    assert called.id in (
                        "render_partial_proof_markdown",
                        "render_model_backed_narrative_markdown",
                    )
        if isinstance(node, ast.If):
            for compare in ast.walk(node.test):
                if not isinstance(compare, ast.Compare):
                    continue
                fields = (compare.left, *compare.comparators)
                names = {value.id for value in fields if isinstance(value, ast.Name)}
                has_literal = any(isinstance(value, ast.Constant)
                                  and type(value.value) is int for value in fields)
                if names & {"n", "k", "dimension"} and has_literal:
                    assert not any(isinstance(op, (ast.Eq, ast.NotEq))
                                   for op in compare.ops)

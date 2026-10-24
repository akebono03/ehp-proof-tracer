"""Focused tests for generic, name-independent intermediate proof-step display."""
from __future__ import annotations

import ast
import inspect
from dataclasses import replace
from pathlib import Path

import pytest

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from web_group_proof import build_standard_web_group_proof_view
from phase168_r3_38_frozen_fulltext_audit import audit as frozen
from phase168_r3_39f_frozen_comparison.audit import assess

PACKAGE = Path(__file__).resolve().parents[1]
CASES = (
    ("pi3_2", 2, 1, 18, 4),
    ("pi4_3", 3, 1, 25, 4),
    ("pi5_4", 4, 1, 10, 3),
)


@pytest.mark.parametrize("name,n,k,step_count,ref_count", CASES)
def test_three_public_group_fulltexts_unmodified(name, n, k, step_count, ref_count):
    current, model, view = frozen.capture(n, k)
    golden = (PACKAGE / "baselines" / f"{name}_current.md").read_text(encoding="utf-8")
    assert current == golden
    assert len(model.steps) == step_count
    assert len(model.citations) == ref_count
    reference, proof = frozen.sections(current)
    assert all(c.statement_bodies for c in model.citations)
    assert all(item["present"] for item in assess(name, proof))
    used = set(__import__("re").findall(r"\[R(\d+)\]", proof))
    expected = {str(c.number) for c in model.citations}
    assert used == expected


def test_renderer_suppression_does_not_depend_on_rule_name():
    bridge = build_shared_typed_bridge()
    contexts = []
    result = search_group_from_registered_goal(
        n=4, k=1, bridge=bridge, context_sink=contexts.append,
    )
    assert result.status is ProofSearchStatus.COMPLETE
    assert contexts
    model = build_linked_proof_narrative_model(result, contexts[-1])
    original = render_model_backed_narrative_markdown(result, model)
    assert model.root_index is not None
    root = model.steps[model.root_index]
    assert root.inference_rule is not None
    renamed = replace(root, inference_rule=replace(
        root.inference_rule,
        name="renamed certified normalization inference without literal rule identity",
    ))
    changed_steps = tuple(
        renamed if i == model.root_index else s
        for i, s in enumerate(model.steps)
    )
    changed_result = replace(result, proven_steps=changed_steps)
    changed_model = replace(model, steps=changed_steps)
    assert render_model_backed_narrative_markdown(changed_result, changed_model) == original


def test_renderer_does_not_identify_normalization_by_rule_name():
    source = inspect.getsource(render_model_backed_narrative_markdown)
    assert "proved generator suspension normalizes transported cyclic group" not in source
    assert "and isinstance(transported.rhs.generator, IteratedSuspension)" in source
    assert "and transported.rhs.generator.exponent == 1" in source
    assert "== element_tex(witness_step.conclusion.source_generator)" in source
    assert "== element_tex(witness_step.conclusion.target_generator)" in source
    assert not any(
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == "match_guard"
        for node in ast.walk(ast.parse(source))
    )

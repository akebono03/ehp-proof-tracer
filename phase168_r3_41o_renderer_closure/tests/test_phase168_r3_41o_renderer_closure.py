"""Phase 168 R3-41O: generic composition, target intro, no rule replay."""
from __future__ import annotations

import ast
import inspect
import re
from pathlib import Path

import pytest

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from phase168_r3_38_frozen_fulltext_audit.audit import sections
from phase165_r12_r12_ehp_consequences import EHPImageEqualsKernelStatement
from phase165_r12_r13_kernel_image import SuspensionKernelFreeCyclicStatement


@pytest.fixture(scope="module")
def cases():
    bridge = build_shared_typed_bridge()
    found = {}
    for name, n, k in (("pi3_2", 2, 1), ("pi4_3", 3, 1), ("pi5_4", 4, 1)):
        contexts = []
        result = search_group_from_registered_goal(n=n, k=k, bridge=bridge,
                                                  context_sink=contexts.append)
        assert result.status is ProofSearchStatus.COMPLETE
        assert contexts
        model = build_linked_proof_narrative_model(result, contexts[-1])
        found[name] = (result, model, render_model_backed_narrative_markdown(result, model))
    return found


@pytest.mark.parametrize("name,target", (
    ("pi3_2", r"\pi_{3}^{2}"),
    ("pi4_3", r"\pi_{4}^{3}"),
    ("pi5_4", r"\pi_{5}^{4}"),
))
def test_intro_uses_typed_target_only(cases, name, target):
    result, _, rendered = cases[name]
    _, proof = sections(rendered)
    if name == "pi5_4":
        assert f"${target}$の群構造を決定する." in proof
        assert "次の完全列を考える" not in proof
    else:
        assert f"${target}$の群構造を決定するために" in proof
        assert "次の完全列を考える" in proof
    assert proof.count("の群構造を決定する") == 1
    assert "未解決 Goal" not in proof


def test_kernel_chain_comes_only_from_typed_premises(cases):
    _, model, rendered = cases["pi4_3"]
    kernel_steps = [s for s in model.steps
                    if isinstance(s.conclusion, SuspensionKernelFreeCyclicStatement)]
    assert kernel_steps
    assert any(any(isinstance(p.conclusion, EHPImageEqualsKernelStatement)
                       for p in step.premises) for step in kernel_steps)
    _, proof = sections(rendered)
    assert (r"完全性より, $\ker E=\operatorname{Im}\Delta="
            r"\mathbb{Z}\{2\eta_{2}\}$.") in proof
    assert r"\operatorname{Im}\Delta=\mathbb{Z}\{2\eta_{2}\}" in proof
    assert r"\operatorname{Im}\Delta=\ker E" not in proof


def test_pi54_final_group_has_no_duplicate_transport(cases):
    _, model, rendered = cases["pi5_4"]
    assert len(model.steps) == 10
    _, proof = sections(rendered)
    assert r"\pi_{5}^{4} = \mathbb{Z}/2\{\eta_{4}\}" in proof
    assert r"\pi_{5}^{4} = \mathbb{Z}/2\{E\eta_{3}\}" not in proof
    assert proof.index("(n,m,k)=(3,4,1)") < proof.index(r"E(\eta_{3})=\eta_{4}")


@pytest.mark.parametrize("name", ("pi3_2", "pi4_3", "pi5_4"))
def test_reference_and_result_unchanged(cases, name):
    _, model, rendered = cases[name]
    reference, proof = sections(rendered)
    assert all(citation.statement_bodies for citation in model.citations)
    assert {int(num) for num in re.findall(r"\[R(\d+)\]", proof)} == {
        cite.number for cite in model.citations
    }
    assert proof.rstrip().endswith("□")
    assert "導出により" not in proof


def test_renderer_never_replays_match_guard():
    source = inspect.getsource(render_model_backed_narrative_markdown)
    node = ast.parse(source)
    guard_calls = [call for call in ast.walk(node)
                   if isinstance(call, ast.Call)
                   and isinstance(call.func, ast.Attribute)
                   and call.func.attr == "match_guard"]
    assert guard_calls == []
    assert "generator_transport_normalization_rule" not in source

"""Typed-proof-only suppression of redundant intermediate prose."""
from __future__ import annotations

import re

import pytest

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from phase168_r3_38_frozen_fulltext_audit.audit import sections
from phase168_r3_39f_frozen_comparison.audit import assess
from phase165_r12_r12_ehp_consequences import EHPImageEqualsKernelStatement
from phase165_r12_r13_kernel_image import SuspensionKernelFreeCyclicStatement
from phase166_r3v_generator_transport import generator_transport_normalization_rule
from homotopy_groups import FiniteCyclicGroup
from phase165_r14_r14_diagonal_and_prop42 import GeneratorSuspension
from proof import Relation, ProofRule


@pytest.fixture(scope="module")
def cases():
    bridge = build_shared_typed_bridge()
    collected = {}
    for name, n, k, total in (("pi3_2", 2, 1, 18), ("pi4_3", 3, 1, 25), ("pi5_4", 4, 1, 10)):
        contexts = []
        proof = search_group_from_registered_goal(n=n, k=k, bridge=bridge,
                                                  context_sink=contexts.append)
        assert proof.status is ProofSearchStatus.COMPLETE
        assert contexts
        model = build_linked_proof_narrative_model(proof, contexts[-1])
        assert len(model.steps) == total
        markdown = render_model_backed_narrative_markdown(proof, model)
        collected[name] = (proof, model, markdown)
    return collected


def test_pi43_exactness_is_consumed_by_concrete_kernel(cases):
    _, model, markdown = cases["pi4_3"]
    equality_steps = [step for step in model.steps
                      if isinstance(step.conclusion, EHPImageEqualsKernelStatement)
                      and step.conclusion.window.first_map is not None]
    assert equality_steps
    assert any(
        isinstance(step.conclusion, SuspensionKernelFreeCyclicStatement)
        and len(step.premises) == 2
        and any(parent is equality for parent in step.premises)
        for equality in equality_steps for step in model.steps
    )
    reference, proof = sections(markdown)
    assert r"\operatorname{Im}\Delta=\ker E" not in proof
    assert r"\ker E=\mathbb{Z}\{2\eta_{2}\}" in proof
    assert r"\operatorname{Im}\Delta=\mathbb{Z}\{2\eta_{2}\}" in proof
    assert "完全性より" in proof


def test_pi54_transported_intermediate_is_consumed_by_normalization(cases):
    _, model, markdown = cases["pi5_4"]
    candidates = [(step, step.premises[0]) for step in model.steps
                  if step.rule is ProofRule.INFERENCE
                  and isinstance(step.conclusion, Relation)
                  and isinstance(step.conclusion.rhs, FiniteCyclicGroup)
                  and len(step.premises) == 2
                  and isinstance(step.premises[1].conclusion, GeneratorSuspension)
                  and generator_transport_normalization_rule(step.conclusion).match_guard(
                      step.premises, {}
                  )]
    assert candidates
    assert any(candidate.rule is ProofRule.INFERENCE for _, candidate in candidates)
    _, proof = sections(markdown)
    assert r"\pi_{5}^{4} = \mathbb{Z}/2\{\eta_{4}\}" in proof
    assert not any(r"\pi_{5}^{4} = " in line and r"\eta_{3}" in line
                   for line in proof.splitlines())
    assert proof.index(r"\pi_{4}^{3} = ") < proof.index("(n,m,k)=(3,4,1)")
    assert proof.index("(n,m,k)=(3,4,1)") < proof.index(r"E(\eta_{3})=\eta_{4}")
    assert proof.index(r"E(\eta_{3})=\eta_{4}") < proof.index(r"\pi_{5}^{4} = ")


@pytest.mark.parametrize("name", ["pi3_2", "pi4_3", "pi5_4"])
def test_no_source_citation_or_benchmark_regression(cases, name):
    _, model, markdown = cases[name]
    reference, proof = sections(markdown)
    used = {int(n) for n in re.findall(r"\[R(\d+)\]", proof)}
    expected = {citation.number for citation in model.citations}
    assert used == expected
    assert all(citation.statement_bodies for citation in model.citations)
    assert all(check["present"] for check in assess(name, proof))
    assert proof.rstrip().endswith("□")
    assert "導出により" not in proof
    assert " を得る" not in proof


def test_pi32_hopf_reasoning_does_not_lose_exactness(cases):
    _, model, markdown = cases["pi3_2"]
    _, proof = sections(markdown)
    assert r"\operatorname{Im}\Delta=\ker E=0" in proof
    assert "単射性と全射性より" in proof
    assert "は単射" in proof and "は全射" in proof and "は同型" in proof

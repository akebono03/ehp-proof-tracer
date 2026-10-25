"""R3-41P13: public positioned proof handoff and counterfeit rejection."""
from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from unittest.mock import patch

import pytest

from phase165_r52_partial_proof import ProofSearchStatus, make_partial_proof_result
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase168_r3_3_proof_narrative_model import build_proof_narrative_model
from phase168_r3_41p13_trust_boundary import (
    UnverifiedProofTree,
    verify_proof_tree_for_narrative,
)
from proof import ProofRule, ProofStep
from phase165_r12_r12_ehp_consequences import ehp_image_equals_kernel_inference_rule
from phase166_r3ac_stable_notation import stable_eta_notation_rule
from phase168_r3_38_frozen_fulltext_audit.audit import capture
from web_group_proof import build_standard_web_group_proof_view


@pytest.fixture(scope="module")
def positioned_cases():
    bridge = build_shared_typed_bridge()
    found = {}
    for name, n, k in (("pi3_2", 2, 1), ("pi4_3", 3, 1), ("pi5_4", 4, 1)):
        screened = []
        result = search_group_from_registered_goal(
            n=n, k=k, bridge=bridge, context_sink=screened.append,
        )
        assert result.status is ProofSearchStatus.COMPLETE
        assert screened
        citing = resolve_specialized_goal_citing_id(bridge, result.conclusion)
        assert citing is not None
        found[name] = result, screened[-1], citing
    return found


@pytest.mark.parametrize("name,counts", (
    ("pi3_2", (13, 5)),
    ("pi4_3", (19, 6)),
    ("pi5_4", (7, 3)),
))
def test_real_positioned_proof_trees_are_verified(positioned_cases, name, counts):
    result, screened, citing = positioned_cases[name]
    assert verify_proof_tree_for_narrative(
        result, screened, citing_assertion_id=citing,
    ) == counts


@pytest.mark.parametrize("name", ("pi3_2", "pi4_3", "pi5_4"))
def test_web_handoff_keeps_reference_proof_citations_unchanged(name):
    dims = {"pi3_2": (2, 1), "pi4_3": (3, 1), "pi5_4": (4, 1)}
    n, k = dims[name]
    import phase168_r3_41p13_trust_boundary as boundary
    calls = []
    original = boundary.verify_proof_tree_for_narrative

    def observe(result, bridge, *, citing_assertion_id):
        counts = original(result, bridge, citing_assertion_id=citing_assertion_id)
        calls.append(counts)
        return counts

    with patch.object(boundary, "verify_proof_tree_for_narrative", side_effect=observe):
        rendered, model, _ = capture(n, k)
    assert len(calls) == 1
    assert len(model.steps) == sum(calls[0])
    baseline = Path(__file__).resolve().parents[2] / (
        "phase168_r3_41p12_publication_boundary_audit/baselines/" + name + ".md"
    )
    assert rendered == baseline.read_text(encoding="utf-8")


def test_counterfeit_stable_eta_inference_cannot_cross_boundary(positioned_cases):
    result, screened, citing = positioned_cases["pi5_4"]
    givens = tuple(step for step in result.proven_steps if step.rule is ProofRule.GIVEN)
    assert len(givens) >= 2
    counterfeit = ProofStep(
        conclusion=result.conclusion,
        premises=givens[:2],
        rule=ProofRule.INFERENCE,
        inference_rule=stable_eta_notation_rule(result.conclusion),
    )
    corrupted = replace(result, proven_steps=result.proven_steps + (counterfeit,))
    with pytest.raises(UnverifiedProofTree):
        verify_proof_tree_for_narrative(corrupted, screened, citing_assertion_id=citing)


def test_counterfeit_ehp_exactness_inference_cannot_cross_boundary(positioned_cases):
    result, screened, citing = positioned_cases["pi4_3"]
    given = next(step for step in result.proven_steps if step.rule is ProofRule.GIVEN)
    counterfeit = ProofStep(
        conclusion="counterfeit EHP image equals kernel",
        premises=(given,),
        rule=ProofRule.INFERENCE,
        inference_rule=ehp_image_equals_kernel_inference_rule(),
    )
    corrupted = replace(result, proven_steps=result.proven_steps + (counterfeit,))
    with pytest.raises(UnverifiedProofTree):
        verify_proof_tree_for_narrative(corrupted, screened, citing_assertion_id=citing)


def test_counterfeit_given_cannot_cross_boundary_but_raw_model_api_remains(positioned_cases):
    result, screened, citing = positioned_cases["pi3_2"]
    counterfeit = ProofStep(
        conclusion="unregistered source", premises=(), rule=ProofRule.GIVEN,
    )
    corrupted = replace(result, proven_steps=result.proven_steps + (counterfeit,))
    assert counterfeit in build_proof_narrative_model(corrupted).steps
    with pytest.raises(UnverifiedProofTree, match="GIVEN"):
        verify_proof_tree_for_narrative(corrupted, screened, citing_assertion_id=citing)


def test_given_cannot_use_target_as_its_own_publication_source(positioned_cases):
    result, screened, _ = positioned_cases["pi3_2"]
    given = next(step for step in result.proven_steps if step.rule is ProofRule.GIVEN)
    source = next(link.assertion_id for link in screened.proof_links if link.step == given)
    with pytest.raises(UnverifiedProofTree, match="GIVEN"):
        verify_proof_tree_for_narrative(result, screened, citing_assertion_id=source)


def test_unpositioned_partial_can_still_render_without_promotion():
    partial = make_partial_proof_result(
        n=12, k=9, status=ProofSearchStatus.PARTIAL,
        open_goals=("unresolved",), diagnostics=("not yet derived",),
    )
    model = build_proof_narrative_model(partial)
    assert model.status is ProofSearchStatus.PARTIAL
    assert model.steps == ()
    assert model.open_goals == ("unresolved",)

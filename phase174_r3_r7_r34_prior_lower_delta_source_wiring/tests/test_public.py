"""Proof-use screening and R30 shared-provider regression for R34."""
from __future__ import annotations

from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase169_r10e2_unpositioned_citation.source_first import (
    screen_independent_sources_for_derived_goal,
)
from phase174_r3_r7_r25_prop27_isolated_inference.rule import (
    Prop27GeneralTheoremPremise,
    typed_specialization,
)
from phase174_r3_r7_r34_prior_lower_delta_source_wiring.audit import screen_report
from proof import ProofRule
from toda_rules import TodaDeltaImageUpToSignStatement


def test_r34_two_prior_cited_leaves_reach_public_screen():
    result = screen_report()
    assert result["screened_prior_codomain_leaves"] == 1
    assert result["screened_prior_delta_generator_leaves"] == 1
    assert result["new_direct_kernel_givens"] == 0
    assert result["new_direct_root_givens"] == 0
    assert result["lower_kernel_proved"] is False
    assert result["root_complete"] is False


def test_shared_bridge_presents_signed_delta_as_only_cited_leaf():
    root = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    bridge = screen_independent_sources_for_derived_goal(
        build_shared_typed_bridge(), goal=root,
    )
    matches = tuple(
        link.step for link in bridge.proof_links
        if link.step is not None
        and type(link.step.conclusion) is TodaDeltaImageUpToSignStatement
        and link.step.conclusion.map.source_group == TodaPrimaryGroup(11, 11)
        and link.step.conclusion.map.target_group == TodaPrimaryGroup(9, 5)
    )
    assert len(matches) == 1
    assert matches[0].rule is ProofRule.GIVEN
    assert matches[0].inference_rule.literature_reference.locator == "(5.10)"


def test_r30_cited_prop27_shared_provider_remains_operational():
    root = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    bridge = screen_independent_sources_for_derived_goal(
        build_shared_typed_bridge(), goal=root,
    )
    provider = shared_expansion_provider(bridge, proof_target=root)
    proposals = provider(typed_specialization(6))
    assert any(proposal.subgoals == (Prop27GeneralTheoremPremise(),)
               for proposal in proposals)

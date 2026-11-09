"""Public source-first R36 connection and exact verified ancestry checks."""
from __future__ import annotations

from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
from phase165_r12_r2_quotient_rules import KernelMultipleStatement
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase169_r10e2_unpositioned_citation.source_first import (
    screen_independent_sources_for_derived_goal,
)
from phase174_r3_r7_r34_prior_lower_delta_source_wiring.source import checked_prior_statements
from phase174_r3_r7_r35_isolated_cyclic_delta_kernel.rule import RULE_NAME
from phase174_r3_r7_r36_cited_kernel_provider_wiring.audit import audit_public_connection
from proof import ProofRule


def test_shared_provider_offers_real_cited_kernel_expansion() -> None:
    root = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    bridge = screen_independent_sources_for_derived_goal(build_shared_typed_bridge(), goal=root)
    group, image = checked_prior_statements()
    goal = KernelMultipleStatement(image.map, image.map.source_group, image.element, 2)
    proposals = shared_expansion_provider(bridge, proof_target=root)(goal)
    matches = tuple(item for item in proposals if item.rule.name == RULE_NAME)
    assert matches
    assert matches[0].subgoals[1:] == (group, image)


def test_cited_diagonal_and_real_priors_form_inference_only() -> None:
    outcome = audit_public_connection()
    assert outcome["diagonal_source_inferred"] is True
    assert outcome["three_real_cited_premises_form_inference"] is True
    assert outcome["kernel_inference_in_audit"] is True
    assert outcome["kernel_inference_inserted_as_given"] is False
    assert outcome["root_complete"] is False


def test_source_bridge_has_no_direct_kernel_or_root_given() -> None:
    root = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    bridge = screen_independent_sources_for_derived_goal(build_shared_typed_bridge(), goal=root)
    _, image = checked_prior_statements()
    matches = tuple(
        link.step for link in bridge.proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
        and (link.step.conclusion == root
             or (type(link.step.conclusion) is KernelMultipleStatement
                 and link.step.conclusion.map == image.map))
    )
    assert matches == ()

"""Focused regression tests for one new public order-four backward proposal."""
from __future__ import annotations

from dataclasses import replace

from expression import GeneratorSymbol, HomotopyElement, Multiple
from homotopy_groups import TodaPrimaryGroup
from phase165_r52_r9_shared_math import shared_expansion_provider
from phase171_r2i_eta_hopf_bridge.audit import _screened_context
from phase171_r2j_r4_r6_middle_cardinality.source import FiniteGroupCardinality
from phase171_r2j_r4_r7_nonzero_nu_order.audit import build_nonzero_nu_order_proof
from phase171_r2j_r4_r7_nonzero_nu_order.source import (
    FiniteElementOrder,
    NonZeroGroupElement,
    expand_public_order_four_from_nonzero_double,
)
from proof import ProofRule, find_inference_matches_for_rule
from phase164_r8_proofstep_factory import derive_inference_proof_step


def _goal() -> FiniteElementOrder:
    group = TodaPrimaryGroup(6, 3)
    element = HomotopyElement(
        name="ν′", dimension=3, source=6, target=3,
        generator=GeneratorSymbol(family="ν", decoration="′"),
    )
    return FiniteElementOrder(group, element, 4)


def test_public_order_four_requires_cardinality_and_nonzero_double() -> None:
    goal = _goal()
    routes = expand_public_order_four_from_nonzero_double(goal)
    assert len(routes) == 1
    option = routes[0]
    assert option.subgoals == (
        FiniteGroupCardinality(goal.group, 4),
        NonZeroGroupElement(goal.group, Multiple(2, goal.element)),
    )
    assert option.rule.name == "finite order-four group and nonzero double imply order-four element"


def test_public_order_four_rejects_untyped_and_other_orders() -> None:
    goal = _goal()
    assert expand_public_order_four_from_nonzero_double("unrelated") == ()
    assert expand_public_order_four_from_nonzero_double(replace(goal, order=2)) == ()
    assert expand_public_order_four_from_nonzero_double(replace(goal, order=True)) == ()
    bad = replace(goal.element, source=None)
    assert expand_public_order_four_from_nonzero_double(replace(goal, element=bad)) == ()


def test_public_provider_matches_real_inferred_r4_r7_parents() -> None:
    screened, target, _ = _screened_context()
    _, inferred, _, report = build_nonzero_nu_order_proof()
    assert report["new_given_added"] == 0
    assert inferred.rule is ProofRule.INFERENCE
    proposals = shared_expansion_provider(screened, proof_target=target)(inferred.conclusion)
    matches = tuple(
        proposal for proposal in proposals
        if proposal.rule.name == inferred.inference_rule.name
        and proposal.subgoals == tuple(parent.conclusion for parent in inferred.premises)
    )
    assert len(matches) == 1
    verified = find_inference_matches_for_rule(matches[0].rule, inferred.premises)
    assert any(
        derive_inference_proof_step(match).conclusion == inferred.conclusion
        and all(parent.rule is ProofRule.INFERENCE for parent in match.premises)
        for match in verified
    )

"""Focused public double-image proposal tests using independently established proof."""
from __future__ import annotations

from dataclasses import replace

import pytest

from phase165_r52_r9_shared_math import shared_expansion_provider
from phase169_r10e5_composite_generator_image.rule import _endpoints
from phase171_r2i_eta_hopf_bridge.audit import _screened_context
from phase171_r2j_r4_r3_double_image_bridge.audit import build_double_image_proof
from phase171_r2j_r4_r3_double_image_bridge.source import (
    expand_public_cited_double_image_equality,
)
from proof import ProofRule


def _fixture():
    screened, target, _ = _screened_context()
    root, _, report = build_double_image_proof()
    assert root.rule is ProofRule.INFERENCE
    assert report["new_given_added"] == 0
    available = tuple(
        link.step.conclusion for link in screened.proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
    )
    return target, root, available, screened


def test_public_cited_double_image_matches_existing_inference() -> None:
    target, root, available, screened = _fixture()
    candidates = expand_public_cited_double_image_equality(root.conclusion, available)
    expected = tuple(parent.conclusion for parent in root.premises)
    assert any(item.subgoals == expected and item.rule.name == root.inference_rule.name for item in candidates)
    shared = shared_expansion_provider(screened, proof_target=target)(root.conclusion)
    assert any(item.subgoals == expected and item.rule.name == root.inference_rule.name for item in shared)


def test_public_cited_double_image_missing_sources_fail_closed() -> None:
    _, root, available, _ = _fixture()
    assert expand_public_cited_double_image_equality(root.conclusion, ()) == ()
    without_double = tuple(item for item in available if getattr(item, "lhs", None) != root.conclusion.lhs)
    assert expand_public_cited_double_image_equality(root.conclusion, without_double) == ()
    with pytest.raises(TypeError, match="screened"):
        expand_public_cited_double_image_equality(root.conclusion, [])


def test_public_cited_double_image_rejects_wrong_goal() -> None:
    _, root, available, _ = _fixture()
    assert expand_public_cited_double_image_equality(root.conclusion.lhs, available) == ()
    assert expand_public_cited_double_image_equality(
        replace(root.conclusion, lhs=root.conclusion.rhs), available,
    ) == ()


def test_public_cited_double_image_checks_suspension_domain() -> None:
    _, root, available, _ = _fixture()
    lhs_endpoint = _endpoints(root.conclusion.lhs.expression)
    source_endpoint = _endpoints(root.conclusion.rhs.expression)
    assert lhs_endpoint == (6, 3)
    assert source_endpoint == (5, 2)
    assert source_endpoint == (lhs_endpoint[0] - 1, lhs_endpoint[1] - 1)
    proposals = expand_public_cited_double_image_equality(root.conclusion, available)
    assert any(
        proposal.subgoals == tuple(p.conclusion for p in root.premises)
        for proposal in proposals
    )

def test_public_cited_double_uses_target_generator_not_suspension_input() -> None:
    _, root, available, _ = _fixture()
    source_double = root.premises[0].conclusion
    inferred_image = root.premises[1].conclusion
    # Toda (5.3) identifies 2*nu' with the suspended *target* generator.
    # The E argument is a different element, in the source group.
    assert source_double.rhs == inferred_image.target_generator
    assert source_double.rhs != root.conclusion.rhs.expression
    assert _endpoints(source_double.rhs) == _endpoints(root.conclusion.lhs.expression)
    assert _endpoints(inferred_image.source_generator) == _endpoints(root.conclusion.rhs.expression)
    proposals = expand_public_cited_double_image_equality(root.conclusion, available)
    assert any(
        proposal.subgoals == (source_double, inferred_image)
        and proposal.rule.name == root.inference_rule.name
        for proposal in proposals
    )

"""Focused R20R8 public proposal and negative tests."""
from __future__ import annotations

from dataclasses import replace

import pytest

from phase171_r2i_eta_hopf_bridge.audit import _screened_context
from phase171_r2j_r4_r7_nonzero_nu_order.audit import build_nonzero_nu_order_proof
from phase171_r2j_r4_r7_nonzero_nu_order.source import (
    expand_public_nonzero_double_from_cited_source,
)
from expression import Multiple
from phase165_r52_r9_shared_math import shared_expansion_provider
from proof import ProofRule


def _fixture():
    screened, target, _ = _screened_context()
    double, _, _, _ = build_nonzero_nu_order_proof()
    available = tuple(
        link.step.conclusion for link in screened.proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
    )
    return target, double, available, screened


def test_public_nonzero_double_matches_independent_proof() -> None:
    target, root, available, screened = _fixture()
    options = expand_public_nonzero_double_from_cited_source(root.conclusion, available)
    assert len(options) == 1
    assert options[0].subgoals == tuple(parent.conclusion for parent in root.premises)
    assert options[0].rule.name == root.inference_rule.name
    from_provider = shared_expansion_provider(screened, proof_target=target)(root.conclusion)
    assert any(
        option.subgoals == options[0].subgoals
        and option.rule.name == options[0].rule.name
        for option in from_provider
    )


def test_nonzero_double_rejects_missing_citations_and_invalid_coefficient() -> None:
    _, root, available, _ = _fixture()
    assert expand_public_nonzero_double_from_cited_source(root.conclusion, ()) == ()
    assert expand_public_nonzero_double_from_cited_source(
        replace(root.conclusion, element=Multiple(3, root.conclusion.element.expression)),
        available,
    ) == ()
    with pytest.raises(TypeError, match="screened"):
        expand_public_nonzero_double_from_cited_source(root.conclusion, [])


def test_nonzero_double_missing_source_relation_is_rejected() -> None:
    _, root, available, _ = _fixture()
    original = root.conclusion.element
    without_double = tuple(
        claim for claim in available
        if getattr(claim, "lhs", None) != original
    )
    assert expand_public_nonzero_double_from_cited_source(root.conclusion, without_double) == ()

"""Focused EHP runtime contracts for bounded public source-first connection."""
from __future__ import annotations

from pathlib import Path

import pytest

from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase173_r4_r7_source_first_rule.rule import checked_inputs
from phase173_r4_r8_public_connection.route import prepare_pi4_higher_public_connection
from proof import ProofRule
from phase173_r4_r1_lemma54_source_bridge.source import TodaLemma54TypedSource


@pytest.mark.parametrize("dimension", (8, 9, 10))
def test_only_verified_toda56_targets_have_bounded_public_connection(dimension: int) -> None:
    bridge = build_shared_typed_bridge()
    goal = exact_prior_database_result(4, dimension - 4)
    assert checked_inputs(goal) is not None
    original_assertions = len(bridge.registry._assertions)
    prepared = prepare_pi4_higher_public_connection(
        bridge=bridge, goal=goal, prior_conclusions=(),
    )
    assert prepared is not None
    screened, provider = prepared
    assert callable(provider)
    assert len(bridge.registry._assertions) == original_assertions
    roots = provider(goal)
    assert roots
    source = tuple(
        link.step.conclusion for link in screened.proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
    )
    assert sum(type(item) is TodaLemma54TypedSource for item in source) == 1
    assert all(link.step.conclusion != goal for link in screened.proof_links
               if link.step is not None)


def test_pi74_public_route_not_selected_by_new_connection() -> None:
    bridge = build_shared_typed_bridge()
    goal = exact_prior_database_result(4, 3)
    assert prepare_pi4_higher_public_connection(
        bridge=bridge, goal=goal, prior_conclusions=(),
    ) is None


def test_no_unverified_prior_context() -> None:
    bridge = build_shared_typed_bridge()
    goal = exact_prior_database_result(4, 4)
    assert prepare_pi4_higher_public_connection(
        bridge=bridge, goal=goal, prior_conclusions=[],
    ) is None

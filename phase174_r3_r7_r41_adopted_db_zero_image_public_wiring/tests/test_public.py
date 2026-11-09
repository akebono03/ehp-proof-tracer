"""R41 typed public integration and source fail-closed contract."""
from __future__ import annotations

from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement, TodaSuspensionMap
from map_property_rules import ImageZeroStatement
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase169_r10e2_unpositioned_citation.source_first import screen_independent_sources_for_derived_goal
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase174_r3_r7_r40_adopted_db_zero_image_isolated.rule import RULE_NAME
from phase174_r3_r7_r41_adopted_db_zero_image_public_wiring.provider import (
    build_public_adopted_zero_image_provider, screened_general_law,
)


def fixture():
    root = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    bridge = screen_independent_sources_for_derived_goal(build_shared_typed_bridge(), goal=root)
    prior = exact_prior_database_result(5, 5)
    suspension = TodaSuspensionMap(prior.lhs, TodaPrimaryGroup(11, 6))
    return root, bridge, prior, ImageZeroStatement(suspension)


def test_public_provider_contains_one_source_bound_adopted_db_candidate():
    root, bridge, prior, goal = fixture()
    assert len(screened_general_law(bridge)) == 1
    proposed = tuple(x for x in shared_expansion_provider(bridge, proof_target=root)(goal)
                     if x.rule.name == RULE_NAME)
    assert len(proposed) == 1
    assert proposed[0].subgoals[0] == prior
    assert len(proposed[0].subgoals) == 2


def test_source_stripping_and_invalid_roots_fail_closed():
    root, bridge, prior, goal = fixture()
    source_free = RegistryBridgeResult(bridge.registry, bridge.records, ())
    assert screened_general_law(source_free) == ()
    assert build_public_adopted_zero_image_provider(
        bridge=source_free, proof_target=root,
    )(goal) == ()
    assert build_public_adopted_zero_image_provider(
        bridge=bridge, proof_target=TodaPrimaryGroupZeroStatement(prior.lhs),
    )(goal) == ()
    assert build_public_adopted_zero_image_provider(
        bridge=bridge, proof_target=None,
    )(goal) == ()


def test_public_chain_preserves_isolated_proof_and_does_not_claim_root():
    from phase174_r3_r7_r41_adopted_db_zero_image_public_wiring.audit import inspect_public_r41
    result = inspect_public_r41()
    assert result["public_r41_zero_image_proposals"] == 1
    assert result["r40_isolated_zero_image_verified"] is True
    assert result["r40_db_given_preserved"] is True
    assert result["new_given_statements"] == 0
    assert result["upper_delta_surjectivity_verified"] is False
    assert result["root_complete"] is False

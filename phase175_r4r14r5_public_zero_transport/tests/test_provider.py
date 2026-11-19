"""Focused Phase 175 R4R14R5 public source and generic-proof contracts."""
from __future__ import annotations

from dataclasses import replace

from expression import Zero
from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement, TodaSuspensionMap
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase169_r10e2_unpositioned_citation.source_first import (
    screen_independent_sources_for_derived_goal,
)
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase175_r4r14r4_general_zero_transport.rule import (
    RULE_NAME, composite_value_zero_inputs,
)
from phase175_r4r14r5_public_zero_transport.provider import (
    build_public_composite_zero_transport_provider,
)


def _inputs():
    root = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(10, 6))
    screened = screen_independent_sources_for_derived_goal(
        build_shared_typed_bridge(), goal=root,
    )
    previous = exact_prior_database_result(5, 4)
    assert previous is not None
    mapping = TodaSuspensionMap(
        TodaPrimaryGroup(9, 5), TodaPrimaryGroup(10, 6),
    )
    goal = GeneratorImage(mapping, previous.rhs.generator, Zero())
    return root, screened, goal


def test_source_screened_binary_composition_generates_two_real_goals():
    _, screened, goal = _inputs()
    options = build_public_composite_zero_transport_provider(screened)(goal)
    assert len(options) == 1
    assert options[0].rule.name == RULE_NAME
    parents = options[0].subgoals
    assert composite_value_zero_inputs(goal, parents[0]) == parents
    assert parents[0].source_generator == goal.source_generator
    assert parents[0].map == goal.map
    assert parents[1].rhs == Zero()
    assert options[0].rule.literature_reference is None


def test_shared_provider_offers_same_generic_rule():
    root, screened, goal = _inputs()
    options = shared_expansion_provider(screened, proof_target=root)(goal)
    matching = tuple(candidate for candidate in options if candidate.rule.name == RULE_NAME)
    assert len(matching) == 1
    assert matching[0].subgoals == build_public_composite_zero_transport_provider(screened)(goal)[0].subgoals


def test_no_cited_source_no_zero_proposal():
    _, screened, goal = _inputs()
    from phase163_r4_registry_bridge import RegistryBridgeResult
    from unified_statement_registry import UnifiedStatementRegistry
    empty = RegistryBridgeResult(registry=UnifiedStatementRegistry(), records=(), proof_links=())
    assert build_public_composite_zero_transport_provider(empty)(goal) == ()
    assert build_public_composite_zero_transport_provider(screened)(
        replace(goal, target_generator=goal.source_generator)
    ) == ()


def test_unproved_parents_cannot_close_any_step():
    _, screened, goal = _inputs()
    option = build_public_composite_zero_transport_provider(screened)(goal)[0]
    from proof import find_inference_matches_for_rule
    assert find_inference_matches_for_rule(option.rule, ()) == ()

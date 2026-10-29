"""Integration contracts for the printed Proposition 5.8 source adoption."""
from dataclasses import replace
from hashlib import sha256

import pytest

from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase163_r4_registry_bridge import MigrationStatus, RegistryBridgeResult
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import registered_group_goal_candidates
from phase169_r10e2_unpositioned_citation.source_first import (
    screen_independent_sources_for_derived_goal,
)
from phase165_r52_r27_r5_literature import Toda52UniversalStatement
from phase168_r2_toda52_transport import expand_toda52_finite_cyclic_goal
from phase170_r3_r6_prop58_source import (
    COMPONENT_ID,
    SOURCE_CLAUSE,
    SOURCE_DIGEST,
    SOURCE_ID,
    _source_checked_pi73_relation,
    register_source_checked_prop58_pi73,
)
from unified_statement_registry import AssertionOrigin, UnifiedStatementRegistry


def test_prop58_pi73_is_unique_registered_typed_source():
    bridge = build_shared_typed_bridge()
    assertion_id = "shared:0:" + COMPONENT_ID
    assertion = bridge.registry.assertion(assertion_id)
    assert assertion.origin is AssertionOrigin.FIXED_STATEMENT
    assert assertion.content.lhs == TodaPrimaryGroup(7, 3)
    assert isinstance(assertion.content.rhs, FiniteCyclicGroup)
    assert assertion.content.rhs.order == 2
    record = tuple(item for item in bridge.records if item.assertion_id == assertion_id)
    assert len(record) == 1
    assert record[0].status is MigrationStatus.STRUCTURED


def test_prop58_other_components_remain_metadata_only():
    bridge = build_shared_typed_bridge()
    for key in ("pi6_2_group_relation", "pi8_4_group_relation", "pi9_5_group_relation"):
        claim = bridge.registry.assertion("shared:0:boundary:Proposition 5.8:" + key)
        assert type(claim.content).__name__ == "TodaFixedStatementComponent"


def test_pi72_general_toda52_proposes_exact_screened_pi73_source():
    bridge = build_shared_typed_bridge()
    goals = registered_group_goal_candidates(bridge, n=2, k=5)
    assert len(goals) == 1
    goal = goals[0]
    screened = screen_independent_sources_for_derived_goal(bridge, goal=goal)
    available = tuple(link.step.conclusion for link in screened.proof_links if link.step is not None)
    source = bridge.registry.assertion("shared:0:" + COMPONENT_ID).content
    assert source in available
    assert Toda52UniversalStatement() in available
    proposals = expand_toda52_finite_cyclic_goal(goal, available)
    assert len(proposals) == 1
    assert proposals[0].subgoals == (source, Toda52UniversalStatement())


def test_mismatching_printed_source_is_rejected():
    from phase165_r9_production_wiring import discover_goal_search_inputs
    base = discover_goal_search_inputs().bridge
    archive = tuple(a for a in base.registry._assertions.values()
                    if a.origin is AssertionOrigin.SOURCE_ARCHIVE
                    and isinstance(a.content, dict)
                    and a.content.get("source_statement_id") == SOURCE_ID)
    assert len(archive) == 1
    original = archive[0]
    changed = dict(original.content)
    changed["source_text"] = str(changed["source_text"]).replace(SOURCE_CLAUSE, "MALFORMED")
    changed["source_sha256"] = sha256(changed["source_text"].encode("utf-8")).hexdigest()
    registry = UnifiedStatementRegistry()
    for reference in base.registry._references.values():
        registry.add_reference(reference)
    for assertion in base.registry._assertions.values():
        registry.add_assertion(replace(assertion, content=changed) if assertion.assertion_id == original.assertion_id else assertion)
    altered = RegistryBridgeResult(registry, base.records, base.proof_links)
    with pytest.raises(ValueError, match="source not verified"):
        register_source_checked_prop58_pi73(altered)

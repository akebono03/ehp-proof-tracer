from dataclasses import replace

import pytest

from phase165_r4_production_connection import (
    describe_production_blockers,
    discover_production_registry,
    execute_production_goal,
)
from phase165_r3_recursive_search import RegisteredGoalUnresolved


def test_live_registry_has_no_automatic_approval():
    discovery = discover_production_registry()
    assert discovery.verified_fixed_ids == ()
    assert discovery.fixed_assertion_count >= 0
    assert discovery.ordered_fixed_count <= discovery.fixed_assertion_count


def test_no_global_catalog_is_reported():
    discovery = discover_production_registry()
    blockers = describe_production_blockers(discovery)
    assert "NO_GLOBAL_RULE_EXPANSION_PROVIDER_CONNECTED" in blockers
    assert "NO_INDEPENDENTLY_VERIFIED_ASSERTION_IDS" in blockers


def test_unregistered_review_id_rejected():
    discovery = discover_production_registry()
    with pytest.raises(ValueError, match="reviewed assertion missing"):
        execute_production_goal(
            "unknown", "unknown", lambda goal: (),
            discovery=discovery, verified_assertion_ids=("nonexistent-phase165-id",),
        )


def test_search_does_not_invent_citing_statement():
    discovery = discover_production_registry()
    with pytest.raises(KeyError):
        execute_production_goal("not-proved", "missing-target", lambda goal: (), discovery=discovery)

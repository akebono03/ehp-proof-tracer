"""Focused typed-source and no-fabricated-specialization checks."""
from dataclasses import replace

import pytest

from phase165_r52_r27_r5_literature import (
    Toda52UniversalStatement, TodaProp44UniversalStatement,
    build_typed_literature_bridge,
)
from phase165_r9_production_wiring import discover_goal_search_inputs
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from proof import ProofRule
from phase165_r3_recursive_search import _typed_reference_steps
from unified_statement_registry import AssertionOrigin


def test_r5_two_general_literature_claims_linked_as_exact_references():
    production = discover_goal_search_inputs().bridge
    bridge = build_typed_literature_bridge(production)
    assert len(bridge.proof_links) == 2
    assert {type(a.content) for a in bridge.registry._assertions.values()} == {
        TodaProp44UniversalStatement, Toda52UniversalStatement,
    }
    for assertion in bridge.registry._assertions.values():
        assert assertion.origin is AssertionOrigin.FIXED_STATEMENT
        steps = _typed_reference_steps(bridge, assertion.content)
        assert len(steps) == 1
        assert steps[0].rule is ProofRule.GIVEN
        assert steps[0].conclusion == assertion.content


def test_r5_shared_bridge_contains_two_typed_literature_claims():
    bridge = build_shared_typed_bridge()
    for statement in (TodaProp44UniversalStatement(), Toda52UniversalStatement()):
        assert len(_typed_reference_steps(bridge, statement)) == 1


def test_r5_no_unchecked_source_promotion():
    production = discover_goal_search_inputs().bridge
    old = build_typed_literature_bridge(production)
    assert len(old.proof_links) == 2
    assert Toda52UniversalStatement().minimum_i == 3
    assert TodaProp44UniversalStatement().includes_suspension_injectivity
    assert all(link.step.rule is ProofRule.GIVEN for link in old.proof_links)


def test_r5_missing_source_rejected():
    from phase163_r4_registry_bridge import RegistryBridgeResult
    from unified_statement_registry import UnifiedStatementRegistry
    empty = RegistryBridgeResult(UnifiedStatementRegistry(), (), ())
    with pytest.raises(ValueError, match="unique source archive"):
        build_typed_literature_bridge(empty)

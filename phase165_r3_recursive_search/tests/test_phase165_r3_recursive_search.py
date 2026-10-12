"""Focused generic search tests; synthetic positions do not certify Toda."""
import pytest

from phase163_r4_registry_bridge import MigrationRecord, MigrationStatus, RegistryBridgeResult
from phase165_r3_recursive_search import (
    GoalExpansion,
    RegisteredGoalUnresolved,
    reconstruct_registered_goal,
)
from unified_statement_registry import (
    AssertionEntry,
    AssertionKind,
    LiteratureEntry,
    ReferenceKind,
    UnifiedStatementRegistry,
)


def _catalog():
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry(
        "src", ReferenceKind.PROPOSITION, "Proposition source",
        source_id="synthetic", publication_position=1,
    ))
    registry.add_reference(LiteratureEntry(
        "dst", ReferenceKind.PROPOSITION, "Proposition target",
        source_id="synthetic", publication_position=2,
    ))
    registry.add_assertion(AssertionEntry(
        "source", "src", AssertionKind.STATEMENT, "premise",
        available_after_position=1,
    ))
    registry.add_assertion(AssertionEntry(
        "target", "dst", AssertionKind.STATEMENT, "goal",
    ))
    bridge = RegistryBridgeResult(
        registry,
        (MigrationRecord("fixture", "source", "source", MigrationStatus.STRUCTURED, "fixture"),),
        (),
    )
    return bridge


def test_unproved_registered_assertion_is_not_a_proof_step():
    with pytest.raises(RegisteredGoalUnresolved, match="found 0"):
        reconstruct_registered_goal(
            "premise", _catalog(), "target", lambda goal: (),
            verified_assertion_ids=("source",),
        )


def test_unverified_assertion_is_not_a_proof_step():
    with pytest.raises(RegisteredGoalUnresolved, match="found 0"):
        reconstruct_registered_goal("premise", _catalog(), "target", lambda goal: ())


def test_cycle_is_rejected():
    bridge = _catalog()
    with pytest.raises(RegisteredGoalUnresolved):
        reconstruct_registered_goal(
            "goal", bridge, "target",
            lambda goal: (GoalExpansion(object(), ("goal",)),),
        )


def test_expansion_provider_must_be_callable():
    with pytest.raises(TypeError, match="callable"):
        reconstruct_registered_goal("goal", _catalog(), "target", None)


def test_expansion_provider_requires_tuple():
    with pytest.raises(TypeError, match="tuple"):
        reconstruct_registered_goal("goal", _catalog(), "target", lambda goal: [])

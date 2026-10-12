"""Focused R2 tests: order and verification gates, without actual Toda certification."""
import pytest

from phase163_r4_registry_bridge import (
    MigrationRecord,
    MigrationStatus,
    RegistryBridgeResult,
)
from phase165_r2_registry_lookup import (
    find_eligible_goal_candidates,
    require_unique_registered_proof_step,
)
from unified_statement_registry import (
    AssertionEntry,
    AssertionKind,
    AssertionOrigin,
    LiteratureEntry,
    ReferenceKind,
    UnifiedStatementRegistry,
)


def _bridge(*, available=1, origin=AssertionOrigin.FIXED_STATEMENT):
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry(
        "ref:source", ReferenceKind.PROPOSITION, "Source",
        publication_position=1,
    ))
    registry.add_reference(LiteratureEntry(
        "ref:goal", ReferenceKind.PROPOSITION, "Goal",
        publication_position=2,
    ))
    registry.add_assertion(AssertionEntry(
        "source", "ref:source", AssertionKind.STATEMENT, "claim",
        origin=origin, available_after_position=available,
    ))
    registry.add_assertion(AssertionEntry(
        "goal", "ref:goal", AssertionKind.STATEMENT, "target",
    ))
    return RegistryBridgeResult(
        registry,
        (MigrationRecord("fixture", "source", "source", MigrationStatus.STRUCTURED, "fixture"),),
        (),
    )


def test_eligible_goal_is_found_by_content():
    result = find_eligible_goal_candidates(
        _bridge(), "claim", "goal", verified_assertion_ids=("source",),
    )
    assert len(result) == 1
    assert result[0].assertion.assertion_id == "source"
    assert result[0].proof_step is None


def test_unknown_or_later_statement_is_excluded():
    assert find_eligible_goal_candidates(_bridge(), "claim", "goal") == ()
    assert find_eligible_goal_candidates(
        _bridge(available=2), "claim", "goal",
        verified_assertion_ids=("source",),
    ) == ()
    assert find_eligible_goal_candidates(
        _bridge(available=None), "claim", "goal",
        verified_assertion_ids=("source",),
    ) == ()


def test_archive_is_not_promoted():
    result = find_eligible_goal_candidates(
        _bridge(origin=AssertionOrigin.SOURCE_ARCHIVE), "claim", "goal",
        verified_assertion_ids=("source",),
    )
    assert result == ()


def test_eligible_metadata_cannot_become_fabricated_proof():
    with pytest.raises(ValueError, match="no unique verified ProofStep"):
        require_unique_registered_proof_step(
            _bridge(), "claim", "goal", verified_assertion_ids=("source",),
        )

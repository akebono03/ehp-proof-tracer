"""R10 focused end-to-end behavior; fixtures never certify Toda literature."""
from dataclasses import dataclass

from phase163_r4_registry_bridge import MigrationRecord, MigrationStatus, RegistryBridgeResult
from phase165_r10_goal_diagnostics import diagnose_registered_goal
from phase165_r3_recursive_search import GoalExpansion
from proof import ProofRule, ProofStep
from unified_statement_registry import (
    AssertionEntry, AssertionKind, AssertionOrigin,
    LiteratureEntry, ProofStepLink, ReferenceKind, UnifiedStatementRegistry,
)


@dataclass(frozen=True)
class Claim:
    value: str


def _bridge(link=True):
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry("early", ReferenceKind.PROPOSITION, "Early", source_id="fixture", publication_position=1))
    registry.add_reference(LiteratureEntry("late", ReferenceKind.PROPOSITION, "Late", source_id="fixture", publication_position=2))
    registry.add_assertion(AssertionEntry("given", "early", AssertionKind.STATEMENT, Claim("base"), origin=AssertionOrigin.FIXED_STATEMENT, available_after_position=1))
    registry.add_assertion(AssertionEntry("context", "late", AssertionKind.STATEMENT, Claim("result")))
    proof_links = (ProofStepLink("given", step=ProofStep(Claim("base"), (), ProofRule.GIVEN)),) if link else ()
    record = MigrationRecord("fixture", "given", "given", MigrationStatus.STRUCTURED, "fixture reviewed")
    return RegistryBridgeResult(registry, (record,), proof_links)


def test_reviewed_linked_leaf_is_proved():
    result = diagnose_registered_goal(Claim("base"), _bridge(), "context", lambda goal: (), verified_assertion_ids=("given",))
    assert result.status == "PROVED"
    assert result.proof_step is not None


def test_reviewed_but_unlinked_leaf_is_unresolved():
    result = diagnose_registered_goal(Claim("base"), _bridge(link=False), "context", lambda goal: (), verified_assertion_ids=("given",))
    assert result.status == "UNRESOLVED"
    assert any("UNVERIFIED_OR_UNLINKED_REGISTERED_GOAL" in reason for reason in result.unresolved)


def test_unreviewed_link_remains_unresolved():
    result = diagnose_registered_goal(Claim("base"), _bridge(), "context", lambda goal: ())
    assert result.status == "UNRESOLVED"


def test_missing_goal_reports_concrete_frontier():
    result = diagnose_registered_goal(Claim("unknown"), _bridge(), "context", lambda goal: ())
    assert result.status == "UNRESOLVED"
    assert any("NO_REGISTERED_GOAL_OR_INVERTIBLE_RULE" in reason for reason in result.unresolved)


def test_cycle_is_reported_without_new_premises():
    from proof import InferenceRule
    rule = InferenceRule("cycle")
    def expand(goal):
        return (GoalExpansion(rule, (goal,)),)
    result = diagnose_registered_goal(Claim("unknown"), _bridge(), "context", expand)
    assert result.status == "UNRESOLVED"
    assert any("CYCLIC_OR_REVISITED_GOAL" in reason for reason in result.unresolved)

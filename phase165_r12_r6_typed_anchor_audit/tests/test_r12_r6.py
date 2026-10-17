"""R12-R6 focused audit contracts. No fabricated production witnesses."""
from dataclasses import dataclass

from expression import eta
from homotopy_groups import TodaPrimaryGroup
from phase165_r10_rule_registry import build_rule_registry
from phase165_r12_r2_quotient_rules import CyclicStructureStatement, QuotientIsomorphismStatement
from phase165_r12_r6_typed_anchor_audit.audit import RULE_ID, binding_report, fixed_typed_steps
from phase165_r8_rule_provider import DEFAULT_RULE_MODULES
from proof import ProofRule, ProofStep
from unified_statement_registry import (
    AssertionEntry, AssertionKind, AssertionOrigin, LiteratureEntry,
    ProofStepLink, ReferenceKind, UnifiedStatementRegistry,
)
from phase163_r4_registry_bridge import RegistryBridgeResult


def _rule_and_goal():
    registry = build_rule_registry(DEFAULT_RULE_MODULES)
    return registry.by_id(RULE_ID).rule, CyclicStructureStatement(TodaPrimaryGroup(4, 3), eta(3), 2)


def test_r2_registered_and_unbound_when_no_sources():
    rule, goal = _rule_and_goal()
    report = binding_report(rule, goal, ())
    assert report["goal_unbound_variables"] == ["domain", "map", "source_generator"]
    assert report["source_seeded_proposals"] == 0


def test_typed_seed_never_converts_to_completed_proof():
    rule, goal = _rule_and_goal()
    # Synthetic test-only GIVEN; never inserted into the production registry.
    fake_premise = QuotientIsomorphismStatement(
        "test-map", "test-domain", goal.group, "test-generator", goal.generator, goal.order
    )
    seed = ProofStep(fake_premise, (), ProofRule.GIVEN)
    report = binding_report(rule, goal, (seed,))
    assert report["source_seeded_proposals"] == 1
    assert len(report["source_seeded_subgoals"][0]) == 2


def test_fixed_witness_filter_rejects_unlinked_and_internal_steps():
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry("fixture", ReferenceKind.PROPOSITION, "fixture"))
    registry.add_assertion(AssertionEntry(
        "fixed", "fixture", AssertionKind.STATEMENT, "fixed conclusion", origin=AssertionOrigin.FIXED_STATEMENT
    ))
    registry.add_assertion(AssertionEntry(
        "internal", "fixture", AssertionKind.STATEMENT, "internal conclusion", origin=AssertionOrigin.PROOF_INTERNAL
    ))
    bridge = RegistryBridgeResult(registry, (), (
        ProofStepLink("fixed", step=ProofStep("fixed conclusion", (), ProofRule.GIVEN)),
        ProofStepLink("internal", step=ProofStep("internal conclusion", (), ProofRule.GIVEN)),
    ))
    result = fixed_typed_steps(bridge)
    assert len(result) == 1
    assert result[0].conclusion == "fixed conclusion"


def test_fixed_witness_filter_rejects_mismatched_claim():
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry("fixture", ReferenceKind.PROPOSITION, "fixture"))
    registry.add_assertion(AssertionEntry("fixed", "fixture", AssertionKind.STATEMENT, "expected"))
    bridge = RegistryBridgeResult(registry, (), (
        ProofStepLink("fixed", step=ProofStep("different", (), ProofRule.GIVEN)),
    ))
    assert fixed_typed_steps(bridge) == ()

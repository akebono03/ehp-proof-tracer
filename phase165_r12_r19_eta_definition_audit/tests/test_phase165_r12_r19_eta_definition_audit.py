"""Minimal R12-R19 regression checks; no new definition GIVEN."""
from __future__ import annotations

from dataclasses import dataclass

from phase165_r12_r19_eta_definition_audit import inspect_fixed_definition_links
from proof import ProofRule, ProofStep
from unified_statement_registry import (
    AssertionEntry, AssertionKind, AssertionOrigin, LiteratureEntry,
    ProofStepLink, ReferenceKind, UnifiedStatementRegistry,
)
from phase163_r4_registry_bridge import RegistryBridgeResult


@dataclass(frozen=True)
class Definition:
    n: int


def _bridge(origin: AssertionOrigin, rule: ProofRule) -> RegistryBridgeResult:
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry("eta-ref", ReferenceKind.EQUATION, "eta family definition"))
    item = Definition(3)
    registry.add_assertion(AssertionEntry(
        "eta-assertion", "eta-ref", AssertionKind.STATEMENT, item, origin=origin,
    ))
    step = ProofStep(conclusion=item, premises=(), rule=rule)
    return RegistryBridgeResult(registry, (), (ProofStepLink("eta-assertion", step=step),))


def test_r19_accepts_only_cited_fixed_definition():
    result = inspect_fixed_definition_links(_bridge(AssertionOrigin.FIXED_STATEMENT, ProofRule.GIVEN), Definition)
    assert result.matching_count == 1
    assert result.assertion_ids == ("eta-assertion",)


def test_r19_does_not_promote_internal_definition():
    result = inspect_fixed_definition_links(_bridge(AssertionOrigin.PROOF_INTERNAL, ProofRule.GIVEN), Definition)
    assert result.matching_count == 0


def test_r19_does_not_promote_inference_to_reference():
    result = inspect_fixed_definition_links(_bridge(AssertionOrigin.FIXED_STATEMENT, ProofRule.INFERENCE), Definition)
    assert result.matching_count == 0

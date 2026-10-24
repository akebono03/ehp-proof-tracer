"""Focused tests for a read-only finite cyclic blocker audit."""
from __future__ import annotations

from dataclasses import dataclass
from types import SimpleNamespace

from phase168_r3_41h_finite_cyclic_blocker_audit.audit import (
    classify_blocker, inspect_cyclic_goal, unique_by_typed_value,
)


def test_unique_by_typed_value_preserves_first_identity():
    first = SimpleNamespace(value=2)
    duplicate = SimpleNamespace(value=2)
    another = SimpleNamespace(value=4)
    selected = unique_by_typed_value([first, duplicate, another])
    assert len(selected) == 2
    assert selected[0] is first
    assert selected[1] is another


def test_classify_blocked_finite_cyclic_premise_without_inventing_steps():
    assert classify_blocker(
        status="search_failed", proved=0, finite_blocked=1, root_options=3,
    ) == "FINITE_CYCLIC_PREMISE_NO_EXPANSION"
    assert classify_blocker(
        status="partial", proved=1, finite_blocked=1, root_options=3,
    ) == "FINITE_CYCLIC_PREMISE_BLOCKED_WITH_OTHER_PROGRESS"


def test_classify_no_root_expansion_and_complete_controls():
    assert classify_blocker(
        status="search_failed", proved=0, finite_blocked=0, root_options=0,
    ) == "ROOT_NO_EXPANSION_OR_NOT_REACHED"
    assert classify_blocker(
        status="complete", proved=3, finite_blocked=0, root_options=2,
    ) == "COMPLETE"


def test_exact_screened_links_do_not_count_unrelated_given():
    from phase165_r12_r2_quotient_rules import CyclicStructureStatement
    from phase163_r4_registry_bridge import RegistryBridgeResult
    from proof import ProofRule, ProofStep
    from unified_statement_registry import (
        AssertionEntry, AssertionKind, AssertionOrigin,
        LiteratureEntry, ReferenceKind, ProofStepLink, UnifiedStatementRegistry,
    )

    goal = CyclicStructureStatement("G", "g", 2)
    other = CyclicStructureStatement("G", "g", 4)
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry("r", ReferenceKind.PROPOSITION, "P"))
    registry.add_assertion(AssertionEntry(
        "a", "r", AssertionKind.STATEMENT, goal,
        origin=AssertionOrigin.FIXED_STATEMENT,
    ))
    registry.add_assertion(AssertionEntry(
        "b", "r", AssertionKind.STATEMENT, other,
        origin=AssertionOrigin.FIXED_STATEMENT,
    ))
    link = ProofStepLink("b", step=ProofStep(other, (), ProofRule.GIVEN))
    context = RegistryBridgeResult(registry, (), (link,))
    findings = inspect_cyclic_goal(
        goal, screened=context, registry=registry, all_links=(link,),
    )
    assert findings["order"] == 2
    assert findings["screened_exact_given_assertion_ids"] == []
    assert [x["assertion_id"] for x in findings["registered_fixed_exact_assertions"]] == ["a"]


def test_audit_never_promotes_source_archive_to_fixed_proof():
    from phase165_r12_r2_quotient_rules import CyclicStructureStatement
    from phase163_r4_registry_bridge import RegistryBridgeResult
    from unified_statement_registry import (
        AssertionEntry, AssertionKind, AssertionOrigin,
        LiteratureEntry, ReferenceKind, UnifiedStatementRegistry,
    )
    goal = CyclicStructureStatement("G", "g", 2)
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry("r", ReferenceKind.PROPOSITION, "P"))
    registry.add_assertion(AssertionEntry(
        "archived", "r", AssertionKind.STATEMENT, goal,
        origin=AssertionOrigin.SOURCE_ARCHIVE,
    ))
    context = RegistryBridgeResult(registry, (), ())
    findings = inspect_cyclic_goal(
        goal, screened=context, registry=registry, all_links=(),
    )
    assert findings["registered_fixed_exact_assertions"] == []
    assert findings["screened_exact_given_assertion_ids"] == []

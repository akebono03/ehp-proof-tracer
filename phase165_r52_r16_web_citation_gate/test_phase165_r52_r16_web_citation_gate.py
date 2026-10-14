from dataclasses import replace

from phase163_r4_registry_bridge import MigrationRecord, MigrationStatus, RegistryBridgeResult
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from proof import ProofRule, ProofStep
from unified_statement_registry import (
    UnifiedStatementRegistry, LiteratureEntry, ReferenceKind,
    AssertionEntry, AssertionKind, ProofStepLink,
)


def _fixture(*, available=1, source_id="Toda", adopted=False):
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry(
        "cited_ref", ReferenceKind.PROPOSITION, "Prop A",
        source_id=source_id, publication_position=1,
    ))
    registry.add_reference(LiteratureEntry(
        "goal_ref", ReferenceKind.PROPOSITION, "Prop B",
        source_id="Toda", publication_position=2,
    ))
    assertion_id = (
        "shared:2:toda:adopted:prop5.1:finite_dimensional" if adopted else "cited"
    )
    registry.add_assertion(AssertionEntry(
        assertion_id, "cited_ref", AssertionKind.STATEMENT, "fact",
        available_after_position=available,
    ))
    registry.add_assertion(AssertionEntry(
        "goal", "goal_ref", AssertionKind.STATEMENT, "goal",
    ))
    step = ProofStep("fact", (), ProofRule.GIVEN)
    bridge = RegistryBridgeResult(
        registry,
        (MigrationRecord("test", "fact", assertion_id, MigrationStatus.STRUCTURED, "fixture"),),
        (ProofStepLink(assertion_id, step=step),),
    )
    return bridge, step


def test_r16_verified_earlier_reference_is_used():
    bridge, step = _fixture()
    result = screen_shared_proof_context(
        bridge, goal="other goal", citing_assertion_id="goal",
        verified_assertion_ids=("cited",),
    )
    assert tuple(x.step for x in result.proof_links) == (step,)


def test_r16_unreviewed_or_late_reference_is_not_used():
    for bridge, verified in (
        (_fixture()[0], ()),
        (_fixture(available=2)[0], ("cited",)),
        (_fixture(source_id="Another book")[0], ("cited",)),
    ):
        result = screen_shared_proof_context(
            bridge, goal="other goal", citing_assertion_id="goal",
            verified_assertion_ids=verified,
        )
        assert result.proof_links == ()


def test_r16_goal_self_citation_is_excluded_even_if_reviewed():
    bridge, _ = _fixture()
    result = screen_shared_proof_context(
        bridge, goal="fact", citing_assertion_id="goal",
        verified_assertion_ids=("cited",),
    )
    assert result.proof_links == ()
    assert bridge.proof_links


def test_r16_explicit_adopted_source_still_available_but_not_certified():
    bridge, step = _fixture(adopted=True, source_id="translated adopted Toda")
    result = screen_shared_proof_context(
        bridge, goal="other goal", citing_assertion_id="goal",
    )
    assert tuple(x.step for x in result.proof_links) == (step,)
    assert result.registry.assertion(bridge.proof_links[0].assertion_id).available_after_position == 1

"""Phase 166 R3-Q: definition is eligible iff its printed position is earlier."""
from dataclasses import dataclass

from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from proof import ProofRule
from unified_statement_registry import (
    AssertionEntry, AssertionKind, AssertionOrigin,
    LiteratureEntry, ReferenceKind, UnifiedStatementRegistry,
)


@dataclass(frozen=True)
class Fact:
    value: str


def _bridge(definition_position: int, target_position: int = 200) -> RegistryBridgeResult:
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry(
        "r3q:definition", ReferenceKind.DEFINITION, "test definition",
        publication_position=100,
    ))
    registry.add_reference(LiteratureEntry(
        "r3q:goal", ReferenceKind.PROPOSITION, "test proposition",
        publication_position=100,
    ))
    registry.add_assertion(AssertionEntry(
        "r3q:definition", "r3q:definition", AssertionKind.DEFINITION,
        Fact("definition"), origin=AssertionOrigin.FIXED_STATEMENT,
        defined_symbol="test_symbol", component_position=definition_position,
    ))
    registry.add_assertion(AssertionEntry(
        "r3q:goal", "r3q:goal", AssertionKind.STATEMENT,
        Fact("goal"), origin=AssertionOrigin.FIXED_STATEMENT,
        component_position=target_position,
    ))
    return RegistryBridgeResult(registry, (), ())


def test_r3q_prior_definition_is_usable_without_manual_link():
    bridge = _bridge(100)
    result = screen_shared_proof_context(
        bridge, goal=Fact("goal"), citing_assertion_id="r3q:goal",
        explicit_publication_target=True,
    )
    assert len(result.proof_links) == 1
    assert result.proof_links[0].assertion_id == "r3q:definition"
    assert result.proof_links[0].step.rule is ProofRule.GIVEN
    assert result.proof_links[0].step.conclusion == Fact("definition")


def test_r3q_later_definition_is_not_usable():
    result = screen_shared_proof_context(
        _bridge(300), goal=Fact("goal"), citing_assertion_id="r3q:goal",
        explicit_publication_target=True,
    )
    assert result.proof_links == ()


def test_r3q_equal_position_definition_is_not_usable():
    result = screen_shared_proof_context(
        _bridge(200), goal=Fact("goal"), citing_assertion_id="r3q:goal",
        explicit_publication_target=True,
    )
    assert result.proof_links == ()


def test_r3q_legacy_implicit_mode_is_unchanged():
    result = screen_shared_proof_context(
        _bridge(100), goal=Fact("goal"), citing_assertion_id="r3q:goal",
        explicit_publication_target=False,
    )
    assert result.proof_links == ()

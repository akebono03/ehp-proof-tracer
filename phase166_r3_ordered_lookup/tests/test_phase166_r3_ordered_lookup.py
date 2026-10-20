"""Phase 166 R3: explicit order only; no production Web cutover."""
import pytest

from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r3_recursive_search import (
    RegisteredGoalUnresolved,
    reconstruct_registered_goal,
)
from phase165_r52_r15_ordered_citation import ordered_typed_reference_steps
from proof import ProofRule, ProofStep
from unified_statement_registry import (
    AssertionEntry,
    AssertionKind,
    LiteratureEntry,
    ProofStepLink,
    ReferenceKind,
    UnifiedStatementRegistry,
)


def _fixture(*, available=1, citing_position=2, source_id="Toda", linked=True):
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry(
        "source", ReferenceKind.EQUATION, "(5.1)",
        source_id="Toda", publication_position=1,
    ))
    registry.add_reference(LiteratureEntry(
        "target", ReferenceKind.PROPOSITION, "Proposition 5.1",
        source_id=source_id, publication_position=citing_position,
    ))
    registry.add_assertion(AssertionEntry(
        "premise", "source", AssertionKind.STATEMENT, "pi21=0",
        available_after_position=available,
    ))
    registry.add_assertion(AssertionEntry(
        "goal", "target", AssertionKind.STATEMENT, "pi32",
    ))
    step = ProofStep("pi21=0", (), ProofRule.GIVEN)
    links = (ProofStepLink("premise", step=step),) if linked else ()
    return RegistryBridgeResult(registry, (), links), step


def test_earlier_reference_available_without_independent_review():
    bridge, step = _fixture()
    assert ordered_typed_reference_steps(bridge, "pi21=0", "goal") == (step,)
    assert ordered_typed_reference_steps(
        bridge, "pi21=0", "goal", verified_assertion_ids=("unrelated",)
    ) == (step,)


def test_later_same_and_missing_positions_do_not_qualify():
    for position in (2, 3, None):
        bridge, _ = _fixture(available=position)
        assert ordered_typed_reference_steps(bridge, "pi21=0", "goal") == ()


def test_different_source_order_is_unknown():
    bridge, _ = _fixture(source_id="Other")
    assert ordered_typed_reference_steps(bridge, "pi21=0", "goal") == ()


def test_link_required_to_construct_proof_leaf():
    bridge, _ = _fixture(linked=False)
    assert ordered_typed_reference_steps(bridge, "pi21=0", "goal") == ()


def test_ordered_branch_integrates_with_common_search():
    bridge, step = _fixture()
    result = reconstruct_registered_goal(
        "pi21=0", bridge, "goal", lambda _: (),
        lookup_mode="typed_reference_ordered",
    )
    assert result is step
    later, _ = _fixture(available=2)
    with pytest.raises(RegisteredGoalUnresolved):
        reconstruct_registered_goal(
            "pi21=0", later, "goal", lambda _: (),
            lookup_mode="typed_reference_ordered",
        )

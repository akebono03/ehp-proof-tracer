"""R3-C: actual manifest ranks and shared lookup, no whole-suite testing."""
from dataclasses import replace

import pytest

from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r3_recursive_search import RegisteredGoalUnresolved, reconstruct_registered_goal
from proof import ProofRule, ProofStep
from unified_statement_registry import (
    AssertionEntry, AssertionKind, LiteratureEntry, ProofStepLink,
    ReferenceKind, UnifiedStatementRegistry,
)


def _case(source_id='toda:(5.1)', target_id='toda:Proposition 5.1', *, linked=True):
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry(source_id, ReferenceKind.EQUATION, '(5.1)', source_id='Toda'))
    registry.add_reference(LiteratureEntry(target_id, ReferenceKind.PROPOSITION, 'Proposition 5.1', source_id='Toda'))
    registry.add_assertion(AssertionEntry('premise', source_id, AssertionKind.STATEMENT, 'X'))
    registry.add_assertion(AssertionEntry('target', target_id, AssertionKind.STATEMENT, 'Y'))
    step = ProofStep('X', (), ProofRule.GIVEN)
    links = (ProofStepLink('premise', step=step),) if linked else ()
    return RegistryBridgeResult(registry, (), links), step


@pytest.mark.parametrize('mode', ['legacy', 'typed_reference', 'typed_reference_ordered'])
def test_all_lookup_modes_use_existing_manifest_order(mode):
    bridge, step = _case()
    assert reconstruct_registered_goal('X', bridge, 'target', lambda _: (), lookup_mode=mode) is step
    assert bridge.registry.reference('toda:(5.1)').publication_position is None


@pytest.mark.parametrize('mode', ['legacy', 'typed_reference', 'typed_reference_ordered'])
def test_later_reference_never_becomes_a_premise(mode):
    bridge, _ = _case('toda:Proposition 5.1', 'toda:(5.1)')
    with pytest.raises(RegisteredGoalUnresolved):
        reconstruct_registered_goal('X', bridge, 'target', lambda _: (), lookup_mode=mode)


def test_unlinked_typed_statement_not_promoted_to_given():
    bridge, _ = _case(linked=False)
    with pytest.raises(RegisteredGoalUnresolved):
        reconstruct_registered_goal('X', bridge, 'target', lambda _: (), lookup_mode='typed_reference')


def test_unknown_reference_order_is_not_guessed():
    bridge, _ = _case('unmapped:(5.1)', 'toda:Proposition 5.1')
    with pytest.raises(RegisteredGoalUnresolved):
        reconstruct_registered_goal('X', bridge, 'target', lambda _: (), lookup_mode='typed_reference')


def test_existing_assertion_metadata_not_changed():
    bridge, _ = _case()
    before = bridge.registry.assertion('premise')
    assert before.dependencies == ()
    reconstruct_registered_goal('X', bridge, 'target', lambda _: (), lookup_mode='typed_reference')
    assert bridge.registry.assertion('premise') is before

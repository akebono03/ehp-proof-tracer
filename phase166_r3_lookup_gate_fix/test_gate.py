import pytest

from phase163_r4_registry_bridge import MigrationRecord, MigrationStatus, RegistryBridgeResult
from phase165_r3_recursive_search import RegisteredGoalUnresolved, reconstruct_registered_goal
from proof import ProofRule, ProofStep
from unified_statement_registry import AssertionEntry, AssertionKind, LiteratureEntry, ProofStepLink, ReferenceKind, UnifiedStatementRegistry


def make_bridge(status=MigrationStatus.STRUCTURED, order=1):
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry('source_ref', ReferenceKind.EQUATION, '(5.3)', source_id='Toda', publication_position=1))
    registry.add_reference(LiteratureEntry('goal_ref', ReferenceKind.PROPOSITION, 'Goal', source_id='Toda', publication_position=2))
    registry.add_assertion(AssertionEntry('source', 'source_ref', AssertionKind.STATEMENT, 'typed fact', available_after_position=order))
    registry.add_assertion(AssertionEntry('goal', 'goal_ref', AssertionKind.STATEMENT, 'target'))
    step = ProofStep(conclusion='typed fact', premises=(), rule=ProofRule.GIVEN)
    return RegistryBridgeResult(registry, (MigrationRecord('fixture', 'source', 'source', status, 'fixture'),), (ProofStepLink('source', step=step),)), step


def search(bridge, mode, verified=()):
    return reconstruct_registered_goal('typed fact', bridge, 'goal', lambda goal: (), lookup_mode=mode, verified_assertion_ids=verified)


@pytest.mark.parametrize('mode', ['legacy', 'typed_reference', 'typed_reference_ordered'])
def test_unreviewed_link_denied_for_all_modes(mode):
    bridge, _ = make_bridge()
    with pytest.raises(RegisteredGoalUnresolved):
        search(bridge, mode)


@pytest.mark.parametrize('mode', ['legacy', 'typed_reference', 'typed_reference_ordered'])
def test_metadata_only_denied_even_when_id_supplied(mode):
    bridge, _ = make_bridge(status=MigrationStatus.METADATA_ONLY)
    with pytest.raises(RegisteredGoalUnresolved):
        search(bridge, mode, ('source',))


@pytest.mark.parametrize('mode', ['legacy', 'typed_reference', 'typed_reference_ordered'])
def test_reviewed_structured_prior_given_works(mode):
    bridge, step = make_bridge()
    assert search(bridge, mode, ('source',)) == step


@pytest.mark.parametrize('mode', ['legacy', 'typed_reference', 'typed_reference_ordered'])
def test_later_source_denied(mode):
    bridge, _ = make_bridge(order=2)
    with pytest.raises(RegisteredGoalUnresolved):
        search(bridge, mode, ('source',))

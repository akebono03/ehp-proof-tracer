from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r3_recursive_search import _typed_reference_steps, reconstruct_registered_goal, RegisteredGoalUnresolved
from proof import ProofRule, ProofStep
from unified_statement_registry import (
    AssertionEntry, AssertionKind, LiteratureEntry, ProofStepLink,
    ReferenceKind, UnifiedStatementRegistry,
)
import pytest


def fixture(*, available=1, cited_position=1, citing_position=2, same_reference=False, cited_component=1, citing_component=2):
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry('ref', ReferenceKind.PROPOSITION, 'A', source_id='Toda', publication_position=cited_position))
    if not same_reference:
        registry.add_reference(LiteratureEntry('goal', ReferenceKind.PROPOSITION, 'B', source_id='Toda', publication_position=citing_position))
    registry.add_assertion(AssertionEntry('prior', 'ref', AssertionKind.STATEMENT, 'fact', component_position=cited_component, available_after_position=available))
    registry.add_assertion(AssertionEntry('current', 'ref' if same_reference else 'goal', AssertionKind.STATEMENT, 'target', component_position=citing_component))
    step = ProofStep('fact', (), ProofRule.GIVEN)
    return RegistryBridgeResult(registry, (), (ProofStepLink('prior', step=step),)), step


@pytest.mark.parametrize('mode', ['legacy', 'typed_reference', 'typed_reference_ordered'])
def test_prior_reference_is_available_without_independent_verification(mode):
    bridge, step = fixture()
    assert reconstruct_registered_goal('fact', bridge, 'current', lambda _: (), lookup_mode=mode) is step


@pytest.mark.parametrize('mode', ['legacy', 'typed_reference', 'typed_reference_ordered'])
@pytest.mark.parametrize('available', [2, None])
def test_later_or_unknown_order_is_unavailable(mode, available):
    bridge, _ = fixture(available=available)
    with pytest.raises(RegisteredGoalUnresolved):
        reconstruct_registered_goal('fact', bridge, 'current', lambda _: (), lookup_mode=mode, verified_assertion_ids=('prior',))


def test_same_statement_components_follow_their_order():
    bridge, step = fixture(same_reference=True)
    assert _typed_reference_steps(bridge, 'fact', 'current') == (step,)
    reverse, _ = fixture(same_reference=True, cited_component=2, citing_component=1)
    assert _typed_reference_steps(reverse, 'fact', 'current') == ()


def test_link_is_required_but_review_status_is_not():
    bridge, _ = fixture()
    no_link = RegistryBridgeResult(bridge.registry, (), ())
    assert _typed_reference_steps(no_link, 'fact', 'current') == ()

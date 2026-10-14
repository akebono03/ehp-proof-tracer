"""Regression tests for legacy schema and explicit future composite metadata."""
from dataclasses import dataclass

from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r3_recursive_search import reconstruct_registered_goal
from phase165_r52_r12_component_bridge import expand_cited_given_components
from phase165_typed_component_lookup import index_typed_components
from proof import ProofRule, ProofStep
from unified_statement_registry import (
    AssertionEntry,
    AssertionKind,
    LiteratureEntry,
    ProofStepLink,
    ReferenceKind,
    UnifiedStatementRegistry,
)


@dataclass(frozen=True)
class LegacyFourPart:
    pi3_2_group_relation: str
    eta2_hopf_relation: str
    delta_iota5_relation: str
    higher_eta_group_relation: str


@dataclass(frozen=True)
class OtherComposite:
    first_claim: str
    second_claim: str


def _bridge(content: object, scope=None) -> RegistryBridgeResult:
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry(
        'compat:reference', ReferenceKind.PROPOSITION, 'Proposition Example',
    ))
    registry.add_assertion(AssertionEntry(
        'compat:parent', 'compat:reference', AssertionKind.STATEMENT,
        content, scope=scope,
    ))
    step = ProofStep(conclusion=content, premises=(), rule=ProofRule.GIVEN)
    return RegistryBridgeResult(
        registry, (), (ProofStepLink('compat:parent', step=step),),
    )


def test_r3_legacy_four_fields_are_split_without_class_name_dispatch():
    bridge = _bridge(LegacyFourPart('group', 'hopf', 'delta', 'higher'))
    indexed = index_typed_components(bridge.registry)
    assert {entry.component_name for entry in indexed} == {
        'pi3_2_group_relation', 'eta2_hopf_relation',
        'delta_iota5_relation', 'higher_eta_group_relation',
    }
    expanded = expand_cited_given_components(bridge)
    assert len(expanded.registry._assertions) == 5
    step = reconstruct_registered_goal(
        'delta', expanded, 'compat:parent', lambda goal: (),
        lookup_mode='typed_reference',
    )
    assert step.rule is ProofRule.GIVEN
    assert step.conclusion == 'delta'


def test_r3_explicitly_declared_new_composite_is_reusable():
    content = OtherComposite('x', 'y')
    bridge = _bridge(content, ('typed_composite_fields', ('first_claim', 'second_claim')))
    expanded = expand_cited_given_components(bridge)
    assert len(expanded.registry._assertions) == 3
    step = reconstruct_registered_goal(
        'y', expanded, 'compat:parent', lambda goal: (),
        lookup_mode='typed_reference',
    )
    assert step.rule is ProofRule.GIVEN
    assert step.conclusion == 'y'


def test_r3_undeclared_nonlegacy_dataclass_remains_atomic():
    bridge = _bridge(OtherComposite('x', 'y'))
    entries = index_typed_components(bridge.registry)
    assert len(entries) == 1
    assert entries[0].component_name == '__self__'
    assert len(expand_cited_given_components(bridge).registry._assertions) == 1

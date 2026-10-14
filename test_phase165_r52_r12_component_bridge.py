"""R52-R12 targeted tests for trusted component references."""
from dataclasses import dataclass

from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r52_r12_component_bridge import expand_cited_given_components
from phase165_r3_recursive_search import reconstruct_registered_goal
from proof import ProofRule, ProofStep
from unified_statement_registry import (
    AssertionEntry, AssertionKind, AssertionOrigin, LiteratureEntry,
    ProofStepLink, ReferenceKind, UnifiedStatementRegistry,
)


@dataclass(frozen=True)
class CompositeFact:
    pi3_2_group_relation: str
    eta2_hopf_relation: str
    delta_iota5_relation: str
    higher_eta_group_relation: str


def _source_bridge(rule=ProofRule.GIVEN, origin=AssertionOrigin.FIXED_STATEMENT):
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry(
        'r52r12:prop51', ReferenceKind.PROPOSITION, 'Proposition 5.1',
    ))
    statement = CompositeFact('group', 'hopf', 'delta', 'higher')
    registry.add_assertion(AssertionEntry(
        'r52r12:parent', 'r52r12:prop51', AssertionKind.STATEMENT,
        statement, origin=origin,
    ))
    step = ProofStep(conclusion=statement, premises=(), rule=rule)
    return RegistryBridgeResult(
        registry, (), (ProofStepLink('r52r12:parent', step=step),),
    )


def test_r12_cited_given_split_into_four_searchable_components():
    original = _source_bridge()
    result = expand_cited_given_components(original)
    assert len(original.registry._assertions) == 1
    assert len(result.registry._assertions) == 5
    assert len(result.proof_links) == 5
    assert all(link.step.rule is ProofRule.GIVEN for link in result.proof_links)
    assert {assertion.content for assertion in result.registry._assertions.values()
            if assertion.assertion_id != 'r52r12:parent'} == {'group', 'hopf', 'delta', 'higher'}


def test_r12_individual_component_resolves_as_common_typed_reference():
    result = expand_cited_given_components(_source_bridge())
    step = reconstruct_registered_goal(
        'delta', result, 'r52r12:parent', lambda goal: (),
        lookup_mode='typed_reference',
    )
    assert step.rule is ProofRule.GIVEN
    assert step.conclusion == 'delta'


def test_r12_never_promotes_legacy_inferred_composite():
    result = expand_cited_given_components(_source_bridge(rule=ProofRule.INFERENCE))
    assert len(result.registry._assertions) == 1
    assert len(result.proof_links) == 1


def test_r12_never_promotes_internal_or_missing_provenance():
    result = expand_cited_given_components(_source_bridge(origin=AssertionOrigin.PROOF_INTERNAL))
    assert len(result.registry._assertions) == 1
    original = _source_bridge()
    without_link = RegistryBridgeResult(original.registry, (), ())
    assert len(expand_cited_given_components(without_link).proof_links) == 0

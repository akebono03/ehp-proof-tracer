from dataclasses import replace

import pytest

from expression import Composition, Multiple, Zero
from homotopy_groups import TodaDeltaMap, TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase169_r10e2_unpositioned_citation.source_first import screen_independent_sources_for_derived_goal
from phase175_r4r7_prop25_typed_composition.rule import typed_endpoints
from phase178_r16_toda513_isolated.audit import classify_existing_513
from phase178_r16_toda513_isolated.source import build_cited_513_source, canonical_513
from proof import ProofRule, ProofStep
from toda_literature_statement_boundary import (
    TodaFixedStatementComponent, TodaLiteratureStatementRole,
)
from toda_rules import TodaDeltaImageUpToSignStatement
from unified_statement_registry import (
    AssertionEntry, AssertionKind, AssertionOrigin, LiteratureEntry, ProofStepLink,
    ReferenceKind, UnifiedStatementRegistry,
)


def test_exact_three_typed_source_leaves():
    bridge = build_cited_513_source()
    signed, z11, z13 = canonical_513()
    assert type(signed) is TodaDeltaImageUpToSignStatement
    assert signed.map == TodaDeltaMap(TodaPrimaryGroup(12,9),TodaPrimaryGroup(10,4))
    assert typed_endpoints(signed.element) == (12,9)
    assert type(signed.positive_value) is Multiple and signed.positive_value.coefficient == 2
    assert type(signed.positive_value.expression) is Composition
    assert typed_endpoints(signed.positive_value.expression) == (10,4)
    for item, src, dst in ((z11,(13,11),(11,5)),(z13,(14,13),(12,6))):
        assert type(item) is GeneratorImage
        assert item.map == TodaDeltaMap(TodaPrimaryGroup(*src),TodaPrimaryGroup(*dst))
        assert typed_endpoints(item.source_generator) == src
        assert type(item.target_generator) is Zero
    assert type(z11.source_generator) is Composition
    assert tuple(link.step.conclusion for link in bridge.proof_links) == (signed,z11,z13)
    assert len(bridge.registry._assertions) == 3
    for link in bridge.proof_links:
        a = bridge.registry.assertion(link.assertion_id)
        ref = bridge.registry.reference(a.reference_id)
        assert a.origin is AssertionOrigin.FIXED_STATEMENT and a.content == link.step.conclusion
        assert ref.publication_position == 10000 and ref.locator == '(5.13)'
        assert link.step.rule is ProofRule.GIVEN and not link.step.premises
        assert link.step.inference_rule.literature_reference.locator == '(5.13)'


@pytest.mark.parametrize('n',[5,6,7])
def test_derived_goal_screen_keeps_intermediate_images(n):
    bridge = build_cited_513_source()
    # A typed query marker, never registered as a group theorem.
    goal = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(n+6,n))
    screened = screen_independent_sources_for_derived_goal(bridge,goal=goal)
    assert tuple(x.step.conclusion for x in screened.proof_links) == canonical_513()


@pytest.mark.parametrize('position,expected',[(9900,0),(10100,3)])
def test_explicit_publication_screen(position,expected):
    bridge = build_cited_513_source()
    # Synthetic citation boundary only; not a published mathematical statement.
    bridge.registry.add_reference(LiteratureEntry('test:boundary',ReferenceKind.PROPOSITION,
        'test-only citation boundary',source_id='test',publication_position=position))
    bridge.registry.add_assertion(AssertionEntry('test:marker','test:boundary',AssertionKind.STATEMENT,
        'test-only marker',origin=AssertionOrigin.SOURCE_ARCHIVE))
    goal = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(11,5))
    screened = screen_shared_proof_context(bridge,goal=goal,citing_assertion_id='test:marker',
                                           explicit_publication_target=True)
    assert len(screened.proof_links) == expected



def metadata_fixture():
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry('boundary-ref', ReferenceKind.EQUATION,
        '(5.13)', source_id='test-only', publication_position=10000))
    for key in ('delta_nu9_relation', 'delta_eta11_squared_zero', 'delta_eta13_zero'):
        component = TodaFixedStatementComponent('(5.13)', key,
            TodaLiteratureStatementRole.MAP_VALUE, None, None, True)
        registry.add_assertion(AssertionEntry(key, 'boundary-ref', AssertionKind.STATEMENT,
            component, origin=AssertionOrigin.FIXED_STATEMENT))
    return RegistryBridgeResult(registry, (), ())


def test_reviewed_boundary_metadata_is_not_a_typed_duplicate():
    bridge = metadata_fixture()
    before = tuple(bridge.registry._assertions.values())
    metadata, conflicts = classify_existing_513(bridge, canonical_513())
    assert len(metadata) == 3 and not conflicts
    assert {r['component_key'] for r in metadata} == {a.assertion_id for a in before}
    assert tuple(bridge.registry._assertions.values()) == before
    assert not bridge.proof_links


@pytest.mark.parametrize('index', [0, 1, 2])
@pytest.mark.parametrize('locator', ['(5.13)', 'other source'])
def test_real_typed_duplicate_is_still_detected(index, locator):
    bridge = metadata_fixture()
    bridge.registry.add_reference(LiteratureEntry('typed-ref', ReferenceKind.EQUATION,
        locator, source_id='test-only', publication_position=10000))
    claim = canonical_513()[index]
    bridge.registry.add_assertion(AssertionEntry('typed', 'typed-ref', AssertionKind.STATEMENT,
        claim, origin=AssertionOrigin.FIXED_STATEMENT))
    metadata, conflicts = classify_existing_513(bridge, canonical_513())
    assert len(metadata) == 3 and [r['id'] for r in conflicts] == ['typed']


def test_metadata_with_proof_link_is_not_silently_ignored():
    bridge = metadata_fixture()
    key = 'delta_nu9_relation'
    step = ProofStep(bridge.registry.assertion(key).content, (), ProofRule.GIVEN)
    linked = RegistryBridgeResult(bridge.registry, (), (ProofStepLink(key, step=step),))
    metadata, conflicts = classify_existing_513(linked, canonical_513())
    assert len(metadata) == 2 and [r['id'] for r in conflicts] == [key]


@pytest.mark.parametrize('changes', [
    {'component_key': 'unreviewed'},
    {'reference_locator': '(5.12)'},
    {'statement_role': TodaLiteratureStatementRole.OTHER},
    {'range_is_explicit_in_current_aggregate': False},
])
def test_unreviewed_metadata_is_not_silently_ignored(changes):
    bridge = metadata_fixture()
    original = bridge.registry.assertion('delta_nu9_relation').content
    component = replace(original, **changes)
    bridge.registry.add_assertion(AssertionEntry('unexpected', 'boundary-ref', AssertionKind.STATEMENT,
        component, origin=AssertionOrigin.FIXED_STATEMENT))
    metadata, conflicts = classify_existing_513(bridge, canonical_513())
    assert len(metadata) == 3 and [r['id'] for r in conflicts] == ['unexpected']

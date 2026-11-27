"""Check the real shared registry and exact source lookup, not a group proof."""
import pytest

from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r3_recursive_search import _typed_reference_steps, reconstruct_registered_goal
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase169_r10e2_unpositioned_citation.source_first import screen_independent_sources_for_derived_goal
from phase178_r16_toda513_isolated.source import canonical_513
from phase178_r15_toda512_isolated.source import CitedToda512
from proof import ProofRule
from toda_literature_statement_boundary import TodaFixedStatementComponent
from unified_statement_registry import AssertionOrigin


@pytest.fixture(scope='module')
def bridge():
    return build_shared_typed_bridge()


def cited_links(bridge):
    return tuple(link for link in bridge.proof_links
                 if link.step is not None and link.step.conclusion in canonical_513())


def test_exact_three_fixed_source_leaves_and_metadata(bridge):
    links = cited_links(bridge)
    assert len(links) == 3
    assert tuple(link.step.conclusion for link in links) == canonical_513()
    for link in links:
        a = bridge.registry.assertion(link.assertion_id)
        ref = bridge.registry.reference(a.reference_id)
        assert a.origin is AssertionOrigin.FIXED_STATEMENT
        assert a.content == link.step.conclusion
        assert ref.locator == '(5.13)' and ref.publication_position == 10000
        assert link.step.rule is ProofRule.GIVEN and not link.step.premises
        assert link.step.inference_rule.literature_reference.locator == '(5.13)'
    metadata = tuple(a for a in bridge.registry._assertions.values()
                     if type(a.content) is TodaFixedStatementComponent
                     and a.content.reference_locator == '(5.13)')
    assert {a.content.component_key for a in metadata} == {
        'delta_nu9_relation', 'delta_eta11_squared_zero', 'delta_eta13_zero'}
    assert len(metadata) == 3
    assert not any(l.assertion_id in {a.assertion_id for a in metadata} for l in bridge.proof_links)
    assert sum(l.step is not None and type(l.step.conclusion) is CitedToda512
               for l in bridge.proof_links) == 3
    print('PHASE178_R16R2_PUBLIC_GIVEN_COUNT=3')
    print('PHASE178_R16R2_BOUNDARY_METADATA_COUNT=3')


@pytest.mark.parametrize('n', [5,6,7])
def test_derived_group_screen_and_exact_lookup(bridge,n):
    # A query marker only; never registered as a mathematical premise.
    target = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(n+6,n))
    screened = screen_independent_sources_for_derived_goal(bridge, goal=target)
    assert len(cited_links(screened)) == 3
    claim = canonical_513()[n-5]
    link, = (l for l in cited_links(screened) if l.step.conclusion == claim)
    assert _typed_reference_steps(screened, claim) == (link.step,)
    # The ordinary recursive resolver must find the exact screened GIVEN.
    # No alternative inference or fabricated parent is supplied.
    def no_expansion(goal):
        return ()
    step = reconstruct_registered_goal(claim, screened, link.assertion_id,
                                       no_expansion, lookup_mode='typed_reference')
    assert step == link.step and step.rule is ProofRule.GIVEN
    assert not _typed_reference_steps(screened, target)
    print(f'PHASE178_R16R2_N{n}_CITED_DELTA_LOOKUP=VERIFIED')


@pytest.mark.parametrize('position,count', [(9900,0),(10100,3)])
def test_explicit_publication_screen(bridge,position,count):
    citing = next(a for a in bridge.registry._assertions.values()
                  if bridge.registry.reference(a.reference_id).publication_position == position)
    target = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(11,5))
    screened = screen_shared_proof_context(bridge, goal=target,
                    citing_assertion_id=citing.assertion_id, explicit_publication_target=True)
    assert len(cited_links(screened)) == count
    assert all(len(_typed_reference_steps(screened, claim)) == int(count == 3)
               for claim in canonical_513())
    print(f'PHASE178_R16R2_SCREEN_{position}=VERIFIED')


def test_removed_links_cannot_be_used_by_exact_lookup(bridge):
    target = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(11,5))
    screened = screen_independent_sources_for_derived_goal(bridge,goal=target)
    reduced = RegistryBridgeResult(screened.registry,screened.records,
                        tuple(l for l in screened.proof_links if l not in cited_links(screened)))
    assert all(not _typed_reference_steps(reduced, claim) for claim in canonical_513())

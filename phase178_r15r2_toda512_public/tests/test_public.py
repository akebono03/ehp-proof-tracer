"""Exercise the real common registry, source screens and provider."""
import pytest

from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement, TodaSuspensionMap
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r14_r6_generic_iso import MapSurjective
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase169_r10e2_unpositioned_citation.source_first import screen_independent_sources_for_derived_goal
from phase175_r4r12r13r4_hopf_zero_public.rule import DELTA_TO_H_ZERO, H_ZERO_TO_E_SURJ, suspension_surjective_inputs
from phase178_r15_toda512_isolated.source import CitedToda512, canonical_512
from phase178_r15_toda512_isolated.provider import RULE_NAME
from proof import ProofRule, find_inference_matches_for_rule, apply_inference_match
from unified_statement_registry import AssertionOrigin


@pytest.fixture(scope='module')
def bridge():
    return build_shared_typed_bridge()


def cited_links(bridge):
    return tuple(link for link in bridge.proof_links if link.step is not None and type(link.step.conclusion) is CitedToda512)


def test_exactly_three_fixed_source_leaves(bridge):
    links = cited_links(bridge)
    assert len(links) == 3
    assert {link.step.conclusion.n for link in links} == {4, 5, 6}
    for link in links:
        assertion = bridge.registry.assertion(link.assertion_id)
        ref = bridge.registry.reference(assertion.reference_id)
        assert assertion.origin is AssertionOrigin.FIXED_STATEMENT
        assert assertion.content == link.step.conclusion == canonical_512(link.step.conclusion.n)
        assert ref.publication_position == 9700 and ref.locator == '(5.12)'
        assert link.step.rule is ProofRule.GIVEN and not link.step.premises
    print('PHASE178_R15R2_PUBLIC_GIVEN_COUNT=3')


@pytest.mark.parametrize('n', [4, 5, 6])
def test_public_typed_candidate_and_existing_ehp_chain(bridge, n):
    # The group placeholder is used for source screening only, never asserted or proved.
    root = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(n + 7, n + 1))
    screened = screen_independent_sources_for_derived_goal(bridge, goal=root)
    claim = canonical_512(n)
    link, = (x for x in cited_links(screened) if x.step.conclusion == claim)
    provider = shared_expansion_provider(screened, proof_target=root)
    option, = (o for o in provider(claim.statement) if o.rule.name == RULE_NAME)
    assert option.subgoals == (claim,)
    matches = find_inference_matches_for_rule(option.rule, (link.step,))
    result, = (apply_inference_match(m) for m in matches if m.premises == (link.step,))
    assert result.rule is ProofRule.INFERENCE and result.conclusion == claim.statement
    e = MapSurjective(TodaSuspensionMap(TodaPrimaryGroup(n + 6, n), TodaPrimaryGroup(n + 7, n + 1)))
    h, eh_exact = suspension_surjective_inputs(e)
    h_options = [o for o in provider(h) if o.rule.name == DELTA_TO_H_ZERO]
    e_options = [o for o in provider(e) if o.rule.name == H_ZERO_TO_E_SURJ]
    assert any(o.subgoals[0] == claim.statement for o in h_options)
    assert any(o.subgoals == (h, eh_exact) for o in e_options)
    print(f'PHASE178_R15R2_N{n+1}_CITED_DELTA_AND_EHP_CANDIDATES=VERIFIED')


def test_earlier_publication_context_excludes_512(bridge):
    earlier = next(a for a in bridge.registry._assertions.values()
                   if bridge.registry.reference(a.reference_id).publication_position == 9500)
    root = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(11, 5))
    screened = screen_shared_proof_context(bridge, goal=root, citing_assertion_id=earlier.assertion_id,
                                           explicit_publication_target=True)
    assert not cited_links(screened)
    provider = shared_expansion_provider(screened, proof_target=root)
    assert not any(o.rule.name == RULE_NAME for o in provider(canonical_512(4).statement))
    print('PHASE178_R15R2_EARLIER_SOURCE_SCREEN=VERIFIED')


def test_screened_link_removal_disables_provider(bridge):
    reduced = RegistryBridgeResult(bridge.registry, bridge.records,
                                   tuple(x for x in bridge.proof_links if x not in cited_links(bridge)))
    provider = shared_expansion_provider(reduced)
    assert not any(o.rule.name == RULE_NAME for o in provider(canonical_512(4).statement))

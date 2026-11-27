from dataclasses import replace
import pytest

from homotopy_groups import TodaDeltaMap, TodaPrimaryGroup
from phase165_r14_r6_generic_iso import MapInjective
from phase175_r4r12r13r4_hopf_zero_public.rule import hopf_zero_inputs
from homotopy_groups import TodaHopfInvariantMap
from toda_rules import TodaHopfInvariantZeroStatement
from proof import ProofRule, find_inference_matches_for_rule, apply_inference_match
from unified_statement_registry import AssertionOrigin
from phase178_r15_toda512_isolated.source import build_cited_512_source, canonical_512
from phase178_r15_toda512_isolated.provider import build_cited_512_provider, expand_cited_512


@pytest.mark.parametrize('n', [4,5,6])
def test_cited_injective_replay(n):
    bridge = build_cited_512_source()
    assert len(bridge.proof_links) == 3
    claim = canonical_512(n)
    assert claim.statement == MapInjective(TodaDeltaMap(TodaPrimaryGroup(n+7,2*n+1), TodaPrimaryGroup(n+5,n)))
    link, = (x for x in bridge.proof_links if x.step.conclusion == claim)
    assertion = bridge.registry.assertion(link.assertion_id)
    assert assertion.origin is AssertionOrigin.FIXED_STATEMENT
    assert bridge.registry.reference(assertion.reference_id).publication_position == 9700
    assert link.step.rule is ProofRule.GIVEN and not link.step.premises
    option, = build_cited_512_provider(bridge)(claim.statement)
    assert option.subgoals == (claim,)
    matches = find_inference_matches_for_rule(option.rule, (link.step,))
    result, = (apply_inference_match(m) for m in matches if m.premises == (link.step,))
    assert result.rule is ProofRule.INFERENCE and result.conclusion == claim.statement
    assert result.premises == (link.step,)
    assert not find_inference_matches_for_rule(option.rule, ())
    h = TodaHopfInvariantZeroStatement(TodaHopfInvariantMap(TodaPrimaryGroup(n+7,n+1), TodaPrimaryGroup(n+7,2*n+1)))
    assert hopf_zero_inputs(h)[0] == result.conclusion


@pytest.mark.parametrize('n', [3,7,True,4.0])
def test_bad_n(n):
    with pytest.raises(ValueError):
        canonical_512(n)


def test_reject_missing_duplicate_or_altered_citation():
    c = canonical_512(4)
    assert not expand_cited_512(c.statement, ())
    assert not expand_cited_512(c.statement, (c,c))
    assert not expand_cited_512(c.statement, (replace(c,locator='(5.13)'),))
    assert not expand_cited_512(canonical_512(5).statement,(c,))
    assert not expand_cited_512(c.statement,(replace(c,n=5),))

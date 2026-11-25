"""General typed hypotheses, real source/DB admission, and rejection cases."""
from dataclasses import replace

import pytest

from expression import GeneratorSymbol, HomotopyElement
from homotopy_groups import FiniteCyclicGroup, TodaDeltaMap, TodaPrimaryGroup
from phase165_r12_r2_quotient_rules import KernelMultipleStatement
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase169_r10e2_unpositioned_citation.source_first import screen_independent_sources_for_derived_goal
from phase169_r10e4_ordered_db_prior.db_prior import admitted_prior_group_step, exact_prior_database_result
from phase176_r3r48_cited_finite_delta_kernel.apply import ROOT, PINS, updated_source
from phase176_r3r48_cited_finite_delta_kernel.provider import build_finite_delta_kernel_provider
from phase176_r3r48_cited_finite_delta_kernel.rule import RULE_NAME, conditional_inputs, linked_cited_steps
from phase176_r3r48_cited_finite_delta_kernel.source import canonical_signed_delta, build_cited_lemma57_delta_source
from proof import ProofRule, ProofStep, Relation, RelationType, find_inference_matches_for_rule, apply_inference_match
from toda_rules import TodaDeltaImageUpToSignStatement


def fixture(q,n,M,m):
    a,b = TodaPrimaryGroup(q+2,2*n+1), TodaPrimaryGroup(q,n)
    x = HomotopyElement('a',2*n+1,q+2,2*n+1,GeneratorSymbol('a',2*n+1))
    y = HomotopyElement('b',n,q,n,GeneratorSymbol('b',n))
    delta = TodaDeltaMap(a,b)
    return (KernelMultipleStatement(delta,a,x,m),
            Relation(a,FiniteCyclicGroup(M,x),RelationType.EQUALITY),
            Relation(b,FiniteCyclicGroup(m,y),RelationType.EQUALITY),
            TodaDeltaImageUpToSignStatement(delta,x,y))


@pytest.mark.parametrize('q,n,M,m',[(6,2,8,4),(9,5,16,2),(13,6,32,8),(6,2,4,4)])
def test_generic_typed_inputs(q,n,M,m):
    goal,a,b,signed = fixture(q,n,M,m)
    assert conditional_inputs(goal,a,b,signed) == (a,b,signed)
    assert conditional_inputs(replace(goal,multiple=m+1),a,b,signed) is None
    assert conditional_inputs(goal,replace(a,rhs=FiniteCyclicGroup(M+1,a.rhs.generator)),b,signed) is None
    assert conditional_inputs(goal,a,b,replace(signed,positive_value=a.rhs.generator)) is None
    assert conditional_inputs(goal,b,a,signed) is None


def test_one_literal_source_not_a_kernel_given():
    bridge = build_cited_lemma57_delta_source(ROOT)
    link, = bridge.proof_links
    assert link.step.rule is ProofRule.GIVEN and link.step.conclusion == canonical_signed_delta()
    assert bridge.registry.reference(bridge.registry.assertion(link.assertion_id).reference_id).publication_position == 9100
    assert not any(type(x.step.conclusion) is KernelMultipleStatement for x in bridge.proof_links)


@pytest.fixture(scope='module')
def actual():
    root = exact_prior_database_result(3,5)
    bridge = screen_independent_sources_for_derived_goal(build_shared_typed_bridge(),goal=root)
    signed = canonical_signed_delta()
    a = admitted_prior_group_step(signed.map.source_group,proof_target=root,bridge=bridge)
    b = admitted_prior_group_step(signed.map.target_group,proof_target=root,bridge=bridge)
    assert a is not None and b is not None
    assert a.conclusion.rhs.generator == signed.element
    assert b.conclusion.rhs.generator == signed.positive_value
    goal = KernelMultipleStatement(signed.map,signed.map.source_group,signed.element,b.conclusion.rhs.order)
    cited, = linked_cited_steps(bridge,signed)
    return root,bridge,goal,(a,b,cited)


def test_public_candidate_and_verified_ancestry(actual):
    root,bridge,goal,facts = actual
    options = shared_expansion_provider(bridge,proof_target=root)(goal)
    option, = [x for x in options if x.rule.name == RULE_NAME]
    assert option.subgoals == tuple(s.conclusion for s in facts)
    match, = find_inference_matches_for_rule(option.rule,facts)
    derived = apply_inference_match(match)
    assert derived.rule is ProofRule.INFERENCE and derived.conclusion == goal
    assert derived.premises == facts
    for i in range(3):
        assert not find_inference_matches_for_rule(option.rule,tuple(x for j,x in enumerate(facts) if j != i))
        forged = ProofStep(facts[i].conclusion,(),ProofRule.GIVEN)
        assert not find_inference_matches_for_rule(option.rule,tuple(forged if j == i else x for j,x in enumerate(facts)))


def test_self_prior_and_missing_signed_source_do_not_supply_candidate(actual):
    root,bridge,goal,facts = actual
    expand = build_finite_delta_kernel_provider(bridge=bridge,proof_target=facts[0].conclusion)
    assert not expand(goal)
    missing = replace(bridge,proof_links=tuple(link for link in bridge.proof_links if link.step != facts[2]))
    assert not build_finite_delta_kernel_provider(bridge=missing,proof_target=root)(goal)
    assert not build_finite_delta_kernel_provider(bridge=bridge,proof_target=root)(replace(goal,multiple=3))


def test_patch_idempotence_and_unknown_bytes():
    for path in PINS:
        raw = (ROOT/path).read_bytes()
        assert updated_source(path,raw) == raw
        with pytest.raises(ValueError):
            updated_source(path,raw+b'\n# unknown edit\n')

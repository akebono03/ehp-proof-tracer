"""Exercise the unchanged R14 rules through ordinary public root search."""
from dataclasses import replace
from unittest.mock import patch

import pytest

from expression import HomotopyElement
from homotopy_groups import DirectSumGroup, FiniteCyclicGroup, TodaDeltaMap, TodaPrimaryGroup
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from phase165_r14_r6_generic_iso import GeneratorImage, MapInjective
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result, verified_db_step
from phase171_r2j_r4_r7_nonzero_nu_order.source import FiniteElementOrder
from phase175_r4r12_public_two_summand_quotient.provider import expand_public_two_summand_quotient
from phase175_r4r12r9_delta_generator_image_bridge.rule import delta_image_equality
from phase175_r4r12r10r1_cited_511_public.provider import same_registered_cited_511
from phase175_r4r12r10r1_cited_511_public.source import CitedToda511, canonical_511
from phase175_r4r12r13r4_hopf_zero_public.rule import hopf_zero_inputs, suspension_surjective_inputs
from phase177_r9_delta_rhs_normalization_audit.audit import canonical_delta, route_matches
from phase177_r14_finite_cyclic_delta_injective_isolated.rule import ORDER_RULE, INJECTIVE_RULE
from phase177_r15_finite_cyclic_delta_injective_public.provider import expand_from_presentations
from proof import ProofRule, Relation, apply_inference_match, find_inference_matches_for_rule


def ancestors(step):
    yield step
    for parent in step.premises:
        yield from ancestors(parent)


@pytest.mark.parametrize('n,m', [(3,2),(4,4),(5,8),(6,16)])
def test_generic_candidates(n,m):
    source = TodaPrimaryGroup(2*n+2,2*n+1)
    target = TodaPrimaryGroup(2*n,n)
    a = HomotopyElement('a',2*n+1,2*n+2,2*n+1)
    b,c = (HomotopyElement(name,n,2*n,n) for name in ('b','c'))
    domain = Relation(source,FiniteCyclicGroup(m,a))
    codomain = Relation(target,DirectSumGroup((FiniteCyclicGroup(m,b),FiniteCyclicGroup(m,c))))
    delta = TodaDeltaMap(source,target)
    goal = MapInjective(delta)
    def lookup(group):
        return tuple(x for x in (domain,codomain) if x.lhs == group)
    options = expand_from_presentations(goal,lookup)
    assert len(options) == 2
    for part, option in zip(codomain.rhs.summands,options):
        image = GeneratorImage(delta,a,part.generator)
        order = FiniteElementOrder(target,part.generator,m)
        assert option.rule.name == INJECTIVE_RULE and option.subgoals == (domain,image,order)
        first, = expand_from_presentations(order,lookup)
        assert first.rule.name == ORDER_RULE and first.subgoals == (codomain,)
        assert not find_inference_matches_for_rule(option.rule,())
        assert not find_inference_matches_for_rule(first.rule,())
        assert not expand_from_presentations(replace(order,order=m+1),lookup)
    assert not expand_from_presentations(goal,lambda group: ())
    assert not expand_from_presentations(MapInjective(TodaDeltaMap(source,TodaPrimaryGroup(2*n,n+1))),lookup)


def capture_actual():
    import phase165_r55_nk_only_goal as entry
    import phase165_r52_r9_shared_math as shared
    from web_group_proof import build_standard_web_group_proof_view
    invocations,results,calls = [],[],[]
    real_entry = entry.search_group_from_registered_goal
    real_adapter = shared.search_registered_partial_proof
    def observed_entry(*args,**kwargs):
        result = real_entry(*args,**kwargs)
        results.append(result)
        return result
    def observed_adapter(*args,**kwargs):
        if (kwargs.get('n'),kwargs.get('k')) != (5,5):
            return real_adapter(*args,**kwargs)
        invocations.append(dict(kwargs))
        provider = kwargs['expansion_provider']
        def observed(goal):
            options = provider(goal)
            calls.append((goal,options))
            return options
        return real_adapter(*args,**dict(kwargs,expansion_provider=observed))
    with patch.object(entry,'search_group_from_registered_goal',observed_entry), \
         patch.object(shared,'search_registered_partial_proof',observed_adapter):
        view = build_standard_web_group_proof_view(n=5,k=5,max_depth=2,mode='narrative',citation_source='model')
    assert len(invocations) == len(results) == 1
    return invocations[0],results[0],calls,view


def verify_step(step, rule_name, subgoals):
    assert step.rule is ProofRule.INFERENCE and step.inference_rule is not None
    assert step.inference_rule.name == rule_name
    assert tuple(p.conclusion for p in step.premises) == subgoals
    matches = find_inference_matches_for_rule(step.inference_rule,step.premises)
    assert any(apply_inference_match(m).conclusion == step.conclusion and m.premises == step.premises for m in matches)


def test_actual_public_chain():
    invocation,result,calls,view = capture_actual()
    root,bridge = invocation['goal'],invocation['bridge']
    assert root.lhs == result.target == TodaPrimaryGroup(10,5)
    assert isinstance(root.rhs,FiniteCyclicGroup) and root.rhs.order == 2
    print('PHASE177_R15_ROOT_STATUS='+result.status.value,flush=True)
    print('PHASE177_R15_ROOT_OPEN_GOALS='+str(len(result.open_goals)),flush=True)
    print('PHASE177_R15_WEB_KEY='+view.key,flush=True)
    for goal in result.open_goals:
        print('PHASE177_R15_OPEN='+repr(goal),flush=True)
    cyclic = CyclicStructureStatement(root.lhs,root.rhs.generator,2)
    routes = expand_public_two_summand_quotient(cyclic,proof_target=root)
    chosen, = [r for r in routes if route_matches(canonical_delta(),delta_image_equality(r.subgoals[2]))]
    middle,upper_domain,upper_image,exact,e_surj,e_image = chosen.subgoals
    h_zero,e_h = suspension_surjective_inputs(e_surj)
    delta_goal,h_delta = hopf_zero_inputs(h_zero)
    domain = exact_prior_database_result(9,1)
    codomain = exact_prior_database_result(4,4)
    images = [GeneratorImage(delta_goal.map,domain.rhs.generator,p.generator)
              for p in codomain.rhs.summands if isinstance(p,FiniteCyclicGroup)]
    lower_image, = [g for g in images if delta_image_equality(g) is not None
                    and same_registered_cited_511(delta_image_equality(g))]
    order = FiniteElementOrder(codomain.lhs,lower_image.target_generator,domain.rhs.order)
    for label,goal in [('upper_image',upper_image),('domain',domain),('codomain',codomain),
                       ('lower_image',lower_image),('order',order),('delta_injective',delta_goal),
                       ('hopf_zero',h_zero),('e_surjective',e_surj),('surviving_image',e_image)]:
        accepted = any(s.conclusion == goal for s in result.proven_steps)
        batches = [opts for g,opts in calls if type(g) is type(goal) and g == goal]
        print('PHASE177_R15_CASE='+label+':'+('ACCEPTED' if accepted else ('REACHED' if batches else 'NOT_REACHED')),flush=True)
    steps = tuple(result.proven_steps)
    def accepted(goal):
        matches = [s for s in steps if type(s.conclusion) is type(goal) and s.conclusion == goal]
        assert matches, ('ACTUAL_ROOT_PREMISE_NOT_ACCEPTED',repr(goal))
        return matches[-1]
    injective = accepted(delta_goal)
    verify_step(injective,INJECTIVE_RULE,(domain,lower_image,order))
    domain_step,image_step,order_step = injective.premises
    verify_step(order_step,ORDER_RULE,(codomain,))
    codomain_step, = order_step.premises
    for group_step in (domain_step,codomain_step):
        if group_step.rule is ProofRule.GIVEN and group_step.note == 'ADOPTED_DATABASE_PRIOR; independent reference not asserted':
            assert verified_db_step(group_step,proof_target=root,bridge=bridge)
    assert any(s.rule is ProofRule.GIVEN and s.conclusion == CitedToda511(canonical_511()) for s in ancestors(image_step))
    assert accepted(upper_image).rule is ProofRule.INFERENCE
    surj = accepted(e_surj)
    assert surj.rule is ProofRule.INFERENCE
    assert any(s is injective for s in ancestors(surj))
    print('PHASE177_R15_ACTUAL_DELTA_INJECTIVE=PUBLIC_PROVED',flush=True)
    print('PHASE177_R15_ACTUAL_E_SURJECTIVE=PUBLIC_PROVED',flush=True)
    if result.status.value == 'complete':
        assert result.conclusion == root and not result.open_goals
        assert view.key == 'generic-complete-proof'
        root_step = accepted(root)
        assert any(s is injective for s in ancestors(root_step))
        assert any(s.conclusion == e_image for s in ancestors(root_step))
        assert any(s.conclusion == upper_image for s in ancestors(root_step))
        print('PHASE177_R15_ACTUAL_ROOT=COMPLETE',flush=True)
    else:
        assert result.status.value == 'partial' and result.conclusion is None
        print('PHASE177_R15_ACTUAL_ROOT=PARTIAL_REQUIRES_FRONTIER_AUDIT',flush=True)

from dataclasses import replace

import pytest

from expression import HomotopyElement, Zero
from homotopy_groups import FiniteCyclicGroup, TodaDeltaMap, TodaPrimaryGroup, TodaSuspensionMap
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase169_r10e2_unpositioned_citation.source_first import screen_independent_sources_for_derived_goal
from phase169_r10e4_ordered_db_prior.db_prior import (
    admitted_prior_group_step, exact_prior_database_result, verified_db_step,
)
from phase176_r3r48_cited_finite_delta_kernel.rule import linked_cited_steps
from phase178_r16_toda513_isolated.source import canonical_513
from phase178_r21_finite_cyclic_generator_zero_image_isolated import rule as r21
from proof import (
    InferenceRule, LiteratureReference, ProofRule, ProofStep, Relation, RelationType,
    apply_inference_match, find_inference_matches_for_rule,
)
from toda_rules import TodaDeltaZeroStatement
from unified_statement_registry import (
    AssertionEntry, AssertionKind, AssertionOrigin, LiteratureEntry, ProofStepLink,
    ReferenceKind, UnifiedStatementRegistry,
)


def presentation(q, n, order=2, name='a'):
    return Relation(TodaPrimaryGroup(q, n),
                    FiniteCyclicGroup(order, HomotopyElement(name, n, q, n)))


def synthetic_case(n=4, k=5, order=4):
    q = 2*n-1+k
    a = presentation(q+2, 2*n+1, order)
    goal = TodaDeltaZeroStatement(TodaDeltaMap(a.lhs, TodaPrimaryGroup(q, n)))
    root = presentation(q+1, n+1, order, 'root')
    return goal, a, root


def synthetic_bridge(*claims):
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry('r21:test', ReferenceKind.EQUATION,
        'synthetic R21', publication_position=1))
    links = []
    for i, claim in enumerate(claims):
        key = 'r21:test:' + str(i)
        registry.add_assertion(AssertionEntry(key, 'r21:test', AssertionKind.STATEMENT,
            claim, origin=AssertionOrigin.FIXED_STATEMENT))
        step = ProofStep(claim, (), ProofRule.GIVEN, inference_rule=InferenceRule(
            'synthetic hypothesis only', literature_reference=LiteratureReference(
                label='synthetic R21', locator='synthetic R21')))
        links.append(ProofStepLink(key, step=step))
    return RegistryBridgeResult(registry, (), tuple(links))


@pytest.mark.parametrize('n,k,order', [(2,1,2), (4,5,4), (8,3,8), (9,2,3)])
def test_general_typed_obligations_and_conditional_replay(n,k,order,monkeypatch):
    goal, a, root = synthetic_case(n,k,order)
    image = GeneratorImage(goal.map, a.rhs.generator, Zero())
    bridge = synthetic_bridge(a,image)
    monkeypatch.setattr(r21, 'admitted_prior_group_step', lambda *args, **kwargs: None)
    option, = r21.build_finite_cyclic_delta_zero_provider(bridge=bridge,proof_target=root)(goal)
    assert option.subgoals == r21.finite_cyclic_delta_zero_inputs(goal,a) == (a,image)
    assert option.rule.name == r21.RULE_NAME and option.rule.literature_reference is None
    assert not any(isinstance(x,ProofStep) for x in option.subgoals)
    parents = tuple(link.step for link in bridge.proof_links)
    match, = find_inference_matches_for_rule(option.rule,parents)
    result = apply_inference_match(match)
    assert result.rule is ProofRule.INFERENCE and result.conclusion == goal
    assert result.premises == parents
    for i in range(2):
        assert not find_inference_matches_for_rule(option.rule,parents[:i]+parents[i+1:])
        forged = ProofStep(parents[i].conclusion,(),ProofRule.GIVEN)
        assert not find_inference_matches_for_rule(option.rule,parents[:i]+(forged,)+parents[i+1:])


@pytest.mark.parametrize('kind', ['wrong_map_type','wrong_delta_dimension','wrong_delta_sphere',
    'wrong_group','wrong_generator_dimension','zero_generator','bool_order','order_one',
    'non_equality','bool_dimension','float_dimension','not_delta_goal'])
def test_invalid_typed_inputs(kind):
    goal,a,root = synthetic_case()
    d = goal.map
    q,n = d.target_group.group_dimension,d.target_group.sphere_dimension
    if kind == 'wrong_map_type':
        goal = TodaDeltaZeroStatement(TodaSuspensionMap(d.source_group,d.target_group))
    elif kind == 'wrong_delta_dimension':
        goal = TodaDeltaZeroStatement(TodaDeltaMap(d.source_group,TodaPrimaryGroup(q+1,n)))
    elif kind == 'wrong_delta_sphere':
        goal = TodaDeltaZeroStatement(TodaDeltaMap(d.source_group,TodaPrimaryGroup(q,n+1)))
    elif kind == 'wrong_group':
        a = presentation(q+3,2*n+1)
    elif kind == 'wrong_generator_dimension':
        a = replace(a,rhs=FiniteCyclicGroup(2,root.rhs.generator))
    elif kind == 'zero_generator':
        a = replace(a,rhs=FiniteCyclicGroup(2,Zero()))
    elif kind == 'bool_order':
        a = replace(a,rhs=FiniteCyclicGroup(True,a.rhs.generator))
    elif kind == 'order_one':
        a = replace(a,rhs=FiniteCyclicGroup(1,a.rhs.generator))
    elif kind == 'non_equality':
        a = replace(a,relation_type=RelationType.ORDER)
    elif kind == 'bool_dimension':
        goal = TodaDeltaZeroStatement(TodaDeltaMap(TodaPrimaryGroup(q+2,True),d.target_group))
    elif kind == 'float_dimension':
        goal = TodaDeltaZeroStatement(TodaDeltaMap(TodaPrimaryGroup(float(q+2),2*n+1),d.target_group))
    elif kind == 'not_delta_goal':
        goal = GeneratorImage(d,a.rhs.generator,Zero())
    assert r21.finite_cyclic_delta_zero_inputs(goal,a) is None
    with pytest.raises(ValueError):
        r21.finite_cyclic_delta_zero_rule(goal,a,proof_target=root,bridge=synthetic_bridge())


def test_source_first_and_missing_or_mismatched_source(monkeypatch):
    goal,a,root = synthetic_case()
    b = presentation(a.lhs.group_dimension,a.lhs.sphere_dimension,4,'b')
    image_a = GeneratorImage(goal.map,a.rhs.generator,Zero())
    image_b = GeneratorImage(goal.map,b.rhs.generator,Zero())
    witness = ProofStep(b,(),ProofRule.GIVEN)
    monkeypatch.setattr(r21,'admitted_prior_group_step',lambda *args,**kwargs: witness)
    monkeypatch.setattr(r21,'verified_db_step',lambda *args,**kwargs: True)
    bridge = synthetic_bridge(a,a,image_a,image_b)
    options = r21.build_finite_cyclic_delta_zero_provider(bridge=bridge,proof_target=root)(goal)
    assert tuple(o.subgoals for o in options) == ((a,image_a),(b,image_b))
    # Wrong generator, nonzero image, or a zero image of a different map is not enough.
    for claim in (image_a, replace(image_b,target_generator=b.rhs.generator),
                  GeneratorImage(TodaDeltaMap(goal.map.source_group,root.lhs),b.rhs.generator,Zero())):
        bridge = synthetic_bridge(claim)
        assert not r21.build_finite_cyclic_delta_zero_provider(bridge=bridge,proof_target=root)(goal)
    monkeypatch.setattr(r21,'verified_db_step',lambda *args,**kwargs: False)
    assert not r21.build_finite_cyclic_delta_zero_provider(bridge=synthetic_bridge(image_b),proof_target=root)(goal)


@pytest.fixture(scope='module')
def real_n6():
    root = exact_prior_database_result(6,6)
    assert root is not None and root.lhs == TodaPrimaryGroup(12,6)
    bridge = screen_independent_sources_for_derived_goal(build_shared_typed_bridge(),goal=root)
    image = canonical_513()[1]
    goal = TodaDeltaZeroStatement(image.map)
    prior = admitted_prior_group_step(image.map.source_group,proof_target=root,bridge=bridge)
    assert prior is not None and verified_db_step(prior,proof_target=root,bridge=bridge)
    assert prior.conclusion == exact_prior_database_result(11,2)
    assert prior.conclusion.rhs.order == 2 and prior.conclusion.rhs.generator == image.source_generator
    cited = linked_cited_steps(bridge,image)
    assert cited and cited[0].inference_rule.literature_reference.locator == '(5.13)'
    return root,bridge,goal,prior,cited[0]


def test_real_n6_admitted_db_and_citation_replay(real_n6):
    root,bridge,goal,prior,cited = real_n6
    before = (tuple(bridge.proof_links),tuple(bridge.registry._assertions.items()))
    expand = r21.build_finite_cyclic_delta_zero_provider(bridge=bridge,proof_target=root)
    options = expand(goal)
    option, = [o for o in options if o.subgoals == (prior.conclusion,cited.conclusion)]
    match, = find_inference_matches_for_rule(option.rule,(prior,cited))
    result = apply_inference_match(match)
    assert result.rule is ProofRule.INFERENCE and result.conclusion == goal
    assert result.premises == (prior,cited)
    assert result.inference_rule.literature_reference is None
    assert not any(link.step is not None and link.step.conclusion == root for link in bridge.proof_links)
    public = shared_expansion_provider(bridge,proof_target=root)(goal)
    assert sum(o.rule.name == r21.RULE_NAME and o.subgoals == option.subgoals for o in public) == 1
    assert before == (tuple(bridge.proof_links),tuple(bridge.registry._assertions.items()))
    print('R21_N6_DELTA_ZERO_ISOLATED_REPLAY=VERIFIED')
    print('R21R1_N6_PUBLIC_PROVIDER_MATCH=VERIFIED')


def test_real_n6_reject_unadmitted_or_unlinked_steps(real_n6):
    root,bridge,goal,prior,cited = real_n6
    option, = [o for o in r21.build_finite_cyclic_delta_zero_provider(bridge=bridge,proof_target=root)(goal)
               if o.subgoals == (prior.conclusion,cited.conclusion)]
    for parents in ((prior,), (cited,), (replace(prior,note='forged'),cited),
                    (prior,ProofStep(cited.conclusion,(),ProofRule.GIVEN)),
                    (prior,replace(cited,rule=ProofRule.INFERENCE)),
                    (prior,replace(cited,conclusion=replace(cited.conclusion,source_generator=root.rhs.generator)))):
        assert not find_inference_matches_for_rule(option.rule,parents)
    missing = replace(bridge,proof_links=tuple(link for link in bridge.proof_links if link.step != cited))
    assert not r21.build_finite_cyclic_delta_zero_provider(bridge=missing,proof_target=root)(goal)
    assert not r21.build_finite_cyclic_delta_zero_provider(bridge=bridge,proof_target=prior.conclusion)(goal)
    db_only = replace(bridge,proof_links=tuple(link for link in bridge.proof_links
                           if link.step is None or link.step.conclusion != prior.conclusion))
    assert not r21.build_finite_cyclic_delta_zero_provider(bridge=db_only,proof_target=presentation(2,2))(goal)

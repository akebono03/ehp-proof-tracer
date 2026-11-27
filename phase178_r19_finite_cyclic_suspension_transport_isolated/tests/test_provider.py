"""Synthetic conditional replay and real source-screened proposal discovery."""
from dataclasses import replace

import pytest

from expression import Composition, HomotopyElement, Zero
from homotopy_groups import (
    FiniteCyclicGroup, TodaPrimaryGroup, TodaSuspensionIsomorphismStatement,
    TodaSuspensionMap,
)
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r12_r24_web_search_connection import expand_finite_cyclic_relation
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase169_r10e2_unpositioned_citation.source_first import screen_independent_sources_for_derived_goal
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase178_r19_finite_cyclic_suspension_transport_isolated import provider
from proof import (
    InferenceRule, LiteratureReference, ProofRule, ProofStep, Relation, RelationType,
    apply_inference_match, find_inference_matches_for_rule,
)
from unified_statement_registry import (
    AssertionEntry, AssertionKind, AssertionOrigin, LiteratureEntry, ProofStepLink,
    ReferenceKind, UnifiedStatementRegistry,
)

RULE = 'finite cyclic presentation transported by proved suspension isomorphism'


def presentation(n, k, order, name='x'):
    return Relation(TodaPrimaryGroup(n+k, n),
                    FiniteCyclicGroup(order, HomotopyElement(name, n, n+k, n)))


def synthetic_bridge(*sources):
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry('r19:test', ReferenceKind.EQUATION,
        'synthetic R19', publication_position=1))
    links = []
    for i, source in enumerate(sources):
        key = 'r19:test:' + str(i)
        registry.add_assertion(AssertionEntry(key, 'r19:test', AssertionKind.STATEMENT,
            source, origin=AssertionOrigin.FIXED_STATEMENT))
        step = ProofStep(source, (), ProofRule.GIVEN, inference_rule=InferenceRule(
            'synthetic hypothesis only', literature_reference=LiteratureReference(
                label='synthetic R19', locator='synthetic R19')))
        links.append(ProofStepLink(key, step=step))
    return RegistryBridgeResult(registry, (), tuple(links))


@pytest.mark.parametrize('n,k,order', [(3,1,2), (4,3,8), (6,6,2), (9,7,16)])
def test_general_inputs(n, k, order):
    a, b = presentation(n-1,k,order), presentation(n,k,order,'y')
    e = TodaSuspensionMap(a.lhs,b.lhs)
    assert provider.suspension_transport_inputs(b,a) == (
        a, TodaSuspensionIsomorphismStatement(e),
        GeneratorImage(e,a.rhs.generator,b.rhs.generator))


@pytest.mark.parametrize('kind', ['wrong_order','wrong_group','wrong_stem','wrong_source_type',
                                 'wrong_relation','wrong_generator','zero_generator','bool_order',
                                 'annotated_root','bad_target_generator','nonadjacent'])
def test_reject_invalid_inputs(kind):
    a,b = presentation(5,6,2), presentation(6,6,2,'y')
    if kind == 'wrong_order':
        a = presentation(5,6,4)
    elif kind == 'wrong_group':
        a = presentation(6,6,2)
    elif kind == 'wrong_stem':
        a = presentation(5,5,2)
    elif kind == 'wrong_source_type':
        a = a.rhs
    elif kind == 'wrong_relation':
        a = replace(a,relation_type=RelationType.ORDER)
    elif kind == 'wrong_generator':
        a = replace(a,rhs=FiniteCyclicGroup(2,b.rhs.generator))
    elif kind == 'zero_generator':
        a = replace(a,rhs=FiniteCyclicGroup(2,Zero()))
    elif kind == 'bool_order':
        a = replace(a,rhs=FiniteCyclicGroup(True,a.rhs.generator))
    elif kind == 'annotated_root':
        b = replace(b,note='test annotation')
    elif kind == 'bad_target_generator':
        b = replace(b,rhs=FiniteCyclicGroup(2,a.rhs.generator))
    elif kind == 'nonadjacent':
        a = presentation(4,6,2)
    assert provider.suspension_transport_inputs(b,a) is None


def test_existing_rule_replays_only_with_three_hypotheses(monkeypatch):
    a,b = presentation(5,6,2), presentation(6,6,2,'y')
    monkeypatch.setattr(provider,'admitted_prior_group_step',lambda *args,**kwargs: None)
    bridge = synthetic_bridge(a)
    expand = provider.build_finite_cyclic_suspension_transport_provider(bridge=bridge,proof_target=b)
    option, = expand(b)
    assert option.rule.name == RULE and option.rule.literature_reference is None
    assert option.subgoals == provider.suspension_transport_inputs(b,a)
    assert all(not isinstance(x,ProofStep) for x in option.subgoals)
    # These are synthetic assumptions for a conditional matcher test only.
    parents = tuple(ProofStep(x,(),ProofRule.GIVEN) for x in option.subgoals)
    match, = find_inference_matches_for_rule(option.rule,parents)
    result = apply_inference_match(match)
    assert result.conclusion == b and result.rule is ProofRule.INFERENCE
    assert result.premises == parents
    for i in range(3):
        assert not find_inference_matches_for_rule(option.rule,parents[:i]+parents[i+1:])
    wrong = replace(parents[2],conclusion=GeneratorImage(option.subgoals[2].map,b.rhs.generator,a.rhs.generator))
    assert not find_inference_matches_for_rule(option.rule,parents[:2]+(wrong,))


def test_source_first_and_no_duplicate_candidates(monkeypatch):
    cited, db, goal = presentation(5,6,2,'cited'),presentation(5,6,2,'db'),presentation(6,6,2,'y')
    bridge = synthetic_bridge(cited,cited)
    witness = ProofStep(db,(),ProofRule.GIVEN)
    monkeypatch.setattr(provider,'admitted_prior_group_step',lambda *args,**kwargs: witness)
    monkeypatch.setattr(provider,'verified_db_step',lambda *args,**kwargs: True)
    expand = provider.build_finite_cyclic_suspension_transport_provider(bridge=bridge,proof_target=goal)
    options = expand(goal)
    assert tuple(o.subgoals[0] for o in options) == (cited,db)
    assert expand(cited) == ()
    # A duplicate DB candidate must not introduce another route.
    monkeypatch.setattr(provider,'admitted_prior_group_step',lambda *args,**kwargs: ProofStep(cited,(),ProofRule.GIVEN))
    assert len(expand(goal)) == 1


def test_no_source_or_unverified_db_means_no_candidate(monkeypatch):
    a,b = presentation(5,6,2),presentation(6,6,2,'y')
    bridge = synthetic_bridge()
    expand = provider.build_finite_cyclic_suspension_transport_provider(bridge=bridge,proof_target=b)
    monkeypatch.setattr(provider,'admitted_prior_group_step',lambda *args,**kwargs: None)
    assert expand(b) == ()
    monkeypatch.setattr(provider,'admitted_prior_group_step',lambda *args,**kwargs: ProofStep(a,(),ProofRule.GIVEN))
    monkeypatch.setattr(provider,'verified_db_step',lambda *args,**kwargs: False)
    assert expand(b) == ()


def test_root_scope_rejects_invalid_goals_before_db_lookup(monkeypatch):
    a,b = presentation(5,6,2),presentation(6,6,2,'y')
    def unexpected(*args,**kwargs):
        pytest.fail('ineligible goal must not trigger source discovery')
    monkeypatch.setattr(provider,'admitted_prior_group_step',unexpected)
    expand = provider.build_finite_cyclic_suspension_transport_provider(bridge=synthetic_bridge(),proof_target=b)
    assert expand(a) == () and expand(b.rhs) == ()
    low = presentation(2,6,2)
    assert provider.build_finite_cyclic_suspension_transport_provider(bridge=synthetic_bridge(),proof_target=low)(low) == ()


def test_real_n6_candidate_not_publicly_installed():
    root, lower = exact_prior_database_result(6,6), exact_prior_database_result(5,6)
    assert root.lhs == TodaPrimaryGroup(12,6) and lower.lhs == TodaPrimaryGroup(11,5)
    assert type(root.rhs.generator) is Composition and type(lower.rhs.generator) is Composition
    assert root.rhs.order == lower.rhs.order == 2
    bridge = screen_independent_sources_for_derived_goal(build_shared_typed_bridge(),goal=root)
    original_links = tuple(bridge.proof_links)
    original_assertions = tuple(bridge.registry._assertions.items())
    expand = provider.build_finite_cyclic_suspension_transport_provider(bridge=bridge,proof_target=root)
    options = expand(root)
    expected = provider.suspension_transport_inputs(root,lower)
    assert expected is not None
    selected, = [o for o in options if o.subgoals == expected]
    assert selected.rule.name == RULE
    assert len(selected.subgoals) == 3 and not any(isinstance(s,ProofStep) for s in selected.subgoals)
    assert all(o.rule.name != RULE for o in expand_finite_cyclic_relation(root))
    public = shared_expansion_provider(bridge,proof_target=root)(root)
    assert all(o.rule.name != RULE for o in public)
    assert tuple(bridge.proof_links) == original_links
    assert tuple(bridge.registry._assertions.items()) == original_assertions
    assert not any(link.step is not None and link.step.conclusion == root for link in bridge.proof_links)
    print('PHASE178_R19_N6_THREE_PREMISES=VERIFIED')
    for premise in selected.subgoals:
        print('PHASE178_R19_OBLIGATION='+repr(premise))
    print('PHASE178_R19_PUBLIC_PROVIDER_UNCHANGED=VERIFIED')

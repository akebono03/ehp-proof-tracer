"""Synthetic hypotheses test the conditional inference; no production proof."""
from dataclasses import replace
from math import gcd

import pytest

from expression import HomotopyElement, Multiple
from homotopy_groups import FiniteCyclicGroup, TodaDeltaMap, TodaPrimaryGroup, TodaSuspensionMap
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from phase165_r12_r5_structure_bridge import finite_cyclic_structure_as_relation_inference_rule
from phase165_r14_r6_generic_iso import GeneratorImage
from phase178_r17_finite_cyclic_quotient_isolated.rule import (
    RULE_NAME, expand_finite_cyclic_quotient, finite_cyclic_quotient_inputs,
)
from proof import InferenceRule, LiteratureReference, ProofRule, ProofStep, Relation, RelationType, apply_inference_match, find_inference_matches_for_rule
from toda_rules import TodaDeltaImageUpToSignStatement
from unified_statement_registry import AssertionEntry, AssertionKind, AssertionOrigin, LiteratureEntry, ProofStepLink, ReferenceKind, UnifiedStatementRegistry


def fixture(N=8, M=8, t=2, n=4):
    # Same EHP window geometry for arbitrary concrete dimensions.
    a, b, c = TodaPrimaryGroup(2*n+2,n), TodaPrimaryGroup(2*n+3,n+1), TodaPrimaryGroup(2*n+4,2*n+1)
    x = HomotopyElement('x', n, a.group_dimension, n)
    y = HomotopyElement('y', n+1, b.group_dimension, n+1)
    z = HomotopyElement('z', 2*n+1, c.group_dimension, 2*n+1)
    return (CyclicStructureStatement(b,y,gcd(N,t)), Relation(a,FiniteCyclicGroup(N,x)),
            Relation(c,FiniteCyclicGroup(M,z)),
            TodaDeltaImageUpToSignStatement(TodaDeltaMap(c,a),z,Multiple(t,x)),
            GeneratorImage(TodaSuspensionMap(a,b),x,y))


def cited_fixture(claim, *, copies=1):
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry('fixture',ReferenceKind.EQUATION,'synthetic',publication_position=1))
    links = []
    for i in range(copies):
        key = 'fixture:'+str(i)
        registry.add_assertion(AssertionEntry(key,'fixture',AssertionKind.STATEMENT,claim,origin=AssertionOrigin.FIXED_STATEMENT))
        step = ProofStep(claim,(),ProofRule.GIVEN,inference_rule=InferenceRule('synthetic only',literature_reference=LiteratureReference(label='synthetic',locator='synthetic')))
        links.append(ProofStepLink(key,step=step))
    return RegistryBridgeResult(registry,(),tuple(links))


def synthetic(value, kind=ProofRule.INFERENCE):
    return ProofStep(value,(),kind,inference_rule=InferenceRule('synthetic hypothesis only'))


def options_and_parents(values):
    bridge = cited_fixture(values[3])
    option, = expand_finite_cyclic_quotient(*values,bridge=bridge)
    parents = tuple(bridge.proof_links[0].step if i==2 else synthetic(value,ProofRule.GIVEN if i<2 else ProofRule.INFERENCE)
                    for i,value in enumerate(option.subgoals))
    return option, parents, bridge


@pytest.mark.parametrize('N,M,t,n',[(8,8,2,4),(16,8,4,5),(16,4,12,6),(8,4,6,7),(8,4,-2,4)])
def test_general_quotient_replays(N,M,t,n):
    values = fixture(N,M,t,n)
    option, parents, _ = options_and_parents(values)
    assert option.rule.name == RULE_NAME and len(parents)==6
    assert option.subgoals == finite_cyclic_quotient_inputs(*values)
    assert not any(isinstance(x,ProofStep) for x in option.subgoals)
    goal = values[0]
    assert goal not in option.subgoals
    relation = Relation(goal.group,FiniteCyclicGroup(gcd(N,t),goal.generator))
    assert relation not in option.subgoals
    match, = find_inference_matches_for_rule(option.rule,parents)
    step = apply_inference_match(match)
    assert step.conclusion == goal and step.rule is ProofRule.INFERENCE and step.premises == parents
    final, = find_inference_matches_for_rule(finite_cyclic_structure_as_relation_inference_rule(),(step,))
    assert apply_inference_match(final).conclusion == relation


@pytest.mark.parametrize('i',range(6))
def test_each_premise_required(i):
    option,parents,_ = options_and_parents(fixture())
    assert not find_inference_matches_for_rule(option.rule,parents[:i]+parents[i+1:])


@pytest.mark.parametrize('i',[3,4,5])
def test_derived_map_and_exactness_cannot_be_given(i):
    option,parents,_ = options_and_parents(fixture())
    assert not find_inference_matches_for_rule(option.rule,parents[:i]+(synthetic(parents[i].conclusion,ProofRule.GIVEN),)+parents[i+1:])


def test_unsigned_or_incompatible_or_wrong_order_rejected():
    goal,middle,source,signed,suspension = fixture()
    for values in ((replace(goal,order=4),middle,source,signed,suspension),
                   (goal,middle,replace(source,rhs=FiniteCyclicGroup(2,source.rhs.generator)),signed,suspension),
                   (goal,middle,source,replace(signed,positive_value=Multiple(True,middle.rhs.generator)),suspension),
                   (goal,middle,source,replace(signed,positive_value=Multiple(0,middle.rhs.generator)),suspension),
                   (goal,middle,source,replace(signed,positive_value=Multiple(2,source.rhs.generator)),suspension),
                   (goal,middle,source,GeneratorImage(signed.map,signed.element,signed.positive_value),suspension),
                   (goal,middle,source,signed,replace(suspension,source_generator=source.rhs.generator)),
                   (goal,middle,source,replace(signed,map=TodaDeltaMap(source.lhs,goal.group)),suspension),
                   (replace(goal,group=TodaPrimaryGroup(12,6)),middle,source,signed,suspension),
                   (goal,replace(middle,relation_type=RelationType.ORDER),source,signed,suspension)):
        assert finite_cyclic_quotient_inputs(*values) is None


def test_screened_signed_leaf_required_and_duplicates_rejected():
    values = fixture()
    for count in (0,2):
        assert not expand_finite_cyclic_quotient(*values,bridge=cited_fixture(values[3],copies=count))
    option,parents,_ = options_and_parents(values)
    for kind in (ProofRule.GIVEN,ProofRule.INFERENCE):
        forged = synthetic(values[3],kind)
        assert not find_inference_matches_for_rule(option.rule,parents[:2]+(forged,)+parents[3:])

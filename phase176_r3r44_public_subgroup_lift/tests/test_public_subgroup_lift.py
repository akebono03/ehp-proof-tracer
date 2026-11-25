"""Candidate wiring, no proof fabrication; actual Web integration is audited separately."""
from dataclasses import replace

import pytest

from expression import Multiple
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from phase166_r3aj_structured_generator import database_structured_group_goal_candidates
from phase176_r3r43r1_finite_cyclic_subgroup_lift_isolated.rule import RULE_NAME
from phase176_r3r43r1_finite_cyclic_subgroup_lift_isolated.tests.test_finite_cyclic_subgroup_lift import fixture
from phase176_r3r44_public_subgroup_lift import provider
from phase176_r3r44_public_subgroup_lift.apply import TARGET, SETUP, DISPATCH, updated_source
from proof import ProofStep, find_inference_matches_for_rule


def test_source_candidate_keeps_five_obligations(monkeypatch):
    goal, exact, group, kernel, image = fixture()
    monkeypatch.setattr(provider,'database_structured_group_goal_candidates',lambda **kwargs: ())
    options = provider.build_public_subgroup_lift_provider((group,))(goal)
    assert len(options)==1
    option=options[0]
    assert option.rule.name==RULE_NAME
    assert option.subgoals[1:]==(exact,group,kernel,image)
    assert len(option.subgoals)==5
    assert not any(isinstance(x,ProofStep) for x in option.subgoals)
    assert not find_inference_matches_for_rule(option.rule,())


def test_db_candidate_is_open_and_deduplicated(monkeypatch):
    goal, exact, group, kernel, image = fixture()
    seen=[]
    def db(**kwargs):
        seen.append(kwargs)
        return (group,group)
    monkeypatch.setattr(provider,'database_structured_group_goal_candidates',db)
    options=provider.build_public_subgroup_lift_provider((),(group,))(goal)
    assert seen==[{'n':5,'k':3}]
    assert len(options)==1
    assert options[0].subgoals[1:]==(exact,group,kernel,image)
    assert not find_inference_matches_for_rule(options[0].rule,())
    assert len(provider.build_public_subgroup_lift_provider(())(goal))==1


@pytest.mark.parametrize('n,i,m,q',[(4,10,16,4),(5,12,32,8)])
def test_no_target_specific_dimensions(monkeypatch,n,i,m,q):
    goal, exact, group, kernel, image=fixture(n,i,m,q)
    monkeypatch.setattr(provider,'database_structured_group_goal_candidates',lambda **kwargs:(group,))
    option,=provider.build_public_subgroup_lift_provider(())(goal)
    assert option.subgoals[1:]==(exact,group,kernel,image)


def test_wrong_group_or_order_is_not_a_candidate(monkeypatch):
    goal, _, group, _, _=fixture()
    wrong=(replace(group,lhs=TodaPrimaryGroup(9,5)),
           replace(group,rhs=FiniteCyclicGroup(3,group.rhs.generator)),
           replace(group,rhs=FiniteCyclicGroup(2,group.rhs.generator)))
    monkeypatch.setattr(provider,'database_structured_group_goal_candidates',lambda **kwargs:wrong)
    expand=provider.build_public_subgroup_lift_provider(wrong)
    assert expand(goal)==()
    assert expand(group)==()


def test_actual_db_root_candidate_requires_same_typed_goal():
    root,=database_structured_group_goal_candidates(n=3,k=5)
    goal=CyclicStructureStatement(root.lhs,root.rhs.generator,root.rhs.order)
    options=provider.build_public_subgroup_lift_provider(())(goal)
    assert options
    for option in options:
        assert option.rule.name==RULE_NAME and len(option.subgoals)==5
        assert option.subgoals[2].lhs==TodaPrimaryGroup(8,5)
        assert option.subgoals[3].multiple==4
        assert option.subgoals[4].lhs.expression==goal.generator
        assert option.subgoals[4].rhs==Multiple(4,option.subgoals[2].rhs.generator)
        assert not find_inference_matches_for_rule(option.rule,())


def test_patch_minimal_and_idempotent():
    # Test the historical R44 installer on the reviewed pre-R51 shared blob.
    import subprocess
    source=subprocess.check_output(
        ['git', 'cat-file', 'blob', '937e8627f2d8d8a60ec7b36186fec5633b5604cd'],
        cwd=TARGET.parent,
    ).decode('utf-8').replace('\r\n', '\n')
    assert updated_source(source)==source
    assert source.count(SETUP)==source.count(DISPATCH)==1
    baseline=source.replace(SETUP,'',1).replace(DISPATCH,'',1)
    assert updated_source(baseline)==source
    with pytest.raises(ValueError):
        updated_source(source.replace(DISPATCH,'',1))
    with pytest.raises(ValueError):
        updated_source(source.replace('\n','\r\n'))

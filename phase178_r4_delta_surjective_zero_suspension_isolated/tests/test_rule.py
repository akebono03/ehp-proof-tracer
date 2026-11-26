"""Isolated tests. All hypothetical premises are test-only, never registered."""
from dataclasses import replace

import pytest

from homotopy_groups import (
    TodaDeltaMap, TodaEHPExactnessWindow, TodaPrimaryGroup,
    TodaPrimaryGroupZeroStatement, TodaSuspensionMap,
)
from map_facts import EHP_DELTA_MAP, EHP_E_MAP, EHP_H_MAP
from map_property_rules import ImageZeroStatement
from phase165_r14_r6_generic_iso import MapInjective, MapSurjective
from phase178_r4_delta_surjective_zero_suspension_isolated.rule import (
    RULE_NAME, delta_surjective_inputs,
    delta_surjective_from_zero_suspension_rule,
    expand_delta_surjective_from_zero_suspension,
)
from proof import (
    InferenceRule, ProofRule, ProofStep, apply_inference_match,
    find_inference_matches_for_rule,
)
from toda_rules import TodaProp42ExactnessStatement


def fixture(n=2, q=7):
    a = TodaPrimaryGroup(q+2, 2*n+1)
    b = TodaPrimaryGroup(q,n)
    c = TodaPrimaryGroup(q+1,n+1)
    goal = MapSurjective(TodaDeltaMap(a,b))
    exact = TodaProp42ExactnessStatement(TodaEHPExactnessWindow(
        a,b,c,EHP_DELTA_MAP,EHP_E_MAP,
    ))
    zero = ImageZeroStatement(TodaSuspensionMap(b,c))
    return goal, exact, zero


def hypothetical(statement, kind=ProofRule.INFERENCE):
    return ProofStep(statement, (), kind, inference_rule=InferenceRule('test-only hypothesis'))


@pytest.mark.parametrize('n,q', [(2,7),(3,6),(4,9),(5,11),(8,18)])
def test_generic_typed_candidate_and_replay(n,q):
    goal, exact, zero = fixture(n,q)
    assert delta_surjective_inputs(goal) == (exact,zero)
    option, = expand_delta_surjective_from_zero_suspension(goal)
    assert option.rule.name == RULE_NAME
    assert option.subgoals == (exact,zero)
    parents = (hypothetical(exact),hypothetical(zero))
    matches = find_inference_matches_for_rule(option.rule,parents)
    step, = tuple(apply_inference_match(m) for m in matches if m.premises == parents)
    assert step.conclusion == goal
    assert step.rule is ProofRule.INFERENCE
    assert step.premises == parents


def test_require_both_inferred_premises():
    goal, exact, zero = fixture()
    rule = delta_surjective_from_zero_suspension_rule(goal)
    e,z = hypothetical(exact),hypothetical(zero)
    for bad in ((),(e,),(z,),
                (hypothetical(exact,ProofRule.GIVEN),z),
                (e,hypothetical(zero,ProofRule.GIVEN)),
                (e,hypothetical(zero,ProofRule.RELATION))):
        assert not find_inference_matches_for_rule(rule,bad)


def test_wrong_window_or_zero_map_rejected():
    goal, exact, zero = fixture()
    rule = delta_surjective_from_zero_suspension_rule(goal)
    for bad in (replace(exact,window=replace(exact.window,second_map=EHP_H_MAP)),
                replace(exact,window=replace(exact.window,target_term=TodaPrimaryGroup(9,3))),
                fixture(3,7)[1]):
        assert not find_inference_matches_for_rule(rule,(hypothetical(bad),hypothetical(zero)))
    for bad in (fixture(3,7)[2],
                ImageZeroStatement(TodaSuspensionMap(zero.map.source_group,TodaPrimaryGroup(9,3))),
                TodaPrimaryGroupZeroStatement(zero.map.source_group),
                TodaPrimaryGroupZeroStatement(zero.map.target_group)):
        assert not find_inference_matches_for_rule(rule,(hypothetical(exact),hypothetical(bad)))


def test_invalid_goal_coordinates_and_types_rejected():
    goal, _, zero = fixture()
    for bad in (object(),MapInjective(goal.map),MapSurjective(zero.map),
                MapSurjective(replace(goal.map,source_group=TodaPrimaryGroup(9,6))),
                MapSurjective(replace(goal.map,target_group=TodaPrimaryGroup(6,2))),
                MapSurjective(TodaDeltaMap(TodaPrimaryGroup(4,5),TodaPrimaryGroup(2,True))),
                MapSurjective(TodaDeltaMap(TodaPrimaryGroup(3,7),TodaPrimaryGroup(1,3)))):
        assert delta_surjective_inputs(bad) is None
        assert not expand_delta_surjective_from_zero_suspension(bad)
        with pytest.raises(ValueError):
            delta_surjective_from_zero_suspension_rule(bad)

"""Test candidate selection without registering a source or proof."""
from expression import HomotopyElement
from homotopy_groups import DirectSumGroup, FiniteCyclicGroup, TodaPrimaryGroup
from phase171_r2j_r4_r6_middle_cardinality.source import FiniteGroupCardinality
from phase178_r6_finite_group_cardinality_isolated.rule import RULE_NAME
from phase178_r7_finite_group_cardinality_public.provider import expand_from_presentations
from proof import Relation


def test_cyclic_and_sum_candidates():
    group = TodaPrimaryGroup(11, 5)
    a = FiniteCyclicGroup(2, HomotopyElement('a',5,11,5))
    b = FiniteCyclicGroup(4, HomotopyElement('b',5,11,5))
    cyclic = Relation(group,a)
    direct = Relation(group,DirectSumGroup((a,b)))
    for claim, order in ((cyclic,2),(direct,8)):
        goal = FiniteGroupCardinality(group,order)
        lookup = lambda g: (claim,claim) if g == group else ()
        option, = expand_from_presentations(goal,lookup)
        assert option.rule.name == RULE_NAME and option.subgoals == (claim,)
        assert not expand_from_presentations(FiniteGroupCardinality(group,order+1),lookup)
        assert not expand_from_presentations(goal,lambda g: ())


def test_noncardinality_goal_does_not_request_presentations():
    def forbidden(group):
        raise AssertionError('unexpected lookup')
    assert expand_from_presentations(object(),forbidden) == ()

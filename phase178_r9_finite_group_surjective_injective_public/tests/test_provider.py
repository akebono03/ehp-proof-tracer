"""Synthetic proposals, not proof leaves or independent group searches."""
import pytest
from expression import HomotopyElement
from homotopy_groups import DirectSumGroup, FiniteCyclicGroup, FreeCyclicGroup, TodaDeltaMap, TodaHopfInvariantMap, TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import MapInjective, MapSurjective
from phase171_r2j_r4_r6_middle_cardinality.source import FiniteGroupCardinality
from phase178_r8_finite_group_surjective_injective_isolated.rule import RULE_NAME
from phase178_r9_finite_group_surjective_injective_public.provider import expand_from_presentations
from proof import Relation


def claim(group, orders):
    q, n = group.group_dimension, group.sphere_dimension
    parts = tuple(FiniteCyclicGroup(m, HomotopyElement(f'g{i}',n,q,n)) for i,m in enumerate(orders))
    return Relation(group,parts[0] if len(parts)==1 else DirectSumGroup(parts))


@pytest.mark.parametrize('mapping', [
    TodaDeltaMap(TodaPrimaryGroup(9,5),TodaPrimaryGroup(7,2)),
    TodaDeltaMap(TodaPrimaryGroup(13,9),TodaPrimaryGroup(11,4)),
    TodaSuspensionMap(TodaPrimaryGroup(9,4),TodaPrimaryGroup(10,5)),
    TodaHopfInvariantMap(TodaPrimaryGroup(11,5),TodaPrimaryGroup(11,9)),
])
def test_equal_orders_without_generator_images(mapping):
    a,b = mapping.source_group,mapping.target_group
    left,right = claim(a,(8,)),claim(b,(2,4))
    def lookup(group):
        return (left,left) if group==a else (right,right) if group==b else ()
    goal = MapInjective(mapping)
    option, = expand_from_presentations(goal,lookup)
    assert option.rule.name == RULE_NAME
    assert option.subgoals == (FiniteGroupCardinality(a,8),FiniteGroupCardinality(b,8),MapSurjective(mapping))
    assert not expand_from_presentations(goal,lambda group: (left,) if group==a else (claim(b,(4,)),))
    assert not expand_from_presentations(goal,lambda group: ())


def test_infinite_and_wrong_group_rejected():
    mapping = TodaDeltaMap(TodaPrimaryGroup(9,5),TodaPrimaryGroup(7,2))
    a,b = mapping.source_group,mapping.target_group
    left,right = claim(a,(2,)),claim(b,(2,))
    for bad in (Relation(b,FreeCyclicGroup(right.rhs.generator)),left):
        assert not expand_from_presentations(MapInjective(mapping),lambda group: (left,) if group==a else (bad,))


def test_invalid_goal_never_reads_presentations():
    def forbidden(group):
        raise AssertionError('invalid goal queried source presentations')
    invalid = TodaDeltaMap(TodaPrimaryGroup(9,6),TodaPrimaryGroup(7,2))
    for goal in (object(),MapSurjective(invalid),MapInjective(invalid)):
        assert not expand_from_presentations(goal,forbidden)

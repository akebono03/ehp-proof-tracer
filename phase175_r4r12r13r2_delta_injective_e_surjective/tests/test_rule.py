"""Focused tests of isolated R13R2 inference rules (no public installation)."""
from expression import Multiple, Sum
from homotopy_groups import (
    DirectSumGroup, FiniteCyclicGroup, FreeCyclicGroup,
    TodaDeltaMap, TodaPrimaryGroup, TodaSuspensionMap,
)
from phase165_r14_r6_generic_iso import MapInjective, MapSurjective
from phase175_r4r10_cited_58_prop25_public.source import canonical_toda58
from phase175_r4r12r13r2_delta_injective_e_surjective.rule import (
    delta_injective_inputs, expand_delta_injective_from_free_coordinate,
    e_surjective_inputs, expand_e_surjective_from_delta_injective,
)
from proof import Relation, RelationType
from toda_rules import TodaDeltaImageUpToSignStatement


def _delta_fixture():
    signed = canonical_toda58()
    free = signed.positive_value.left.expression
    torsion = signed.positive_value.right.expression
    source = Relation(
        lhs=TodaPrimaryGroup(9, 9), rhs=FreeCyclicGroup(signed.element),
        relation_type=RelationType.EQUALITY,
    )
    target = Relation(
        lhs=TodaPrimaryGroup(7, 4),
        rhs=DirectSumGroup((FreeCyclicGroup(free), FiniteCyclicGroup(4, torsion))),
        relation_type=RelationType.EQUALITY,
    )
    return MapInjective(signed.map), source, target, signed


def test_toda58_nonzero_free_coordinate_has_conditional_branch():
    goal, source, target, signed = _delta_fixture()
    assert delta_injective_inputs(goal, source, target, signed) == (source, target, signed)
    expansions = expand_delta_injective_from_free_coordinate(goal, source, target, signed)
    assert len(expansions) == 1
    assert expansions[0].subgoals == (source, target, signed)


def test_zero_free_coordinate_is_rejected():
    goal, source, target, signed = _delta_fixture()
    torsion_only = TodaDeltaImageUpToSignStatement(
        map=signed.map, element=signed.element,
        positive_value=Multiple(-1, signed.positive_value.right.expression),
    )
    assert delta_injective_inputs(goal, source, target, torsion_only) is None


def test_unlisted_generator_is_rejected():
    goal, source, target, signed = _delta_fixture()
    wrong = Relation(
        lhs=target.lhs,
        rhs=DirectSumGroup((FreeCyclicGroup(signed.element),
                            FiniteCyclicGroup(4, signed.positive_value.right.expression))),
        relation_type=RelationType.EQUALITY,
    )
    assert delta_injective_inputs(goal, source, wrong, signed) is None


def test_matching_consecutive_exactness_windows():
    goal = MapSurjective(TodaSuspensionMap(TodaPrimaryGroup(8, 4), TodaPrimaryGroup(9, 5)))
    required = e_surjective_inputs(goal)
    assert required is not None
    assert required[0] == MapInjective(TodaDeltaMap(TodaPrimaryGroup(9, 9), TodaPrimaryGroup(7, 4)))
    assert len(expand_e_surjective_from_delta_injective(goal)) == 1
    assert expand_e_surjective_from_delta_injective(goal)[0].subgoals == required


def test_invalid_suspension_dimensions_are_rejected():
    goal = MapSurjective(TodaSuspensionMap(TodaPrimaryGroup(8, 4), TodaPrimaryGroup(9, 6)))
    assert e_surjective_inputs(goal) is None
    assert expand_e_surjective_from_delta_injective(goal) == ()

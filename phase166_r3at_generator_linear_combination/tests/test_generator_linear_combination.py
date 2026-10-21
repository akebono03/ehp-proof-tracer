from pathlib import Path

from expression import Composition, Multiple, Sum
from homotopy_groups import DirectSumGroup, FiniteCyclicGroup
from phase166_r3aj_structured_generator import database_structured_group_goal_candidates
from toda_human_readable_renderer import render_toda_public_group_relation_latex


def test_pi_28_10_second_generator_is_sum_of_representatives():
    goals = database_structured_group_goal_candidates(n=10, k=18)
    assert len(goals) == 1
    structure = goals[0].rhs
    assert isinstance(structure, DirectSumGroup)
    second = structure.summands[1]
    assert isinstance(second, FiniteCyclicGroup)
    assert isinstance(second.generator, Sum)
    latex = render_toda_public_group_relation_latex(goals[0])
    assert r"\xi'' + \lambda''" in latex
    assert r"\mathbb{Z}/2\{\xi'' + \lambda''\}" in latex


def test_pi_36_11_third_generator_uses_gen_coe():
    goals = database_structured_group_goal_candidates(n=11, k=25)
    assert len(goals) == 1
    third = goals[0].rhs.summands[2].generator
    assert isinstance(third, Sum)
    assert isinstance(third.left, Composition)
    assert isinstance(third.right, Composition)


def test_unit_coefficient_keeps_single_representative():
    goals = database_structured_group_goal_candidates(n=20, k=20)
    assert len(goals) == 1
    first = goals[0].rhs.summands[0].generator
    assert not isinstance(first, (Sum, Multiple))

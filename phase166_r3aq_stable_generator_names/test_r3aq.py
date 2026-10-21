from pathlib import Path

from expression import HomotopyElement, IteratedSuspension
from phase166_r3aj_structured_generator import structured_generator_from_ids, database_structured_group_goal_candidates
from toda_human_readable_renderer import render_toda_expression_latex, render_toda_public_group_relation_latex

ROOT = Path(__file__).resolve().parent.parent
GEN = ROOT / 'data' / 'HyoujiGen.csv'


def test_bar_nu_12_is_indexed_without_suspension():
    element = structured_generator_from_ids(ids=[11], start_dimension=12, generator_csv=GEN)
    assert isinstance(element, HomotopyElement)
    assert not isinstance(element, IteratedSuspension)
    assert (element.source, element.target) == (20, 12)
    assert render_toda_expression_latex(element) == r'\bar{\nu}_{12}'


def test_epsilon_12_is_indexed_without_suspension():
    element = structured_generator_from_ids(ids=[10], start_dimension=12, generator_csv=GEN)
    assert isinstance(element, HomotopyElement)
    assert (element.source, element.target) == (20, 12)
    assert render_toda_expression_latex(element) == r'\varepsilon_{12}'


def test_pi20_12_full_goal():
    goals = database_structured_group_goal_candidates(n=12, k=8)
    assert len(goals) == 1
    rendered = render_toda_public_group_relation_latex(goals[0])
    assert r'\bar{\nu}_{12}' in rendered
    assert r'\varepsilon_{12}' in rendered
    assert 'E^{' not in rendered


def test_exceptional_nu_prime_still_suspends():
    element = structured_generator_from_ids(ids=[3], start_dimension=4, generator_csv=GEN)
    assert isinstance(element, IteratedSuspension)
    assert render_toda_expression_latex(element).startswith('E')

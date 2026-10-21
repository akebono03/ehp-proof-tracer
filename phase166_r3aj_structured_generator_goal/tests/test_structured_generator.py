from pathlib import Path

from expression import Composition, HomotopyElement
from phase166_r3aj_structured_generator import (
    database_structured_group_goal_candidates,
    structured_generator_from_ids,
)
from toda_human_readable_renderer import render_toda_expression_latex


def test_eta_squared_from_generator_ids():
    gen_path = Path(__file__).resolve().parents[2] / "data" / "HyoujiGen.csv"
    expression = structured_generator_from_ids(
        ids=[2, 2], start_dimension=13, generator_csv=gen_path
    )
    assert isinstance(expression, Composition)
    assert expression.left.source == expression.right.target
    assert render_toda_expression_latex(expression) == r"\eta_{13}\eta_{14}"


def test_group_database_generator_ids():
    candidates = database_structured_group_goal_candidates(n=13, k=2)
    assert len(candidates) == 1
    goal = candidates[0]
    assert goal.lhs.group_dimension == 15
    assert isinstance(goal.rhs.generator, Composition)


def test_missing_metadata_does_not_invent_generator(tmp_path):
    from csv import DictWriter
    path = tmp_path / "sphere.csv"
    columns = ["k", "n", "id", "orders", "generator", "Element", "gen_coe"]
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = DictWriter(stream, fieldnames=columns)
        writer.writeheader()
        writer.writerow(dict(k=2,n=13,id=0,orders=2,generator="η13^2",Element="",gen_coe=""))
    assert database_structured_group_goal_candidates(n=13,k=2,csv_path=path) == ()

from math import inf
from pathlib import Path

from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
from phase166_r3af_goal_adapter import (
    database_group_goal_candidates,
    database_zero_group_goal_candidates,
)


def test_112_groups_have_23_typed_zero_goals():
    goals = {
        (n, k): database_zero_group_goal_candidates(n=n, k=k)
        for n in range(2, 16)
        for k in range(8)
    }
    actual = {key: goal[0] for key, goal in goals.items() if goal}
    assert len(actual) == 23
    for (n, k), statement in actual.items():
        assert isinstance(statement, TodaPrimaryGroupZeroStatement)
        assert statement.group == TodaPrimaryGroup(n + k, n)
        assert not hasattr(statement, "premises")


def test_zero_goal_does_not_change_existing_nonzero_route():
    assert database_zero_group_goal_candidates(n=2, k=1) == ()
    assert database_group_goal_candidates(n=2, k=1)
    assert database_zero_group_goal_candidates(n=2, k=7) == (
        TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(9, 2)),
    )


def test_zero_group_stable_fallback():
    assert database_zero_group_goal_candidates(n=8, k=4) == (
        TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 8)),
    )


def test_mixed_or_unknown_rows_are_not_zero_goals(tmp_path: Path):
    csv_file = tmp_path / "sphere.csv"
    csv_file.write_text(
        "k,n,id,orders,generator,Element,gen_coe\n"
        "4,6,0,0,0,0,0\n"
        "4,6,1,2,η6,0,1\n",
        encoding="utf-8",
    )
    assert database_zero_group_goal_candidates(n=6, k=4, csv_path=csv_file) == ()
    assert database_zero_group_goal_candidates(n=10, k=4, csv_path=csv_file) == ()


def test_invalid_parameters_do_not_create_zero_goals():
    for n, k in ((True, 4), (2, True), (1, 0), (2, -1)):
        assert database_zero_group_goal_candidates(n=n, k=k) == ()

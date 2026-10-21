from pathlib import Path

from homotopy_groups import FiniteCyclicGroup, FreeCyclicGroup, TodaPrimaryGroup
from phase166_r3af_goal_adapter import database_group_goal_candidates


def test_nonstable_direct_csv_group_can_define_goal():
    candidates = database_group_goal_candidates(n=2, k=1)
    assert len(candidates) == 1
    assert candidates[0].lhs == TodaPrimaryGroup(3, 2)
    assert isinstance(candidates[0].rhs, FreeCyclicGroup)
    assert not hasattr(candidates[0], "premises")


def test_nonstable_finite_cyclic_direct_group():
    candidates = database_group_goal_candidates(n=3, k=1)
    assert len(candidates) == 1
    assert candidates[0].lhs == TodaPrimaryGroup(4, 3)
    assert isinstance(candidates[0].rhs, FiniteCyclicGroup)
    assert candidates[0].rhs.order == 2


def test_unsupported_nonstable_generator_stays_unconverted():
    assert database_group_goal_candidates(n=3, k=3) == ()


def test_database_goal_precedes_registry_candidates():
    from phase165_r55_nk_only_goal import registered_group_goal_candidates
    result = registered_group_goal_candidates(object(), n=3, k=1)
    assert result == database_group_goal_candidates(n=3, k=1)


def test_stable_base_fallback_still_works():
    candidates = database_group_goal_candidates(n=6, k=1)
    assert len(candidates) == 1
    assert candidates[0].lhs == TodaPrimaryGroup(7, 6)

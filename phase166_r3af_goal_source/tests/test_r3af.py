from pathlib import Path
from phase166_r3af_goal_adapter import database_group_goal_candidates
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import registered_group_goal_candidates
from homotopy_groups import TodaPrimaryGroup


def test_database_only_supplies_goals_not_evidence():
    candidates = database_group_goal_candidates(n=4, k=2)
    assert len(candidates) == 1
    assert candidates[0].lhs == TodaPrimaryGroup(6, 4)
    assert not hasattr(candidates[0], 'premises')


def test_multistem_candidate_connects_to_existing_goal_selector():
    bridge = build_shared_typed_bridge()
    for n,k in ((4,2),(5,3)):
        candidates = registered_group_goal_candidates(bridge, n=n, k=k)
        assert candidates, (n,k)
        assert all(candidate.lhs == TodaPrimaryGroup(n+k,n) for candidate in candidates)


def test_unsupported_generator_fails_closed(tmp_path):
    sample=tmp_path/'sphere.csv'
    sample.write_text('k,n,id,orders,generator,Element,gen_coe\n7,9,0,8,unknown,0,1\n', encoding='utf-8')
    assert database_group_goal_candidates(n=9,k=7,csv_path=sample)==()

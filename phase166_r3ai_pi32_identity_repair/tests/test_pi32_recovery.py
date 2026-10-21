from homotopy_groups import FreeCyclicGroup, TodaPrimaryGroup
from hopf_facts import ETA_2
from phase166_r3af_goal_adapter import database_group_goal_candidates
from phase165_r55_nk_only_goal import registered_group_goal_candidates, search_group_from_registered_goal
from phase165_r52_partial_proof import ProofSearchStatus


def test_db_pi32_goal_has_canonical_eta2_identity():
    candidates = database_group_goal_candidates(n=2, k=1)
    assert len(candidates) == 1
    assert candidates[0].lhs == TodaPrimaryGroup(3, 2)
    assert candidates[0].rhs == FreeCyclicGroup(ETA_2)


def test_selector_pi32_keeps_canonical_goal_identity():
    candidates = registered_group_goal_candidates(object(), n=2, k=1)
    assert len(candidates) == 1
    assert candidates[0].rhs.generator == ETA_2


def test_pi32_real_shared_search_completes():
    result = search_group_from_registered_goal(n=2, k=1)
    assert result.status is ProofSearchStatus.COMPLETE, (
        result.status, result.open_goals, result.diagnostics
    )
    assert result.conclusion.rhs == FreeCyclicGroup(ETA_2)

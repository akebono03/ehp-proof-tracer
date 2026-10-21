from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from web_group_proof import build_standard_web_group_proof_view

def test_zero_goal_is_searched_not_assumed():
    result = search_group_from_registered_goal(n=2, k=7)
    assert result.status is not ProofSearchStatus.NOT_SEARCHED
    zero = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(9, 2))
    if result.status is ProofSearchStatus.COMPLETE:
        assert result.conclusion == zero
        assert any(step.conclusion == zero for step in result.proven_steps)
    else:
        assert zero in result.open_goals

def test_zero_web_keeps_entire_equation():
    result = build_standard_web_group_proof_view(n=2, k=7, mode="narrative")
    assert "= 0" in result.conclusion_latex

def test_pi32_remains_complete():
    result = search_group_from_registered_goal(n=2, k=1)
    assert result.status is ProofSearchStatus.COMPLETE

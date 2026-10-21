from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
from phase165_r52_partial_proof import ProofSearchStatus, render_partial_proof_markdown
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase165_r52_r3_web_adapter import build_partial_web_group_proof_view


def test_zero_goal_is_display_only():
    result = search_group_from_registered_goal(n=2, k=7)
    assert result.status is ProofSearchStatus.NOT_SEARCHED
    assert result.open_goals == (TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(9, 2)),)
    assert result.conclusion is None
    assert not result.proven_steps


def test_zero_goal_narrative_shows_equality():
    result = search_group_from_registered_goal(n=2, k=7)
    markdown = render_partial_proof_markdown(result)
    assert markdown.count(r"\pi_{9}^{2} = 0") >= 2


def test_web_proof_target_shows_zero():
    result = search_group_from_registered_goal(n=2, k=7)
    view = build_partial_web_group_proof_view(result, mode="narrative")
    assert view.conclusion_latex == r"\pi_{9}^{2} = 0"
    assert view.partial_result


def test_pi32_still_complete():
    result = search_group_from_registered_goal(n=2, k=1)
    assert result.status is ProofSearchStatus.COMPLETE

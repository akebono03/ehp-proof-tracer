from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase165_r52_r3_web_adapter import build_partial_web_group_proof_view
from phase165_r52_partial_proof import ProofSearchStatus


def test_pi1513_proof_target_has_structure_and_eta_square():
    result = search_group_from_registered_goal(n=13, k=2)
    view = build_partial_web_group_proof_view(result, mode="narrative")
    assert r"\pi_{15}^{13}" in view.conclusion_latex
    assert r"\mathbb{Z}/2" in view.conclusion_latex
    assert r"\eta_{13}^{2}" in view.conclusion_latex


def test_pi2113_proof_target_has_both_summands():
    result = search_group_from_registered_goal(n=13, k=8)
    view = build_partial_web_group_proof_view(result, mode="narrative")
    assert r"\pi_{21}^{13}" in view.conclusion_latex
    assert r"\oplus" in view.conclusion_latex
    assert view.partial_result


def test_zero_group_proof_target_keeps_equality():
    result = search_group_from_registered_goal(n=2, k=7)
    view = build_partial_web_group_proof_view(result, mode="narrative")
    assert view.conclusion_latex == r"\pi_{9}^{2} = 0"


def test_pi32_remains_complete():
    result = search_group_from_registered_goal(n=2, k=1)
    assert result.status is ProofSearchStatus.COMPLETE
    view = build_partial_web_group_proof_view(result, mode="narrative")
    assert r"\pi_{3}^{2}" in view.conclusion_latex

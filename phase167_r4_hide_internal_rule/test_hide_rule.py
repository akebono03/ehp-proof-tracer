from pathlib import Path
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase165_r52_partial_proof import render_partial_proof_markdown


def test_r4_internal_rule_is_hidden_in_pi43():
    text = render_partial_proof_markdown(search_group_from_registered_goal(n=3, k=1))
    assert 'infinite cyclic quotient structure' not in text
    assert r'\operatorname{Im}\Delta' in text
    assert r'\ker E' in text
    assert '第一同型定理' in text


def test_r4_pi32_has_unchanged_required_sections():
    text = render_partial_proof_markdown(search_group_from_registered_goal(n=2, k=1))
    assert '使用する結果' in text and '証明' in text and '以上より' in text


def test_r4_old_completed_renderer_stays_removed():
    import phase165_r57_r10_step_narrative as old
    assert not hasattr(old, 'render_completed_from_proofsteps')

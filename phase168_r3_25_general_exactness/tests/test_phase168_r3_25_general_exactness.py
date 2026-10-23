from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown


def _render(n, k):
    bridge = build_shared_typed_bridge()
    result = search_group_from_registered_goal(n=n, k=k, bridge=bridge)
    assert result.status is ProofSearchStatus.COMPLETE
    model = build_linked_proof_narrative_model(result, bridge)
    return render_model_backed_narrative_markdown(result, model)


def test_pi32_three_overlapping_windows_make_one_sequence():
    text = _render(2, 1)
    sequence = (
        r"\pi_{2}^{1} \xrightarrow{E} \pi_{3}^{2}"
        r" \xrightarrow{H} \pi_{3}^{3}"
        r" \xrightarrow{\Delta} \pi_{1}^{1}"
        r" \xrightarrow{E} \pi_{2}^{2}"
    )
    assert sequence in text
    assert text.count(r"\xrightarrow{E}") == 2
    assert text.count(r"\xrightarrow{H}") == 1
    assert text.count(r"\xrightarrow{\Delta}") == 1
    assert text.count("次の完全列を考える") == 1
    assert "is exact" not in text


def test_pi43_two_overlapping_windows_remain_one_sequence():
    text = _render(3, 1)
    sequence = (
        r"\pi_{5}^{5} \xrightarrow{\Delta} \pi_{3}^{2}"
        r" \xrightarrow{E} \pi_{4}^{3}"
        r" \xrightarrow{H} \pi_{4}^{5}"
    )
    assert sequence in text
    assert text.count("次の完全列を考える") == 1
    assert text.count(r"\xrightarrow{\Delta}") == 1
    assert text.count(r"\xrightarrow{E}") == 1
    assert text.count(r"\xrightarrow{H}") == 1
    assert text.index(r"\pi_{3}^{2} = \mathbb{Z}\{\eta_{2}\}") < text.index("準同型定理")

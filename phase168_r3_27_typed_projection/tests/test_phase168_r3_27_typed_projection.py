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


def test_pi32_map_properties_and_generator_image():
    text = _render(2, 1)
    assert r"H: \pi_{3}^{2}\to \pi_{3}^{3}" in text
    assert "は単射" in text
    assert "は全射" in text
    assert "は同型" in text
    assert r"H(\eta_{2})=\iota_{3}" in text
    assert text.count("次の完全列を考える") == 1


def test_pi43_existing_typed_output_maintained():
    text = _render(3, 1)
    assert "準同型定理" in text
    assert r"\ker E=\mathbb{Z}\{2\eta_{2}\}" in text
    assert text.count("次の完全列を考える") == 1

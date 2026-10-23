from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown


def test_pi43_single_exactness_and_quotient_order():
    bridge = build_shared_typed_bridge()
    result = search_group_from_registered_goal(n=3, k=1, bridge=bridge)
    assert result.status is ProofSearchStatus.COMPLETE
    model = build_linked_proof_narrative_model(result, bridge)
    rendered = render_model_backed_narrative_markdown(result, model)
    assert rendered.count(r"\xrightarrow{\Delta}") == 1
    assert rendered.count(r"\xrightarrow{E}") == 1
    assert rendered.count(r"\xrightarrow{H}") == 1
    assert "is exact" not in rendered
    assert rendered.index(r"\pi_{3}^{2} = \mathbb{Z}\{\eta_{2}\}") < rendered.index("準同型定理")
    assert rendered.index("準同型定理") < rendered.index(r"\pi_{4}^{3} = \mathbb{Z}/2")
    assert rendered.strip().endswith("□")


def test_pi43_keeps_proven_image_and_kernel():
    bridge = build_shared_typed_bridge()
    result = search_group_from_registered_goal(n=3, k=1, bridge=bridge)
    model = build_linked_proof_narrative_model(result, bridge)
    rendered = render_model_backed_narrative_markdown(result, model)
    assert r"\operatorname{Im}\Delta=\mathbb{Z}\{2\eta_{2}\}" in rendered
    assert r"\ker E=\mathbb{Z}\{2\eta_{2}\}" in rendered
    assert "は全射" in rendered
    assert r"E(\eta_{2})=\eta_{3}" in rendered

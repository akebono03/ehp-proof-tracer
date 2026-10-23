from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown


def test_pi43_typed_image_kernel_onto_quotient():
    bridge = build_shared_typed_bridge()
    result = search_group_from_registered_goal(n=3, k=1, bridge=bridge)
    assert result.status is ProofSearchStatus.COMPLETE
    model = build_linked_proof_narrative_model(result, bridge)
    rendered = render_model_backed_narrative_markdown(result, model)
    for marker in (
        r"\operatorname{Im}\Delta=\mathbb{Z}\{2\eta_{2}\}",
        r"\ker E=\mathbb{Z}\{2\eta_{2}\}",
        "は全射",
        "準同型定理",
        r"E(\eta_{2})=\eta_{3}",
        r"\pi_{4}^{3} = \mathbb{Z}/2\{\eta_{3}\}",
    ):
        assert marker in rendered, (marker, rendered)
    assert rendered.index(r"\operatorname{Im}\Delta=\mathbb{Z}") < rendered.index(r"\ker E=\mathbb{Z}")
    assert rendered.index("は全射") < rendered.index("準同型定理")
    assert rendered.strip().endswith("□")


def test_pi43_references_come_from_model_only():
    bridge = build_shared_typed_bridge()
    result = search_group_from_registered_goal(n=3, k=1, bridge=bridge)
    model = build_linked_proof_narrative_model(result, bridge)
    rendered = render_model_backed_narrative_markdown(result, model)
    for citation in model.citations:
        locator = citation.reference.locator or citation.reference.label
        assert f"**[R{citation.number}] {locator}.**" in rendered

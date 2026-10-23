from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from phase165_r12_r12_ehp_consequences import EHPImageEqualsKernelStatement
from web_group_proof import build_standard_web_group_proof_view


def test_r321_pi43_exactness_is_real_proof_step():
    bridge = build_shared_typed_bridge()
    result = search_group_from_registered_goal(n=3, k=1, bridge=bridge)
    model = build_linked_proof_narrative_model(result, bridge)
    assert any(isinstance(step.conclusion, EHPImageEqualsKernelStatement) for step in model.steps)
    text = render_model_backed_narrative_markdown(result, model)
    assert r"\operatorname{Im}\Delta=\ker E" in text
    assert "完全性より" in text


def test_r321_web_pi43_exactness_visible():
    view = build_standard_web_group_proof_view(3, 1, citation_source="model")
    rendered = "\n".join(line.prefix + (line.statement_latex or "") + line.suffix for line in view.rendered_lines)
    assert r"\operatorname{Im}\Delta=\ker E" in rendered


def test_r321_pi32_still_complete():
    view = build_standard_web_group_proof_view(2, 1, citation_source="model")
    assert not view.partial_result
    assert any("Proposition 5.1" in line.prefix for line in view.rendered_lines)

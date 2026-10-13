from phase165_r14_r39_web_connection import build_phase165_pi32_web_view
from web_group_proof import build_standard_web_group_proof_view


def test_registered_pi32_web_narrative_has_goal_and_proof():
    view = build_standard_web_group_proof_view(2, 1, mode="narrative")
    assert view.key == "phase165:registered:pi3_2"
    assert view.rendered_lines
    assert view.steps[0].rule_name
    assert "pi" in view.conclusion_latex.lower()


def test_registered_pi32_web_trace_uses_proofsteps():
    view = build_standard_web_group_proof_view(2, 1, mode="trace", max_depth=2)
    assert view.steps
    assert view.mode == "trace"
    assert view.rendered_lines == ()


def test_registered_pi32_web_outline_supported():
    view = build_standard_web_group_proof_view(2, 1, mode="outline", max_depth=1)
    assert view.rendered_lines


def test_web_narrative_contains_final_equation():
    view = build_phase165_pi32_web_view()
    combined = " ".join((x.prefix + (x.statement_latex or "") + x.suffix) for x in view.rendered_lines)
    assert "eta_2" in combined
    assert "pi_3^2" in combined

import pytest
from web_group_proof import build_standard_web_group_proof_view
from web_app import create_app


@pytest.mark.parametrize("n", [4, 5])
def test_phase162_r4_b3_web_uses_derived_common_markdown(n):
    from phase162_r4_b3_web_common_display import (
        build_phase162_r4_b3_web_common_display_view,
    )
    view = build_phase162_r4_b3_web_common_display_view(n, 1, 2)
    assert view.mode == "narrative"
    assert view.rendered_lines
    all_text = "\n".join(
        line.prefix + " ".join(segment.value for segment in line.segments)
        for line in view.rendered_lines
    )
    assert "(4.5)" in all_text
    assert "Proposition 5.1" in all_text
    assert "これより, 以上より" in all_text


@pytest.mark.parametrize("n", [4, 5])
def test_phase162_r4_b3_public_web_view_uses_derived_steps(n):
    public = build_standard_web_group_proof_view(n, 1, max_depth=2, mode="narrative")
    assert public.mode == "narrative"
    assert any("concrete transported-generator normalization" in step.rule_name
               for step in public.steps)


@pytest.mark.parametrize("n", [4, 5])
def test_phase162_r4_b3_flask_web_renders_group_proof(n):
    client = create_app().test_client()
    response = client.post("/", data={
        "form_kind": "group_proof", "n": str(n), "k": "1",
        "group_proof_mode": "narrative", "group_proof_depth": "2",
    })
    assert response.status_code == 200
    assert b"(4.5)" in response.data

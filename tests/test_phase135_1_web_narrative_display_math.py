from web_app import create_app
from web_group_proof import (
  build_standard_web_group_proof_view,
)


def _build_test_client():
  app = create_app()
  app.config.update(
    TESTING=True,
  )
  return app.test_client()


def test_phase135_1_pi6_3_narrative_display_math_is_structured_for_web(
):
  view = (
    build_standard_web_group_proof_view(
      3,
      3,
      max_depth=1,
      mode="narrative",
    )
  )

  latex_values = tuple(
    line.statement_latex
    for line in view.rendered_lines
    if line.statement_latex is not None
  )

  assert (
    r"\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}"
    in latex_values
  )

  assert (
    r"\nu'\in\pi_{6}^{3}.\tag{3}"
    in latex_values
  )

  assert not any(
    line.prefix in (
      r"\[",
      r"\]",
    )
    for line in view.rendered_lines
  )

def test_phase135_1_pi6_3_web_html_uses_data_latex_for_narrative_display_math(
):
  client = _build_test_client()

  response = client.post(
    "/",
    data={
      "form_kind": "group_proof",
      "n": "3",
      "k": "3",
      "group_proof_depth": "1",
      "group_proof_mode": "narrative",
    },
  )

  assert response.status_code == 200

  assert (
    b"group-proof-rendered-math"
    in response.data
  )

  assert (
    b'data-proof-mode="narrative"'
    in response.data
  )

  assert (
    rb"\pi_{6}^{3}"
    in response.data
  )

def test_phase135_1_existing_inline_math_adapter_is_preserved(
):
  view = (
    build_standard_web_group_proof_view(
      3,
      3,
      max_depth=1,
      mode="narrative",
    )
  )

  assert any(
    line.statement_latex == r"\nu'"
    and "の位数を決定するために," in line.suffix
    for line in view.rendered_lines
  )

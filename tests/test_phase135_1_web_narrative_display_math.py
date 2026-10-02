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
    (
      r"\pi_{5}^{2} \xrightarrow{E} "
      r"\pi_{6}^{3} \xrightarrow{H} "
      r"\pi_{6}^{5}"
    )
    in latex_values
  )

  assert not any(
    line.prefix in (
      r"\[",
      r"\]",
    )
    for line in view.rendered_lines
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
    and "の位数を決定する." in line.suffix
    for line in view.rendered_lines
  )

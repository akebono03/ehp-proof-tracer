import pytest

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


def test_phase132_9_narrative_is_default_web_group_proof_mode():
  view = (
    build_standard_web_group_proof_view(
      9,
      7,
    )
  )

  assert view.mode == "narrative"
  assert view.max_depth == 2
  assert view.rendered_lines
  assert view.steps


@pytest.mark.parametrize(
  "mode",
  (
    "trace",
    "outline",
    "narrative",
  ),
)
def test_phase132_9_web_group_proof_accepts_all_modes(
  mode,
):
  view = (
    build_standard_web_group_proof_view(
      9,
      7,
      max_depth=2,
      mode=mode,
    )
  )

  assert view.mode == mode
  assert view.max_depth == 2

  if mode == "trace":
    assert view.rendered_lines == ()
  else:
    assert view.rendered_lines


def test_phase132_9_outline_web_adapter_preserves_math():
  view = (
    build_standard_web_group_proof_view(
      9,
      7,
      max_depth=1,
      mode="outline",
    )
  )

  latex_values = tuple(
    line.statement_latex
    for line in view.rendered_lines
    if line.statement_latex is not None
  )

  assert (
    r"\pi_{16}^{9} = "
    r"\mathbb{Z}/16\{\sigma_{9}\}"
    in latex_values
  )


def test_phase132_9_narrative_web_adapter_preserves_math():
  view = (
    build_standard_web_group_proof_view(
      9,
      7,
      max_depth=2,
      mode="narrative",
    )
  )

  latex_values = tuple(
    line.statement_latex
    for line in view.rendered_lines
    if line.statement_latex is not None
  )

  assert (
    r"\pi_{16}^{9} = "
    r"\mathbb{Z}/16\{\sigma_{9}\}"
    in latex_values
  )

  assert (
    view.theorem
    == "Toda Proposition 5.15"
  )


def test_phase132_9_invalid_web_mode_is_rejected():
  with pytest.raises(
    ValueError,
    match=(
      "mode must be trace, outline, or narrative"
    ),
  ):
    build_standard_web_group_proof_view(
      9,
      7,
      mode="unknown",
    )


@pytest.mark.parametrize(
  "mode",
  (
    "trace",
    "outline",
    "narrative",
  ),
)
def test_phase132_9_web_depth_semantics_are_shared_across_modes(
  mode,
):
  view = (
    build_standard_web_group_proof_view(
      9,
      7,
      max_depth=0,
      mode=mode,
    )
  )

  assert view.max_depth == 0

  if mode == "trace":
    assert len(
      view.steps
    ) == 1
  else:
    assert view.rendered_lines



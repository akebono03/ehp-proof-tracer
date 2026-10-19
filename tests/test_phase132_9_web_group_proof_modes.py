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





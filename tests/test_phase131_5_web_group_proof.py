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
  "depth",
  (
    0,
    1,
    2,
  ),
)
def test_phase131_5_group_proof_view_accepts_web_depths(
  depth,
):
  view = (
    build_standard_web_group_proof_view(
      9,
      7,
      max_depth=depth,
    )
  )

  assert view.max_depth == depth
  assert all(
    step.depth <= depth
    for step in view.steps
  )









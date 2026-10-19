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


def test_phase131_5_sigma9_group_proof_view_uses_group_result_replay():
  view = (
    build_standard_web_group_proof_view(
      9,
      7,
    )
  )

  assert (
    view.conclusion_latex
    == (
      r"\pi_{16}^{9} = "
      r"\mathbb{Z}/16\{\sigma_{9}\}"
    )
  )
  assert view.theorem == "Toda Proposition 5.15"
  assert view.phase == "75"
  assert view.max_depth == 2
  assert view.mode == "narrative"
  assert (
    view.steps[
      0
    ].depth
    == 0
  )


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


def test_phase131_5_zero_group_is_replayed_without_generator_input():
  view = (
    build_standard_web_group_proof_view(
      2,
      7,
    )
  )

  assert view.conclusion_latex == r"\pi_{9}^{2} = 0"
  assert view.theorem == "Toda Proposition 5.15"


def test_phase131_5_connectivity_zero_is_replayed():
  view = (
    build_standard_web_group_proof_view(
      11,
      -1,
    )
  )

  assert view.conclusion_latex == r"\pi_{10}^{11} = 0"
  assert view.theorem == "Sphere connectivity"
  assert view.phase == "130"
  assert len(
    view.steps
  ) == 1


def test_phase131_5_domain_only_result_is_rejected():
  with pytest.raises(
    ValueError,
    match=(
      "group proof is available only for "
      "repository-backed group results"
    ),
  ):
    build_standard_web_group_proof_view(
      3,
      -3,
    )



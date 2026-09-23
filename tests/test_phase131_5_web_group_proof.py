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
  assert view.max_depth == 1
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


def test_phase131_5_group_result_shows_proof_button():
  client = _build_test_client()

  response = client.post(
    "/",
    data={
      "form_kind": "group",
      "n": "9",
      "k": "7",
    },
  )

  assert response.status_code == 200
  assert b'id="result-math"' in response.data
  assert b'value="group_proof"' in response.data
  assert b"Show proof" in response.data
  assert b'name="group_proof_depth"' in response.data


def test_phase131_5_group_proof_post_keeps_result_and_shows_proof():
  client = _build_test_client()

  response = client.post(
    "/",
    data={
      "form_kind": "group_proof",
      "n": "9",
      "k": "7",
      "group_proof_depth": "2",
    },
  )

  assert response.status_code == 200
  assert b'id="result-math"' in response.data
  assert b'id="group-proof-conclusion"' in response.data
  assert b"Selected depth:" in response.data
  assert b"Depth 2" in response.data
  assert b"Toda Proposition 5.15" in response.data
  assert b"Phase 75" in response.data


def test_phase131_5_domain_only_result_has_no_proof_button():
  client = _build_test_client()

  response = client.post(
    "/",
    data={
      "form_kind": "group",
      "n": "3",
      "k": "-3",
    },
  )

  assert response.status_code == 200
  assert b'value="group_proof"' not in response.data


def test_phase131_5_group_proof_depth_validation_is_explicit():
  client = _build_test_client()

  response = client.post(
    "/",
    data={
      "form_kind": "group_proof",
      "n": "9",
      "k": "7",
      "group_proof_depth": "3",
    },
  )

  assert response.status_code == 200
  assert (
    b"group_proof_depth must be 0, 1, or 2"
    in response.data
  )

from pathlib import Path

import pytest

from web_app import (
  create_app,
)
from web_operation_query_proof import (
  build_standard_web_operation_query_proof_view,
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
def test_phase118_4_web_adapter_accepts_depth_zero_one_two(
  depth,
):
  view = (
    build_standard_web_operation_query_proof_view(
      "H(nu_prime)",
      fact_number=2,
      max_depth=depth,
    )
  )

  assert (
    view.max_depth
    == depth
  )

  assert all(
    step.depth <= depth
    for step in view.steps
  )


def test_phase118_4_depth_zero_contains_only_root():
  view = (
    build_standard_web_operation_query_proof_view(
      "H(nu_prime)",
      fact_number=2,
      max_depth=0,
    )
  )

  assert len(
    view.steps
  ) == 1

  assert (
    view.steps[
      0
    ].depth
    == 0
  )


def test_phase118_4_depth_two_reaches_deeper_than_default_where_available():
  default_view = (
    build_standard_web_operation_query_proof_view(
      "H(nu_prime)",
      fact_number=2,
      max_depth=1,
    )
  )

  depth_two_view = (
    build_standard_web_operation_query_proof_view(
      "H(nu_prime)",
      fact_number=2,
      max_depth=2,
    )
  )

  assert len(
    depth_two_view.steps
  ) >= len(
    default_view.steps
  )

  assert any(
    step.depth == 2
    for step in depth_two_view.steps
  )


def test_phase118_4_negative_depth_is_rejected_by_web_adapter():
  with pytest.raises(
    ValueError,
    match="max_depth must be nonnegative",
  ):
    build_standard_web_operation_query_proof_view(
      "H(nu_prime)",
      fact_number=1,
      max_depth=-1,
    )


@pytest.mark.parametrize(
  "depth",
  (
    "0",
    "1",
    "2",
  ),
)
def test_phase118_4_web_forwards_selected_depth(
  depth,
):
  client = _build_test_client()

  response = client.post(
    "/",
    data={
      "form_kind": "operation_proof",
      "operation_query": "H(nu_prime)",
      "fact_number": "2",
      "proof_depth": depth,
    },
  )

  assert response.status_code == 200
  assert (
    f"Selected depth:\n          {depth}".encode()
    in response.data
  )


def test_phase118_4_multiple_facts_remain_explicit_at_depth_ui_boundary():
  client = _build_test_client()

  response = client.post(
    "/",
    data={
      "form_kind": "operation",
      "operation_query": "H(nu_prime)",
    },
  )

  assert response.status_code == 200

  assert (
    response.data.count(
      b'value="operation_proof"'
    )
    == 2
  )

  assert (
    response.data.count(
      b'name="proof_depth"'
    )
    == 2
  )


def test_phase118_4_katex_smoke_targets_all_data_latex_elements():
  script = Path(
    "static/web_math.js"
  ).read_text(
    encoding="utf-8"
  )

  assert (
    'querySelectorAll(\n        "[data-latex]"'
    in script
  )

  assert (
    "throwOnError: false"
    in script
  )

  assert (
    "displayMode: displayMode"
    in script
  )

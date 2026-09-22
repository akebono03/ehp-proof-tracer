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


def test_phase118_4_browser_form_exposes_only_supported_depth_choices():
  client = _build_test_client()

  response = client.post(
    "/",
    data={
      "form_kind": "operation",
      "operation_query": "H(nu_prime)",
    },
  )

  assert response.status_code == 200
  assert b'name="proof_depth"' in response.data
  assert b'<option value="0">0</option>' in response.data
  assert b'<option value="1" selected>1</option>' in response.data
  assert b'<option value="2">2</option>' in response.data


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


def test_phase118_4_unsupported_web_depth_is_safe_error():
  client = _build_test_client()

  response = client.post(
    "/",
    data={
      "form_kind": "operation_proof",
      "operation_query": "H(nu_prime)",
      "fact_number": "1",
      "proof_depth": "3",
    },
  )

  assert response.status_code == 200
  assert (
    b"proof_depth must be 0, 1, or 2"
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


def test_phase118_4_safe_fallback_reaches_web_without_python_repr():
  client = _build_test_client()

  response = client.post(
    "/",
    data={
      "form_kind": "operation_proof",
      "operation_query": "eta_2 o nu_prime",
      "fact_number": "4",
      "proof_depth": "1",
    },
  )

  assert response.status_code == 200
  assert (
    b"TodaProp56FiniteDimensionalStatement"
    in response.data
  )
  assert (
    b"TodaProp56FiniteDimensionalStatement("
    not in response.data
  )
  assert (
    b"HomotopyElement(name="
    not in response.data
  )
  assert (
    b"object at 0x"
    not in response.data
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
    "displayMode: true"
    in script
  )

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


def test_phase132_9_trace_remains_default_web_group_proof_mode():
  view = (
    build_standard_web_group_proof_view(
      9,
      7,
    )
  )

  assert view.mode == "trace"
  assert view.rendered_lines == ()
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

  assert any(
    "既出の"
    in line.prefix
    for line in view.rendered_lines
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


def test_phase132_9_group_result_form_exposes_mode_selector():
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
  assert b'name="group_proof_mode"' in response.data
  assert b'value="trace"' in response.data
  assert b'value="outline"' in response.data
  assert b'value="narrative"' in response.data


def test_phase132_9_web_trace_post_preserves_existing_trace_view():
  client = _build_test_client()

  response = client.post(
    "/",
    data={
      "form_kind": "group_proof",
      "n": "9",
      "k": "7",
      "group_proof_depth": "1",
      "group_proof_mode": "trace",
    },
  )

  assert response.status_code == 200
  assert b"Selected view:" in response.data
  assert b"trace" in response.data
  assert b"Depth 0" in response.data
  assert b"Depth 1" in response.data
  assert b'id="group-proof-rendered-lines"' not in response.data


def test_phase132_9_web_outline_post_uses_structured_rendered_lines():
  client = _build_test_client()

  response = client.post(
    "/",
    data={
      "form_kind": "group_proof",
      "n": "9",
      "k": "7",
      "group_proof_depth": "1",
      "group_proof_mode": "outline",
    },
  )

  assert response.status_code == 200
  assert b'data-proof-mode="outline"' in response.data
  assert b"group-proof-rendered-line" in response.data
  assert b"group-proof-rendered-math" in response.data
  assert b"Premise 1:" in response.data
  assert b"Depth 0" not in response.data


def test_phase132_9_web_narrative_post_uses_structured_rendered_lines():
  client = _build_test_client()

  response = client.post(
    "/",
    data={
      "form_kind": "group_proof",
      "n": "9",
      "k": "7",
      "group_proof_depth": "2",
      "group_proof_mode": "narrative",
    },
  )

  assert response.status_code == 200
  assert b'data-proof-mode="narrative"' in response.data
  assert b"group-proof-rendered-math" in response.data
  assert "既出の".encode(
    "utf-8"
  ) in response.data


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


def test_phase132_9_web_post_rejects_unknown_mode_explicitly():
  client = _build_test_client()

  response = client.post(
    "/",
    data={
      "form_kind": "group_proof",
      "n": "9",
      "k": "7",
      "group_proof_depth": "1",
      "group_proof_mode": "unknown",
    },
  )

  assert response.status_code == 200
  assert (
    b"mode must be trace, outline, or narrative"
    in response.data
  )

import web_group_proof as web_group_proof_module
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


def _rendered_segment_values(
  view,
  kind,
):
  return tuple(
    segment.value
    for line in view.rendered_lines
    for segment in line.segments
    if segment.kind == kind
  )


def _rendered_text(
  view,
):
  return "\n".join(
    segment.value
    for line in view.rendered_lines
    for segment in line.segments
    if segment.kind in (
      "text",
      "strong",
    )
  )


def test_phase144_6_r25_22_web_depth2_narrative_uses_complete_replay(
  monkeypatch,
):
  original = (
    web_group_proof_module
    .build_complete_toda_group_result_proof_replay
  )
  calls = []

  def recording_complete_replay(
    group_result,
  ):
    calls.append(
      group_result
    )
    return original(
      group_result
    )

  monkeypatch.setattr(
    web_group_proof_module,
    "build_complete_toda_group_result_proof_replay",
    recording_complete_replay,
  )

  view = (
    build_standard_web_group_proof_view(
      3,
      3,
      max_depth=2,
      mode="narrative",
    )
  )

  assert len(calls) == 1
  assert view.max_depth == 2
  assert all(
    step.depth <= 2
    for step in view.steps
  )


def test_phase144_6_r25_22_web_depth2_narrative_preserves_numbered_equations():
  view = (
    build_standard_web_group_proof_view(
      3,
      3,
      max_depth=2,
      mode="narrative",
    )
  )

  display_math = (
    _rendered_segment_values(
      view,
      "display_math",
    )
  )

  assert any(
    r"\tag{1}" in value
    for value in display_math
  )
  assert any(
    r"\tag{2}" in value
    for value in display_math
  )
  assert any(
    r"\tag{3}" in value
    for value in display_math
  )


def test_phase144_6_r25_22_web_depth2_narrative_preserves_dependency_references():
  view = (
    build_standard_web_group_proof_view(
      3,
      3,
      max_depth=2,
      mode="narrative",
    )
  )

  text = _rendered_text(
    view
  )

  assert "(1) と (2) より、" in text
  assert "(4) と (5) より、" in text


def test_phase144_6_r25_22_web_response_exposes_numbered_narrative_latex():
  client = _build_test_client()

  response = client.post(
    "/",
    data={
      "form_kind": "group_proof",
      "n": "3",
      "k": "3",
      "group_proof_depth": "2",
      "group_proof_mode": "narrative",
    },
  )

  assert response.status_code == 200
  assert b"Selected depth:" in response.data
  assert b"Depth 2" in response.data
  assert b"\\\\tag{1}" in response.data
  assert b"\\\\tag{2}" in response.data
  assert b"\\\\tag{3}" in response.data
  assert "(1)".encode("utf-8") in response.data
  assert "(2)".encode("utf-8") in response.data


def test_phase144_6_r25_22_trace_does_not_use_complete_replay(
  monkeypatch,
):
  def forbidden_complete_replay(
    group_result,
  ):
    raise AssertionError(
      "Trace must preserve explicit depth replay semantics."
    )

  monkeypatch.setattr(
    web_group_proof_module,
    "build_complete_toda_group_result_proof_replay",
    forbidden_complete_replay,
  )

  view = (
    build_standard_web_group_proof_view(
      3,
      3,
      max_depth=2,
      mode="trace",
    )
  )

  assert view.max_depth == 2
  assert all(
    step.depth <= 2
    for step in view.steps
  )


def test_phase144_6_r25_22_outline_does_not_use_complete_replay(
  monkeypatch,
):
  def forbidden_complete_replay(
    group_result,
  ):
    raise AssertionError(
      "Outline must preserve explicit depth replay semantics."
    )

  monkeypatch.setattr(
    web_group_proof_module,
    "build_complete_toda_group_result_proof_replay",
    forbidden_complete_replay,
  )

  view = (
    build_standard_web_group_proof_view(
      3,
      3,
      max_depth=2,
      mode="outline",
    )
  )

  assert view.max_depth == 2
  assert all(
    step.depth <= 2
    for step in view.steps
  )

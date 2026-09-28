from web_app import create_app
from web_group_proof import (
  _build_group_proof_inline_segments,
  build_standard_web_group_proof_view,
)


def _build_test_client():
  app = create_app()
  app.config.update(
    TESTING=True,
  )
  return app.test_client()


def _segments(
  view,
):
  return tuple(
    segment
    for line in view.rendered_lines
    for segment in line.segments
  )


def _text_values(
  view,
):
  return tuple(
    segment.value
    for segment in _segments(
      view
    )
    if segment.kind in (
      "text",
      "strong",
    )
  )


def test_phase144_6_r25_22_r2_promotes_tagged_inline_math_to_display_math():
  segments = (
    _build_group_proof_inline_segments(
      r"$2\nu' = \eta_{3}^{3}\tag{3}$"
    )
  )

  assert tuple(
    (
      segment.kind,
      segment.value,
    )
    for segment in segments
  ) == (
    (
      "display_math",
      r"2\nu' = \eta_{3}^{3}\tag{3}",
    ),
  )


def test_phase144_6_r25_22_r2_keeps_ordinary_inline_math_inline():
  segments = (
    _build_group_proof_inline_segments(
      r"まず、$\nu'$ を定める."
    )
  )

  assert tuple(
    segment.kind
    for segment in segments
  ) == (
    "text",
    "inline_math",
    "text",
  )


def test_phase144_6_r25_22_r2_web_depth2_narrative_exposes_numbered_display_math():
  view = (
    build_standard_web_group_proof_view(
      3,
      3,
      max_depth=2,
      mode="narrative",
    )
  )

  display_math = tuple(
    segment.value
    for segment in _segments(
      view
    )
    if segment.kind == "display_math"
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


def test_phase144_6_r25_22_r2_web_depth2_narrative_keeps_dependency_reference():
  view = (
    build_standard_web_group_proof_view(
      3,
      3,
      max_depth=2,
      mode="narrative",
    )
  )

  text = "\n".join(
    _text_values(
      view
    )
  )

  assert "(1) と (2) より、" in text


def test_phase144_6_r25_22_r2_web_response_contains_display_numbered_equation():
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
  compact = (
    response.data
    .replace(
      b"\n",
      b"",
    )
    .replace(
      b" ",
      b"",
    )
  )
  assert b"Selecteddepth:2</p>" in compact
  assert (
    b"group-proof-rendered-display-math"
    in response.data
  )
  assert rb"\tag{1}" in response.data
  assert rb"\tag{2}" in response.data
  assert rb"\tag{3}" in response.data
  assert "(1)".encode(
    "utf-8"
  ) in response.data
  assert "(2)".encode(
    "utf-8"
  ) in response.data

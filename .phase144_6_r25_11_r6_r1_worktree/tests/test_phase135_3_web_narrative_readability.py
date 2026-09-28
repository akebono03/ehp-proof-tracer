from pathlib import Path

from web_app import create_app


ROOT = Path(
  __file__
).resolve().parents[
  1
]


def _build_test_client():
  app = create_app()
  app.config.update(
    TESTING=True,
  )
  return app.test_client()


def test_phase135_3_inline_math_uses_inline_katex_mode():
  javascript = (
    ROOT
    / "static"
    / "web_math.js"
  ).read_text(
    encoding="utf-8"
  )

  assert (
    '"group-proof-rendered-inline-math"'
    in javascript
  )
  assert (
    "displayMode: displayMode"
    in javascript
  )
  assert (
    "!element.classList.contains"
    in javascript
  )


def test_phase135_3_group_proof_has_compact_reading_width():
  stylesheet = (
    ROOT
    / "static"
    / "web_style.css"
  ).read_text(
    encoding="utf-8"
  )

  assert (
    "#group-proof-rendered-lines"
    in stylesheet
  )
  assert (
    "max-width: 52rem;"
    in stylesheet
  )
  assert (
    "margin-left: auto;"
    in stylesheet
  )
  assert (
    "margin-right: auto;"
    in stylesheet
  )


def test_phase135_3_group_proof_reduces_display_math_vertical_spacing():
  stylesheet = (
    ROOT
    / "static"
    / "web_style.css"
  ).read_text(
    encoding="utf-8"
  )

  assert (
    "#group-proof-rendered-lines .katex-display"
    in stylesheet
  )
  assert (
    "margin-top: 0.5rem;"
    in stylesheet
  )
  assert (
    "margin-bottom: 0.5rem;"
    in stylesheet
  )


def test_phase135_3_web_page_loads_group_proof_stylesheet():
  client = _build_test_client()

  response = client.get(
    "/"
  )

  assert response.status_code == 200
  assert (
    b"/static/web_style.css"
    in response.data
  )


def test_phase135_3_narrative_keeps_inline_math_segment_class():
  client = _build_test_client()

  response = client.post(
    "/",
    data={
      "form_kind": "group_proof",
      "n": "3",
      "k": "3",
      "group_proof_depth": "1",
      "group_proof_mode": "narrative",
    },
  )

  assert response.status_code == 200
  assert (
    b"group-proof-rendered-inline-math"
    in response.data
  )
  assert (
    b'group-proof-rendered-lines'
    in response.data
  )

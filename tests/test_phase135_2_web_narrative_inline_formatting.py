from web_app import create_app
from web_group_proof import (
  _build_group_proof_rendered_lines,
)


def _build_test_client():
  app = create_app()
  app.config.update(
    TESTING=True,
  )
  return app.test_client()


def test_phase135_2_web_adapter_splits_multiple_inline_math_segments():
  rendered_lines = (
    _build_group_proof_rendered_lines(
      r"**(8)** $\nu'$ の位数は $4$ である."
    )
  )

  assert len(
    rendered_lines
  ) == 1

  line = rendered_lines[
    0
  ]

  assert tuple(
    (
      segment.kind,
      segment.value,
    )
    for segment in line.segments
  ) == (
    (
      "strong",
      "(8)",
    ),
    (
      "text",
      " ",
    ),
    (
      "inline_math",
      r"\nu'",
    ),
    (
      "text",
      " の位数は ",
    ),
    (
      "inline_math",
      "4",
    ),
    (
      "text",
      " である.",
    ),
  )


def test_phase135_2_web_adapter_preserves_reference_emphasis():
  rendered_lines = (
    _build_group_proof_rendered_lines(
      "**[R1] Toda Proposition 5.6.**"
    )
  )

  assert len(
    rendered_lines
  ) == 1

  assert tuple(
    (
      segment.kind,
      segment.value,
    )
    for segment in rendered_lines[
      0
    ].segments
  ) == (
    (
      "strong",
      "[R1] Toda Proposition 5.6.",
    ),
  )


def test_phase135_2_web_adapter_keeps_display_math_separate():
  rendered_lines = (
    _build_group_proof_rendered_lines(
      "\n".join(
        (
          r"\[",
          (
            r"\pi_6^3="
            r"\mathbb Z/4\{\nu'\}, "
            r"\qquad "
            r"\nu'\in\pi_6^3"
          ),
          r"\]",
        )
      )
    )
  )

  assert len(
    rendered_lines
  ) == 1

  line = rendered_lines[
    0
  ]

  assert tuple(
    (
      segment.kind,
      segment.value,
    )
    for segment in line.segments
  ) == (
    (
      "display_math",
      (
        r"\pi_6^3="
        r"\mathbb Z/4\{\nu'\}, "
        r"\qquad "
        r"\nu'\in\pi_6^3"
      ),
    ),
  )


def test_phase135_2_web_narrative_renders_emphasis_and_inline_math():
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

  assert (
    b"group-proof-rendered-inline-math"
    in response.data
  )

  assert (
    b"<strong>"
    in response.data
  )

  assert (
    b"**"
    not in response.data
  )

from test_phase60_toda54_indeterminacy import (
  build_phase60_3_data,
)
from toda_proof_narrative_renderer import (
  render_toda_proof_statement_latex,
)


def test_phase143_75an_renders_eta_generator_semantically():
  statement = (
    build_phase60_3_data()[
      "expected_eta_indeterminacy"
    ]
  )

  rendered = render_toda_proof_statement_latex(
    statement
  )

  assert (
    rendered
    == (
      r"\operatorname{Ind}\left("
      r"\{\eta_{n}, 2\iota_{n + 1}, "
      r"\eta_{n + 1}\}_{t}"
      r"\right) = \left\langle "
      r"\eta_{n}\eta_{n + 1}\eta_{n + 2}"
      r" \right\rangle"
    )
  )


def test_phase143_75an_renders_nu_prime_generator_semantically():
  statement = (
    build_phase60_3_data()[
      "expected_final_indeterminacy"
    ]
  )

  rendered = render_toda_proof_statement_latex(
    statement
  )

  assert (
    rendered
    == (
      r"\operatorname{Ind}\left("
      r"\{\eta_{n}, 2\iota_{n + 1}, "
      r"\eta_{n + 1}\}_{t}"
      r"\right) = \left\langle "
      r"2E^{n - 3}\nu'"
      r" \right\rangle"
    )
  )


def test_phase143_75an_does_not_render_rule_names():
  data = build_phase60_3_data()

  for key in (
    "expected_eta_indeterminacy",
    "expected_final_indeterminacy",
  ):
    rendered = render_toda_proof_statement_latex(
      data[key]
    )

    assert "Toda 5.4" not in rendered
    assert "generator bridge" not in rendered
    assert "eta triple composition" not in rendered

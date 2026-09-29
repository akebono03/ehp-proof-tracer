from test_phase60_toda36_specialization import (
  build_phase60_6_data,
)
from test_phase60_toda54_bracket_statement import (
  build_phase60_2_data,
)
from test_phase60_toda54_t0_bridge import (
  build_phase60_5_data,
)
from toda_proof_narrative_renderer import (
  render_toda_proof_statement_latex,
)


def test_phase143_75w_symbolic_t_ge_1_renders_value_set():
  statement = (
    build_phase60_2_data()[
      "statement"
    ]
  )

  assert (
    render_toda_proof_statement_latex(
      statement
    )
    == (
      r"\{\eta_{n}, 2\iota_{n + 1}, "
      r"\eta_{n + 1}\}_{t}"
      r" = \{\pm E^{n - 3}\nu'\}"
    )
  )


def test_phase143_75w_t0_bridge_renders_value_set():
  statement = (
    build_phase60_5_data()[
      "expected_t0_statement"
    ]
  )

  assert (
    render_toda_proof_statement_latex(
      statement
    )
    == (
      r"\{\eta_{n}, 2\iota_{n + 1}, "
      r"\eta_{n + 1}\}"
      r" = \{\pm E^{n - 3}\nu'\}"
    )
  )


def test_phase143_75w_n5_t3_specialization_renders_value_set():
  statement = (
    build_phase60_6_data()[
      "expected_toda54"
    ]
  )

  assert (
    render_toda_proof_statement_latex(
      statement
    )
    == (
      r"\{\eta_{5}, 2\iota_{6}, "
      r"\eta_{6}\}_{3}"
      r" = \{\pm E^{2}\nu'\}"
    )
  )

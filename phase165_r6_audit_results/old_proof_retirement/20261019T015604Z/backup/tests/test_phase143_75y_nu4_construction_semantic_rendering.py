from dataclasses import replace

from test_phase60_nu4_whitehead_correction import (
  build_phase60_8_data,
)
from toda_proof_narrative_renderer import (
  render_toda_proof_statement_latex,
)


EXPECTED = (
  r"\begin{cases} "
  r"\nu_{4} = α* - (-1)^{u}s"
  r"[\iota_{4}, \iota_{4}]"
  r" & \text{if } 2Eα* = E^{2}\nu'"
  r" \\ "
  r"\nu_{4} = -α* + (-1)^{u}"
  r"\left(s + 1\right)"
  r"[\iota_{4}, \iota_{4}]"
  r" & \text{if } 2Eα* = -E^{2}\nu'"
  r" \end{cases}"
)


def test_phase143_75y_renders_piecewise_nu4_construction():
  statement = (
    build_phase60_8_data()[
      "expected_construction"
    ]
  )

  assert (
    render_toda_proof_statement_latex(
      statement
    )
    == EXPECTED
  )


def test_phase143_75y_uses_branch_parameter_offset_semantically():
  statement = (
    build_phase60_8_data()[
      "expected_construction"
    ]
  )

  changed_negative = replace(
    statement.negative_branch,
    parameter_offset=2,
  )
  changed_statement = replace(
    statement,
    negative_branch=changed_negative,
  )

  rendered = (
    render_toda_proof_statement_latex(
      changed_statement
    )
  )

  assert rendered is not None
  assert (
    r"\left(s + 2\right)"
    in rendered
  )
  assert (
    r"\left(s + 1\right)"
    not in rendered
  )


def test_phase143_75y_rejects_unsupported_branch_sign():
  statement = (
    build_phase60_8_data()[
      "expected_construction"
    ]
  )

  changed_positive = replace(
    statement.positive_branch,
    alpha_star_sign=2,
  )
  changed_statement = replace(
    statement,
    positive_branch=changed_positive,
  )

  assert (
    render_toda_proof_statement_latex(
      changed_statement
    )
    is None
  )

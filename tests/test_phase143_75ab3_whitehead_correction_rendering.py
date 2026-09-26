from test_phase60_nu4_whitehead_correction import (
  build_phase60_8_data,
)
from toda_proof_narrative_renderer import (
  render_toda_proof_statement_latex,
)


def test_phase143_75ab3_renders_whitehead_correction_semantics():
  statement = (
    build_phase60_8_data()[
      "whitehead_data_step"
    ].conclusion
  )

  assert (
    render_toda_proof_statement_latex(
      statement
    )
    == (
      r"H\left([\iota_{4}, \iota_{4}]\right) = 2\iota_{7},"
      r"\quad E[\iota_{4}, \iota_{4}] = 0,"
      r"\quad u\text{ is the sign parameter}"
    )
  )


def test_phase143_75ab3_does_not_render_rule_name():
  statement = (
    build_phase60_8_data()[
      "whitehead_data_step"
    ].conclusion
  )

  rendered = (
    render_toda_proof_statement_latex(
      statement
    )
  )

  assert "Toda Lemma 5.4 Whitehead correction data" not in rendered


def test_phase143_75ab3_preserves_all_first_class_fields():
  statement = (
    build_phase60_8_data()[
      "whitehead_data_step"
    ].conclusion
  )

  rendered = (
    render_toda_proof_statement_latex(
      statement
    )
  )

  assert r"[\iota_{4}, \iota_{4}]" in rendered
  assert r"2\iota_{7}" in rendered
  assert r"E[\iota_{4}, \iota_{4}] = 0" in rendered
  assert r"u\text{ is the sign parameter}" in rendered

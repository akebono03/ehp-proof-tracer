from test_phase60_toda48_hopf_parity import (
  build_phase60_7_data,
)
from toda_proof_narrative_renderer import (
  render_toda_proof_statement_latex,
)


def test_phase143_75ac4_renders_hopf_odd_multiple_semantics():
  statement = (
    build_phase60_7_data()[
      "final_step"
    ].conclusion
  )

  assert (
    render_toda_proof_statement_latex(
      statement
    )
    == (
      r"H\left(α*\right) = "
      r"\left(2s + 1\right)\iota_{7}"
    )
  )


def test_phase143_75ac4_does_not_render_rule_name():
  statement = (
    build_phase60_7_data()[
      "final_step"
    ].conclusion
  )

  rendered = (
    render_toda_proof_statement_latex(
      statement
    )
  )

  assert (
    "Toda 4.8 Lemma 5.4 Hopf odd multiple"
    not in rendered
  )


def test_phase143_75ac4_preserves_all_first_class_fields():
  statement = (
    build_phase60_7_data()[
      "final_step"
    ].conclusion
  )

  rendered = (
    render_toda_proof_statement_latex(
      statement
    )
  )

  assert r"H\left(α*\right)" in rendered
  assert r"2s + 1" in rendered
  assert r"\iota_{7}" in rendered

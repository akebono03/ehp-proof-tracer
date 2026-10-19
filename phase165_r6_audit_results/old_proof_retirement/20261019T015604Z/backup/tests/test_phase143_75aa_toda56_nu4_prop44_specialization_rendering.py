from test_phase63_nu4_prop44_specialization import (
  build_phase63_2_data,
)
from toda_proof_narrative_renderer import (
  render_toda_proof_statement_latex,
)


def test_phase143_75aa_renders_specialization_semantics():
  statement = (
    build_phase63_2_data()[
      "specialization_step"
    ].conclusion
  )

  assert (
    render_toda_proof_statement_latex(
      statement
    )
    == (
      r"n = 4,\quad \alpha = \nu_{4},"
      r"\quad \nu_{4} \in \pi_{7}^{4},"
      r"\quad H\left(\nu_{4}\right) = \iota_{7}"
    )
  )


def test_phase143_75aa_does_not_render_rule_name():
  statement = (
    build_phase63_2_data()[
      "specialization_step"
    ].conclusion
  )

  rendered = (
    render_toda_proof_statement_latex(
      statement
    )
  )

  assert "Proposition 4.4 specialization premises" not in rendered
  assert "Toda (5.6)" not in rendered


def test_phase143_75aa_does_not_expand_lemma54_statement():
  statement = (
    build_phase63_2_data()[
      "specialization_step"
    ].conclusion
  )

  rendered = (
    render_toda_proof_statement_latex(
      statement
    )
  )

  assert r"E^{2}\nu_{4}" not in rendered
  assert r"\Delta" not in rendered
  assert rendered.count(r"\nu_{4}") == 3

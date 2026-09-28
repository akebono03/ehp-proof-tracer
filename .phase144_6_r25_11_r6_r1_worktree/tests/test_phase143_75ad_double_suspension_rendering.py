from test_phase60_toda36_specialization import (
  build_phase60_6_data,
)
from toda_proof_narrative_renderer import (
  render_toda_proof_statement_latex,
)


def test_phase143_75ad_renders_double_suspension_up_to_sign_semantics():
  statement = (
    build_phase60_6_data()[
      "final_step"
    ].conclusion
  )

  assert (
    render_toda_proof_statement_latex(
      statement
    )
    == r"2Eα* = \pm E^{2}\nu'"
  )


def test_phase143_75ad_does_not_render_rule_name():
  statement = (
    build_phase60_6_data()[
      "final_step"
    ].conclusion
  )

  rendered = (
    render_toda_proof_statement_latex(
      statement
    )
  )

  assert (
    "Toda Lemma 5.4 double suspension up to sign"
    not in rendered
  )


def test_phase143_75ad_preserves_both_first_class_fields():
  statement = (
    build_phase60_6_data()[
      "final_step"
    ].conclusion
  )

  rendered = (
    render_toda_proof_statement_latex(
      statement
    )
  )

  assert rendered.startswith("2Eα*")
  assert r"\pm" in rendered
  assert rendered.endswith(r"E^{2}\nu'")

from expression import HomotopyElement
from toda_human_readable_renderer import (
  render_toda_expression_latex,
)


def test_phase150_rc4_5b_3_r1_beta_uses_general_greek_latex_table():
  beta = HomotopyElement(
    name="β",
    dimension=3,
    source=6,
    target=3,
  )

  assert render_toda_expression_latex(beta) == r"\beta"

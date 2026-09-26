from test_phase75_514_first_short_exact import (
  build_phase75_6a_data,
)
from toda_proof_narrative_renderer import (
  render_toda_proof_statement_latex,
)


def test_phase143_75al_renders_three_groups_and_two_maps():
  statement = (
    build_phase75_6a_data()[
      "final_step"
    ].conclusion
  )

  rendered = render_toda_proof_statement_latex(
    statement
  )

  assert (
    rendered
    == (
      r"\pi_{12}^{5} "
      r"\xrightarrow{E} "
      r"\pi_{13}^{6} "
      r"\xrightarrow{H} "
      r"\pi_{13}^{11}"
    )
  )


def test_phase143_75al_does_not_invent_zero_endpoints():
  statement = (
    build_phase75_6a_data()[
      "final_step"
    ].conclusion
  )

  rendered = render_toda_proof_statement_latex(
    statement
  )

  assert not rendered.startswith("0")
  assert not rendered.endswith("0")
  assert r"\to 0" not in rendered


def test_phase143_75al_does_not_render_rule_name():
  statement = (
    build_phase75_6a_data()[
      "final_step"
    ].conclusion
  )

  rendered = render_toda_proof_statement_latex(
    statement
  )

  assert "Toda (5.14)" not in rendered
  assert "first short exact sequence" not in rendered

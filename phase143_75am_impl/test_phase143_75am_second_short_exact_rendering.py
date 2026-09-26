from test_phase75_514_second_short_exact import (
  build_phase75_7a_data,
)
from toda_proof_narrative_renderer import (
  render_toda_proof_statement_latex,
)


def test_phase143_75am_renders_three_groups_and_two_maps():
  statement = (
    build_phase75_7a_data()[
      "final_step"
    ].conclusion
  )

  rendered = render_toda_proof_statement_latex(
    statement
  )

  assert (
    rendered
    == (
      r"\pi_{13}^{6} "
      r"\xrightarrow{E} "
      r"\pi_{14}^{7} "
      r"\xrightarrow{H} "
      r"\pi_{14}^{13}"
    )
  )


def test_phase143_75am_does_not_invent_zero_endpoints():
  statement = (
    build_phase75_7a_data()[
      "final_step"
    ].conclusion
  )

  rendered = render_toda_proof_statement_latex(
    statement
  )

  assert not rendered.startswith("0")
  assert not rendered.endswith("0")
  assert r"\to 0" not in rendered


def test_phase143_75am_does_not_render_rule_name():
  statement = (
    build_phase75_7a_data()[
      "final_step"
    ].conclusion
  )

  rendered = render_toda_proof_statement_latex(
    statement
  )

  assert "Toda (5.14)" not in rendered
  assert "second short exact sequence" not in rendered

from homotopy_groups import (
  TodaPrimaryGroup,
  TodaSuspensionMap,
)
from test_phase73_pi9_3_zero import (
  build_phase73_4_data,
)
from toda_proof_narrative_renderer import (
  render_toda_proof_statement_latex,
)
from toda_rules import (
  TodaSuspensionZeroStatement,
)


def test_phase143_75ae_renders_pi8_2_zero_suspension_map():
  data = build_phase73_4_data()
  statement = data["pi8_zero_step"].conclusion

  assert (
    render_toda_proof_statement_latex(
      statement
    )
    == (
      r"E: \pi_{8}^{2} \to "
      r"\pi_{9}^{3} "
      r"\text{ is the zero map}"
    )
  )


def test_phase143_75ae_renders_pi7_2_zero_suspension_map():
  data = build_phase73_4_data()
  statement = data["pi7_zero_step"].conclusion

  assert (
    render_toda_proof_statement_latex(
      statement
    )
    == (
      r"E: \pi_{7}^{2} \to "
      r"\pi_{8}^{3} "
      r"\text{ is the zero map}"
    )
  )


def test_phase143_75ae_uses_first_class_map_fields():
  statement = TodaSuspensionZeroStatement(
    map=TodaSuspensionMap(
      source_group=TodaPrimaryGroup(
        group_dimension=12,
        sphere_dimension=6,
      ),
      target_group=TodaPrimaryGroup(
        group_dimension=13,
        sphere_dimension=7,
      ),
    )
  )

  assert (
    render_toda_proof_statement_latex(
      statement
    )
    == (
      r"E: \pi_{12}^{6} \to "
      r"\pi_{13}^{7} "
      r"\text{ is the zero map}"
    )
  )


def test_phase143_75ae_does_not_render_rule_name():
  data = build_phase73_4_data()

  for statement in (
    data["pi8_zero_step"].conclusion,
    data["pi7_zero_step"].conclusion,
  ):
    rendered = render_toda_proof_statement_latex(
      statement
    )

    assert rendered is not None
    assert "Toda Proposition" not in rendered
    assert "5.11" not in rendered

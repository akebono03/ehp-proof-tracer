from dataclasses import replace

from test_phase66_literature_aggregate import (
  build_phase66_7_data,
)
from toda_proof_narrative_renderer import (
  render_toda_proof_statement_latex,
)


def test_phase143_75t_equation58_aggregate_renders_semantically():
  statement = (
    build_phase66_7_data()[
      "integration_step"
    ].conclusion
  )

  assert (
    render_toda_proof_statement_latex(
      statement
    )
    == (
      r"\Delta\left(\iota_{9}\right)"
      r" = \pm "
      r"\left(2\nu_{4} - E\nu'\right)"
      r" = \pm "
      r"[\iota_{4}, \iota_{4}]"
    )
  )


def test_phase143_75t_equation58_aggregate_ignores_literature_text():
  statement = (
    build_phase66_7_data()[
      "integration_step"
    ].conclusion
  )

  modified = replace(
    statement,
    literature_statements=(),
  )

  assert (
    render_toda_proof_statement_latex(
      modified
    )
    == render_toda_proof_statement_latex(
      statement
    )
  )


def test_phase143_75t_inconsistent_aggregate_does_not_render():
  statement = (
    build_phase66_7_data()[
      "integration_step"
    ].conclusion
  )

  modified = replace(
    statement,
    delta_whitehead_relation=replace(
      statement.delta_whitehead_relation,
      element=(
        statement.delta_nu_relation
        .positive_value
      ),
    ),
  )

  assert (
    render_toda_proof_statement_latex(
      modified
    )
    is None
  )

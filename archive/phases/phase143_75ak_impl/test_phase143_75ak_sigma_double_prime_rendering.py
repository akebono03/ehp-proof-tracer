from test_phase75_lemma514_sigma_double_prime import (
  build_phase75_6b_data,
)
from toda_proof_narrative_renderer import (
  _render_relation_latex,
  render_toda_proof_statement_latex,
)


def test_phase143_75ak_renders_exact_first_class_relations():
  statement = (
    build_phase75_6b_data()[
      "sigma_step"
    ].conclusion
  )

  rendered = render_toda_proof_statement_latex(
    statement
  )

  expected = r", \qquad ".join(
    (
      _render_relation_latex(
        statement.iterated_suspension_relation
      ),
      _render_relation_latex(
        statement.double_relation
      ),
      _render_relation_latex(
        statement.hopf_relation
      ),
    )
  )

  assert rendered == expected


def test_phase143_75ak_renders_all_three_relations():
  statement = (
    build_phase75_6b_data()[
      "sigma_step"
    ].conclusion
  )

  rendered = render_toda_proof_statement_latex(
    statement
  )

  assert (
    _render_relation_latex(
      statement.iterated_suspension_relation
    )
    in rendered
  )
  assert (
    _render_relation_latex(
      statement.double_relation
    )
    in rendered
  )
  assert (
    _render_relation_latex(
      statement.hopf_relation
    )
    in rendered
  )


def test_phase143_75ak_does_not_render_rule_name():
  statement = (
    build_phase75_6b_data()[
      "sigma_step"
    ].conclusion
  )

  rendered = render_toda_proof_statement_latex(
    statement
  )

  assert "Toda Lemma 5.14" not in rendered
  assert "sigma double-prime branch" not in rendered

from barratt_hilton_rules import (
  HomotopyGroupMembershipStatement,
)
from expression import (
  GeneratorSymbol,
  HomotopyElement,
  Multiple,
  Suspension,
  TodaBracket,
)
from toda_proof_narrative_renderer import (
  render_toda_proof_statement_latex,
)
from toda_rules import (
  Toda36Lemma54SpecializationStatement,
  TodaBracketMembershipStatement,
)


def build_statement():
  eta_2 = HomotopyElement(
    name="η₂",
    dimension=2,
    source=3,
    target=2,
    generator=GeneratorSymbol(
      family="η",
      index=2,
    ),
  )
  iota_3 = HomotopyElement(
    name="ι_3",
    dimension=3,
    generator=GeneratorSymbol(
      family="ι",
      index=3,
    ),
  )
  alpha_star = HomotopyElement(
    name="α*",
    dimension=7,
    source=7,
    target=4,
  )
  eta_5 = HomotopyElement(
    name="η₅",
    dimension=5,
    source=6,
    target=5,
    generator=GeneratorSymbol(
      family="η",
      index=5,
    ),
  )
  iota_6 = HomotopyElement(
    name="ι_6",
    dimension=6,
    generator=GeneratorSymbol(
      family="ι",
      index=6,
    ),
  )
  eta_6 = HomotopyElement(
    name="η₆",
    dimension=6,
    source=7,
    target=6,
    generator=GeneratorSymbol(
      family="η",
      index=6,
    ),
  )

  return Toda36Lemma54SpecializationStatement(
    alpha=eta_2,
    beta=Multiple(
      coefficient=2,
      expression=iota_3,
    ),
    alpha_star=alpha_star,
    alpha_star_membership=(
      HomotopyGroupMembershipStatement(
        element=alpha_star,
        group_dimension=7,
        sphere_dimension=4,
      )
    ),
    negative_bracket_membership=(
      TodaBracketMembershipStatement(
        element=Multiple(
          coefficient=-2,
          expression=Suspension(
            expression=alpha_star,
          ),
        ),
        bracket=TodaBracket(
          first=eta_5,
          second=Multiple(
            coefficient=2,
            expression=iota_6,
          ),
          third=eta_6,
          index=3,
        ),
      )
    ),
  )


def test_phase143_75aj_renders_both_first_class_memberships():
  rendered = render_toda_proof_statement_latex(
    build_statement()
  )

  assert "α*" in rendered
  assert r"\pi_{7}^{4}" in rendered
  assert r"-2Eα*" in rendered
  assert (
    r"\{\eta_{5}, 2\iota_{6}, \eta_{6}\}_{3}"
    in rendered
  )


def test_phase143_75aj_preserves_membership_semantics():
  rendered = render_toda_proof_statement_latex(
    build_statement()
  )

  assert rendered.count(r"\in") == 2


def test_phase143_75aj_does_not_render_rule_name():
  rendered = render_toda_proof_statement_latex(
    build_statement()
  )

  assert "Toda Theorem" not in rendered
  assert "Lemma 5.4 specialization" not in rendered

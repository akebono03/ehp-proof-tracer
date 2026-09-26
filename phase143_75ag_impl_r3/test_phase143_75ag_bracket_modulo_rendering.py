from expression import (
  GeneratorSymbol,
  HomotopyElement,
  MapApplication,
  Multiple,
  TodaBracket,
)
from homotopy_groups import (
  HomotopyGroup,
)
from map_facts import (
  EHP_DELTA_MAP,
)
from toda_proof_narrative_renderer import (
  render_toda_proof_statement_latex,
)
from toda_rules import (
  TodaLemma510BracketModuloStatement,
)


def build_phase143_75ag_statement():
  nu_6 = HomotopyElement(
    name="ν_6",
    dimension=6,
    source=9,
    target=6,
    generator=GeneratorSymbol(
      family="ν",
      index=6,
    ),
  )
  eta_9 = HomotopyElement(
    name="η_9",
    dimension=9,
    source=10,
    target=9,
    generator=GeneratorSymbol(
      family="η",
      index=9,
    ),
  )
  iota_10 = HomotopyElement(
    name="ι_10",
    dimension=10,
    generator=GeneratorSymbol(
      family="ι",
      index=10,
    ),
  )
  iota_13 = HomotopyElement(
    name="ι_13",
    dimension=13,
    generator=GeneratorSymbol(
      family="ι",
      index=13,
    ),
  )

  return TodaLemma510BracketModuloStatement(
    element=MapApplication(
      map=EHP_DELTA_MAP,
      expression=iota_13,
    ),
    bracket=TodaBracket(
      first=nu_6,
      second=eta_9,
      third=Multiple(
        coefficient=2,
        expression=iota_10,
      ),
    ),
    ambient_group=HomotopyGroup(
      group_dimension=11,
      sphere_dimension=6,
    ),
    modulus=2,
  )


def test_phase143_75ag_renders_modulo_relation():
  statement = build_phase143_75ag_statement()

  assert render_toda_proof_statement_latex(
    statement
  ) == (
    r"\Delta\iota_{13}"
    r" \in "
    r"\{\nu_{6}, \eta_{9}, 2\iota_{10}\}"
    r" \pmod{2\pi_{11}^{6}}"
  )


def test_phase143_75ag_uses_first_class_modulus():
  statement = build_phase143_75ag_statement()

  statement = TodaLemma510BracketModuloStatement(
    element=statement.element,
    bracket=statement.bracket,
    ambient_group=statement.ambient_group,
    modulus=4,
  )

  rendered = render_toda_proof_statement_latex(
    statement
  )

  assert r"\pmod{4\pi_{11}^{6}}" in rendered


def test_phase143_75ag_is_not_ordinary_membership():
  rendered = render_toda_proof_statement_latex(
    build_phase143_75ag_statement()
  )

  assert r"\pmod{" in rendered


def test_phase143_75ag_does_not_render_rule_name():
  rendered = render_toda_proof_statement_latex(
    build_phase143_75ag_statement()
  )

  assert "Toda Lemma" not in rendered
  assert "5.10" not in rendered
  assert "corrected ordinary" not in rendered

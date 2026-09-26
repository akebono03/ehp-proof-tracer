from expression import (
  GeneratorSymbol,
  HomotopyElement,
  IteratedSuspension,
  ScalarSum,
  ScalarSymbol,
)
from homotopy_groups import (
  TodaPrimaryGroup,
)
from toda_proof_narrative_renderer import (
  render_toda_proof_statement_latex,
)
from toda_rules import (
  TodaLemma57TwoIota5ImageMembershipStatement,
)


def test_phase143_75ah_renders_nu_prime_specialization():
  nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
    source=6,
    target=3,
    generator=GeneratorSymbol(
      family="ν",
      decoration="′",
    ),
  )

  statement = TodaLemma57TwoIota5ImageMembershipStatement(
    element=IteratedSuspension(
      expression=nu_prime,
      exponent=2,
    ),
    source_group=TodaPrimaryGroup(
      group_dimension=8,
      sphere_dimension=5,
    ),
  )

  assert render_toda_proof_statement_latex(
    statement
  ) == (
    r"E^{2}\nu'"
    r" \in 2\iota_{5}\circ "
    r"\pi_{8}^{5}"
  )


def test_phase143_75ah_uses_first_class_element():
  alpha = HomotopyElement(
    name="α",
    dimension=6,
    source=6,
    target=3,
  )

  statement = TodaLemma57TwoIota5ImageMembershipStatement(
    element=IteratedSuspension(
      expression=alpha,
      exponent=2,
    ),
    source_group=TodaPrimaryGroup(
      group_dimension=8,
      sphere_dimension=5,
    ),
  )

  rendered = render_toda_proof_statement_latex(
    statement
  )

  assert rendered.startswith(
    "E^{2}α"
  )


def test_phase143_75ah_uses_first_class_source_group():
  i = ScalarSymbol(
    name="i",
  )

  alpha = HomotopyElement(
    name="α",
    dimension=i,
    source=i,
    target=3,
  )

  statement = TodaLemma57TwoIota5ImageMembershipStatement(
    element=IteratedSuspension(
      expression=alpha,
      exponent=2,
    ),
    source_group=TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=i,
        right=2,
      ),
      sphere_dimension=5,
    ),
  )

  rendered = render_toda_proof_statement_latex(
    statement
  )

  assert r"\pi_{i + 2}^{5}" in rendered


def test_phase143_75ah_does_not_render_rule_name():
  nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
    source=6,
    target=3,
    generator=GeneratorSymbol(
      family="ν",
      decoration="′",
    ),
  )

  statement = TodaLemma57TwoIota5ImageMembershipStatement(
    element=IteratedSuspension(
      expression=nu_prime,
      exponent=2,
    ),
    source_group=TodaPrimaryGroup(
      group_dimension=8,
      sphere_dimension=5,
    ),
  )

  rendered = render_toda_proof_statement_latex(
    statement
  )

  assert "Toda Lemma" not in rendered
  assert "nu-prime hypothesis" not in rendered

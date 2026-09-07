from expression import (
  GeneratorSymbol,
  HomotopyElement,
  IteratedSuspension,
  ScalarSum,
  ScalarSymbol,
)
from toda_rules import (
  TodaEtaFamilyDefinitionStatement,
  toda_eta_family_definition_statement,
)


def test_phase54_2_symbolic_eta_family_definition_is_representable():
  n = ScalarSymbol(
    name="n",
  )

  definition = (
    toda_eta_family_definition_statement(
      n
    )
  )

  assert isinstance(
    definition,
    TodaEtaFamilyDefinitionStatement,
  )

  assert definition.index == n


def test_phase54_2_symbolic_eta_n_has_expected_structure():
  n = ScalarSymbol(
    name="n",
  )

  definition = (
    toda_eta_family_definition_statement(
      n
    )
  )

  expected_eta_n = HomotopyElement(
    name="η_n",
    dimension=n,
    source=ScalarSum(
      left=n,
      right=1,
    ),
    target=n,
    generator=GeneratorSymbol(
      family="η",
      index=n,
    ),
  )

  assert (
    definition.element
    == expected_eta_n
  )


def test_phase54_2_symbolic_eta_n_preserves_n_index():
  n = ScalarSymbol(
    name="n",
  )

  definition = (
    toda_eta_family_definition_statement(
      n
    )
  )

  assert (
    definition
    .element
    .generator
    .family
    == "η"
  )

  assert (
    definition
    .element
    .generator
    .index
    == n
  )


def test_phase54_2_symbolic_eta_n_has_source_n_plus_1_and_target_n():
  n = ScalarSymbol(
    name="n",
  )

  definition = (
    toda_eta_family_definition_statement(
      n
    )
  )

  assert (
    definition.element.source
    == ScalarSum(
      left=n,
      right=1,
    )
  )

  assert (
    definition.element.target
    == n
  )


def test_phase54_2_symbolic_eta_definition_represents_e_n_minus_2_eta2():
  n = ScalarSymbol(
    name="n",
  )

  definition = (
    toda_eta_family_definition_statement(
      n
    )
  )

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

  assert (
    definition.iterated_suspension
    == IteratedSuspension(
      expression=eta_2,
      exponent=ScalarSum(
        left=n,
        right=-2,
      ),
    )
  )


def test_phase54_2_symbolic_eta_definition_does_not_build_higher_bridge():
  n = ScalarSymbol(
    name="n",
  )

  definition = (
    toda_eta_family_definition_statement(
      n
    )
  )

  eta_3 = HomotopyElement(
    name="η₃",
    dimension=3,
    source=4,
    target=3,
    generator=GeneratorSymbol(
      family="η",
      index=3,
    ),
  )

  higher_eta_suspension = (
    IteratedSuspension(
      expression=eta_3,
      exponent=ScalarSum(
        left=n,
        right=-3,
      ),
    )
  )

  assert (
    definition.iterated_suspension
    != higher_eta_suspension
  )


def test_phase54_2_existing_eta3_definition_remains_compatible():
  definition = (
    toda_eta_family_definition_statement(
      3
    )
  )

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

  eta_3 = HomotopyElement(
    name="η₃",
    dimension=3,
    source=4,
    target=3,
    generator=GeneratorSymbol(
      family="η",
      index=3,
    ),
  )

  assert definition.index == 3

  assert (
    definition.element
    == eta_3
  )

  assert (
    definition.iterated_suspension
    == IteratedSuspension(
      expression=eta_2,
      exponent=1,
    )
  )


def test_phase54_2_existing_eta2_definition_remains_compatible():
  definition = (
    toda_eta_family_definition_statement(
      2
    )
  )

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

  assert definition.index == 2

  assert (
    definition.element
    == eta_2
  )

  assert (
    definition.iterated_suspension
    == IteratedSuspension(
      expression=eta_2,
      exponent=0,
    )
  )




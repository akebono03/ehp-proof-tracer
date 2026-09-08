import pytest

from expression import (
  GeneratorSymbol,
  HomotopyElement,
  IteratedSuspension,
  ScalarSum,
  ScalarSymbol,
)
from toda_rules import (
  TodaNuFamilyDefinitionStatement,
  toda_nu_family_definition_statement,
)


def test_phase62_2_nu4_definition_is_statement():
  definition = (
    toda_nu_family_definition_statement(
      4
    )
  )

  assert isinstance(
    definition,
    TodaNuFamilyDefinitionStatement,
  )


def test_phase62_2_nu4_definition_preserves_index():
  definition = (
    toda_nu_family_definition_statement(
      4
    )
  )

  assert (
    definition.index
    == 4
  )


def test_phase62_2_nu4_definition_uses_canonical_nu4():
  definition = (
    toda_nu_family_definition_statement(
      4
    )
  )

  nu_4 = HomotopyElement(
    name="ν₄",
    dimension=4,
    source=7,
    target=4,
    generator=GeneratorSymbol(
      family="ν",
      index=4,
    ),
  )

  assert (
    definition.element
    == nu_4
  )

  assert (
    definition.iterated_suspension
    == IteratedSuspension(
      expression=nu_4,
      exponent=0,
    )
  )


def test_phase62_2_nu5_definition_is_e_nu4():
  definition = (
    toda_nu_family_definition_statement(
      5
    )
  )

  nu_4 = HomotopyElement(
    name="ν₄",
    dimension=4,
    source=7,
    target=4,
    generator=GeneratorSymbol(
      family="ν",
      index=4,
    ),
  )

  nu_5 = HomotopyElement(
    name="ν_5",
    dimension=5,
    source=8,
    target=5,
    generator=GeneratorSymbol(
      family="ν",
      index=5,
    ),
  )

  assert (
    definition.element
    == nu_5
  )

  assert (
    definition.iterated_suspension
    == IteratedSuspension(
      expression=nu_4,
      exponent=1,
    )
  )


def test_phase62_2_concrete_higher_nu_has_expected_typing():
  definition = (
    toda_nu_family_definition_statement(
      8
    )
  )

  assert (
    definition.element
    == HomotopyElement(
      name="ν_8",
      dimension=8,
      source=11,
      target=8,
      generator=GeneratorSymbol(
        family="ν",
        index=8,
      ),
    )
  )

  assert (
    definition.iterated_suspension.exponent
    == 4
  )


def test_phase62_2_symbolic_definition_preserves_family_shape():
  n = ScalarSymbol(
    name="n",
  )

  definition = (
    toda_nu_family_definition_statement(
      n
    )
  )

  nu_4 = HomotopyElement(
    name="ν₄",
    dimension=4,
    source=7,
    target=4,
    generator=GeneratorSymbol(
      family="ν",
      index=4,
    ),
  )

  expected_nu_n = HomotopyElement(
    name="ν_n",
    dimension=n,
    source=ScalarSum(
      left=n,
      right=3,
    ),
    target=n,
    generator=GeneratorSymbol(
      family="ν",
      index=n,
    ),
  )

  assert (
    definition.index
    == n
  )

  assert (
    definition.element
    == expected_nu_n
  )

  assert (
    definition.iterated_suspension
    == IteratedSuspension(
      expression=nu_4,
      exponent=ScalarSum(
        left=n,
        right=-4,
      ),
    )
  )


def test_phase62_2_symbolic_definition_does_not_encode_range_proof():
  n = ScalarSymbol(
    name="n",
  )

  definition = (
    toda_nu_family_definition_statement(
      n
    )
  )

  assert (
    definition.index
    == n
  )


def test_phase62_2_rejects_concrete_index_below_four():
  with pytest.raises(
    ValueError,
    match=(
      "nu family requires n >= 4"
    ),
  ):
    toda_nu_family_definition_statement(
      3
    )


def test_phase62_2_rejects_non_scalar_index():
  with pytest.raises(
    TypeError,
    match=(
      "n must be an int or ScalarSymbol"
    ),
  ):
    toda_nu_family_definition_statement(
      "5"
    )



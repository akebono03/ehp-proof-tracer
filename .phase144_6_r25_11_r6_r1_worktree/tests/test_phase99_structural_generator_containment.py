import pytest

from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
  Multiple,
  Suspension,
  TodaBracket,
)
from proof import Relation
from structural_containment import (
  contains_generator_symbol,
)
from toda_rules import (
  TodaBracketMembershipStatement,
)


def test_phase99_3_matches_generator_symbol_directly():
  nu_prime_generator = GeneratorSymbol(
    family="ν",
    decoration="′",
  )

  assert contains_generator_symbol(
    nu_prime_generator,
    nu_prime_generator,
  )


def test_phase99_3_matches_generator_inside_typed_homotopy_element():
  nu_prime_generator = GeneratorSymbol(
    family="ν",
    decoration="′",
  )

  nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
    source=6,
    target=3,
    generator=nu_prime_generator,
  )

  assert contains_generator_symbol(
    nu_prime,
    nu_prime_generator,
  )


def test_phase99_3_matches_same_generator_inside_untyped_homotopy_element():
  nu_prime_generator = GeneratorSymbol(
    family="ν",
    decoration="′",
  )

  nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
    generator=nu_prime_generator,
  )

  assert contains_generator_symbol(
    nu_prime,
    nu_prime_generator,
  )


def test_phase99_3_typed_and_untyped_elements_share_generator_search_identity():
  nu_prime_generator = GeneratorSymbol(
    family="ν",
    decoration="′",
  )

  typed_nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
    source=6,
    target=3,
    generator=nu_prime_generator,
  )

  untyped_nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
    generator=nu_prime_generator,
  )

  assert typed_nu_prime != (
    untyped_nu_prime
  )

  assert contains_generator_symbol(
    typed_nu_prime,
    nu_prime_generator,
  )

  assert contains_generator_symbol(
    untyped_nu_prime,
    nu_prime_generator,
  )


def test_phase99_3_plain_nu_does_not_match_nu_prime():
  plain_nu_generator = GeneratorSymbol(
    family="ν",
  )

  nu_prime_generator = GeneratorSymbol(
    family="ν",
    decoration="′",
  )

  plain_nu = HomotopyElement(
    name="ν",
    dimension=3,
    generator=plain_nu_generator,
  )

  assert not contains_generator_symbol(
    plain_nu,
    nu_prime_generator,
  )


def test_phase99_3_finds_generator_inside_nested_toda_bracket():
  nu_prime_generator = GeneratorSymbol(
    family="ν",
    decoration="′",
  )

  eta_3 = HomotopyElement(
    name="η₃",
    dimension=3,
    generator=GeneratorSymbol(
      family="η",
      index=3,
    ),
  )

  iota_4 = HomotopyElement(
    name="ι₄",
    dimension=4,
    generator=GeneratorSymbol(
      family="ι",
      index=4,
    ),
  )

  eta_4 = HomotopyElement(
    name="η₄",
    dimension=4,
    generator=GeneratorSymbol(
      family="η",
      index=4,
    ),
  )

  nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
    generator=nu_prime_generator,
  )

  bracket = TodaBracket(
    first=eta_3,
    second=Composition(
      left=Multiple(
        coefficient=2,
        expression=iota_4,
      ),
      right=Suspension(
        expression=nu_prime,
      ),
    ),
    third=eta_4,
    index=1,
  )

  assert contains_generator_symbol(
    bracket,
    nu_prime_generator,
  )


def test_phase99_3_finds_generator_inside_toda_bracket_membership_statement():
  nu_prime_generator = GeneratorSymbol(
    family="ν",
    decoration="′",
  )

  eta_3 = HomotopyElement(
    name="η₃",
    dimension=3,
    generator=GeneratorSymbol(
      family="η",
      index=3,
    ),
  )

  iota_4 = HomotopyElement(
    name="ι₄",
    dimension=4,
    generator=GeneratorSymbol(
      family="ι",
      index=4,
    ),
  )

  eta_4 = HomotopyElement(
    name="η₄",
    dimension=4,
    generator=GeneratorSymbol(
      family="η",
      index=4,
    ),
  )

  nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
    source=6,
    target=3,
    generator=nu_prime_generator,
  )

  membership = (
    TodaBracketMembershipStatement(
      element=nu_prime,
      bracket=TodaBracket(
        first=eta_3,
        second=Multiple(
          coefficient=2,
          expression=iota_4,
        ),
        third=eta_4,
        index=1,
      ),
    )
  )

  assert contains_generator_symbol(
    membership,
    nu_prime_generator,
  )


def test_phase99_3_finds_generator_deep_inside_relation():
  nu_prime_generator = GeneratorSymbol(
    family="ν",
    decoration="′",
  )

  eta_3 = HomotopyElement(
    name="η₃",
    dimension=3,
    generator=GeneratorSymbol(
      family="η",
      index=3,
    ),
  )

  nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
    source=6,
    target=3,
    generator=nu_prime_generator,
  )

  relation = Relation(
    lhs=eta_3,
    rhs=Composition(
      left=eta_3,
      right=Suspension(
        expression=nu_prime,
      ),
    ),
  )

  assert contains_generator_symbol(
    relation,
    nu_prime_generator,
  )


def test_phase99_3_finds_generator_inside_tuple():
  nu_prime_generator = GeneratorSymbol(
    family="ν",
    decoration="′",
  )

  eta_3 = HomotopyElement(
    name="η₃",
    dimension=3,
    generator=GeneratorSymbol(
      family="η",
      index=3,
    ),
  )

  nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
    generator=nu_prime_generator,
  )

  values = (
    eta_3,
    (
      Suspension(
        expression=nu_prime,
      ),
    ),
  )

  assert contains_generator_symbol(
    values,
    nu_prime_generator,
  )


def test_phase99_3_returns_false_when_generator_is_absent():
  eta_3 = HomotopyElement(
    name="η₃",
    dimension=3,
    generator=GeneratorSymbol(
      family="η",
      index=3,
    ),
  )

  nu_prime_generator = GeneratorSymbol(
    family="ν",
    decoration="′",
  )

  assert not contains_generator_symbol(
    eta_3,
    nu_prime_generator,
  )


def test_phase99_3_returns_false_for_non_structural_leaf():
  nu_prime_generator = GeneratorSymbol(
    family="ν",
    decoration="′",
  )

  assert not contains_generator_symbol(
    "ν′",
    nu_prime_generator,
  )

  assert not contains_generator_symbol(
    3,
    nu_prime_generator,
  )

  assert not contains_generator_symbol(
    None,
    nu_prime_generator,
  )


def test_phase99_3_rejects_non_generator_search_target():
  with pytest.raises(
    TypeError,
    match=(
      "generator must be a GeneratorSymbol"
    ),
  ):
    contains_generator_symbol(
      HomotopyElement(
        name="ν′",
        dimension=3,
      ),
      "ν′",
    )


def test_phase99_3_does_not_mutate_input_structure():
  nu_prime_generator = GeneratorSymbol(
    family="ν",
    decoration="′",
  )

  nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
    source=6,
    target=3,
    generator=nu_prime_generator,
  )

  suspended = Suspension(
    expression=nu_prime,
  )

  original_expression = (
    suspended.expression
  )

  assert contains_generator_symbol(
    suspended,
    nu_prime_generator,
  )

  assert (
    suspended.expression
    is original_expression
  )

  assert suspended.expression is (
    nu_prime
  )

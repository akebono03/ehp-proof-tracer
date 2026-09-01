from composition_facts import (
  ETA_3_E_NU_PRIME_ZERO_COMPOSITION_FACT,
  E_NU_PRIME_NU_7_ZERO_COMPOSITION_FACT,
)
from expression import (
  Composition,
  HomotopyElement,
  Suspension,
  Zero,
)
from generator_facts import (
  ETA_3_GENERATOR,
  NU_7_GENERATOR,
  NU_PRIME_GENERATOR,
)
from proof import (
  Relation,
  RelationType,
)


def test_phase27_1_eta_3_e_nu_prime_zero_composition_fact_is_zero_relation():
  fact = (
    ETA_3_E_NU_PRIME_ZERO_COMPOSITION_FACT
  )

  assert isinstance(
    fact,
    Relation,
  )

  assert fact.relation_type == (
    RelationType.ZERO
  )

  assert fact.rhs == Zero()


def test_phase27_1_eta_3_e_nu_prime_zero_composition_fact_has_composition_lhs():
  fact = (
    ETA_3_E_NU_PRIME_ZERO_COMPOSITION_FACT
  )

  assert isinstance(
    fact.lhs,
    Composition,
  )


def test_phase27_1_eta_3_e_nu_prime_zero_composition_fact_preserves_actual_generator_structure():
  fact = (
    ETA_3_E_NU_PRIME_ZERO_COMPOSITION_FACT
  )

  composition = fact.lhs

  assert isinstance(
    composition,
    Composition,
  )

  assert isinstance(
    composition.left,
    HomotopyElement,
  )

  assert composition.left.generator is (
    ETA_3_GENERATOR
  )

  assert isinstance(
    composition.right,
    Suspension,
  )

  assert isinstance(
    composition.right.expression,
    HomotopyElement,
  )

  assert (
    composition.right.expression.generator
    is NU_PRIME_GENERATOR
  )


def test_phase27_1_eta_3_e_nu_prime_zero_composition_fact_has_expected_structure():
  expected = Relation(
    lhs=Composition(
      left=HomotopyElement(
        name="η₃",
        dimension=3,
        generator=ETA_3_GENERATOR,
      ),
      right=Suspension(
        expression=HomotopyElement(
          name="ν′",
          dimension=3,
          generator=NU_PRIME_GENERATOR,
        ),
      ),
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  assert (
    ETA_3_E_NU_PRIME_ZERO_COMPOSITION_FACT
    == expected
  )


def test_phase27_1_zero_composition_fact_does_not_add_typing_implicitly():
  composition = (
    ETA_3_E_NU_PRIME_ZERO_COMPOSITION_FACT
    .lhs
  )

  assert isinstance(
    composition,
    Composition,
  )

  eta_3 = composition.left
  e_nu_prime = composition.right

  assert isinstance(
    eta_3,
    HomotopyElement,
  )

  assert isinstance(
    e_nu_prime,
    Suspension,
  )

  assert isinstance(
    e_nu_prime.expression,
    HomotopyElement,
  )

  assert eta_3.source is None
  assert eta_3.target is None

  assert (
    e_nu_prime.expression.source
    is None
  )

  assert (
    e_nu_prime.expression.target
    is None
  )

  assert e_nu_prime.source is None
  assert e_nu_prime.target is None


def test_phase27_2_e_nu_prime_nu_7_zero_composition_fact_is_zero_relation():
  fact = (
    E_NU_PRIME_NU_7_ZERO_COMPOSITION_FACT
  )

  assert isinstance(
    fact,
    Relation,
  )

  assert fact.relation_type == (
    RelationType.ZERO
  )

  assert fact.rhs == Zero()


def test_phase27_2_e_nu_prime_nu_7_zero_composition_fact_has_composition_lhs():
  fact = (
    E_NU_PRIME_NU_7_ZERO_COMPOSITION_FACT
  )

  assert isinstance(
    fact.lhs,
    Composition,
  )


def test_phase27_2_e_nu_prime_nu_7_zero_composition_fact_preserves_actual_generator_structure():
  fact = (
    E_NU_PRIME_NU_7_ZERO_COMPOSITION_FACT
  )

  composition = fact.lhs

  assert isinstance(
    composition,
    Composition,
  )

  assert isinstance(
    composition.left,
    Suspension,
  )

  assert isinstance(
    composition.left.expression,
    HomotopyElement,
  )

  assert (
    composition.left.expression.generator
    is NU_PRIME_GENERATOR
  )

  assert isinstance(
    composition.right,
    HomotopyElement,
  )

  assert composition.right.generator is (
    NU_7_GENERATOR
  )


def test_phase27_2_e_nu_prime_nu_7_zero_composition_fact_has_expected_structure():
  expected = Relation(
    lhs=Composition(
      left=Suspension(
        expression=HomotopyElement(
          name="ν′",
          dimension=3,
          generator=NU_PRIME_GENERATOR,
        ),
      ),
      right=HomotopyElement(
        name="ν₇",
        dimension=7,
        generator=NU_7_GENERATOR,
      ),
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  assert (
    E_NU_PRIME_NU_7_ZERO_COMPOSITION_FACT
    == expected
  )


def test_phase27_2_zero_composition_fact_does_not_add_typing_implicitly():
  composition = (
    E_NU_PRIME_NU_7_ZERO_COMPOSITION_FACT
    .lhs
  )

  assert isinstance(
    composition,
    Composition,
  )

  e_nu_prime = composition.left
  nu_7 = composition.right

  assert isinstance(
    e_nu_prime,
    Suspension,
  )

  assert isinstance(
    e_nu_prime.expression,
    HomotopyElement,
  )

  assert isinstance(
    nu_7,
    HomotopyElement,
  )

  assert (
    e_nu_prime.expression.source
    is None
  )

  assert (
    e_nu_prime.expression.target
    is None
  )

  assert e_nu_prime.source is None
  assert e_nu_prime.target is None

  assert nu_7.source is None
  assert nu_7.target is None





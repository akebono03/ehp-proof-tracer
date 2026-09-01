from composition_facts import (
  ETA_3_E_NU_PRIME_ZERO_COMPOSITION_FACT,
  E_NU_6_EQUALS_NU_7_FACT,
  NU_PRIME_NU_6_ZERO_COMPOSITION_FACT,
  ZERO_COMPOSITION_FACT_REPOSITORY,
  ZeroCompositionFactRepository,
)
from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
  Suspension,
  Zero,
)
from generator_facts import (
  ETA_3_GENERATOR,
  GENERATOR_FACT_REPOSITORY,
  NU_6_GENERATOR,
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
  composition = (
    ETA_3_E_NU_PRIME_ZERO_COMPOSITION_FACT
    .lhs
  )

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

  assert eta_3.source is None
  assert eta_3.target is None
  assert e_nu_prime.source is None
  assert e_nu_prime.target is None


def test_phase27_2_nu_prime_nu_6_zero_composition_fact_is_zero_relation():
  fact = (
    NU_PRIME_NU_6_ZERO_COMPOSITION_FACT
  )

  assert isinstance(
    fact,
    Relation,
  )

  assert fact.relation_type == (
    RelationType.ZERO
  )

  assert fact.rhs == Zero()


def test_phase27_2_nu_prime_nu_6_zero_composition_fact_has_composition_lhs():
  assert isinstance(
    NU_PRIME_NU_6_ZERO_COMPOSITION_FACT.lhs,
    Composition,
  )


def test_phase27_2_nu_prime_nu_6_zero_composition_fact_preserves_generator_structure():
  composition = (
    NU_PRIME_NU_6_ZERO_COMPOSITION_FACT
    .lhs
  )

  assert isinstance(
    composition.left,
    HomotopyElement,
  )

  assert composition.left.generator is (
    NU_PRIME_GENERATOR
  )

  assert isinstance(
    composition.right,
    HomotopyElement,
  )

  assert composition.right.generator is (
    NU_6_GENERATOR
  )


def test_phase27_2_nu_prime_nu_6_zero_composition_fact_has_expected_structure():
  expected = Relation(
    lhs=Composition(
      left=HomotopyElement(
        name="ν′",
        dimension=3,
        generator=NU_PRIME_GENERATOR,
      ),
      right=HomotopyElement(
        name="ν₆",
        dimension=6,
        generator=NU_6_GENERATOR,
      ),
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  assert (
    NU_PRIME_NU_6_ZERO_COMPOSITION_FACT
    == expected
  )


def test_phase27_2_nu_prime_nu_6_zero_fact_does_not_add_typing_implicitly():
  composition = (
    NU_PRIME_NU_6_ZERO_COMPOSITION_FACT
    .lhs
  )

  assert composition.left.source is None
  assert composition.left.target is None
  assert composition.right.source is None
  assert composition.right.target is None


def test_phase27_correction_e_nu_6_equals_nu_7_fact_has_expected_structure():
  expected = Relation(
    lhs=Suspension(
      expression=HomotopyElement(
        name="ν₆",
        dimension=6,
        generator=NU_6_GENERATOR,
      ),
    ),
    rhs=HomotopyElement(
      name="ν₇",
      dimension=7,
      generator=NU_7_GENERATOR,
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert E_NU_6_EQUALS_NU_7_FACT == (
    expected
  )


def test_phase27_correction_e_nu_6_equals_nu_7_is_not_zero_repository_fact():
  assert E_NU_6_EQUALS_NU_7_FACT not in (
    ZERO_COMPOSITION_FACT_REPOSITORY
    .facts
  )


def test_phase27_3_zero_composition_fact_repository_is_empty_by_default():
  repository = (
    ZeroCompositionFactRepository()
  )

  assert repository.facts == ()


def test_phase27_3_production_repository_preserves_actual_primitive_zero_composition_facts():
  assert (
    ETA_3_E_NU_PRIME_ZERO_COMPOSITION_FACT
    in ZERO_COMPOSITION_FACT_REPOSITORY.facts
  )

  assert (
    NU_PRIME_NU_6_ZERO_COMPOSITION_FACT
    in ZERO_COMPOSITION_FACT_REPOSITORY.facts
  )


def test_phase27_3_repository_lookup_returns_eta_3_e_nu_prime_fact():
  result = (
    ZERO_COMPOSITION_FACT_REPOSITORY
    .lookup(
      ETA_3_E_NU_PRIME_ZERO_COMPOSITION_FACT
      .lhs
    )
  )

  assert result is (
    ETA_3_E_NU_PRIME_ZERO_COMPOSITION_FACT
  )


def test_phase27_3_repository_lookup_returns_nu_prime_nu_6_fact():
  result = (
    ZERO_COMPOSITION_FACT_REPOSITORY
    .lookup(
      NU_PRIME_NU_6_ZERO_COMPOSITION_FACT
      .lhs
    )
  )

  assert result is (
    NU_PRIME_NU_6_ZERO_COMPOSITION_FACT
  )


def test_phase27_3_repository_lookup_returns_none_for_unknown_composition():
  unknown = Composition(
    left=HomotopyElement(
      name="η₃",
      dimension=3,
      generator=ETA_3_GENERATOR,
    ),
    right=HomotopyElement(
      name="ν₇",
      dimension=7,
      generator=NU_7_GENERATOR,
    ),
  )

  assert (
    ZERO_COMPOSITION_FACT_REPOSITORY
    .lookup(
      unknown
    )
    is None
  )


def test_phase27_3_repository_rejects_duplicate_zero_composition_fact():
  try:
    ZeroCompositionFactRepository(
      facts=(
        ETA_3_E_NU_PRIME_ZERO_COMPOSITION_FACT,
        ETA_3_E_NU_PRIME_ZERO_COMPOSITION_FACT,
      ),
    )
  except ValueError as error:
    assert str(error) == (
      "duplicate zero-composition fact"
    )
  else:
    raise AssertionError(
      "duplicate zero-composition fact "
      "was not rejected"
    )


def test_phase27_3_repository_rejects_non_zero_composition_relation():
  invalid_fact = Relation(
    lhs=Composition(
      left=HomotopyElement(
        name="a",
        dimension=1,
      ),
      right=HomotopyElement(
        name="b",
        dimension=2,
      ),
    ),
    rhs=HomotopyElement(
      name="c",
      dimension=1,
    ),
    relation_type=RelationType.EQUALITY,
  )

  try:
    ZeroCompositionFactRepository(
      facts=(
        invalid_fact,
      ),
    )
  except ValueError as error:
    assert str(error) == (
      "invalid zero-composition fact"
    )
  else:
    raise AssertionError(
      "invalid zero-composition fact "
      "was not rejected"
    )


def test_phase27_3_exact_lookup_does_not_match_typed_composition_implicitly():
  typed_eta_3 = HomotopyElement(
    name="η₃",
    dimension=3,
    source=4,
    target=3,
    generator=ETA_3_GENERATOR,
  )

  typed_nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
    source=6,
    target=3,
    generator=NU_PRIME_GENERATOR,
  )

  typed_composition = Composition(
    left=typed_eta_3,
    right=Suspension(
      expression=typed_nu_prime,
    ),
  )

  assert (
    ZERO_COMPOSITION_FACT_REPOSITORY
    .lookup(
      typed_composition
    )
    is None
  )


def test_phase27_4_typed_eta_3_e_nu_prime_matches_zero_fact_by_untyped_structure():
  eta_3 = (
    GENERATOR_FACT_REPOSITORY
    .materialize_typed_element(
      HomotopyElement(
        name="η₃",
        dimension=3,
        generator=ETA_3_GENERATOR,
      )
    )
  )

  nu_prime = (
    GENERATOR_FACT_REPOSITORY
    .materialize_typed_element(
      HomotopyElement(
        name="ν′",
        dimension=3,
        generator=NU_PRIME_GENERATOR,
      )
    )
  )

  assert eta_3 is not None
  assert nu_prime is not None

  composition = Composition(
    left=eta_3,
    right=Suspension(
      expression=nu_prime,
    ),
  )

  result = (
    ZERO_COMPOSITION_FACT_REPOSITORY
    .lookup_by_untyped_structure(
      composition
    )
  )

  assert result is (
    ETA_3_E_NU_PRIME_ZERO_COMPOSITION_FACT
  )


def test_phase27_4_typed_nu_prime_nu_6_matches_second_zero_fact_by_untyped_structure():
  nu_prime = (
    GENERATOR_FACT_REPOSITORY
    .materialize_typed_element(
      HomotopyElement(
        name="ν′",
        dimension=3,
        generator=NU_PRIME_GENERATOR,
      )
    )
  )

  assert nu_prime is not None

  composition = Composition(
    left=nu_prime,
    right=HomotopyElement(
      name="ν₆",
      dimension=6,
      generator=NU_6_GENERATOR,
    ),
  )

  result = (
    ZERO_COMPOSITION_FACT_REPOSITORY
    .lookup_by_untyped_structure(
      composition
    )
  )

  assert result is (
    NU_PRIME_NU_6_ZERO_COMPOSITION_FACT
  )


def test_phase27_4_displayed_e_nu_prime_nu_7_is_not_primitive_zero_fact():
  nu_prime = (
    GENERATOR_FACT_REPOSITORY
    .materialize_typed_element(
      HomotopyElement(
        name="ν′",
        dimension=3,
        generator=NU_PRIME_GENERATOR,
      )
    )
  )

  nu_7 = (
    GENERATOR_FACT_REPOSITORY
    .materialize_typed_element(
      HomotopyElement(
        name="ν₇",
        dimension=7,
        generator=NU_7_GENERATOR,
      )
    )
  )

  assert nu_prime is not None
  assert nu_7 is not None

  composition = Composition(
    left=Suspension(
      expression=nu_prime,
    ),
    right=nu_7,
  )

  assert (
    ZERO_COMPOSITION_FACT_REPOSITORY
    .lookup_by_untyped_structure(
      composition
    )
    is None
  )


def test_phase27_4_exact_lookup_still_does_not_match_typed_composition():
  eta_3 = (
    GENERATOR_FACT_REPOSITORY
    .materialize_typed_element(
      HomotopyElement(
        name="η₃",
        dimension=3,
        generator=ETA_3_GENERATOR,
      )
    )
  )

  nu_prime = (
    GENERATOR_FACT_REPOSITORY
    .materialize_typed_element(
      HomotopyElement(
        name="ν′",
        dimension=3,
        generator=NU_PRIME_GENERATOR,
      )
    )
  )

  assert eta_3 is not None
  assert nu_prime is not None

  composition = Composition(
    left=eta_3,
    right=Suspension(
      expression=nu_prime,
    ),
  )

  assert (
    ZERO_COMPOSITION_FACT_REPOSITORY
    .lookup(
      composition
    )
    is None
  )

  assert (
    ZERO_COMPOSITION_FACT_REPOSITORY
    .lookup_by_untyped_structure(
      composition
    )
    is ETA_3_E_NU_PRIME_ZERO_COMPOSITION_FACT
  )


def test_phase27_4_structure_lookup_rejects_different_generator():
  different_generator = GeneratorSymbol(
    family="μ",
    index=3,
  )

  composition = Composition(
    left=HomotopyElement(
      name="η₃",
      dimension=3,
      source=4,
      target=3,
      generator=different_generator,
    ),
    right=Suspension(
      expression=HomotopyElement(
        name="ν′",
        dimension=3,
        source=6,
        target=3,
        generator=NU_PRIME_GENERATOR,
      ),
    ),
  )

  assert (
    ZERO_COMPOSITION_FACT_REPOSITORY
    .lookup_by_untyped_structure(
      composition
    )
    is None
  )


def test_phase27_4_structure_lookup_rejects_missing_suspension():
  composition = Composition(
    left=HomotopyElement(
      name="η₃",
      dimension=3,
      source=4,
      target=3,
      generator=ETA_3_GENERATOR,
    ),
    right=HomotopyElement(
      name="ν′",
      dimension=3,
      source=6,
      target=3,
      generator=NU_PRIME_GENERATOR,
    ),
  )

  assert (
    ZERO_COMPOSITION_FACT_REPOSITORY
    .lookup_by_untyped_structure(
      composition
    )
    is None
  )


def test_phase27_4_structure_lookup_ignores_only_typing_annotations():
  composition = Composition(
    left=HomotopyElement(
      name="wrong-name",
      dimension=3,
      source=4,
      target=3,
      generator=ETA_3_GENERATOR,
    ),
    right=Suspension(
      expression=HomotopyElement(
        name="ν′",
        dimension=3,
        source=6,
        target=3,
        generator=NU_PRIME_GENERATOR,
      ),
    ),
  )

  assert (
    ZERO_COMPOSITION_FACT_REPOSITORY
    .lookup_by_untyped_structure(
      composition
    )
    is None
  )

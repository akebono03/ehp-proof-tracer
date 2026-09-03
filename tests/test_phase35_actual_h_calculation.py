from expression import (
  GeneratorSymbol,
  HomotopyElement,
  Multiple,
)
from generator_facts import (
  GENERATOR_FACT_REPOSITORY,
)


def test_phase35_1_iota_1_identity_is_representable_with_explicit_typing():
  iota_1_generator = GeneratorSymbol(
    family="ι",
    index=1,
  )

  iota_1 = HomotopyElement(
    name="ι₁",
    dimension=1,
    source=1,
    target=1,
    generator=iota_1_generator,
  )

  assert iota_1.generator == (
    iota_1_generator
  )

  assert iota_1.source == 1
  assert iota_1.target == 1


def test_phase35_1_iota_2_identity_is_representable_with_explicit_typing():
  iota_2_generator = GeneratorSymbol(
    family="ι",
    index=2,
  )

  iota_2 = HomotopyElement(
    name="ι₂",
    dimension=2,
    source=2,
    target=2,
    generator=iota_2_generator,
  )

  assert iota_2.generator == (
    iota_2_generator
  )

  assert iota_2.source == 2
  assert iota_2.target == 2


def test_phase35_1_iota_3_identity_is_representable_with_explicit_typing():
  iota_3_generator = GeneratorSymbol(
    family="ι",
    index=3,
  )

  iota_3 = HomotopyElement(
    name="ι₃",
    dimension=3,
    source=3,
    target=3,
    generator=iota_3_generator,
  )

  assert iota_3.generator == (
    iota_3_generator
  )

  assert iota_3.source == 3
  assert iota_3.target == 3


def test_phase35_1_eta_2_is_representable_with_explicit_typing():
  eta_2_generator = GeneratorSymbol(
    family="η",
    index=2,
  )

  eta_2 = HomotopyElement(
    name="η₂",
    dimension=2,
    source=3,
    target=2,
    generator=eta_2_generator,
  )

  assert eta_2.generator == (
    eta_2_generator
  )

  assert eta_2.source == 3
  assert eta_2.target == 2


def test_phase35_1_two_iota_1_is_representable_as_multiple():
  iota_1 = HomotopyElement(
    name="ι₁",
    dimension=1,
    source=1,
    target=1,
    generator=GeneratorSymbol(
      family="ι",
      index=1,
    ),
  )

  two_iota_1 = Multiple(
    coefficient=2,
    expression=iota_1,
  )

  assert two_iota_1 == Multiple(
    coefficient=2,
    expression=iota_1,
  )

  assert two_iota_1.coefficient == 2
  assert two_iota_1.expression == iota_1


def test_phase35_1_two_iota_2_is_representable_as_multiple():
  iota_2 = HomotopyElement(
    name="ι₂",
    dimension=2,
    source=2,
    target=2,
    generator=GeneratorSymbol(
      family="ι",
      index=2,
    ),
  )

  two_iota_2 = Multiple(
    coefficient=2,
    expression=iota_2,
  )

  assert two_iota_2 == Multiple(
    coefficient=2,
    expression=iota_2,
  )

  assert two_iota_2.coefficient == 2
  assert two_iota_2.expression == iota_2


def test_phase35_1_actual_generators_are_structurally_distinct():
  iota_1 = GeneratorSymbol(
    family="ι",
    index=1,
  )

  iota_2 = GeneratorSymbol(
    family="ι",
    index=2,
  )

  iota_3 = GeneratorSymbol(
    family="ι",
    index=3,
  )

  eta_2 = GeneratorSymbol(
    family="η",
    index=2,
  )

  assert iota_1 != iota_2
  assert iota_2 != iota_3
  assert iota_2 != eta_2


def test_phase35_1_current_generator_repository_does_not_yet_type_iota_1():
  iota_1_generator = GeneratorSymbol(
    family="ι",
    index=1,
  )

  assert (
    GENERATOR_FACT_REPOSITORY
    .lookup_typing(
      iota_1_generator
    )
    is None
  )


def test_phase35_1_current_generator_repository_does_not_yet_type_iota_2():
  iota_2_generator = GeneratorSymbol(
    family="ι",
    index=2,
  )

  assert (
    GENERATOR_FACT_REPOSITORY
    .lookup_typing(
      iota_2_generator
    )
    is None
  )


def test_phase35_1_current_generator_repository_does_not_yet_type_iota_3():
  iota_3_generator = GeneratorSymbol(
    family="ι",
    index=3,
  )

  assert (
    GENERATOR_FACT_REPOSITORY
    .lookup_typing(
      iota_3_generator
    )
    is None
  )


def test_phase35_1_current_generator_repository_does_not_yet_type_eta_2():
  eta_2_generator = GeneratorSymbol(
    family="η",
    index=2,
  )

  assert (
    GENERATOR_FACT_REPOSITORY
    .lookup_typing(
      eta_2_generator
    )
    is None
  )


def test_phase35_1_generator_notation_does_not_implicitly_add_typing():
  eta_2 = HomotopyElement(
    name="η₂",
    dimension=2,
    generator=GeneratorSymbol(
      family="η",
      index=2,
    ),
  )

  assert eta_2.source is None
  assert eta_2.target is None


def test_phase35_1_representative_actual_elements_need_no_new_expression_type():
  iota_1 = HomotopyElement(
    name="ι₁",
    dimension=1,
    source=1,
    target=1,
    generator=GeneratorSymbol(
      family="ι",
      index=1,
    ),
  )

  iota_2 = HomotopyElement(
    name="ι₂",
    dimension=2,
    source=2,
    target=2,
    generator=GeneratorSymbol(
      family="ι",
      index=2,
    ),
  )

  iota_3 = HomotopyElement(
    name="ι₃",
    dimension=3,
    source=3,
    target=3,
    generator=GeneratorSymbol(
      family="ι",
      index=3,
    ),
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

  two_iota_1 = Multiple(
    coefficient=2,
    expression=iota_1,
  )

  two_iota_2 = Multiple(
    coefficient=2,
    expression=iota_2,
  )

  assert isinstance(
    iota_1,
    HomotopyElement,
  )

  assert isinstance(
    iota_2,
    HomotopyElement,
  )

  assert isinstance(
    iota_3,
    HomotopyElement,
  )

  assert isinstance(
    eta_2,
    HomotopyElement,
  )

  assert isinstance(
    two_iota_1,
    Multiple,
  )

  assert isinstance(
    two_iota_2,
    Multiple,
  )

  assert two_iota_1.expression == (
    iota_1
  )

  assert two_iota_2.expression == (
    iota_2
  )






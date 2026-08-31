from expression import (
  GeneratorSymbol,
  HomotopyElement,
)
from generator_facts import (
  GeneratorTypingFact,
)


def test_phase25_1_generator_typing_fact_preserves_minimum_structure():
  generator = GeneratorSymbol(
    family="η",
    index=3,
  )

  fact = GeneratorTypingFact(
    generator=generator,
    source=4,
    target=3,
  )

  assert fact.generator == generator
  assert fact.source == 4
  assert fact.target == 3


def test_phase25_1_same_generator_typing_facts_are_structurally_equal():
  left = GeneratorTypingFact(
    generator=GeneratorSymbol(
      family="η",
      index=3,
    ),
    source=4,
    target=3,
  )

  right = GeneratorTypingFact(
    generator=GeneratorSymbol(
      family="η",
      index=3,
    ),
    source=4,
    target=3,
  )

  assert left == right


def test_phase25_1_generator_identity_is_part_of_typing_fact_identity():
  eta_3_fact = GeneratorTypingFact(
    generator=GeneratorSymbol(
      family="η",
      index=3,
    ),
    source=4,
    target=3,
  )

  eta_4_fact = GeneratorTypingFact(
    generator=GeneratorSymbol(
      family="η",
      index=4,
    ),
    source=5,
    target=4,
  )

  mu_3_fact = GeneratorTypingFact(
    generator=GeneratorSymbol(
      family="μ",
      index=3,
    ),
    source=4,
    target=3,
  )

  assert eta_3_fact != eta_4_fact
  assert eta_3_fact != mu_3_fact


def test_phase25_1_generator_decoration_is_part_of_typing_fact_identity():
  nu_fact = GeneratorTypingFact(
    generator=GeneratorSymbol(
      family="ν",
    ),
    source=6,
    target=3,
  )

  nu_prime_fact = GeneratorTypingFact(
    generator=GeneratorSymbol(
      family="ν",
      decoration="′",
    ),
    source=6,
    target=3,
  )

  assert nu_fact != nu_prime_fact


def test_phase25_1_source_and_target_are_part_of_typing_fact_identity():
  generator = GeneratorSymbol(
    family="η",
    index=3,
  )

  original = GeneratorTypingFact(
    generator=generator,
    source=4,
    target=3,
  )

  different_source = GeneratorTypingFact(
    generator=generator,
    source=5,
    target=3,
  )

  different_target = GeneratorTypingFact(
    generator=generator,
    source=4,
    target=4,
  )

  assert original != different_source
  assert original != different_target


def test_phase25_1_generator_typing_fact_does_not_type_homotopy_element_automatically():
  generator = GeneratorSymbol(
    family="η",
    index=3,
  )

  fact = GeneratorTypingFact(
    generator=generator,
    source=4,
    target=3,
  )

  element = HomotopyElement(
    name="η₃",
    dimension=3,
    generator=generator,
  )

  assert fact.generator == element.generator
  assert fact.source == 4
  assert fact.target == 3

  assert element.source is None
  assert element.target is None




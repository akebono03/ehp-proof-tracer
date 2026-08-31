from expression import (
  GeneratorSymbol,
  HomotopyElement,
)
from generator_facts import (
  GeneratorAmbientGroupFact,
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


def test_phase25_2_generator_typing_fact_matches_same_generator():
  fact = GeneratorTypingFact(
    generator=GeneratorSymbol(
      family="η",
      index=3,
    ),
    source=4,
    target=3,
  )

  generator = GeneratorSymbol(
    family="η",
    index=3,
  )

  assert fact.matches_generator(
    generator
  )


def test_phase25_2_generator_typing_fact_rejects_different_family():
  fact = GeneratorTypingFact(
    generator=GeneratorSymbol(
      family="η",
      index=3,
    ),
    source=4,
    target=3,
  )

  generator = GeneratorSymbol(
    family="μ",
    index=3,
  )

  assert not fact.matches_generator(
    generator
  )


def test_phase25_2_generator_typing_fact_rejects_different_index():
  fact = GeneratorTypingFact(
    generator=GeneratorSymbol(
      family="η",
      index=3,
    ),
    source=4,
    target=3,
  )

  generator = GeneratorSymbol(
    family="η",
    index=4,
  )

  assert not fact.matches_generator(
    generator
  )


def test_phase25_2_generator_typing_fact_rejects_different_decoration():
  fact = GeneratorTypingFact(
    generator=GeneratorSymbol(
      family="ν",
      decoration="′",
    ),
    source=6,
    target=3,
  )

  plain_nu = GeneratorSymbol(
    family="ν",
  )

  nu_bar = GeneratorSymbol(
    family="ν",
    decoration="bar",
  )

  assert not fact.matches_generator(
    plain_nu
  )

  assert not fact.matches_generator(
    nu_bar
  )


def test_phase25_2_unindexed_generator_is_not_wildcard():
  fact = GeneratorTypingFact(
    generator=GeneratorSymbol(
      family="η",
    ),
    source=4,
    target=3,
  )

  indexed_generator = GeneratorSymbol(
    family="η",
    index=3,
  )

  assert not fact.matches_generator(
    indexed_generator
  )


def test_phase25_2_typing_fact_matches_generator_stored_by_homotopy_element():
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
    generator=GeneratorSymbol(
      family="η",
      index=3,
    ),
  )

  assert fact.matches_generator(
    element.generator
  )

  assert element.source is None
  assert element.target is None


def test_phase25_3_generator_ambient_group_fact_preserves_minimum_structure():
  generator = GeneratorSymbol(
    family="η",
    index=3,
  )

  fact = GeneratorAmbientGroupFact(
    generator=generator,
    group_dimension=4,
    sphere_dimension=3,
  )

  assert fact.generator == generator
  assert fact.group_dimension == 4
  assert fact.sphere_dimension == 3


def test_phase25_3_same_generator_ambient_group_facts_are_structurally_equal():
  left = GeneratorAmbientGroupFact(
    generator=GeneratorSymbol(
      family="η",
      index=3,
    ),
    group_dimension=4,
    sphere_dimension=3,
  )

  right = GeneratorAmbientGroupFact(
    generator=GeneratorSymbol(
      family="η",
      index=3,
    ),
    group_dimension=4,
    sphere_dimension=3,
  )

  assert left == right


def test_phase25_3_generator_identity_is_part_of_ambient_group_fact_identity():
  eta_3_fact = GeneratorAmbientGroupFact(
    generator=GeneratorSymbol(
      family="η",
      index=3,
    ),
    group_dimension=4,
    sphere_dimension=3,
  )

  mu_3_fact = GeneratorAmbientGroupFact(
    generator=GeneratorSymbol(
      family="μ",
      index=3,
    ),
    group_dimension=4,
    sphere_dimension=3,
  )

  assert eta_3_fact != mu_3_fact


def test_phase25_3_group_dimension_is_part_of_ambient_group_fact_identity():
  generator = GeneratorSymbol(
    family="η",
    index=3,
  )

  original = GeneratorAmbientGroupFact(
    generator=generator,
    group_dimension=4,
    sphere_dimension=3,
  )

  different_group_dimension = GeneratorAmbientGroupFact(
    generator=generator,
    group_dimension=5,
    sphere_dimension=3,
  )

  assert original != different_group_dimension


def test_phase25_3_sphere_dimension_is_part_of_ambient_group_fact_identity():
  generator = GeneratorSymbol(
    family="η",
    index=3,
  )

  original = GeneratorAmbientGroupFact(
    generator=generator,
    group_dimension=4,
    sphere_dimension=3,
  )

  different_sphere_dimension = GeneratorAmbientGroupFact(
    generator=generator,
    group_dimension=4,
    sphere_dimension=4,
  )

  assert original != different_sphere_dimension


def test_phase25_3_ambient_group_fact_does_not_type_homotopy_element_automatically():
  generator = GeneratorSymbol(
    family="η",
    index=3,
  )

  fact = GeneratorAmbientGroupFact(
    generator=generator,
    group_dimension=4,
    sphere_dimension=3,
  )

  element = HomotopyElement(
    name="η₃",
    dimension=3,
    generator=generator,
  )

  assert fact.generator == element.generator
  assert fact.group_dimension == 4
  assert fact.sphere_dimension == 3

  assert element.source is None
  assert element.target is None







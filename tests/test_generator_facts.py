from expression import (
  GeneratorSymbol,
  HomotopyElement,
  Suspension,
  TodaBracket,
)
from generator_facts import (
  ETA_3_AMBIENT_GROUP_FACT,
  ETA_3_GENERATOR,
  ETA_3_TYPING_FACT,
  GENERATOR_FACT_REPOSITORY,
  NU_7_AMBIENT_GROUP_FACT,
  NU_7_GENERATOR,
  NU_7_TYPING_FACT,
  NU_PRIME_AMBIENT_GROUP_FACT,
  NU_PRIME_GENERATOR,
  NU_PRIME_TYPING_FACT,
  GeneratorAmbientGroupFact,
  GeneratorFactRepository,
  GeneratorTypingFact,
)
from theorem_facts import (
  THEOREM_FACT_REPOSITORY,
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


def test_phase25_4_eta_3_generator_representative_is_registered():
  assert ETA_3_GENERATOR == GeneratorSymbol(
    family="η",
    index=3,
  )


def test_phase25_4_eta_3_typing_fact_representative_is_registered():
  assert ETA_3_TYPING_FACT == GeneratorTypingFact(
    generator=GeneratorSymbol(
      family="η",
      index=3,
    ),
    source=4,
    target=3,
  )


def test_phase25_4_eta_3_ambient_group_fact_representative_is_registered():
  assert ETA_3_AMBIENT_GROUP_FACT == (
    GeneratorAmbientGroupFact(
      generator=GeneratorSymbol(
        family="η",
        index=3,
      ),
      group_dimension=4,
      sphere_dimension=3,
    )
  )


def test_phase25_4_eta_3_representatives_share_generator_identity():
  assert ETA_3_TYPING_FACT.generator == (
    ETA_3_GENERATOR
  )

  assert ETA_3_AMBIENT_GROUP_FACT.generator == (
    ETA_3_GENERATOR
  )

  assert (
    ETA_3_TYPING_FACT.generator
    == ETA_3_AMBIENT_GROUP_FACT.generator
  )


def test_phase25_4_eta_3_typing_and_ambient_group_facts_remain_distinct():
  assert isinstance(
    ETA_3_TYPING_FACT,
    GeneratorTypingFact,
  )

  assert isinstance(
    ETA_3_AMBIENT_GROUP_FACT,
    GeneratorAmbientGroupFact,
  )

  assert (
    ETA_3_TYPING_FACT
    != ETA_3_AMBIENT_GROUP_FACT
  )


def test_phase25_4_eta_3_representative_does_not_type_homotopy_element_automatically():
  element = HomotopyElement(
    name="η₃",
    dimension=3,
    generator=ETA_3_GENERATOR,
  )

  assert ETA_3_TYPING_FACT.matches_generator(
    element.generator
  )

  assert (
    ETA_3_AMBIENT_GROUP_FACT.generator
    == element.generator
  )

  assert element.source is None
  assert element.target is None


def test_phase25_5_generator_fact_repository_is_empty_by_default():
  repository = GeneratorFactRepository()

  assert repository.typing_facts == ()
  assert repository.ambient_group_facts == ()


def test_phase25_5_production_repository_preserves_eta_3_facts():
  assert ETA_3_TYPING_FACT in (
    GENERATOR_FACT_REPOSITORY
    .typing_facts
  )

  assert ETA_3_AMBIENT_GROUP_FACT in (
    GENERATOR_FACT_REPOSITORY
    .ambient_group_facts
  )


def test_phase25_5_repository_lookup_returns_eta_3_typing_fact():
  result = (
    GENERATOR_FACT_REPOSITORY
    .lookup_typing(
      ETA_3_GENERATOR
    )
  )

  assert result is ETA_3_TYPING_FACT


def test_phase25_5_repository_lookup_returns_eta_3_ambient_group_fact():
  result = (
    GENERATOR_FACT_REPOSITORY
    .lookup_ambient_group(
      ETA_3_GENERATOR
    )
  )

  assert result is (
    ETA_3_AMBIENT_GROUP_FACT
  )


def test_phase25_5_repository_lookup_returns_none_for_unknown_generator():
  unknown_generator = GeneratorSymbol(
    family="η",
    index=4,
  )

  typing_result = (
    GENERATOR_FACT_REPOSITORY
    .lookup_typing(
      unknown_generator
    )
  )

  ambient_result = (
    GENERATOR_FACT_REPOSITORY
    .lookup_ambient_group(
      unknown_generator
    )
  )

  assert typing_result is None
  assert ambient_result is None


def test_phase25_5_repository_lookup_does_not_type_homotopy_element_automatically():
  element = HomotopyElement(
    name="η₃",
    dimension=3,
    generator=ETA_3_GENERATOR,
  )

  typing_fact = (
    GENERATOR_FACT_REPOSITORY
    .lookup_typing(
      element.generator
    )
  )

  ambient_fact = (
    GENERATOR_FACT_REPOSITORY
    .lookup_ambient_group(
      element.generator
    )
  )

  assert typing_fact is (
    ETA_3_TYPING_FACT
  )

  assert ambient_fact is (
    ETA_3_AMBIENT_GROUP_FACT
  )

  assert element.source is None
  assert element.target is None


def test_phase25_6_repository_materializes_typed_eta_3_element():
  element = HomotopyElement(
    name="η₃",
    dimension=3,
    generator=ETA_3_GENERATOR,
  )

  typed_element = (
    GENERATOR_FACT_REPOSITORY
    .materialize_typed_element(
      element
    )
  )

  assert typed_element == HomotopyElement(
    name="η₃",
    dimension=3,
    source=4,
    target=3,
    generator=ETA_3_GENERATOR,
  )


def test_phase25_6_materialization_returns_new_element_without_mutating_original():
  element = HomotopyElement(
    name="η₃",
    dimension=3,
    generator=ETA_3_GENERATOR,
  )

  typed_element = (
    GENERATOR_FACT_REPOSITORY
    .materialize_typed_element(
      element
    )
  )

  assert typed_element is not None
  assert typed_element is not element

  assert element.source is None
  assert element.target is None

  assert typed_element.source == 4
  assert typed_element.target == 3


def test_phase25_6_materialization_preserves_element_identity_fields():
  element = HomotopyElement(
    name="η₃",
    dimension=3,
    generator=ETA_3_GENERATOR,
  )

  typed_element = (
    GENERATOR_FACT_REPOSITORY
    .materialize_typed_element(
      element
    )
  )

  assert typed_element is not None

  assert typed_element.name == (
    element.name
  )

  assert typed_element.dimension == (
    element.dimension
  )

  assert typed_element.generator == (
    element.generator
  )


def test_phase25_6_materialization_returns_none_for_unknown_generator():
  element = HomotopyElement(
    name="η₄",
    dimension=4,
    generator=GeneratorSymbol(
      family="η",
      index=4,
    ),
  )

  typed_element = (
    GENERATOR_FACT_REPOSITORY
    .materialize_typed_element(
      element
    )
  )

  assert typed_element is None

  assert element.source is None
  assert element.target is None


def test_phase25_6_materialization_returns_none_without_generator():
  element = HomotopyElement(
    name="α",
    dimension=3,
  )

  typed_element = (
    GENERATOR_FACT_REPOSITORY
    .materialize_typed_element(
      element
    )
  )

  assert typed_element is None

  assert element.source is None
  assert element.target is None


def test_phase25_6_materialization_requires_untyped_element():
  element = HomotopyElement(
    name="η₃",
    dimension=3,
    source=4,
    target=3,
    generator=ETA_3_GENERATOR,
  )

  typed_element = (
    GENERATOR_FACT_REPOSITORY
    .materialize_typed_element(
      element
    )
  )

  assert typed_element is None

  assert element.source == 4
  assert element.target == 3


def test_phase25_7_eta_3_fact_materialization_connects_to_toda_entry_typing():
  eta_3 = HomotopyElement(
    name="η₃",
    dimension=3,
    generator=ETA_3_GENERATOR,
  )

  typed_eta_3 = (
    GENERATOR_FACT_REPOSITORY
    .materialize_typed_element(
      eta_3
    )
  )

  second = HomotopyElement(
    name="b",
    dimension=4,
    source=6,
    target=4,
  )

  third = HomotopyElement(
    name="c",
    dimension=6,
    source=8,
    target=6,
  )

  assert typed_eta_3 is not None

  bracket = TodaBracket(
    first=typed_eta_3,
    second=second,
    third=third,
  )

  assert (
    bracket
    .are_defining_compositions_type_compatible()
  )



def test_phase25_7_generator_facts_materialize_compatible_toda_entries():
  second_generator = GeneratorSymbol(
    family="b",
    index=4,
  )

  third_generator = GeneratorSymbol(
    family="c",
    index=6,
  )

  repository = GeneratorFactRepository(
    typing_facts=(
      ETA_3_TYPING_FACT,
      GeneratorTypingFact(
        generator=second_generator,
        source=6,
        target=4,
      ),
      GeneratorTypingFact(
        generator=third_generator,
        source=8,
        target=6,
      ),
    ),
  )

  first = HomotopyElement(
    name="η₃",
    dimension=3,
    generator=ETA_3_GENERATOR,
  )

  second = HomotopyElement(
    name="b",
    dimension=4,
    generator=second_generator,
  )

  third = HomotopyElement(
    name="c",
    dimension=6,
    generator=third_generator,
  )

  typed_first = (
    repository
    .materialize_typed_element(
      first
    )
  )

  typed_second = (
    repository
    .materialize_typed_element(
      second
    )
  )

  typed_third = (
    repository
    .materialize_typed_element(
      third
    )
  )

  assert typed_first is not None
  assert typed_second is not None
  assert typed_third is not None

  assert typed_first.source == 4
  assert typed_first.target == 3

  assert typed_second.source == 6
  assert typed_second.target == 4

  assert typed_third.source == 8
  assert typed_third.target == 6

  bracket = TodaBracket(
    first=typed_first,
    second=typed_second,
    third=typed_third,
  )

  assert (
    bracket
    .are_defining_compositions_type_compatible()
  )


def test_phase25_7_generator_fact_typing_mismatch_reaches_toda_compatibility():
  second_generator = GeneratorSymbol(
    family="b",
    index=4,
  )

  third_generator = GeneratorSymbol(
    family="c",
    index=6,
  )

  repository = GeneratorFactRepository(
    typing_facts=(
      ETA_3_TYPING_FACT,
      GeneratorTypingFact(
        generator=second_generator,
        source=6,
        target=5,
      ),
      GeneratorTypingFact(
        generator=third_generator,
        source=8,
        target=6,
      ),
    ),
  )

  first = repository.materialize_typed_element(
    HomotopyElement(
      name="η₃",
      dimension=3,
      generator=ETA_3_GENERATOR,
    )
  )

  second = repository.materialize_typed_element(
    HomotopyElement(
      name="b",
      dimension=4,
      generator=second_generator,
    )
  )

  third = repository.materialize_typed_element(
    HomotopyElement(
      name="c",
      dimension=6,
      generator=third_generator,
    )
  )

  assert first is not None
  assert second is not None
  assert third is not None

  assert first.source == 4
  assert second.target == 5
  assert first.source != second.target

  bracket = TodaBracket(
    first=first,
    second=second,
    third=third,
  )

  assert not (
    bracket
    .are_defining_compositions_type_compatible()
  )


def test_phase25_7_unmaterialized_generator_entries_remain_untyped_for_toda():
  first = HomotopyElement(
    name="η₃",
    dimension=3,
    generator=ETA_3_GENERATOR,
  )

  second = HomotopyElement(
    name="b",
    dimension=4,
    generator=GeneratorSymbol(
      family="b",
      index=4,
    ),
  )

  third = HomotopyElement(
    name="c",
    dimension=6,
    generator=GeneratorSymbol(
      family="c",
      index=6,
    ),
  )

  bracket = TodaBracket(
    first=first,
    second=second,
    third=third,
  )

  assert first.source is None
  assert first.target is None

  assert second.source is None
  assert second.target is None

  assert third.source is None
  assert third.target is None

  assert not (
    bracket
    .are_defining_compositions_type_compatible()
  )


def test_phase25_8_repository_rejects_duplicate_typing_fact():
  try:
    GeneratorFactRepository(
      typing_facts=(
        ETA_3_TYPING_FACT,
        ETA_3_TYPING_FACT,
      ),
    )
  except ValueError as error:
    assert str(error) == (
      "duplicate generator typing fact"
    )
  else:
    raise AssertionError(
      "duplicate generator typing fact "
      "was not rejected"
    )


def test_phase25_8_repository_rejects_conflicting_typing_facts_for_same_generator():
  conflicting_fact = GeneratorTypingFact(
    generator=ETA_3_GENERATOR,
    source=5,
    target=3,
  )

  try:
    GeneratorFactRepository(
      typing_facts=(
        ETA_3_TYPING_FACT,
        conflicting_fact,
      ),
    )
  except ValueError as error:
    assert str(error) == (
      "duplicate generator typing fact"
    )
  else:
    raise AssertionError(
      "conflicting generator typing facts "
      "were not rejected"
    )


def test_phase25_8_repository_rejects_duplicate_ambient_group_fact():
  try:
    GeneratorFactRepository(
      ambient_group_facts=(
        ETA_3_AMBIENT_GROUP_FACT,
        ETA_3_AMBIENT_GROUP_FACT,
      ),
    )
  except ValueError as error:
    assert str(error) == (
      "duplicate generator ambient-group fact"
    )
  else:
    raise AssertionError(
      "duplicate generator ambient-group fact "
      "was not rejected"
    )


def test_phase25_8_repository_rejects_conflicting_ambient_group_facts_for_same_generator():
  conflicting_fact = GeneratorAmbientGroupFact(
    generator=ETA_3_GENERATOR,
    group_dimension=5,
    sphere_dimension=3,
  )

  try:
    GeneratorFactRepository(
      ambient_group_facts=(
        ETA_3_AMBIENT_GROUP_FACT,
        conflicting_fact,
      ),
    )
  except ValueError as error:
    assert str(error) == (
      "duplicate generator ambient-group fact"
    )
  else:
    raise AssertionError(
      "conflicting generator ambient-group "
      "facts were not rejected"
    )


def test_phase25_8_same_generator_is_allowed_across_fact_families():
  repository = GeneratorFactRepository(
    typing_facts=(
      ETA_3_TYPING_FACT,
    ),
    ambient_group_facts=(
      ETA_3_AMBIENT_GROUP_FACT,
    ),
  )

  assert repository.lookup_typing(
    ETA_3_GENERATOR
  ) is ETA_3_TYPING_FACT

  assert repository.lookup_ambient_group(
    ETA_3_GENERATOR
  ) is ETA_3_AMBIENT_GROUP_FACT


def test_phase25_8_unknown_generator_remains_unknown():
  unknown_generator = GeneratorSymbol(
    family="η",
    index=4,
  )

  assert (
    GENERATOR_FACT_REPOSITORY
    .lookup_typing(
      unknown_generator
    )
    is None
  )

  assert (
    GENERATOR_FACT_REPOSITORY
    .lookup_ambient_group(
      unknown_generator
    )
    is None
  )


def test_phase25_8_existing_conflicting_typing_is_not_overwritten():
  element = HomotopyElement(
    name="η₃",
    dimension=3,
    source=5,
    target=3,
    generator=ETA_3_GENERATOR,
  )

  result = (
    GENERATOR_FACT_REPOSITORY
    .materialize_typed_element(
      element
    )
  )

  assert result is None

  assert element.source == 5
  assert element.target == 3


def test_phase25_8_partial_existing_typing_is_not_completed_implicitly():
  element = HomotopyElement(
    name="η₃",
    dimension=3,
    source=4,
    target=None,
    generator=ETA_3_GENERATOR,
  )

  result = (
    GENERATOR_FACT_REPOSITORY
    .materialize_typed_element(
      element
    )
  )

  assert result is None

  assert element.source == 4
  assert element.target is None


def test_phase25_9_lookup_preserves_registered_typing_fact_identity():
  result = (
    GENERATOR_FACT_REPOSITORY
    .lookup_typing(
      GeneratorSymbol(
        family="η",
        index=3,
      )
    )
  )

  assert result is (
    ETA_3_TYPING_FACT
  )


def test_phase25_9_lookup_preserves_registered_ambient_group_fact_identity():
  result = (
    GENERATOR_FACT_REPOSITORY
    .lookup_ambient_group(
      GeneratorSymbol(
        family="η",
        index=3,
      )
    )
  )

  assert result is (
    ETA_3_AMBIENT_GROUP_FACT
  )


def test_phase25_9_unrelated_generator_facts_do_not_change_eta_3_materialization():
  unrelated_generator = GeneratorSymbol(
    family="μ",
    index=3,
  )

  repository = GeneratorFactRepository(
    typing_facts=(
      GeneratorTypingFact(
        generator=unrelated_generator,
        source=12,
        target=3,
      ),
      ETA_3_TYPING_FACT,
    ),
    ambient_group_facts=(
      GeneratorAmbientGroupFact(
        generator=unrelated_generator,
        group_dimension=12,
        sphere_dimension=3,
      ),
      ETA_3_AMBIENT_GROUP_FACT,
    ),
  )

  element = HomotopyElement(
    name="η₃",
    dimension=3,
    generator=ETA_3_GENERATOR,
  )

  typed_element = (
    repository
    .materialize_typed_element(
      element
    )
  )

  assert typed_element == HomotopyElement(
    name="η₃",
    dimension=3,
    source=4,
    target=3,
    generator=ETA_3_GENERATOR,
  )


def test_phase25_9_element_name_does_not_replace_structured_generator_identity():
  element = HomotopyElement(
    name="η₃",
    dimension=3,
    generator=GeneratorSymbol(
      family="μ",
      index=3,
    ),
  )

  typed_element = (
    GENERATOR_FACT_REPOSITORY
    .materialize_typed_element(
      element
    )
  )

  assert typed_element is None

  assert element.name == "η₃"
  assert element.source is None
  assert element.target is None


def test_phase25_9_ambient_group_fact_alone_does_not_materialize_typing():
  repository = GeneratorFactRepository(
    ambient_group_facts=(
      ETA_3_AMBIENT_GROUP_FACT,
    ),
  )

  element = HomotopyElement(
    name="η₃",
    dimension=3,
    generator=ETA_3_GENERATOR,
  )

  typed_element = (
    repository
    .materialize_typed_element(
      element
    )
  )

  assert (
    repository.lookup_ambient_group(
      ETA_3_GENERATOR
    )
    is ETA_3_AMBIENT_GROUP_FACT
  )

  assert typed_element is None

  assert element.source is None
  assert element.target is None


def test_phase25_9_materialization_does_not_modify_repository_state():
  typing_facts_before = (
    GENERATOR_FACT_REPOSITORY
    .typing_facts
  )

  ambient_facts_before = (
    GENERATOR_FACT_REPOSITORY
    .ambient_group_facts
  )

  element = HomotopyElement(
    name="η₃",
    dimension=3,
    generator=ETA_3_GENERATOR,
  )

  typed_element = (
    GENERATOR_FACT_REPOSITORY
    .materialize_typed_element(
      element
    )
  )

  assert typed_element is not None

  assert (
    GENERATOR_FACT_REPOSITORY
    .typing_facts
    == typing_facts_before
  )

  assert (
    GENERATOR_FACT_REPOSITORY
    .ambient_group_facts
    == ambient_facts_before
  )


def test_phase25_9_generator_materialization_does_not_modify_theorem_fact_repository():
  theorem_entries_before = (
    THEOREM_FACT_REPOSITORY.entries
  )

  element = HomotopyElement(
    name="η₃",
    dimension=3,
    generator=ETA_3_GENERATOR,
  )

  typed_element = (
    GENERATOR_FACT_REPOSITORY
    .materialize_typed_element(
      element
    )
  )

  assert typed_element is not None

  assert (
    THEOREM_FACT_REPOSITORY.entries
    == theorem_entries_before
  )


def test_phase26_1_nu_prime_generator_has_expected_structural_identity():
  assert NU_PRIME_GENERATOR == GeneratorSymbol(
    family="ν",
    decoration="′",
  )


def test_phase26_1_nu_prime_typing_fact_has_expected_source_and_target():
  assert NU_PRIME_TYPING_FACT == GeneratorTypingFact(
    generator=GeneratorSymbol(
      family="ν",
      decoration="′",
    ),
    source=6,
    target=3,
  )


def test_phase26_1_nu_prime_typing_fact_uses_nu_prime_generator_identity():
  assert NU_PRIME_TYPING_FACT.generator is (
    NU_PRIME_GENERATOR
  )

  assert NU_PRIME_TYPING_FACT.source == 6
  assert NU_PRIME_TYPING_FACT.target == 3


def test_phase26_1_nu_prime_remains_distinct_from_plain_nu():
  plain_nu = GeneratorSymbol(
    family="ν",
  )

  assert NU_PRIME_GENERATOR != plain_nu

  assert not (
    NU_PRIME_TYPING_FACT
    .matches_generator(
      plain_nu
    )
  )

  assert (
    NU_PRIME_TYPING_FACT
    .matches_generator(
      GeneratorSymbol(
        family="ν",
        decoration="′",
      )
    )
  )


def test_phase26_2_nu_7_generator_has_expected_structural_identity():
  assert NU_7_GENERATOR == GeneratorSymbol(
    family="ν",
    index=7,
  )


def test_phase26_2_nu_7_typing_fact_has_expected_source_and_target():
  assert NU_7_TYPING_FACT == GeneratorTypingFact(
    generator=GeneratorSymbol(
      family="ν",
      index=7,
    ),
    source=10,
    target=7,
  )


def test_phase26_2_nu_7_typing_fact_uses_nu_7_generator_identity():
  assert NU_7_TYPING_FACT.generator is (
    NU_7_GENERATOR
  )

  assert NU_7_TYPING_FACT.source == 10
  assert NU_7_TYPING_FACT.target == 7


def test_phase26_2_nu_7_remains_distinct_from_unindexed_nu():
  unindexed_nu = GeneratorSymbol(
    family="ν",
  )

  assert NU_7_GENERATOR != unindexed_nu

  assert not (
    NU_7_TYPING_FACT
    .matches_generator(
      unindexed_nu
    )
  )

  assert (
    NU_7_TYPING_FACT
    .matches_generator(
      GeneratorSymbol(
        family="ν",
        index=7,
      )
    )
  )


def test_phase26_2_nu_7_remains_distinct_from_nu_prime():
  assert (
    NU_7_GENERATOR
    != NU_PRIME_GENERATOR
  )

  assert not (
    NU_7_TYPING_FACT
    .matches_generator(
      NU_PRIME_GENERATOR
    )
  )

  assert not (
    NU_PRIME_TYPING_FACT
    .matches_generator(
      NU_7_GENERATOR
    )
  )


def test_phase26_3_nu_prime_ambient_group_fact_has_expected_group():
  assert NU_PRIME_AMBIENT_GROUP_FACT == (
    GeneratorAmbientGroupFact(
      generator=GeneratorSymbol(
        family="ν",
        decoration="′",
      ),
      group_dimension=6,
      sphere_dimension=3,
    )
  )


def test_phase26_3_nu_prime_ambient_group_fact_uses_nu_prime_generator_identity():
  assert (
    NU_PRIME_AMBIENT_GROUP_FACT.generator
    is NU_PRIME_GENERATOR
  )

  assert (
    NU_PRIME_AMBIENT_GROUP_FACT.group_dimension
    == 6
  )

  assert (
    NU_PRIME_AMBIENT_GROUP_FACT.sphere_dimension
    == 3
  )


def test_phase26_3_nu_7_ambient_group_fact_has_expected_group():
  assert NU_7_AMBIENT_GROUP_FACT == (
    GeneratorAmbientGroupFact(
      generator=GeneratorSymbol(
        family="ν",
        index=7,
      ),
      group_dimension=10,
      sphere_dimension=7,
    )
  )


def test_phase26_3_nu_7_ambient_group_fact_uses_nu_7_generator_identity():
  assert (
    NU_7_AMBIENT_GROUP_FACT.generator
    is NU_7_GENERATOR
  )

  assert (
    NU_7_AMBIENT_GROUP_FACT.group_dimension
    == 10
  )

  assert (
    NU_7_AMBIENT_GROUP_FACT.sphere_dimension
    == 7
  )


def test_phase26_3_nu_prime_typing_and_ambient_group_facts_remain_distinct():
  assert isinstance(
    NU_PRIME_TYPING_FACT,
    GeneratorTypingFact,
  )

  assert isinstance(
    NU_PRIME_AMBIENT_GROUP_FACT,
    GeneratorAmbientGroupFact,
  )

  assert (
    NU_PRIME_TYPING_FACT
    != NU_PRIME_AMBIENT_GROUP_FACT
  )

  assert (
    NU_PRIME_TYPING_FACT.generator
    == NU_PRIME_AMBIENT_GROUP_FACT.generator
  )


def test_phase26_3_nu_7_typing_and_ambient_group_facts_remain_distinct():
  assert isinstance(
    NU_7_TYPING_FACT,
    GeneratorTypingFact,
  )

  assert isinstance(
    NU_7_AMBIENT_GROUP_FACT,
    GeneratorAmbientGroupFact,
  )

  assert (
    NU_7_TYPING_FACT
    != NU_7_AMBIENT_GROUP_FACT
  )

  assert (
    NU_7_TYPING_FACT.generator
    == NU_7_AMBIENT_GROUP_FACT.generator
  )


def test_phase26_4_production_repository_returns_nu_prime_typing_fact():
  result = (
    GENERATOR_FACT_REPOSITORY
    .lookup_typing(
      NU_PRIME_GENERATOR
    )
  )

  assert result is (
    NU_PRIME_TYPING_FACT
  )


def test_phase26_4_production_repository_materializes_nu_prime():
  element = HomotopyElement(
    name="ν′",
    dimension=3,
    generator=NU_PRIME_GENERATOR,
  )

  typed_element = (
    GENERATOR_FACT_REPOSITORY
    .materialize_typed_element(
      element
    )
  )

  assert typed_element == HomotopyElement(
    name="ν′",
    dimension=3,
    source=6,
    target=3,
    generator=NU_PRIME_GENERATOR,
  )

  assert element.source is None
  assert element.target is None


def test_phase26_4_production_repository_returns_nu_7_typing_fact():
  result = (
    GENERATOR_FACT_REPOSITORY
    .lookup_typing(
      NU_7_GENERATOR
    )
  )

  assert result is (
    NU_7_TYPING_FACT
  )


def test_phase26_4_production_repository_materializes_nu_7():
  element = HomotopyElement(
    name="ν₇",
    dimension=7,
    generator=NU_7_GENERATOR,
  )

  typed_element = (
    GENERATOR_FACT_REPOSITORY
    .materialize_typed_element(
      element
    )
  )

  assert typed_element == HomotopyElement(
    name="ν₇",
    dimension=7,
    source=10,
    target=7,
    generator=NU_7_GENERATOR,
  )

  assert element.source is None
  assert element.target is None


def test_phase26_4_production_repository_returns_nu_prime_ambient_group_fact():
  result = (
    GENERATOR_FACT_REPOSITORY
    .lookup_ambient_group(
      NU_PRIME_GENERATOR
    )
  )

  assert result is (
    NU_PRIME_AMBIENT_GROUP_FACT
  )


def test_phase26_4_production_repository_returns_nu_7_ambient_group_fact():
  result = (
    GENERATOR_FACT_REPOSITORY
    .lookup_ambient_group(
      NU_7_GENERATOR
    )
  )

  assert result is (
    NU_7_AMBIENT_GROUP_FACT
  )


def test_phase26_5_repository_derived_nu_prime_suspends_to_expected_typing():
  nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
    generator=NU_PRIME_GENERATOR,
  )

  typed_nu_prime = (
    GENERATOR_FACT_REPOSITORY
    .materialize_typed_element(
      nu_prime
    )
  )

  assert typed_nu_prime is not None
  assert typed_nu_prime.source == 6
  assert typed_nu_prime.target == 3

  suspended_nu_prime = Suspension(
    expression=typed_nu_prime,
  )

  assert suspended_nu_prime.source == 7
  assert suspended_nu_prime.target == 4


def test_phase26_5_suspended_nu_prime_preserves_repository_derived_base_element():
  nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
    generator=NU_PRIME_GENERATOR,
  )

  typed_nu_prime = (
    GENERATOR_FACT_REPOSITORY
    .materialize_typed_element(
      nu_prime
    )
  )

  assert typed_nu_prime is not None

  suspended_nu_prime = Suspension(
    expression=typed_nu_prime,
  )

  assert suspended_nu_prime.expression is (
    typed_nu_prime
  )

  assert (
    suspended_nu_prime.expression.generator
    is NU_PRIME_GENERATOR
  )


def test_phase26_5_unmaterialized_nu_prime_suspension_remains_untyped():
  nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
    generator=NU_PRIME_GENERATOR,
  )

  suspended_nu_prime = Suspension(
    expression=nu_prime,
  )

  assert nu_prime.source is None
  assert nu_prime.target is None

  assert suspended_nu_prime.source is None
  assert suspended_nu_prime.target is None


def test_phase26_5_suspension_connection_does_not_mutate_original_nu_prime():
  nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
    generator=NU_PRIME_GENERATOR,
  )

  typed_nu_prime = (
    GENERATOR_FACT_REPOSITORY
    .materialize_typed_element(
      nu_prime
    )
  )

  assert typed_nu_prime is not None

  suspended_nu_prime = Suspension(
    expression=typed_nu_prime,
  )

  assert nu_prime.source is None
  assert nu_prime.target is None

  assert typed_nu_prime.source == 6
  assert typed_nu_prime.target == 3

  assert suspended_nu_prime.source == 7
  assert suspended_nu_prime.target == 4


def test_phase26_5_suspended_nu_prime_typing_originates_from_registered_typing_fact():
  typing_fact = (
    GENERATOR_FACT_REPOSITORY
    .lookup_typing(
      NU_PRIME_GENERATOR
    )
  )

  assert typing_fact is (
    NU_PRIME_TYPING_FACT
  )

  nu_prime = HomotopyElement(
    name="ν′",
    dimension=3,
    generator=typing_fact.generator,
  )

  typed_nu_prime = (
    GENERATOR_FACT_REPOSITORY
    .materialize_typed_element(
      nu_prime
    )
  )

  assert typed_nu_prime is not None

  suspended_nu_prime = Suspension(
    expression=typed_nu_prime,
  )

  assert typed_nu_prime.source == (
    NU_PRIME_TYPING_FACT.source
  )

  assert typed_nu_prime.target == (
    NU_PRIME_TYPING_FACT.target
  )

  assert suspended_nu_prime.source == (
    NU_PRIME_TYPING_FACT.source + 1
  )

  assert suspended_nu_prime.target == (
    NU_PRIME_TYPING_FACT.target + 1
  )







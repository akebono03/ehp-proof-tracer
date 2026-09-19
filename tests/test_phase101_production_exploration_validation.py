import pytest

from expression import (
  GeneratorSymbol,
)
from generator_facts import (
  NU_PRIME_GENERATOR,
)
from generator_input import (
  resolve_generator_input,
)
from repository_element_facade import (
  explore_repository_generator,
  explore_standard_repository_generator_input,
)
from standard_production_repository import (
  build_standard_production_proof_repository,
)


def _occurrence_signature(
  report,
):
  return tuple(
    (
      occurrence.entry.key,
      occurrence.path,
      occurrence.matched_generator,
      occurrence.roles,
    )
    for occurrence
    in report.exploration.occurrences
  )


def test_phase101_4_production_nu_prime_aliases_are_equivalent():
  baseline = (
    explore_standard_repository_generator_input(
      "nu_prime"
    )
  )

  assert (
    baseline.exploration.generator
    == NU_PRIME_GENERATOR
  )

  baseline_signature = (
    _occurrence_signature(
      baseline
    )
  )

  assert baseline_signature

  for value in (
    "ν′",
    "ν'",
    "nu'",
  ):
    report = (
      explore_standard_repository_generator_input(
        value
      )
    )

    assert (
      report.exploration.generator
      == NU_PRIME_GENERATOR
    )

    assert (
      _occurrence_signature(
        report
      )
      == baseline_signature
    )

    assert (
      report.markdown
      == baseline.markdown
    )


@pytest.mark.parametrize(
  (
    "value",
    "expected",
  ),
  (
    (
      "eta_2",
      GeneratorSymbol(
        family="η",
        index=2,
      ),
    ),
    (
      "nu_5",
      GeneratorSymbol(
        family="ν",
        index=5,
      ),
    ),
  ),
)
def test_phase101_4_indexed_generator_search_is_exact_and_nonempty(
  value,
  expected,
):
  report = (
    explore_standard_repository_generator_input(
      value
    )
  )

  assert (
    report.exploration.generator
    == expected
  )

  assert (
    report.exploration.occurrences
  )

  assert all(
    occurrence.matched_generator
    == expected
    for occurrence
    in report.exploration.occurrences
  )


def test_phase101_4_unknown_indexed_generator_is_normal_zero_occurrence():
  report = (
    explore_standard_repository_generator_input(
      "eta_999"
    )
  )

  assert (
    report.exploration.generator
    == GeneratorSymbol(
      family="η",
      index=999,
    )
  )

  assert (
    report.exploration.occurrences
    == ()
  )

  assert (
    report.presentation.occurrences
    == ()
  )

  assert (
    "Occurrences: 0"
    in report.markdown
  )


@pytest.mark.parametrize(
  "value",
  (
    "",
    "   ",
    "not_a_generator",
    "nu prime",
    "eta_0",
  ),
)
def test_phase101_4_invalid_string_input_reuses_resolver_validation(
  value,
):
  with pytest.raises(
    ValueError,
  ):
    explore_standard_repository_generator_input(
      value
    )


def test_phase101_4_non_string_input_reuses_resolver_type_validation():
  with pytest.raises(
    TypeError,
    match="value must be a str",
  ):
    explore_standard_repository_generator_input(
      None
    )


def test_phase101_4_production_occurrences_preserve_distinct_structural_paths():
  report = (
    explore_standard_repository_generator_input(
      "nu_prime"
    )
  )

  occurrences = (
    report.exploration.occurrences
  )

  assert occurrences

  entry_path_pairs = tuple(
    (
      occurrence.entry.key,
      occurrence.path,
    )
    for occurrence in occurrences
  )

  assert len(
    entry_path_pairs
  ) == len(
    set(
      entry_path_pairs
    )
  )

  entry_keys = tuple(
    occurrence.entry.key
    for occurrence in occurrences
  )

  assert len(
    set(
      entry_keys
    )
  ) < len(
    entry_keys
  )


def test_phase101_4_production_exploration_is_deterministic():
  first = (
    explore_standard_repository_generator_input(
      "nu_prime"
    )
  )

  second = (
    explore_standard_repository_generator_input(
      "nu_prime"
    )
  )

  assert (
    _occurrence_signature(
      first
    )
    == _occurrence_signature(
      second
    )
  )

  assert (
    first.markdown
    == second.markdown
  )


def test_phase101_4_production_repository_is_not_mutated_by_exploration():
  repository = (
    build_standard_production_proof_repository()
  )

  before = (
    repository.entries()
  )

  generator = (
    resolve_generator_input(
      "nu_prime"
    )
  )

  report = (
    explore_repository_generator(
      repository,
      generator,
    )
  )

  after = (
    repository.entries()
  )

  assert (
    report.exploration.occurrences
  )

  assert (
    after
    == before
  )

  assert all(
    actual is expected
    for actual, expected
    in zip(
      after,
      before,
    )
  )


def test_phase101_4_grouped_occurrences_preserve_master_occurrence_order():
  report = (
    explore_standard_repository_generator_input(
      "nu_prime"
    )
  )

  occurrences = (
    report.exploration.occurrences
  )

  positions = {
    id(
      occurrence
    ): index
    for index, occurrence
    in enumerate(
      occurrences
    )
  }

  grouped_views = (
    report
    .exploration
    .toda_bracket_occurrences,
    report
    .exploration
    .map_input_occurrences,
    report
    .exploration
    .group_generator_occurrences,
    report
    .exploration
    .composition_left_occurrences,
    report
    .exploration
    .composition_right_occurrences,
  )

  for grouped in grouped_views:
    grouped_positions = tuple(
      positions[
        id(
          occurrence
        )
      ]
      for occurrence
      in grouped
    )

    assert (
      grouped_positions
      == tuple(
        sorted(
          grouped_positions
        )
      )
    )

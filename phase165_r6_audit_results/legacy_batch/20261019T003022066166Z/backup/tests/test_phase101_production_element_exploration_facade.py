import pytest

from generator_facts import (
  NU_PRIME_GENERATOR,
)
from generator_input import (
  resolve_generator_input,
)
from repository_element_facade import (
  RepositoryGeneratorExplorationReport,
  explore_repository_generator,
  explore_standard_repository_generator_input,
)
from standard_production_repository import (
  build_standard_production_proof_repository,
)


def test_phase101_2_returns_existing_exploration_report_type():
  report = (
    explore_standard_repository_generator_input(
      "nu_prime"
    )
  )

  assert isinstance(
    report,
    RepositoryGeneratorExplorationReport,
  )


@pytest.mark.parametrize(
  "value",
  (
    "ν′",
    "ν'",
    "nu'",
    "nu_prime",
  ),
)
def test_phase101_2_reuses_existing_nu_prime_alias_resolution(
  value,
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


def test_phase101_2_matches_manual_existing_production_path():
  expected_repository = (
    build_standard_production_proof_repository()
  )

  expected_generator = (
    resolve_generator_input(
      "nu_prime"
    )
  )

  expected = (
    explore_repository_generator(
      expected_repository,
      expected_generator,
    )
  )

  actual = (
    explore_standard_repository_generator_input(
      "nu_prime"
    )
  )

  assert actual == expected


def test_phase101_2_production_occurrences_have_renderable_concrete_context():
  report = (
    explore_standard_repository_generator_input(
      "nu_prime"
    )
  )

  assert (
    report.presentation.occurrences
  )

  assert all(
    occurrence.conclusion_latex
    for occurrence
    in report.presentation.occurrences
  )


def test_phase101_2_preserves_zero_occurrence_as_normal_report():
  report = (
    explore_standard_repository_generator_input(
      "eta_999"
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
    "not_a_generator",
    "eta_0",
  ),
)
def test_phase101_2_reuses_existing_invalid_input_validation(
  value,
):
  with pytest.raises(
    ValueError,
  ):
    explore_standard_repository_generator_input(
      value
    )


def test_phase101_2_preserves_outer_whitespace_normalization():
  report = (
    explore_standard_repository_generator_input(
      "  nu_prime  "
    )
  )

  assert (
    report.exploration.generator
    == NU_PRIME_GENERATOR
  )

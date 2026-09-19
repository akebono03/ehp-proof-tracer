from repository_generator_applicability_facade import (
  explore_standard_repository_generator_applicability_input,
)
from standard_production_applicability_catalog import (
  build_standard_production_applicability_catalog,
)


def test_phase103_6_default_standard_catalog_is_used():
  explicit_catalog = (
    build_standard_production_applicability_catalog()
  )

  explicit = (
    explore_standard_repository_generator_applicability_input(
      "nu_prime",
      explicit_catalog,
    )
  )

  default = (
    explore_standard_repository_generator_applicability_input(
      "nu_prime"
    )
  )

  explicit_shape = tuple(
    (
      candidate.candidate.inference_rule.name,
      candidate.candidate.premise_index,
      candidate.root_entry.key,
      candidate.shortest_depth,
      type(
        candidate.candidate.matched_statement
      ),
    )
    for candidate in explicit.candidates
  )

  default_shape = tuple(
    (
      candidate.candidate.inference_rule.name,
      candidate.candidate.premise_index,
      candidate.root_entry.key,
      candidate.shortest_depth,
      type(
        candidate.candidate.matched_statement
      ),
    )
    for candidate in default.candidates
  )

  assert (
    default_shape
    == explicit_shape
  )


def test_phase103_6_production_nu_prime_has_applicability_candidate():
  result = (
    explore_standard_repository_generator_applicability_input(
      "nu_prime"
    )
  )

  assert (
    result
    .proof_scope_exploration
    .occurrences
  )

  assert (
    result.candidates
  )

  assert any(
    candidate.shortest_depth > 0
    for candidate in result.candidates
  )


def test_phase103_6_unknown_generator_is_valid_zero_result():
  result = (
    explore_standard_repository_generator_applicability_input(
      "eta_999"
    )
  )

  assert (
    result.candidates
    == ()
  )

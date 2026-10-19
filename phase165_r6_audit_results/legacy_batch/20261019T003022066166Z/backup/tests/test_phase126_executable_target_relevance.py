from functools import lru_cache

from repository_generator_user_execution_resolver import (
  resolve_standard_repository_generator_executable_targets_input,
)


_FIRST_FAMILY = (
  "toda_58_delta_iota9_nu4_nu_prime_inference_rule"
)

_SECOND_FAMILY = (
  "toda_lemma57_pi6_2_eta2_nu_prime_inference_rule"
)


@lru_cache(maxsize=1)
def _nu_prime_resolution():
  return (
    resolve_standard_repository_generator_executable_targets_input(
      "nu_prime"
    )
  )


@lru_cache(maxsize=1)
def _nu_5_resolution():
  return (
    resolve_standard_repository_generator_executable_targets_input(
      "nu_5"
    )
  )


@lru_cache(maxsize=1)
def _sigma_11_resolution():
  return (
    resolve_standard_repository_generator_executable_targets_input(
      "sigma_11"
    )
  )


def _is_pi6_2_goal(
  goal,
):
  lhs = getattr(
    goal,
    "lhs",
    None,
  )

  return (
    getattr(
      lhs,
      "group_dimension",
      None,
    )
    == 6
    and getattr(
      lhs,
      "sphere_dimension",
      None,
    )
    == 2
  )


def test_phase126_4_nu_prime_preserves_two_executable_targets():
  result = (
    _nu_prime_resolution()
  )

  assert len(
    result.targets
  ) == 2

  assert {
    target.family_name
    for target in result.targets
  } == {
    _FIRST_FAMILY,
    _SECOND_FAMILY,
  }


def test_phase126_4_nu_5_keeps_applicability_but_drops_unrelated_pi6_2_target():
  result = (
    _nu_5_resolution()
  )

  assert (
    result
    .applicability_result
    .candidates
  )

  assert (
    result
    .qualified_selection
    .candidates
  )

  assert not any(
    _is_pi6_2_goal(
      target.goal
    )
    for target in result.targets
  )


def test_phase126_4_sigma_11_remains_without_executable_target():
  result = (
    _sigma_11_resolution()
  )

  assert result.targets == ()

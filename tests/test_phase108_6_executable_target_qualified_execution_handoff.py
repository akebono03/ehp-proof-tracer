from functools import lru_cache

import pytest

from repository_generator_applicability_execution_orchestration import (
  FirstQualifiedProductionApplicabilityExecutionResult,
)
from repository_generator_qualified_execution_dispatch import (
  QualifiedProductionApplicabilityExecutionDispatchResult,
)
from repository_generator_two_premise_execution_integration import (
  TwoPremiseProductionApplicationExecutionResult,
)
from repository_generator_user_execution_handoff import (
  RepositoryGeneratorExecutableTargetExecutionResult,
  execute_repository_generator_executable_target,
)
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
def _phase108_6_resolution():
  return (
    resolve_standard_repository_generator_executable_targets_input(
      "nu_prime"
    )
  )


def _first_target_for_family(
  family_name,
):
  resolution = (
    _phase108_6_resolution()
  )

  for target in resolution.targets:
    if target.family_name == family_name:
      return (
        resolution,
        target,
      )

  raise AssertionError(
    f"no executable target found for family: {family_name}"
  )


def test_phase108_6_executes_first_family_target_through_existing_dispatch():
  resolution, target = (
    _first_target_for_family(
      _FIRST_FAMILY
    )
  )

  result = (
    execute_repository_generator_executable_target(
      resolution,
      target,
    )
  )

  assert isinstance(
    result,
    RepositoryGeneratorExecutableTargetExecutionResult,
  )

  assert (
    result.resolution
    is resolution
  )

  assert (
    result.target
    is target
  )

  assert result.execution_result.executed is True

  assert isinstance(
    result.execution_result.execution,
    QualifiedProductionApplicabilityExecutionDispatchResult,
  )

  assert isinstance(
    result.execution_result.execution.execution,
    FirstQualifiedProductionApplicabilityExecutionResult,
  )


def test_phase108_6_executes_second_family_target_through_existing_dispatch():
  resolution, target = (
    _first_target_for_family(
      _SECOND_FAMILY
    )
  )

  result = (
    execute_repository_generator_executable_target(
      resolution,
      target,
    )
  )

  assert result.execution_result.executed is True

  assert isinstance(
    result.execution_result.execution,
    QualifiedProductionApplicabilityExecutionDispatchResult,
  )

  assert isinstance(
    result.execution_result.execution.execution,
    TwoPremiseProductionApplicationExecutionResult,
  )


def test_phase108_6_preserves_target_identity_across_handoff():
  resolution, target = (
    _first_target_for_family(
      _SECOND_FAMILY
    )
  )

  result = (
    execute_repository_generator_executable_target(
      resolution,
      target,
    )
  )

  assert (
    result.execution_result.applicability_result
    is resolution.applicability_result
  )

  assert (
    result.execution_result.representative
    is target.representative
  )

  assert (
    result.execution_result.execution.candidate
    is target.representative
  )

  assert (
    result.execution_result.execution.family_name
    == target.family_name
  )

  selected_group = (
    result.execution_result.selected_group
  )

  assert selected_group is not None

  assert (
    selected_group.root_entry
    is target.root_entry
  )

  assert (
    selected_group.source_step
    is target.source_step
  )

  assert (
    selected_group.family_name
    == target.family_name
  )


def test_phase108_6_does_not_require_rebuilt_group_identity():
  resolution, target = (
    _first_target_for_family(
      _SECOND_FAMILY
    )
  )

  result = (
    execute_repository_generator_executable_target(
      resolution,
      target,
    )
  )

  assert (
    result.execution_result.selected_group
    is not target.group
  )

  assert (
    result.execution_result.representative
    is target.representative
  )


def test_phase108_6_preserves_target_goal():
  resolution, target = (
    _first_target_for_family(
      _FIRST_FAMILY
    )
  )

  result = (
    execute_repository_generator_executable_target(
      resolution,
      target,
    )
  )

  assert (
    result.execution_result.execution.goal
    == target.goal
  )

  assert (
    result.execution_result.execution.goal
    is target.target_step.conclusion
  )


def test_phase108_6_rejects_non_resolution():
  resolution, target = (
    _first_target_for_family(
      _FIRST_FAMILY
    )
  )

  assert resolution is not None

  with pytest.raises(
    TypeError,
    match=(
      "resolution must be a "
      "StandardRepositoryGeneratorExecutableTargetResolution"
    ),
  ):
    execute_repository_generator_executable_target(
      object(),
      target,
    )


def test_phase108_6_rejects_non_target():
  resolution = (
    _phase108_6_resolution()
  )

  with pytest.raises(
    TypeError,
    match=(
      "target must be a "
      "RepositoryGeneratorExecutableTarget"
    ),
  ):
    execute_repository_generator_executable_target(
      resolution,
      object(),
    )


def test_phase108_6_rejects_foreign_target_identity():
  first_resolution, first_target = (
    _first_target_for_family(
      _FIRST_FAMILY
    )
  )

  second_resolution = (
    resolve_standard_repository_generator_executable_targets_input(
      "nu_prime"
    )
  )

  assert (
    second_resolution
    is not first_resolution
  )

  with pytest.raises(
    ValueError,
    match=(
      "target must be an original target from resolution"
    ),
  ):
    execute_repository_generator_executable_target(
      second_resolution,
      first_target,
    )

from functools import lru_cache

import pytest

from proof import (
  ProofStep,
)
from repository_generator_user_execution_handoff import (
  execute_repository_generator_executable_target,
)
from repository_generator_user_execution_proof_step import (
  RepositoryGeneratorExecutedProofStepResult,
  extract_repository_generator_executed_target_proof_step,
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
def _phase108_7_resolution():
  return (
    resolve_standard_repository_generator_executable_targets_input(
      "nu_prime"
    )
  )


def _first_target_for_family(
  family_name,
):
  resolution = (
    _phase108_7_resolution()
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


@lru_cache(maxsize=2)
def _phase108_7_execution(
  family_name,
):
  resolution, target = (
    _first_target_for_family(
      family_name
    )
  )

  execution_result = (
    execute_repository_generator_executable_target(
      resolution,
      target,
    )
  )

  return (
    target,
    execution_result,
  )


def test_phase108_7_extracts_first_family_final_proof_step():
  target, execution_result = (
    _phase108_7_execution(
      _FIRST_FAMILY
    )
  )

  result = (
    extract_repository_generator_executed_target_proof_step(
      execution_result
    )
  )

  assert isinstance(
    result,
    RepositoryGeneratorExecutedProofStepResult,
  )

  assert isinstance(
    result.proof_step,
    ProofStep,
  )

  assert (
    result.execution_result
    is execution_result
  )

  assert (
    result.target
    is target
  )


def test_phase108_7_extracts_second_family_final_proof_step():
  target, execution_result = (
    _phase108_7_execution(
      _SECOND_FAMILY
    )
  )

  result = (
    extract_repository_generator_executed_target_proof_step(
      execution_result
    )
  )

  assert isinstance(
    result.proof_step,
    ProofStep,
  )

  assert (
    result.target
    is target
  )


def test_phase108_7_preserves_nested_goal_step_identity():
  _target, execution_result = (
    _phase108_7_execution(
      _SECOND_FAMILY
    )
  )

  result = (
    extract_repository_generator_executed_target_proof_step(
      execution_result
    )
  )

  nested_goal_step = (
    execution_result
    .execution_result
    .execution
    .execution
    .execution
    .execution_result
    .repository_inference_result
    .goal_step
  )

  assert nested_goal_step is not None

  assert (
    result.proof_step
    is nested_goal_step
  )


def test_phase108_7_final_proof_step_conclusion_matches_target_goal():
  for family_name in (
    _FIRST_FAMILY,
    _SECOND_FAMILY,
  ):
    target, execution_result = (
      _phase108_7_execution(
        family_name
      )
    )

    result = (
      extract_repository_generator_executed_target_proof_step(
        execution_result
      )
    )

    assert (
      result.proof_step.conclusion
      == target.goal
    )

    assert (
      result.goal
      is target.target_step.conclusion
    )


def test_phase108_7_final_proof_step_preserves_target_inference_rule_identity():
  for family_name in (
    _FIRST_FAMILY,
    _SECOND_FAMILY,
  ):
    target, execution_result = (
      _phase108_7_execution(
        family_name
      )
    )

    result = (
      extract_repository_generator_executed_target_proof_step(
        execution_result
      )
    )

    assert (
      result.proof_step.inference_rule
      is target
      .representative
      .candidate
      .inference_rule
    )


def test_phase108_7_second_family_final_step_preserves_recovered_premises():
  _target, execution_result = (
    _phase108_7_execution(
      _SECOND_FAMILY
    )
  )

  result = (
    extract_repository_generator_executed_target_proof_step(
      execution_result
    )
  )

  two_premise_execution = (
    execution_result
    .execution_result
    .execution
    .execution
  )

  premise_tuple = (
    two_premise_execution
    .recovery
    .premise_tuple
  )

  assert premise_tuple is not None

  assert (
    result.proof_step.premises
    == premise_tuple
  )


def test_phase108_7_does_not_return_repository_target_step_identity():
  for family_name in (
    _FIRST_FAMILY,
    _SECOND_FAMILY,
  ):
    target, execution_result = (
      _phase108_7_execution(
        family_name
      )
    )

    result = (
      extract_repository_generator_executed_target_proof_step(
        execution_result
      )
    )

    assert (
      result.proof_step
      is not target.target_step
    )


def test_phase108_7_rejects_non_execution_result():
  with pytest.raises(
    TypeError,
    match=(
      "execution_result must be a "
      "RepositoryGeneratorExecutableTargetExecutionResult"
    ),
  ):
    extract_repository_generator_executed_target_proof_step(
      object()
    )

from functools import lru_cache

import pytest

from repository_generator_user_execution_facade import (
  RepositoryGeneratorUserExecutionWorkflowResult,
  RepositoryGeneratorUserExecutionWorkflowStatus,
  run_standard_repository_generator_user_execution_workflow,
)


@lru_cache(maxsize=1)
def _phase108_9_ambiguous_result():
  return (
    run_standard_repository_generator_user_execution_workflow(
      "nu_prime"
    )
  )


def test_phase108_9_nu_prime_without_selection_is_ambiguous():
  result = (
    _phase108_9_ambiguous_result()
  )

  assert isinstance(
    result,
    RepositoryGeneratorUserExecutionWorkflowResult,
  )

  assert (
    result.status
    is RepositoryGeneratorUserExecutionWorkflowStatus.AMBIGUOUS
  )

  assert len(
    result.resolution.targets
  ) > 1

  assert result.selected_target is None
  assert result.execution_result is None
  assert result.proof_result is None
  assert result.presentation is None
  assert result.markdown is None


def test_phase108_9_explicit_candidate_number_executes_selected_target():
  ambiguous_result = (
    _phase108_9_ambiguous_result()
  )

  result = (
    run_standard_repository_generator_user_execution_workflow(
      "nu_prime",
      candidate_number=1,
    )
  )

  assert (
    result.status
    is RepositoryGeneratorUserExecutionWorkflowStatus.EXECUTED
  )

  assert result.selected_target is not None

  assert (
    result.selected_target.family_name
    == ambiguous_result
    .resolution
    .targets[
      0
    ]
    .family_name
  )

  assert (
    result.selected_target.goal
    == ambiguous_result
    .resolution
    .targets[
      0
    ]
    .goal
  )


def test_phase108_9_execution_chain_preserves_identity_within_one_workflow():
  result = (
    run_standard_repository_generator_user_execution_workflow(
      "nu_prime",
      candidate_number=1,
    )
  )

  assert result.selected_target is not None
  assert result.execution_result is not None
  assert result.proof_result is not None
  assert result.presentation is not None
  assert result.markdown is not None

  assert (
    result.execution_result.resolution
    is result.resolution
  )

  assert (
    result.execution_result.target
    is result.selected_target
  )

  assert (
    result.proof_result.execution_result
    is result.execution_result
  )

  assert (
    result.presentation.source_result
    is result.proof_result
  )

  assert (
    result.presentation.proof_step
    is result.proof_result.proof_step
  )


def test_phase108_9_executed_result_contains_minimal_user_facing_markdown():
  result = (
    run_standard_repository_generator_user_execution_workflow(
      "nu_prime",
      candidate_number=1,
    )
  )

  assert result.markdown is not None

  assert result.markdown.startswith(
    "# Result\n"
  )

  assert "\n## Proof\n" in result.markdown
  assert "\nRule: " in result.markdown
  assert "\nConclusion:\n" in result.markdown


def test_phase108_9_candidate_number_is_one_based():
  ambiguous_result = (
    _phase108_9_ambiguous_result()
  )

  first_result = (
    run_standard_repository_generator_user_execution_workflow(
      "nu_prime",
      candidate_number=1,
    )
  )

  assert first_result.selected_target is not None

  assert (
    first_result.selected_target.family_name
    == ambiguous_result
    .resolution
    .targets[
      0
    ]
    .family_name
  )

  assert (
    first_result.selected_target.goal
    == ambiguous_result
    .resolution
    .targets[
      0
    ]
    .goal
  )


def test_phase108_9_rejects_zero_candidate_number():
  with pytest.raises(
    ValueError,
    match="candidate_number must be positive",
  ):
    run_standard_repository_generator_user_execution_workflow(
      "nu_prime",
      candidate_number=0,
    )


def test_phase108_9_rejects_non_integer_candidate_number():
  with pytest.raises(
    TypeError,
    match="candidate_number must be an int or None",
  ):
    run_standard_repository_generator_user_execution_workflow(
      "nu_prime",
      candidate_number="1",
    )


def test_phase108_9_rejects_candidate_number_above_target_count():
  ambiguous_result = (
    _phase108_9_ambiguous_result()
  )

  with pytest.raises(
    ValueError,
    match=(
      "candidate_number exceeds executable target count"
    ),
  ):
    run_standard_repository_generator_user_execution_workflow(
      "nu_prime",
      candidate_number=(
        len(
          ambiguous_result.resolution.targets
        )
        + 1
      ),
    )


def test_phase108_9_preserves_existing_invalid_generator_error():
  with pytest.raises(
    ValueError,
    match="unsupported generator family",
  ):
    run_standard_repository_generator_user_execution_workflow(
      "phase108_unknown_generator"
    )

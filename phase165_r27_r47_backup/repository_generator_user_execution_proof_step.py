from dataclasses import dataclass

from proof import (
  ProofStep,
)
from repository_generator_user_execution_handoff import (
  RepositoryGeneratorExecutableTargetExecutionResult,
)


@dataclass(frozen=True)
class RepositoryGeneratorExecutedProofStepResult:
  execution_result: RepositoryGeneratorExecutableTargetExecutionResult
  proof_step: ProofStep

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.execution_result,
      RepositoryGeneratorExecutableTargetExecutionResult,
    ):
      raise TypeError(
        "execution_result must be a "
        "RepositoryGeneratorExecutableTargetExecutionResult"
      )

    if not isinstance(
      self.proof_step,
      ProofStep,
    ):
      raise TypeError(
        "proof_step must be a ProofStep"
      )

    target = (
      self.execution_result.target
    )

    if (
      self.proof_step.conclusion
      != target.goal
    ):
      raise ValueError(
        "proof_step conclusion must match target goal"
      )

    expected_inference_rule = (
      target
      .representative
      .candidate
      .inference_rule
    )

    if (
      self.proof_step.inference_rule
      is not expected_inference_rule
    ):
      raise ValueError(
        "proof_step must preserve target inference_rule identity"
      )

    nested_goal_step = (
      self.execution_result
      .execution_result
      .execution
      .execution
      .execution
      .execution_result
      .repository_inference_result
      .goal_step
    )

    if (
      nested_goal_step
      is not self.proof_step
    ):
      raise ValueError(
        "proof_step must be the executed repository goal_step"
      )

  @property
  def target(
    self,
  ):
    return self.execution_result.target

  @property
  def goal(
    self,
  ):
    return self.target.goal


def extract_repository_generator_executed_target_proof_step(
  execution_result,
) -> RepositoryGeneratorExecutedProofStepResult:
  if not isinstance(
    execution_result,
    RepositoryGeneratorExecutableTargetExecutionResult,
  ):
    raise TypeError(
      "execution_result must be a "
      "RepositoryGeneratorExecutableTargetExecutionResult"
    )

  dispatch_result = (
    execution_result
    .execution_result
    .execution
  )

  if dispatch_result is None:
    raise ValueError(
      "execution_result must contain dispatched execution"
    )

  family_execution = (
    dispatch_result.execution
  )

  handoff_execution = (
    family_execution.execution
  )

  bounded_execution = (
    handoff_execution.execution_result
  )

  repository_inference_result = (
    bounded_execution.repository_inference_result
  )

  if repository_inference_result is None:
    raise ValueError(
      "executed target must contain repository inference result"
    )

  goal_step = (
    repository_inference_result.goal_step
  )

  if goal_step is None:
    raise ValueError(
      "executed target must contain a final goal_step"
    )

  return RepositoryGeneratorExecutedProofStepResult(
    execution_result=execution_result,
    proof_step=goal_step,
  )

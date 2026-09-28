from dataclasses import dataclass
from enum import Enum

from repository_generator_user_execution_handoff import (
  RepositoryGeneratorExecutableTargetExecutionResult,
  execute_repository_generator_executable_target,
)
from repository_generator_user_execution_presentation import (
  RepositoryGeneratorUserExecutionPresentation,
  build_repository_generator_user_execution_presentation,
)
from repository_generator_user_execution_proof_step import (
  RepositoryGeneratorExecutedProofStepResult,
  extract_repository_generator_executed_target_proof_step,
)
from repository_generator_user_execution_renderer import (
  render_repository_generator_user_execution_markdown,
)
from repository_generator_user_execution_resolver import (
  RepositoryGeneratorExecutableTarget,
  StandardRepositoryGeneratorExecutableTargetResolution,
  resolve_standard_repository_generator_executable_targets_input,
)


class RepositoryGeneratorUserExecutionWorkflowStatus(
  Enum
):
  NONE = "none"
  AMBIGUOUS = "ambiguous"
  EXECUTED = "executed"


@dataclass(frozen=True)
class RepositoryGeneratorUserExecutionWorkflowResult:
  resolution: StandardRepositoryGeneratorExecutableTargetResolution
  status: RepositoryGeneratorUserExecutionWorkflowStatus
  selected_target: RepositoryGeneratorExecutableTarget | None = None
  execution_result: (
    RepositoryGeneratorExecutableTargetExecutionResult
    | None
  ) = None
  proof_result: (
    RepositoryGeneratorExecutedProofStepResult
    | None
  ) = None
  presentation: (
    RepositoryGeneratorUserExecutionPresentation
    | None
  ) = None
  markdown: str | None = None

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.resolution,
      StandardRepositoryGeneratorExecutableTargetResolution,
    ):
      raise TypeError(
        "resolution must be a "
        "StandardRepositoryGeneratorExecutableTargetResolution"
      )

    if not isinstance(
      self.status,
      RepositoryGeneratorUserExecutionWorkflowStatus,
    ):
      raise TypeError(
        "status must be a "
        "RepositoryGeneratorUserExecutionWorkflowStatus"
      )

    execution_fields = (
      self.selected_target,
      self.execution_result,
      self.proof_result,
      self.presentation,
      self.markdown,
    )

    if (
      self.status
      is not RepositoryGeneratorUserExecutionWorkflowStatus.EXECUTED
    ):
      if any(
        value is not None
        for value in execution_fields
      ):
        raise ValueError(
          "non-executed workflow result must not "
          "contain execution output"
        )

      if (
        self.status
        is RepositoryGeneratorUserExecutionWorkflowStatus.NONE
        and self.resolution.targets
      ):
        raise ValueError(
          "NONE status requires zero executable targets"
        )

      if (
        self.status
        is RepositoryGeneratorUserExecutionWorkflowStatus.AMBIGUOUS
        and len(
          self.resolution.targets
        ) <= 1
      ):
        raise ValueError(
          "AMBIGUOUS status requires multiple executable targets"
        )

      return

    if not isinstance(
      self.selected_target,
      RepositoryGeneratorExecutableTarget,
    ):
      raise TypeError(
        "selected_target must be a "
        "RepositoryGeneratorExecutableTarget "
        "for EXECUTED status"
      )

    if not any(
      target is self.selected_target
      for target in self.resolution.targets
    ):
      raise ValueError(
        "selected_target must be an original target "
        "from resolution"
      )

    if not isinstance(
      self.execution_result,
      RepositoryGeneratorExecutableTargetExecutionResult,
    ):
      raise TypeError(
        "execution_result must be a "
        "RepositoryGeneratorExecutableTargetExecutionResult "
        "for EXECUTED status"
      )

    if (
      self.execution_result.target
      is not self.selected_target
    ):
      raise ValueError(
        "execution_result target must be selected_target"
      )

    if (
      self.execution_result.resolution
      is not self.resolution
    ):
      raise ValueError(
        "execution_result resolution must preserve resolution identity"
      )

    if not isinstance(
      self.proof_result,
      RepositoryGeneratorExecutedProofStepResult,
    ):
      raise TypeError(
        "proof_result must be a "
        "RepositoryGeneratorExecutedProofStepResult "
        "for EXECUTED status"
      )

    if (
      self.proof_result.execution_result
      is not self.execution_result
    ):
      raise ValueError(
        "proof_result must preserve execution_result identity"
      )

    if not isinstance(
      self.presentation,
      RepositoryGeneratorUserExecutionPresentation,
    ):
      raise TypeError(
        "presentation must be a "
        "RepositoryGeneratorUserExecutionPresentation "
        "for EXECUTED status"
      )

    if (
      self.presentation.source_result
      is not self.proof_result
    ):
      raise ValueError(
        "presentation must preserve proof_result identity"
      )

    if not isinstance(
      self.markdown,
      str,
    ):
      raise TypeError(
        "markdown must be a str for EXECUTED status"
      )

    if not self.markdown:
      raise ValueError(
        "markdown must not be empty for EXECUTED status"
      )


def _validate_candidate_number(
  candidate_number,
) -> None:
  if candidate_number is None:
    return

  if (
    isinstance(
      candidate_number,
      bool,
    )
    or not isinstance(
      candidate_number,
      int,
    )
  ):
    raise TypeError(
      "candidate_number must be an int or None"
    )

  if candidate_number < 1:
    raise ValueError(
      "candidate_number must be positive"
    )


def _execute_resolved_target(
  resolution,
  target,
  max_depth,
  retry_policy,
) -> RepositoryGeneratorUserExecutionWorkflowResult:
  execution_result = (
    execute_repository_generator_executable_target(
      resolution,
      target,
      max_depth=max_depth,
      retry_policy=retry_policy,
    )
  )

  proof_result = (
    extract_repository_generator_executed_target_proof_step(
      execution_result
    )
  )

  presentation = (
    build_repository_generator_user_execution_presentation(
      proof_result
    )
  )

  markdown = (
    render_repository_generator_user_execution_markdown(
      presentation
    )
  )

  return RepositoryGeneratorUserExecutionWorkflowResult(
    resolution=resolution,
    status=(
      RepositoryGeneratorUserExecutionWorkflowStatus.EXECUTED
    ),
    selected_target=target,
    execution_result=execution_result,
    proof_result=proof_result,
    presentation=presentation,
    markdown=markdown,
  )


def run_standard_repository_generator_user_execution_workflow(
  generator_input,
  candidate_number=None,
  max_depth=2,
  retry_policy=None,
) -> RepositoryGeneratorUserExecutionWorkflowResult:
  if not isinstance(
    generator_input,
    str,
  ):
    raise TypeError(
      "generator_input must be a str"
    )

  _validate_candidate_number(
    candidate_number
  )

  resolution = (
    resolve_standard_repository_generator_executable_targets_input(
      generator_input
    )
  )

  target_count = len(
    resolution.targets
  )

  if target_count == 0:
    if candidate_number is not None:
      raise ValueError(
        "candidate_number cannot select from zero executable targets"
      )

    return RepositoryGeneratorUserExecutionWorkflowResult(
      resolution=resolution,
      status=(
        RepositoryGeneratorUserExecutionWorkflowStatus.NONE
      ),
    )

  if candidate_number is None:
    if target_count > 1:
      return RepositoryGeneratorUserExecutionWorkflowResult(
        resolution=resolution,
        status=(
          RepositoryGeneratorUserExecutionWorkflowStatus.AMBIGUOUS
        ),
      )

    target = resolution.targets[
      0
    ]
  else:
    if candidate_number > target_count:
      raise ValueError(
        "candidate_number exceeds executable target count"
      )

    target = resolution.targets[
      candidate_number - 1
    ]

  return _execute_resolved_target(
    resolution,
    target,
    max_depth,
    retry_policy,
  )

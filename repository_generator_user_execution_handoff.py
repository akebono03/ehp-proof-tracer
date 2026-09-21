from dataclasses import dataclass

from repository_generator_standard_qualified_execution_facade import (
  StandardRepositoryGeneratorMultiFamilyExecutionFacadeResult,
  execute_standard_repository_generator_applicability_result_by_root_source_and_family,
)
from repository_generator_user_execution_resolver import (
  RepositoryGeneratorExecutableTarget,
  StandardRepositoryGeneratorExecutableTargetResolution,
)


@dataclass(frozen=True)
class RepositoryGeneratorExecutableTargetExecutionResult:
  resolution: StandardRepositoryGeneratorExecutableTargetResolution
  target: RepositoryGeneratorExecutableTarget
  execution_result: StandardRepositoryGeneratorMultiFamilyExecutionFacadeResult

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
      self.target,
      RepositoryGeneratorExecutableTarget,
    ):
      raise TypeError(
        "target must be a RepositoryGeneratorExecutableTarget"
      )

    if not isinstance(
      self.execution_result,
      StandardRepositoryGeneratorMultiFamilyExecutionFacadeResult,
    ):
      raise TypeError(
        "execution_result must be a "
        "StandardRepositoryGeneratorMultiFamilyExecutionFacadeResult"
      )

    if not any(
      candidate_target is self.target
      for candidate_target in self.resolution.targets
    ):
      raise ValueError(
        "target must be an original target from resolution"
      )

    if not self.execution_result.executed:
      raise ValueError(
        "execution_result must represent an executed target"
      )

    if (
      self.execution_result.applicability_result
      is not self.resolution.applicability_result
    ):
      raise ValueError(
        "execution_result must preserve applicability_result identity"
      )

    if (
      self.execution_result.representative
      is not self.target.representative
    ):
      raise ValueError(
        "execution_result must preserve target representative identity"
      )

    selected_group = (
      self.execution_result.selected_group
    )

    if selected_group is None:
      raise ValueError(
        "execution_result must preserve a selected group"
      )

    if (
      selected_group.root_entry
      is not self.target.root_entry
    ):
      raise ValueError(
        "execution_result must preserve target root_entry identity"
      )

    if (
      selected_group.source_step
      is not self.target.source_step
    ):
      raise ValueError(
        "execution_result must preserve target source_step identity"
      )

    if (
      selected_group.family_name
      != self.target.family_name
    ):
      raise ValueError(
        "execution_result must preserve target family_name"
      )

    if (
      self.execution_result.execution is None
      or self.execution_result.execution.goal
      != self.target.goal
    ):
      raise ValueError(
        "execution_result goal must match target goal"
      )


def execute_repository_generator_executable_target(
  resolution,
  target,
  max_depth=2,
  retry_policy=None,
) -> RepositoryGeneratorExecutableTargetExecutionResult:
  if not isinstance(
    resolution,
    StandardRepositoryGeneratorExecutableTargetResolution,
  ):
    raise TypeError(
      "resolution must be a "
      "StandardRepositoryGeneratorExecutableTargetResolution"
    )

  if not isinstance(
    target,
    RepositoryGeneratorExecutableTarget,
  ):
    raise TypeError(
      "target must be a RepositoryGeneratorExecutableTarget"
    )

  if not any(
    candidate_target is target
    for candidate_target in resolution.targets
  ):
    raise ValueError(
      "target must be an original target from resolution"
    )

  execution_result = (
    execute_standard_repository_generator_applicability_result_by_root_source_and_family(
      resolution.applicability_result,
      target.root_entry,
      target.source_step,
      target.family_name,
      target.goal,
      max_depth=max_depth,
      retry_policy=retry_policy,
    )
  )

  return RepositoryGeneratorExecutableTargetExecutionResult(
    resolution=resolution,
    target=target,
    execution_result=execution_result,
  )

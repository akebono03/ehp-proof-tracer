from dataclasses import dataclass

from repository_generator_applicability_execution_orchestration import (
  FirstQualifiedProductionApplicabilityExecutionResult,
  execute_first_qualified_production_applicability_candidate,
)
from repository_generator_qualified_execution_selection import (
  RepositoryGeneratorQualifiedExecutionSelection,
  RepositoryGeneratorQualifiedExecutionSelectionStatus,
)


@dataclass(frozen=True)
class RepositoryGeneratorQualifiedExecutionHandoffResult:
  selection: RepositoryGeneratorQualifiedExecutionSelection
  goal: object
  execution: (
    FirstQualifiedProductionApplicabilityExecutionResult
    | None
  )

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.selection,
      RepositoryGeneratorQualifiedExecutionSelection,
    ):
      raise TypeError(
        "selection must be a "
        "RepositoryGeneratorQualifiedExecutionSelection"
      )

    status = self.selection.status

    if (
      status
      is RepositoryGeneratorQualifiedExecutionSelectionStatus.UNIQUE
    ):
      if not isinstance(
        self.execution,
        FirstQualifiedProductionApplicabilityExecutionResult,
      ):
        raise ValueError(
          "UNIQUE selection requires execution"
        )

      unique_candidate = (
        self.selection.unique_candidate
      )

      if (
        unique_candidate is None
        or self.execution.candidate
        is not unique_candidate
      ):
        raise ValueError(
          "execution must preserve unique candidate identity"
        )

      if self.execution.goal != self.goal:
        raise ValueError(
          "execution goal must match handoff goal"
        )

      return

    if self.execution is not None:
      raise ValueError(
        "non-UNIQUE selection must not execute"
      )

  @property
  def status(
    self,
  ) -> RepositoryGeneratorQualifiedExecutionSelectionStatus:
    return self.selection.status

  @property
  def executed(
    self,
  ) -> bool:
    return self.execution is not None


def execute_unique_qualified_repository_generator_applicability_selection(
  selection,
  goal,
  max_depth=2,
  retry_policy=None,
) -> RepositoryGeneratorQualifiedExecutionHandoffResult:
  if not isinstance(
    selection,
    RepositoryGeneratorQualifiedExecutionSelection,
  ):
    raise TypeError(
      "selection must be a "
      "RepositoryGeneratorQualifiedExecutionSelection"
    )

  if (
    selection.status
    is not RepositoryGeneratorQualifiedExecutionSelectionStatus.UNIQUE
  ):
    return RepositoryGeneratorQualifiedExecutionHandoffResult(
      selection=selection,
      goal=goal,
      execution=None,
    )

  candidate = selection.unique_candidate

  if candidate is None:
    raise ValueError(
      "UNIQUE selection requires a unique_candidate"
    )

  execution = (
    execute_first_qualified_production_applicability_candidate(
      candidate,
      goal,
      max_depth=max_depth,
      retry_policy=retry_policy,
    )
  )

  return RepositoryGeneratorQualifiedExecutionHandoffResult(
    selection=selection,
    goal=goal,
    execution=execution,
  )

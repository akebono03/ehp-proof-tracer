from dataclasses import dataclass

from repository_generator_user_execution_facade import (
  RepositoryGeneratorUserExecutionWorkflowResult,
  RepositoryGeneratorUserExecutionWorkflowStatus,
)
from repository_generator_user_execution_resolver import (
  RepositoryGeneratorExecutableTarget,
)


@dataclass(frozen=True)
class RepositoryGeneratorUserExecutionCandidatePresentation:
  source_target: RepositoryGeneratorExecutableTarget
  candidate_number: int
  conclusion: object

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.source_target,
      RepositoryGeneratorExecutableTarget,
    ):
      raise TypeError(
        "source_target must be a "
        "RepositoryGeneratorExecutableTarget"
      )

    if (
      isinstance(
        self.candidate_number,
        bool,
      )
      or not isinstance(
        self.candidate_number,
        int,
      )
    ):
      raise TypeError(
        "candidate_number must be an int"
      )

    if self.candidate_number < 1:
      raise ValueError(
        "candidate_number must be positive"
      )

    if (
      self.conclusion
      is not self.source_target.goal
    ):
      raise ValueError(
        "conclusion must preserve source_target goal identity"
      )


@dataclass(frozen=True)
class RepositoryGeneratorUserExecutionCandidateListPresentation:
  source_result: RepositoryGeneratorUserExecutionWorkflowResult
  candidates: tuple[
    RepositoryGeneratorUserExecutionCandidatePresentation,
    ...,
  ]

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.source_result,
      RepositoryGeneratorUserExecutionWorkflowResult,
    ):
      raise TypeError(
        "source_result must be a "
        "RepositoryGeneratorUserExecutionWorkflowResult"
      )

    if (
      self.source_result.status
      is not RepositoryGeneratorUserExecutionWorkflowStatus.AMBIGUOUS
    ):
      raise ValueError(
        "source_result must have AMBIGUOUS status"
      )

    if not isinstance(
      self.candidates,
      tuple,
    ):
      raise TypeError(
        "candidates must be a tuple"
      )

    source_targets = (
      self.source_result.resolution.targets
    )

    if len(
      self.candidates
    ) != len(
      source_targets
    ):
      raise ValueError(
        "candidates must match every executable target"
      )

    for index, (
      presentation,
      source_target,
    ) in enumerate(
      zip(
        self.candidates,
        source_targets,
      ),
      start=1,
    ):
      if not isinstance(
        presentation,
        RepositoryGeneratorUserExecutionCandidatePresentation,
      ):
        raise TypeError(
          "candidates must contain only "
          "RepositoryGeneratorUserExecutionCandidatePresentation "
          "objects"
        )

      if (
        presentation.source_target
        is not source_target
      ):
        raise ValueError(
          "candidate target identity must match source target order"
        )

      if (
        presentation.candidate_number
        != index
      ):
        raise ValueError(
          "candidate numbers must be consecutive and one-based"
        )


def build_repository_generator_user_execution_candidate_list_presentation(
  result,
) -> RepositoryGeneratorUserExecutionCandidateListPresentation:
  if not isinstance(
    result,
    RepositoryGeneratorUserExecutionWorkflowResult,
  ):
    raise TypeError(
      "result must be a "
      "RepositoryGeneratorUserExecutionWorkflowResult"
    )

  if (
    result.status
    is not RepositoryGeneratorUserExecutionWorkflowStatus.AMBIGUOUS
  ):
    raise ValueError(
      "result must have AMBIGUOUS status"
    )

  candidates = tuple(
    RepositoryGeneratorUserExecutionCandidatePresentation(
      source_target=target,
      candidate_number=index,
      conclusion=target.goal,
    )
    for index, target in enumerate(
      result.resolution.targets,
      start=1,
    )
  )

  return RepositoryGeneratorUserExecutionCandidateListPresentation(
    source_result=result,
    candidates=candidates,
  )

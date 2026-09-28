from dataclasses import dataclass

from repository_operation_query_proof_replay import (
  RepositoryOperationQueryProofReplayResult,
  RepositoryOperationQueryProofReplayStep,
)


@dataclass(frozen=True)
class RepositoryOperationQueryProofReplayPresentation:
  source_result: RepositoryOperationQueryProofReplayResult
  conclusion: object
  conclusion_latex: str
  steps: tuple[
    RepositoryOperationQueryProofReplayStep,
    ...,
  ]

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.source_result,
      RepositoryOperationQueryProofReplayResult,
    ):
      raise TypeError(
        "source_result must be a "
        "RepositoryOperationQueryProofReplayResult"
      )

    if (
      self.conclusion
      is not self.source_result.root_step.conclusion
    ):
      raise ValueError(
        "conclusion must preserve root-step "
        "conclusion identity"
      )

    if not isinstance(
      self.conclusion_latex,
      str,
    ):
      raise TypeError(
        "conclusion_latex must be a str"
      )

    if not self.conclusion_latex:
      raise ValueError(
        "conclusion_latex must not be empty"
      )

    if (
      self.steps
      != self.source_result.steps
    ):
      raise ValueError(
        "steps must match source_result steps"
      )


def build_repository_operation_query_proof_replay_presentation(
  result: RepositoryOperationQueryProofReplayResult,
) -> RepositoryOperationQueryProofReplayPresentation:
  if not isinstance(
    result,
    RepositoryOperationQueryProofReplayResult,
  ):
    raise TypeError(
      "result must be a "
      "RepositoryOperationQueryProofReplayResult"
    )

  return RepositoryOperationQueryProofReplayPresentation(
    source_result=result,
    conclusion=result.root_step.conclusion,
    conclusion_latex=(
      result.source_item.statement_latex
    ),
    steps=result.steps,
  )

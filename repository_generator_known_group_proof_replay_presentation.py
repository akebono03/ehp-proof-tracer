from dataclasses import dataclass

from expression import (
  GeneratorSymbol,
)
from repository_generator_known_group_proof_replay import (
  RepositoryGeneratorKnownGroupProofReplayResult,
  RepositoryGeneratorKnownGroupProofReplayStep,
)


@dataclass(frozen=True)
class RepositoryGeneratorKnownGroupProofReplayPresentation:
  source_result: RepositoryGeneratorKnownGroupProofReplayResult
  generator: GeneratorSymbol
  conclusion: object
  steps: tuple[
    RepositoryGeneratorKnownGroupProofReplayStep,
    ...,
  ]

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.source_result,
      RepositoryGeneratorKnownGroupProofReplayResult,
    ):
      raise TypeError(
        "source_result must be a "
        "RepositoryGeneratorKnownGroupProofReplayResult"
      )

    if (
      self.generator
      is not self.source_result.generator
    ):
      raise ValueError(
        "generator must preserve source_result generator identity"
      )

    if (
      self.conclusion
      is not self.source_result.root_step.conclusion
    ):
      raise ValueError(
        "conclusion must preserve root-step conclusion identity"
      )

    if (
      self.steps
      != self.source_result.steps
    ):
      raise ValueError(
        "steps must match source_result steps"
      )


def build_repository_generator_known_group_proof_replay_presentation(
  result,
) -> RepositoryGeneratorKnownGroupProofReplayPresentation:
  if not isinstance(
    result,
    RepositoryGeneratorKnownGroupProofReplayResult,
  ):
    raise TypeError(
      "result must be a "
      "RepositoryGeneratorKnownGroupProofReplayResult"
    )

  return RepositoryGeneratorKnownGroupProofReplayPresentation(
    source_result=result,
    generator=result.generator,
    conclusion=result.root_step.conclusion,
    steps=result.steps,
  )

from dataclasses import dataclass

from expression import GeneratorSymbol
from proof_repository import ProofRepository
from repository_element_exploration import (
  RepositoryGeneratorExplorationResult,
  build_repository_generator_exploration,
)
from repository_element_presentation import (
  RepositoryGeneratorExplorationPresentation,
  build_repository_generator_exploration_presentation,
)
from repository_element_renderer import (
  render_repository_generator_exploration_markdown,
)


@dataclass(frozen=True)
class RepositoryGeneratorExplorationReport:
  exploration: RepositoryGeneratorExplorationResult
  presentation: RepositoryGeneratorExplorationPresentation
  markdown: str

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.exploration,
      RepositoryGeneratorExplorationResult,
    ):
      raise TypeError(
        "exploration must be a "
        "RepositoryGeneratorExplorationResult"
      )

    if not isinstance(
      self.presentation,
      RepositoryGeneratorExplorationPresentation,
    ):
      raise TypeError(
        "presentation must be a "
        "RepositoryGeneratorExplorationPresentation"
      )

    if (
      self.presentation.source_result
      is not self.exploration
    ):
      raise ValueError(
        "presentation source identity must match "
        "exploration"
      )

    if not isinstance(
      self.markdown,
      str,
    ):
      raise TypeError(
        "markdown must be a str"
      )


def explore_repository_generator(
  repository: ProofRepository,
  generator: GeneratorSymbol,
) -> RepositoryGeneratorExplorationReport:
  exploration = (
    build_repository_generator_exploration(
      repository,
      generator,
    )
  )

  presentation = (
    build_repository_generator_exploration_presentation(
      exploration
    )
  )

  markdown = (
    render_repository_generator_exploration_markdown(
      presentation
    )
  )

  return RepositoryGeneratorExplorationReport(
    exploration=exploration,
    presentation=presentation,
    markdown=markdown,
  )

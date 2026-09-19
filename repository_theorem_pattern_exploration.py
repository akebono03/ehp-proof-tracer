from dataclasses import dataclass

from expression import GeneratorSymbol
from proof_repository import ProofRepository
from repository_element_lookup import (
  RepositoryGeneratorOccurrence,
  find_repository_generator_occurrences,
)


@dataclass(frozen=True)
class RepositoryTheoremPatternOccurrence:
  source_occurrence: RepositoryGeneratorOccurrence
  statement: object

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.source_occurrence,
      RepositoryGeneratorOccurrence,
    ):
      raise TypeError(
        "source_occurrence must be a "
        "RepositoryGeneratorOccurrence"
      )

    if (
      self.statement
      is not self.source_occurrence.entry.step.conclusion
    ):
      raise ValueError(
        "statement must be the source occurrence "
        "entry conclusion"
      )

  @property
  def statement_type(
    self,
  ) -> type:
    return type(
      self.statement
    )


def build_repository_theorem_pattern_occurrences(
  repository: ProofRepository,
  generator: GeneratorSymbol,
) -> tuple[
  RepositoryTheoremPatternOccurrence,
  ...,
]:
  if not isinstance(
    repository,
    ProofRepository,
  ):
    raise TypeError(
      "repository must be a ProofRepository"
    )

  if not isinstance(
    generator,
    GeneratorSymbol,
  ):
    raise TypeError(
      "generator must be a GeneratorSymbol"
    )

  occurrences = (
    find_repository_generator_occurrences(
      repository,
      generator,
    )
  )

  return tuple(
    RepositoryTheoremPatternOccurrence(
      source_occurrence=occurrence,
      statement=occurrence.entry.step.conclusion,
    )
    for occurrence in occurrences
  )

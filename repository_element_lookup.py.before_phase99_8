from expression import GeneratorSymbol
from proof_repository import (
  ProofRepository,
  ProofRepositoryEntry,
)
from structural_containment import (
  contains_generator_symbol,
)


def find_repository_entries_by_conclusion_generator(
  repository: ProofRepository,
  generator: GeneratorSymbol,
) -> tuple[
  ProofRepositoryEntry,
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

  return tuple(
    entry
    for entry in repository.entries()
    if contains_generator_symbol(
      entry.step.conclusion,
      generator,
    )
  )

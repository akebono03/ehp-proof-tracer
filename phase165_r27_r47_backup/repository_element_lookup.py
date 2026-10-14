from dataclasses import dataclass

from expression import GeneratorSymbol
from generator_occurrence_roles import (
  GeneratorOccurrenceRole,
  classify_generator_occurrence_roles,
)
from proof_repository import (
  ProofRepository,
  ProofRepositoryEntry,
)
from structural_containment import (
  contains_generator_symbol,
  find_generator_occurrence_paths,
)


@dataclass(frozen=True)
class RepositoryGeneratorOccurrence:
  entry: ProofRepositoryEntry
  path: tuple[
    str,
    ...,
  ]
  matched_generator: GeneratorSymbol
  roles: tuple[
    GeneratorOccurrenceRole,
    ...,
  ] = ()

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.entry,
      ProofRepositoryEntry,
    ):
      raise TypeError(
        "entry must be a ProofRepositoryEntry"
      )

    if not isinstance(
      self.path,
      tuple,
    ):
      raise TypeError(
        "path must be a tuple"
      )

    for segment in self.path:
      if not isinstance(
        segment,
        str,
      ):
        raise TypeError(
          "path must contain only str segments"
        )

    if not isinstance(
      self.matched_generator,
      GeneratorSymbol,
    ):
      raise TypeError(
        "matched_generator must be a GeneratorSymbol"
      )

    if not isinstance(
      self.roles,
      tuple,
    ):
      raise TypeError(
        "roles must be a tuple"
      )

    for role in self.roles:
      if not isinstance(
        role,
        GeneratorOccurrenceRole,
      ):
        raise TypeError(
          "roles must contain only "
          "GeneratorOccurrenceRole values"
        )


def _value_at_structural_path(
  value,
  path: tuple[
    str,
    ...,
  ],
):
  current = value

  for segment in path:
    if isinstance(
      current,
      tuple,
    ):
      current = current[
        int(
          segment
        )
      ]
      continue

    current = getattr(
      current,
      segment,
    )

  return current


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


def find_repository_generator_occurrences(
  repository: ProofRepository,
  generator: GeneratorSymbol,
) -> tuple[
  RepositoryGeneratorOccurrence,
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

  occurrences = []

  for entry in repository.entries():
    paths = find_generator_occurrence_paths(
      entry.step.conclusion,
      generator,
    )

    for path in paths:
      matched_generator = (
        _value_at_structural_path(
          entry.step.conclusion,
          path,
        )
      )

      if not isinstance(
        matched_generator,
        GeneratorSymbol,
      ):
        raise ValueError(
          "generator occurrence path must "
          "resolve to a GeneratorSymbol"
        )

      roles = (
        classify_generator_occurrence_roles(
          entry.step.conclusion,
          path,
        )
      )

      occurrences.append(
        RepositoryGeneratorOccurrence(
          entry=entry,
          path=path,
          matched_generator=matched_generator,
          roles=roles,
        )
      )

  return tuple(
    occurrences
  )


def find_repository_generator_occurrences_by_role(
  repository: ProofRepository,
  generator: GeneratorSymbol,
  role: GeneratorOccurrenceRole,
) -> tuple[
  RepositoryGeneratorOccurrence,
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

  if not isinstance(
    role,
    GeneratorOccurrenceRole,
  ):
    raise TypeError(
      "role must be a GeneratorOccurrenceRole"
    )

  return tuple(
    occurrence
    for occurrence in (
      find_repository_generator_occurrences(
        repository,
        generator,
      )
    )
    if role in occurrence.roles
  )

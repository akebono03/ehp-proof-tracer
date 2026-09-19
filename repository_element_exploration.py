from dataclasses import dataclass

from expression import GeneratorSymbol
from generator_occurrence_roles import (
  GeneratorOccurrenceRole,
)
from proof_repository import ProofRepository
from repository_element_lookup import (
  RepositoryGeneratorOccurrence,
  find_repository_generator_occurrences,
)


@dataclass(frozen=True)
class RepositoryGeneratorExplorationResult:
  generator: GeneratorSymbol
  occurrences: tuple[
    RepositoryGeneratorOccurrence,
    ...,
  ]
  toda_bracket_occurrences: tuple[
    RepositoryGeneratorOccurrence,
    ...,
  ]
  map_input_occurrences: tuple[
    RepositoryGeneratorOccurrence,
    ...,
  ]
  group_generator_occurrences: tuple[
    RepositoryGeneratorOccurrence,
    ...,
  ]
  composition_left_occurrences: tuple[
    RepositoryGeneratorOccurrence,
    ...,
  ]
  composition_right_occurrences: tuple[
    RepositoryGeneratorOccurrence,
    ...,
  ]

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.generator,
      GeneratorSymbol,
    ):
      raise TypeError(
        "generator must be a GeneratorSymbol"
      )

    fields = (
      (
        "occurrences",
        self.occurrences,
      ),
      (
        "toda_bracket_occurrences",
        self.toda_bracket_occurrences,
      ),
      (
        "map_input_occurrences",
        self.map_input_occurrences,
      ),
      (
        "group_generator_occurrences",
        self.group_generator_occurrences,
      ),
      (
        "composition_left_occurrences",
        self.composition_left_occurrences,
      ),
      (
        "composition_right_occurrences",
        self.composition_right_occurrences,
      ),
    )

    for name, occurrences in fields:
      if not isinstance(
        occurrences,
        tuple,
      ):
        raise TypeError(
          f"{name} must be a tuple"
        )

      for occurrence in occurrences:
        if not isinstance(
          occurrence,
          RepositoryGeneratorOccurrence,
        ):
          raise TypeError(
            f"{name} must contain only "
            "RepositoryGeneratorOccurrence values"
          )


def _has_any_role(
  occurrence: RepositoryGeneratorOccurrence,
  roles: tuple[
    GeneratorOccurrenceRole,
    ...,
  ],
) -> bool:
  return any(
    role in occurrence.roles
    for role in roles
  )


def build_repository_generator_exploration(
  repository: ProofRepository,
  generator: GeneratorSymbol,
) -> RepositoryGeneratorExplorationResult:
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

  toda_roles = (
    GeneratorOccurrenceRole.TODA_BRACKET_FIRST,
    GeneratorOccurrenceRole.TODA_BRACKET_SECOND,
    GeneratorOccurrenceRole.TODA_BRACKET_THIRD,
  )

  return RepositoryGeneratorExplorationResult(
    generator=generator,
    occurrences=occurrences,
    toda_bracket_occurrences=tuple(
      occurrence
      for occurrence in occurrences
      if _has_any_role(
        occurrence,
        toda_roles,
      )
    ),
    map_input_occurrences=tuple(
      occurrence
      for occurrence in occurrences
      if (
        GeneratorOccurrenceRole.MAP_INPUT
        in occurrence.roles
      )
    ),
    group_generator_occurrences=tuple(
      occurrence
      for occurrence in occurrences
      if (
        GeneratorOccurrenceRole.GROUP_GENERATOR
        in occurrence.roles
      )
    ),
    composition_left_occurrences=tuple(
      occurrence
      for occurrence in occurrences
      if (
        GeneratorOccurrenceRole.COMPOSITION_LEFT
        in occurrence.roles
      )
    ),
    composition_right_occurrences=tuple(
      occurrence
      for occurrence in occurrences
      if (
        GeneratorOccurrenceRole.COMPOSITION_RIGHT
        in occurrence.roles
      )
    ),
  )

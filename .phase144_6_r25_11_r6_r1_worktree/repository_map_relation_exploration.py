from dataclasses import dataclass

from expression import (
  GeneratorSymbol,
  MapApplication,
  MapSymbol,
)
from generator_occurrence_roles import (
  GeneratorOccurrenceRole,
)
from proof import (
  Relation,
  RelationType,
)
from proof_repository import ProofRepository
from repository_theorem_pattern_exploration import (
  RepositoryTheoremPatternOccurrence,
  build_repository_theorem_pattern_occurrences,
)


@dataclass(frozen=True)
class RepositoryMapRelationOccurrence:
  source_pattern_occurrence: RepositoryTheoremPatternOccurrence
  relation: Relation
  map_application: MapApplication
  map: MapSymbol
  input_expression: object
  output_expression: object

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.source_pattern_occurrence,
      RepositoryTheoremPatternOccurrence,
    ):
      raise TypeError(
        "source_pattern_occurrence must be a "
        "RepositoryTheoremPatternOccurrence"
      )

    if not isinstance(
      self.relation,
      Relation,
    ):
      raise TypeError(
        "relation must be a Relation"
      )

    if (
      self.relation
      is not self.source_pattern_occurrence.statement
    ):
      raise ValueError(
        "relation must be the source pattern "
        "occurrence statement"
      )

    if (
      self.relation.relation_type
      is not RelationType.EQUALITY
    ):
      raise ValueError(
        "relation must be an equality Relation"
      )

    if not isinstance(
      self.map_application,
      MapApplication,
    ):
      raise TypeError(
        "map_application must be a MapApplication"
      )

    if (
      self.map_application
      is not self.relation.lhs
    ):
      raise ValueError(
        "map_application must be relation.lhs"
      )

    if not isinstance(
      self.map,
      MapSymbol,
    ):
      raise TypeError(
        "map must be a MapSymbol"
      )

    if (
      self.map
      is not self.map_application.map
    ):
      raise ValueError(
        "map must be map_application.map"
      )

    if (
      self.input_expression
      is not self.map_application.expression
    ):
      raise ValueError(
        "input_expression must be "
        "map_application.expression"
      )

    if (
      self.output_expression
      is not self.relation.rhs
    ):
      raise ValueError(
        "output_expression must be relation.rhs"
      )

    roles = (
      self.source_pattern_occurrence
      .source_occurrence
      .roles
    )

    if (
      GeneratorOccurrenceRole.RELATION_LHS
      not in roles
    ):
      raise ValueError(
        "source occurrence must be on relation lhs"
      )

    if (
      GeneratorOccurrenceRole.MAP_INPUT
      not in roles
    ):
      raise ValueError(
        "source occurrence must be a map input"
      )


def find_repository_map_relation_occurrences(
  repository: ProofRepository,
  generator: GeneratorSymbol,
  map_symbol: MapSymbol | None = None,
) -> tuple[
  RepositoryMapRelationOccurrence,
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

  if (
    map_symbol is not None
    and not isinstance(
      map_symbol,
      MapSymbol,
    )
  ):
    raise TypeError(
      "map_symbol must be a MapSymbol or None"
    )

  pattern_occurrences = (
    build_repository_theorem_pattern_occurrences(
      repository,
      generator,
    )
  )

  results = []

  for pattern_occurrence in pattern_occurrences:
    relation = pattern_occurrence.statement

    if not isinstance(
      relation,
      Relation,
    ):
      continue

    if (
      relation.relation_type
      is not RelationType.EQUALITY
    ):
      continue

    map_application = relation.lhs

    if not isinstance(
      map_application,
      MapApplication,
    ):
      continue

    roles = (
      pattern_occurrence
      .source_occurrence
      .roles
    )

    if (
      GeneratorOccurrenceRole.RELATION_LHS
      not in roles
    ):
      continue

    if (
      GeneratorOccurrenceRole.MAP_INPUT
      not in roles
    ):
      continue

    if (
      map_symbol is not None
      and map_application.map != map_symbol
    ):
      continue

    results.append(
      RepositoryMapRelationOccurrence(
        source_pattern_occurrence=pattern_occurrence,
        relation=relation,
        map_application=map_application,
        map=map_application.map,
        input_expression=map_application.expression,
        output_expression=relation.rhs,
      )
    )

  return tuple(
    results
  )

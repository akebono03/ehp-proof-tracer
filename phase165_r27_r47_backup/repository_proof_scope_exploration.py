from dataclasses import dataclass

from expression import (
  GeneratorSymbol,
  MapApplication,
  MapSymbol,
)
from generator_occurrence_roles import (
  GeneratorOccurrenceRole,
  classify_generator_occurrence_roles,
)
from proof import (
  Relation,
  RelationType,
)
from repository_proof_scope import (
  RepositoryProofScopeNode,
  RepositoryProofScopeResult,
)
from structural_containment import (
  find_generator_occurrence_paths,
)
from toda_rules import (
  TodaBracketMembershipStatement,
  TodaBracketMembershipTheoremStatement,
)


@dataclass(frozen=True)
class RepositoryProofScopeGeneratorOccurrence:
  scope_node: RepositoryProofScopeNode
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
      self.scope_node,
      RepositoryProofScopeNode,
    ):
      raise TypeError(
        "scope_node must be a RepositoryProofScopeNode"
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


@dataclass(frozen=True)
class RepositoryProofScopeTodaMembershipOccurrence:
  source_occurrence: RepositoryProofScopeGeneratorOccurrence
  statement: (
    TodaBracketMembershipStatement
    | TodaBracketMembershipTheoremStatement
  )
  is_membership_element: bool
  bracket_positions: tuple[
    str,
    ...,
  ]

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.source_occurrence,
      RepositoryProofScopeGeneratorOccurrence,
    ):
      raise TypeError(
        "source_occurrence must be a "
        "RepositoryProofScopeGeneratorOccurrence"
      )

    if (
      self.statement
      is not self.source_occurrence.scope_node.proof_step.conclusion
    ):
      raise ValueError(
        "statement must be the source occurrence "
        "proof-step conclusion"
      )

    if not isinstance(
      self.statement,
      (
        TodaBracketMembershipStatement,
        TodaBracketMembershipTheoremStatement,
      ),
    ):
      raise TypeError(
        "statement must be a Toda bracket "
        "membership statement"
      )

    if not isinstance(
      self.is_membership_element,
      bool,
    ):
      raise TypeError(
        "is_membership_element must be a bool"
      )

    if not isinstance(
      self.bracket_positions,
      tuple,
    ):
      raise TypeError(
        "bracket_positions must be a tuple"
      )

    valid_positions = {
      "first",
      "second",
      "third",
    }

    for position in self.bracket_positions:
      if position not in valid_positions:
        raise ValueError(
          "bracket_positions must contain only "
          "first, second, or third"
        )

    if (
      not self.is_membership_element
      and not self.bracket_positions
    ):
      raise ValueError(
        "membership occurrence must identify "
        "element or bracket position"
      )


@dataclass(frozen=True)
class RepositoryProofScopeMapRelationOccurrence:
  source_occurrence: RepositoryProofScopeGeneratorOccurrence
  relation: Relation
  map_application: MapApplication
  map: MapSymbol
  input_expression: object
  output_expression: object

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.source_occurrence,
      RepositoryProofScopeGeneratorOccurrence,
    ):
      raise TypeError(
        "source_occurrence must be a "
        "RepositoryProofScopeGeneratorOccurrence"
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
      is not self.source_occurrence.scope_node.proof_step.conclusion
    ):
      raise ValueError(
        "relation must be the source occurrence "
        "proof-step conclusion"
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


def _value_at_path(
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


def _bracket_positions(
  roles: tuple[
    GeneratorOccurrenceRole,
    ...,
  ],
) -> tuple[
  str,
  ...,
]:
  pairs = (
    (
      GeneratorOccurrenceRole.TODA_BRACKET_FIRST,
      "first",
    ),
    (
      GeneratorOccurrenceRole.TODA_BRACKET_SECOND,
      "second",
    ),
    (
      GeneratorOccurrenceRole.TODA_BRACKET_THIRD,
      "third",
    ),
  )

  return tuple(
    position
    for role, position in pairs
    if role in roles
  )


def find_repository_proof_scope_generator_occurrences(
  scope: RepositoryProofScopeResult,
  generator: GeneratorSymbol,
) -> tuple[
  RepositoryProofScopeGeneratorOccurrence,
  ...,
]:
  if not isinstance(
    scope,
    RepositoryProofScopeResult,
  ):
    raise TypeError(
      "scope must be a RepositoryProofScopeResult"
    )

  if not isinstance(
    generator,
    GeneratorSymbol,
  ):
    raise TypeError(
      "generator must be a GeneratorSymbol"
    )

  occurrences = []

  for node in scope.nodes:
    conclusion = (
      node.proof_step.conclusion
    )

    paths = (
      find_generator_occurrence_paths(
        conclusion,
        generator,
      )
    )

    for path in paths:
      matched_generator = (
        _value_at_path(
          conclusion,
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

      occurrences.append(
        RepositoryProofScopeGeneratorOccurrence(
          scope_node=node,
          path=path,
          matched_generator=matched_generator,
          roles=(
            classify_generator_occurrence_roles(
              conclusion,
              path,
            )
          ),
        )
      )

  return tuple(
    occurrences
  )


def find_repository_proof_scope_toda_membership_occurrences(
  scope: RepositoryProofScopeResult,
  generator: GeneratorSymbol,
) -> tuple[
  RepositoryProofScopeTodaMembershipOccurrence,
  ...,
]:
  occurrences = (
    find_repository_proof_scope_generator_occurrences(
      scope,
      generator,
    )
  )

  results = []

  for occurrence in occurrences:
    statement = (
      occurrence
      .scope_node
      .proof_step
      .conclusion
    )

    if not isinstance(
      statement,
      (
        TodaBracketMembershipStatement,
        TodaBracketMembershipTheoremStatement,
      ),
    ):
      continue

    is_membership_element = (
      bool(
        occurrence.path
      )
      and occurrence.path[
        0
      ] == "element"
    )

    positions = _bracket_positions(
      occurrence.roles
    )

    if (
      not is_membership_element
      and not positions
    ):
      continue

    results.append(
      RepositoryProofScopeTodaMembershipOccurrence(
        source_occurrence=occurrence,
        statement=statement,
        is_membership_element=is_membership_element,
        bracket_positions=positions,
      )
    )

  return tuple(
    results
  )


def find_repository_proof_scope_map_relation_occurrences(
  scope: RepositoryProofScopeResult,
  generator: GeneratorSymbol,
  map_symbol: MapSymbol | None = None,
) -> tuple[
  RepositoryProofScopeMapRelationOccurrence,
  ...,
]:
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

  occurrences = (
    find_repository_proof_scope_generator_occurrences(
      scope,
      generator,
    )
  )

  results = []

  for occurrence in occurrences:
    relation = (
      occurrence
      .scope_node
      .proof_step
      .conclusion
    )

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

    if not isinstance(
      relation.lhs,
      MapApplication,
    ):
      continue

    if (
      GeneratorOccurrenceRole.RELATION_LHS
      not in occurrence.roles
    ):
      continue

    if (
      GeneratorOccurrenceRole.MAP_INPUT
      not in occurrence.roles
    ):
      continue

    if (
      map_symbol is not None
      and relation.lhs.map != map_symbol
    ):
      continue

    results.append(
      RepositoryProofScopeMapRelationOccurrence(
        source_occurrence=occurrence,
        relation=relation,
        map_application=relation.lhs,
        map=relation.lhs.map,
        input_expression=relation.lhs.expression,
        output_expression=relation.rhs,
      )
    )

  return tuple(
    results
  )

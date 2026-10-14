from dataclasses import (
  dataclass,
  fields,
  is_dataclass,
)
from enum import Enum

from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
  MapApplication,
  Suspension,
)
from map_facts import (
  EHP_E_MAP,
  EHP_H_MAP,
)
from proof import (
  Relation,
  RelationType,
)
from proof_repository import ProofRepository
from repository_operation_query import (
  RepositoryCompositionQuery,
  RepositoryGeneratorQuery,
  RepositoryMapOperationQuery,
  RepositoryOperationOperand,
  RepositoryOperationQuery,
  RepositoryThreeTermCompositionQuery,
)
from repository_proof_scope import (
  RepositoryProofScopeNode,
  build_repository_proof_scope,
)
from repository_proof_scope_exploration import (
  find_repository_proof_scope_map_relation_occurrences,
)
from toda_rules import (
  TodaDeltaImageUpToSignStatement,
)


class RepositoryOperationQueryMatchKind(
  Enum
):
  MAP_RELATION = "map_relation"
  SUSPENSION_RELATION = (
    "suspension_relation"
  )
  GROUP_MEMBERSHIP = (
    "group_membership"
  )
  DELTA_UP_TO_SIGN = "delta_up_to_sign"
  COMPOSITION_CONTAINMENT = (
    "composition_containment"
  )


@dataclass(frozen=True)
class RepositoryOperationQueryMatch:
  scope_node: RepositoryProofScopeNode
  statement: object
  match_kind: RepositoryOperationQueryMatchKind

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.scope_node,
      RepositoryProofScopeNode,
    ):
      raise TypeError(
        "scope_node must be a "
        "RepositoryProofScopeNode"
      )

    if (
      self.statement
      is not self.scope_node.proof_step.conclusion
    ):
      raise ValueError(
        "statement must be the scope-node "
        "proof-step conclusion"
      )

    if not isinstance(
      self.match_kind,
      RepositoryOperationQueryMatchKind,
    ):
      raise TypeError(
        "match_kind must be a "
        "RepositoryOperationQueryMatchKind"
      )


@dataclass(frozen=True)
class RepositoryOperationQueryResult:
  query: RepositoryOperationQuery
  matches: tuple[
    RepositoryOperationQueryMatch,
    ...,
  ]

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.query,
      (
        RepositoryMapOperationQuery,
        RepositoryCompositionQuery,
        RepositoryThreeTermCompositionQuery,
      ),
    ):
      raise TypeError(
        "query must be a repository "
        "operation query"
      )

    if not isinstance(
      self.matches,
      tuple,
    ):
      raise TypeError(
        "matches must be a tuple"
      )

    for match in self.matches:
      if not isinstance(
        match,
        RepositoryOperationQueryMatch,
      ):
        raise TypeError(
          "matches must contain only "
          "RepositoryOperationQueryMatch values"
        )

  @property
  def found(
    self,
  ) -> bool:
    return bool(
      self.matches
    )


def _direct_generator_symbol(
  value,
) -> GeneratorSymbol | None:
  if isinstance(
    value,
    HomotopyElement,
  ):
    return value.generator

  return None


def _matches_generator_query(
  value,
  query: RepositoryGeneratorQuery,
) -> bool:
  return (
    _direct_generator_symbol(
      value
    )
    == query.generator
  )


def _matches_composition_query(
  value,
  query: RepositoryCompositionQuery,
) -> bool:
  if not isinstance(
    value,
    Composition,
  ):
    return False

  return (
    _matches_generator_query(
      value.left,
      query.left,
    )
    and _matches_generator_query(
      value.right,
      query.right,
    )
  )


def _matches_three_term_composition_query(
  value,
  query: RepositoryThreeTermCompositionQuery,
) -> bool:
  if not isinstance(
    value,
    Composition,
  ):
    return False

  if not isinstance(
    value.right,
    Composition,
  ):
    return False

  return (
    _matches_generator_query(
      value.left,
      query.first,
    )
    and _matches_generator_query(
      value.right.left,
      query.second,
    )
    and _matches_generator_query(
      value.right.right,
      query.third,
    )
  )


def _matches_operand(
  value,
  operand: RepositoryOperationOperand,
) -> bool:
  if isinstance(
    operand,
    RepositoryGeneratorQuery,
  ):
    return _matches_generator_query(
      value,
      operand,
    )

  if isinstance(
    operand,
    RepositoryCompositionQuery,
  ):
    return _matches_composition_query(
      value,
      operand,
    )

  raise TypeError(
    "unsupported repository operation operand"
  )


def _contains_composition_query(
  value,
  query: RepositoryCompositionQuery,
  ancestor_ids: frozenset[int] = frozenset(),
) -> bool:
  if _matches_composition_query(
    value,
    query,
  ):
    return True

  if isinstance(
    value,
    tuple,
  ):
    value_id = id(
      value
    )

    if value_id in ancestor_ids:
      return False

    next_ancestor_ids = (
      ancestor_ids
      | frozenset(
        (
          value_id,
        )
      )
    )

    return any(
      _contains_composition_query(
        item,
        query,
        next_ancestor_ids,
      )
      for item in value
    )

  if (
    is_dataclass(
      value
    )
    and not isinstance(
      value,
      type,
    )
  ):
    value_id = id(
      value
    )

    if value_id in ancestor_ids:
      return False

    next_ancestor_ids = (
      ancestor_ids
      | frozenset(
        (
          value_id,
        )
      )
    )

    return any(
      _contains_composition_query(
        getattr(
          value,
          field.name,
        ),
        query,
        next_ancestor_ids,
      )
      for field in fields(
        value
      )
    )

  return False


def _contains_three_term_composition_query(
  value,
  query: RepositoryThreeTermCompositionQuery,
  ancestor_ids: frozenset[int] = frozenset(),
) -> bool:
  if _matches_three_term_composition_query(
    value,
    query,
  ):
    return True

  if isinstance(
    value,
    tuple,
  ):
    value_id = id(
      value
    )

    if value_id in ancestor_ids:
      return False

    next_ancestor_ids = (
      ancestor_ids
      | frozenset(
        (
          value_id,
        )
      )
    )

    return any(
      _contains_three_term_composition_query(
        item,
        query,
        next_ancestor_ids,
      )
      for item in value
    )

  if (
    is_dataclass(
      value
    )
    and not isinstance(
      value,
      type,
    )
  ):
    value_id = id(
      value
    )

    if value_id in ancestor_ids:
      return False

    next_ancestor_ids = (
      ancestor_ids
      | frozenset(
        (
          value_id,
        )
      )
    )

    return any(
      _contains_three_term_composition_query(
        getattr(
          value,
          field.name,
        ),
        query,
        next_ancestor_ids,
      )
      for field in fields(
        value
      )
    )

  return False


def _find_h_matches(
  scope,
  query: RepositoryMapOperationQuery,
) -> tuple[
  RepositoryOperationQueryMatch,
  ...,
]:
  if not isinstance(
    query.operand,
    RepositoryGeneratorQuery,
  ):
    return ()

  occurrences = (
    find_repository_proof_scope_map_relation_occurrences(
      scope,
      query.operand.generator,
      map_symbol=EHP_H_MAP,
    )
  )

  results = []

  for occurrence in occurrences:
    if not _matches_operand(
      occurrence.input_expression,
      query.operand,
    ):
      continue

    results.append(
      RepositoryOperationQueryMatch(
        scope_node=(
          occurrence
          .source_occurrence
          .scope_node
        ),
        statement=occurrence.relation,
        match_kind=(
          RepositoryOperationQueryMatchKind
          .MAP_RELATION
        ),
      )
    )

  return tuple(
    results
  )


def _find_e_matches(
  scope,
  query: RepositoryMapOperationQuery,
) -> tuple[
  RepositoryOperationQueryMatch,
  ...,
]:
  results = []

  for node in scope.nodes:
    statement = (
      node.proof_step.conclusion
    )

    if not isinstance(
      statement,
      Relation,
    ):
      continue

    if statement.relation_type not in (
      RelationType.EQUALITY,
      RelationType.ZERO,
    ):
      continue

    lhs = statement.lhs

    if isinstance(
      lhs,
      MapApplication,
    ):
      if (
        lhs.map == EHP_E_MAP
        and _matches_operand(
          lhs.expression,
          query.operand,
        )
      ):
        results.append(
          RepositoryOperationQueryMatch(
            scope_node=node,
            statement=statement,
            match_kind=(
              RepositoryOperationQueryMatchKind
              .MAP_RELATION
            ),
          )
        )

      continue

    if isinstance(
      lhs,
      Suspension,
    ):
      if _matches_operand(
        lhs.expression,
        query.operand,
      ):
        results.append(
          RepositoryOperationQueryMatch(
            scope_node=node,
            statement=statement,
            match_kind=(
              RepositoryOperationQueryMatchKind
              .SUSPENSION_RELATION
            ),
          )
        )

  return tuple(
    results
  )


def _find_delta_matches(
  scope,
  query: RepositoryMapOperationQuery,
) -> tuple[
  RepositoryOperationQueryMatch,
  ...,
]:
  if not isinstance(
    query.operand,
    RepositoryGeneratorQuery,
  ):
    return ()

  results = []

  for node in scope.nodes:
    statement = (
      node.proof_step.conclusion
    )

    if not isinstance(
      statement,
      TodaDeltaImageUpToSignStatement,
    ):
      continue

    if not _matches_generator_query(
      statement.element,
      query.operand,
    ):
      continue

    results.append(
      RepositoryOperationQueryMatch(
        scope_node=node,
        statement=statement,
        match_kind=(
          RepositoryOperationQueryMatchKind
          .DELTA_UP_TO_SIGN
        ),
      )
    )

  return tuple(
    results
  )


def _find_composition_matches(
  scope,
  query: RepositoryCompositionQuery,
) -> tuple[
  RepositoryOperationQueryMatch,
  ...,
]:
  results = []

  for node in scope.nodes:
    statement = (
      node.proof_step.conclusion
    )

    if not _contains_composition_query(
      statement,
      query,
    ):
      continue

    results.append(
      RepositoryOperationQueryMatch(
        scope_node=node,
        statement=statement,
        match_kind=(
          RepositoryOperationQueryMatchKind
          .COMPOSITION_CONTAINMENT
        ),
      )
    )

  return tuple(
    results
  )


def _find_three_term_composition_matches(
  scope,
  query: RepositoryThreeTermCompositionQuery,
) -> tuple[
  RepositoryOperationQueryMatch,
  ...,
]:
  results = []

  for node in scope.nodes:
    statement = (
      node.proof_step.conclusion
    )

    if not _contains_three_term_composition_query(
      statement,
      query,
    ):
      continue

    results.append(
      RepositoryOperationQueryMatch(
        scope_node=node,
        statement=statement,
        match_kind=(
          RepositoryOperationQueryMatchKind
          .COMPOSITION_CONTAINMENT
        ),
      )
    )

  return tuple(
    results
  )


def query_repository_operation(
  repository: ProofRepository,
  query: RepositoryOperationQuery,
) -> RepositoryOperationQueryResult:
  if not isinstance(
    repository,
    ProofRepository,
  ):
    raise TypeError(
      "repository must be a ProofRepository"
    )

  if not isinstance(
    query,
    (
      RepositoryMapOperationQuery,
      RepositoryCompositionQuery,
      RepositoryThreeTermCompositionQuery,
    ),
  ):
    raise TypeError(
      "query must be a repository operation query"
    )

  scope = build_repository_proof_scope(
    repository
  )

  if isinstance(
    query,
    RepositoryCompositionQuery,
  ):
    matches = _find_composition_matches(
      scope,
      query,
    )

  elif isinstance(
    query,
    RepositoryThreeTermCompositionQuery,
  ):
    matches = _find_three_term_composition_matches(
      scope,
      query,
    )

  elif query.operation == "H":
    matches = _find_h_matches(
      scope,
      query,
    )

  elif query.operation == "E":
    matches = _find_e_matches(
      scope,
      query,
    )

  elif query.operation == "Delta":
    matches = _find_delta_matches(
      scope,
      query,
    )

  else:
    raise RuntimeError(
      "unsupported repository operation"
    )

  return RepositoryOperationQueryResult(
    query=query,
    matches=matches,
  )

import pytest

from expression import (
  Composition,
  MapApplication,
  Suspension,
)
from map_facts import (
  EHP_H_MAP,
)
from proof import (
  Relation,
  RelationType,
)
from repository_operation_query import (
  RepositoryCompositionQuery,
  RepositoryMapOperationQuery,
  parse_repository_operation_query,
)
from repository_operation_query_facade import (
  query_repository_operation_input,
  query_standard_repository_operation_input,
)
from repository_operation_query_lookup import (
  RepositoryOperationQueryMatchKind,
)
from standard_production_repository import (
  build_standard_production_proof_repository,
)
from toda_rules import (
  TodaDeltaImageUpToSignStatement,
)


def test_phase110_5_parses_h_nu_prime():
  query = parse_repository_operation_query(
    "H(nu_prime)"
  )

  assert isinstance(
    query,
    RepositoryMapOperationQuery,
  )

  assert query.operation == "H"

  assert (
    query.operand.generator.family
    == "ν"
  )

  assert (
    query.operand.generator.decoration
    == "′"
  )


def test_phase110_5_parses_delta_iota9():
  query = parse_repository_operation_query(
    "Delta(iota_9)"
  )

  assert isinstance(
    query,
    RepositoryMapOperationQuery,
  )

  assert query.operation == "Delta"

  assert (
    query.operand.generator.family
    == "ι"
  )

  assert (
    query.operand.generator.index
    == 9
  )


def test_phase110_5_parses_e_composition():
  query = parse_repository_operation_query(
    "E(eta_2 o nu_prime)"
  )

  assert isinstance(
    query,
    RepositoryMapOperationQuery,
  )

  assert query.operation == "E"

  assert isinstance(
    query.operand,
    RepositoryCompositionQuery,
  )

  assert (
    query.operand.left.generator.family
    == "η"
  )

  assert (
    query.operand.left.generator.index
    == 2
  )

  assert (
    query.operand.right.generator.family
    == "ν"
  )

  assert (
    query.operand.right.generator.decoration
    == "′"
  )


def test_phase110_5_parses_composition_query():
  query = parse_repository_operation_query(
    "eta_2 o nu_prime"
  )

  assert isinstance(
    query,
    RepositoryCompositionQuery,
  )


@pytest.mark.parametrize(
  "value",
  (
    "",
    "h(nu_prime)",
    "Delta(iota_9",
    "H(H(nu_prime))",
    "eta_2 o nu_prime o eta_6",
    "eta_2 ∘ nu_prime",
  ),
)
def test_phase110_5_rejects_out_of_scope_syntax(
  value,
):
  with pytest.raises(
    ValueError,
  ):
    parse_repository_operation_query(
      value
    )


def test_phase110_5_h_nu_prime_finds_existing_relation():
  result = (
    query_standard_repository_operation_input(
      "H(nu_prime)"
    )
  )

  assert result.found

  match = next(
    match
    for match in result.matches
    if (
      isinstance(
        match.statement,
        Relation,
      )
      and isinstance(
        match.statement.lhs,
        MapApplication,
      )
      and match.statement.lhs.map
      == EHP_H_MAP
      and getattr(
        match.statement.rhs,
        "generator",
        None,
      )
      is not None
      and (
        match.statement.rhs.generator.family
        == "η"
      )
      and (
        match.statement.rhs.generator.index
        == 5
      )
    )
  )

  assert (
    match.match_kind
    is RepositoryOperationQueryMatchKind.MAP_RELATION
  )


def test_phase110_5_delta_iota9_finds_existing_up_to_sign_statement():
  result = (
    query_standard_repository_operation_input(
      "Delta(iota_9)"
    )
  )

  assert result.found

  match = next(
    match
    for match in result.matches
    if isinstance(
      match.statement,
      TodaDeltaImageUpToSignStatement,
    )
    and getattr(
      match.statement.element,
      "generator",
      None,
    )
    is not None
    and (
      match.statement.element.generator.family
      == "ι"
    )
    and (
      match.statement.element.generator.index
      == 9
    )
  )

  assert (
    match.match_kind
    is RepositoryOperationQueryMatchKind.DELTA_UP_TO_SIGN
  )


def test_phase110_5_e_eta2_nu_prime_finds_existing_zero_relation():
  result = (
    query_standard_repository_operation_input(
      "E(eta_2 o nu_prime)"
    )
  )

  assert result.found

  match = next(
    match
    for match in result.matches
    if (
      isinstance(
        match.statement,
        Relation,
      )
      and (
        match.statement.relation_type
        is RelationType.ZERO
      )
      and isinstance(
        match.statement.lhs,
        Suspension,
      )
      and isinstance(
        match.statement.lhs.expression,
        Composition,
      )
      and (
        match.statement.lhs
        .expression
        .left
        .generator
        .family
        == "η"
      )
      and (
        match.statement.lhs
        .expression
        .left
        .generator
        .index
        == 2
      )
      and (
        match.statement.lhs
        .expression
        .right
        .generator
        .family
        == "ν"
      )
      and (
        match.statement.lhs
        .expression
        .right
        .generator
        .decoration
        == "′"
      )
    )
  )

  assert (
    match.match_kind
    is RepositoryOperationQueryMatchKind.SUSPENSION_RELATION
  )


def test_phase110_5_composition_query_finds_existing_proof_facts():
  result = (
    query_standard_repository_operation_input(
      "eta_2 o nu_prime"
    )
  )

  assert result.found

  assert any(
    match.match_kind
    is RepositoryOperationQueryMatchKind.COMPOSITION_CONTAINMENT
    for match in result.matches
  )

  assert any(
    isinstance(
      match.statement,
      Relation,
    )
    and (
      match.statement.relation_type
      is RelationType.ZERO
    )
    and isinstance(
      match.statement.lhs,
      Suspension,
    )
    and isinstance(
      match.statement.lhs.expression,
      Composition,
    )
    for match in result.matches
  )


def test_phase110_5_unknown_fact_returns_normal_empty_result():
  result = (
    query_standard_repository_operation_input(
      "H(eta_999)"
    )
  )

  assert not result.found

  assert result.matches == ()


def test_phase110_5_lookup_does_not_mutate_repository():
  repository = (
    build_standard_production_proof_repository()
  )

  before = repository.entries()

  result = query_repository_operation_input(
    repository,
    "H(nu_prime)",
  )

  after = repository.entries()

  assert result.found

  assert after == before

  assert all(
    actual is expected
    for actual, expected in zip(
      after,
      before,
    )
  )


def test_phase110_5_lookup_is_deterministic():
  first = (
    query_standard_repository_operation_input(
      "eta_2 o nu_prime"
    )
  )

  second = (
    query_standard_repository_operation_input(
      "eta_2 o nu_prime"
    )
  )

  assert tuple(
    (
      match.scope_node.root_entry.key,
      match.scope_node.shortest_depth,
      match.statement,
      match.match_kind,
    )
    for match in first.matches
  ) == tuple(
    (
      match.scope_node.root_entry.key,
      match.scope_node.shortest_depth,
      match.statement,
      match.match_kind,
    )
    for match in second.matches
  )

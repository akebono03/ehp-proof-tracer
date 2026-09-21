from expression import (
  GeneratorSymbol,
  IteratedSuspension,
  Suspension,
)
from proof import (
  ProofRule,
  Relation,
  RelationType,
)
from repository_operation_query import (
  parse_repository_operation_query,
)
from repository_operation_query_facade import (
  query_repository_operation_input,
  query_standard_repository_operation_input,
)
from repository_operation_query_lookup import (
  RepositoryOperationQueryMatchKind,
  query_repository_operation,
)
from repository_operation_query_presentation import (
  build_repository_operation_query_presentation,
)
from repository_operation_query_proof_replay import (
  build_repository_operation_query_proof_replay,
)
from standard_production_repository import (
  build_standard_production_proof_repository,
)


def test_phase114_3_direct_lookup_for_e_nu5_still_misses():
  repository = (
    build_standard_production_proof_repository()
  )

  query = parse_repository_operation_query(
    "E(nu_5)"
  )

  result = query_repository_operation(
    repository,
    query,
  )

  assert not result.found
  assert result.matches == ()


def test_phase114_3_facade_handoff_derives_e_nu5_equals_nu6():
  result = (
    query_standard_repository_operation_input(
      "E(nu_5)"
    )
  )

  assert result.found

  assert all(
    isinstance(
      match.statement,
      Relation,
    )
    for match in result.matches
  )

  assert all(
    match.statement.relation_type
    is RelationType.EQUALITY
    for match in result.matches
  )

  assert all(
    isinstance(
      match.statement.lhs,
      Suspension,
    )
    for match in result.matches
  )

  assert all(
    match.statement.lhs.expression.generator
    == GeneratorSymbol(
      family="ν",
      index=5,
    )
    for match in result.matches
  )

  assert all(
    match.statement.rhs.generator
    == GeneratorSymbol(
      family="ν",
      index=6,
    )
    for match in result.matches
  )

  assert all(
    match.match_kind
    is RepositoryOperationQueryMatchKind.SUSPENSION_RELATION
    for match in result.matches
  )


def test_phase114_3_handoff_preserves_symbolic_bridge_as_provenance():
  result = (
    query_standard_repository_operation_input(
      "E(nu_5)"
    )
  )

  root_step = (
    result.matches[
      0
    ].scope_node.proof_step
  )

  assert root_step.rule is ProofRule.INFERENCE
  assert len(root_step.premises) == 1

  symbolic_step = root_step.premises[
    0
  ]

  assert isinstance(
    symbolic_step.conclusion,
    Relation,
  )

  assert isinstance(
    symbolic_step.conclusion.lhs,
    IteratedSuspension,
  )

  assert (
    symbolic_step.conclusion.lhs
    .expression
    .generator
    == GeneratorSymbol(
      family="ν",
      index=5,
    )
  )


def test_phase114_3_query_proof_replays_specialized_root_and_symbolic_bridge():
  result = (
    query_standard_repository_operation_input(
      "E(nu_5)"
    )
  )

  presentation = (
    build_repository_operation_query_presentation(
      result
    )
  )

  assert len(presentation.items) == 1

  replay = (
    build_repository_operation_query_proof_replay(
      presentation,
      max_depth=1,
    )
  )

  assert replay.root_step.rule is ProofRule.INFERENCE
  assert len(replay.steps) == 2
  assert replay.steps[0].depth == 0
  assert replay.steps[1].depth == 1
  assert (
    replay.steps[1].proof_step
    is replay.root_step.premises[0]
  )


def test_phase114_3_handoff_does_not_mutate_repository():
  repository = (
    build_standard_production_proof_repository()
  )

  before = repository.entries()

  result = query_repository_operation_input(
    repository,
    "E(nu_5)",
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


def test_phase114_3_handoff_is_deterministic():
  first = (
    query_standard_repository_operation_input(
      "E(nu_5)"
    )
  )

  second = (
    query_standard_repository_operation_input(
      "E(nu_5)"
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


def _assert_facade_preserves_direct_result(
  query_input,
):
  repository = (
    build_standard_production_proof_repository()
  )

  query = parse_repository_operation_query(
    query_input
  )

  direct_result = query_repository_operation(
    repository,
    query,
  )

  facade_result = query_repository_operation_input(
    repository,
    query_input,
  )

  assert facade_result == direct_result


def test_phase114_3_handoff_does_not_expand_to_h_nu5():
  _assert_facade_preserves_direct_result(
    "H(nu_5)"
  )


def test_phase114_3_handoff_does_not_expand_to_e_nu6():
  _assert_facade_preserves_direct_result(
    "E(nu_6)"
  )


def test_phase114_3_handoff_does_not_expand_to_e_sigma11():
  _assert_facade_preserves_direct_result(
    "E(sigma_11)"
  )


def test_phase114_4_direct_e_fact_still_has_priority():
  _assert_facade_preserves_direct_result(
    "E(eta_2 o nu_prime)"
  )


def test_phase114_4_direct_h_fact_still_has_priority():
  _assert_facade_preserves_direct_result(
    "H(nu_prime)"
  )


def test_phase114_4_direct_delta_fact_still_has_priority():
  _assert_facade_preserves_direct_result(
    "Delta(iota_9)"
  )


def test_phase114_4_handoff_does_not_expand_to_delta_nu5():
  _assert_facade_preserves_direct_result(
    "Delta(nu_5)"
  )


def test_phase114_4_handoff_does_not_expand_to_e_nu5_eta8():
  _assert_facade_preserves_direct_result(
    "E(nu_5 o eta_8)"
  )


def test_phase114_4_three_term_map_operand_parser_boundary_is_unchanged():
  try:
    parse_repository_operation_query(
      "E(nu_5 o eta_8 o eta_9)"
    )
  except ValueError as error:
    assert (
      "map-operation composition operands support "
      "exactly two generators"
      in str(
        error
      )
    )
  else:
    raise AssertionError(
      "three-term map-operation operand "
      "must remain out of scope"
    )


def test_phase114_4_four_term_composition_parser_boundary_is_unchanged():
  try:
    parse_repository_operation_query(
      "nu_5 o eta_8 o eta_9 o eta_10"
    )
  except ValueError as error:
    assert (
      "composition query supports exactly two "
      "or three generators"
      in str(
        error
      )
    )
  else:
    raise AssertionError(
      "four-term composition must remain out of scope"
    )

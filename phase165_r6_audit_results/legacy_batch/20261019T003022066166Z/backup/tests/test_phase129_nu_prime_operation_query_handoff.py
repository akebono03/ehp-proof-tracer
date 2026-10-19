import main as cli_main

from barratt_hilton_rules import (
  HomotopyGroupMembershipStatement,
)
from expression import (
  GeneratorSymbol,
  Suspension,
)
from homotopy_groups import (
  DirectSumGroup,
  FiniteCyclicGroup,
  FreeCyclicGroup,
  TodaPrimaryGroup,
)
from proof import (
  ProofRule,
  Relation,
  RelationType,
)
from repository_nu_prime_suspension_membership_specialization import (
  is_nu_prime_suspension_membership_operation_query,
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


def test_phase129_4_direct_lookup_for_e_nu_prime_still_misses():
  repository = (
    build_standard_production_proof_repository()
  )

  query = parse_repository_operation_query(
    "E(nu_prime)"
  )

  result = query_repository_operation(
    repository,
    query,
  )

  assert not result.found
  assert result.matches == ()


def test_phase129_4_facade_handoff_derives_e_nu_prime_membership_pi7_4():
  result = (
    query_standard_repository_operation_input(
      "E(nu_prime)"
    )
  )

  assert result.found
  assert len(result.matches) == 1

  match = result.matches[
    0
  ]

  assert isinstance(
    match.statement,
    HomotopyGroupMembershipStatement,
  )

  assert isinstance(
    match.statement.element,
    Suspension,
  )

  assert (
    match.statement.element.expression.generator
    == GeneratorSymbol(
      family="ν",
      decoration="′",
    )
  )

  assert match.statement.group_dimension == 7
  assert match.statement.sphere_dimension == 4

  assert (
    match.match_kind
    is RepositoryOperationQueryMatchKind.GROUP_MEMBERSHIP
  )


def test_phase129_4_handoff_preserves_prop56_pi7_4_decomposition_as_provenance():
  result = (
    query_standard_repository_operation_input(
      "E(nu_prime)"
    )
  )

  root_step = (
    result.matches[
      0
    ].scope_node.proof_step
  )

  assert root_step.rule is ProofRule.INFERENCE
  assert len(root_step.premises) == 1

  group_step = root_step.premises[
    0
  ]

  assert isinstance(
    group_step.conclusion,
    Relation,
  )

  assert (
    group_step.conclusion.relation_type
    is RelationType.EQUALITY
  )

  assert (
    group_step.conclusion.lhs
    == TodaPrimaryGroup(
      group_dimension=7,
      sphere_dimension=4,
    )
  )

  assert isinstance(
    group_step.conclusion.rhs,
    DirectSumGroup,
  )

  first, second = (
    group_step.conclusion.rhs.summands
  )

  assert isinstance(
    first,
    FreeCyclicGroup,
  )

  assert (
    first.generator.generator
    == GeneratorSymbol(
      family="ν",
      index=4,
    )
  )

  assert isinstance(
    second,
    FiniteCyclicGroup,
  )

  assert second.order == 4
  assert isinstance(
    second.generator,
    Suspension,
  )

  assert (
    second.generator.expression.generator
    == GeneratorSymbol(
      family="ν",
      decoration="′",
    )
  )


def test_phase129_4_presentation_renders_membership_as_user_facing_result():
  result = (
    query_standard_repository_operation_input(
      "E(nu_prime)"
    )
  )

  presentation = (
    build_repository_operation_query_presentation(
      result
    )
  )

  assert len(
    presentation.items
  ) == 1

  assert (
    presentation.items[
      0
    ].statement_latex
    == r"E\nu' \in \pi_{7}^{4}"
  )


def test_phase129_4_query_proof_replays_membership_then_group_decomposition():
  result = (
    query_standard_repository_operation_input(
      "E(nu_prime)"
    )
  )

  presentation = (
    build_repository_operation_query_presentation(
      result
    )
  )

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


def test_phase129_4_handoff_does_not_mutate_repository():
  repository = (
    build_standard_production_proof_repository()
  )

  before = repository.entries()

  result = query_repository_operation_input(
    repository,
    "E(nu_prime)",
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


def test_phase129_4_handoff_is_deterministic():
  first = (
    query_standard_repository_operation_input(
      "E(nu_prime)"
    )
  )

  second = (
    query_standard_repository_operation_input(
      "E(nu_prime)"
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


def test_phase129_4_guard_is_theorem_specific_to_e_nu_prime():
  accepted = parse_repository_operation_query(
    "E(nu_prime)"
  )
  e_nu4 = parse_repository_operation_query(
    "E(nu_4)"
  )
  h_nu_prime = parse_repository_operation_query(
    "H(nu_prime)"
  )
  delta_nu_prime = parse_repository_operation_query(
    "Delta(nu_prime)"
  )
  e_composition = parse_repository_operation_query(
    "E(nu_prime o eta_6)"
  )

  assert (
    is_nu_prime_suspension_membership_operation_query(
      accepted
    )
  )

  for query in (
    e_nu4,
    h_nu_prime,
    delta_nu_prime,
    e_composition,
  ):
    assert not (
      is_nu_prime_suspension_membership_operation_query(
        query
      )
    )


def test_phase129_4_existing_direct_e_composition_fact_still_has_priority():
  repository = (
    build_standard_production_proof_repository()
  )

  query_input = "E(eta_2 o nu_prime)"

  direct_result = query_repository_operation(
    repository,
    parse_repository_operation_query(
      query_input
    ),
  )

  facade_result = query_repository_operation_input(
    repository,
    query_input,
  )

  assert facade_result == direct_result


def test_phase129_4_existing_h_nu_prime_results_remain_unchanged():
  repository = (
    build_standard_production_proof_repository()
  )

  query_input = "H(nu_prime)"

  direct_result = query_repository_operation(
    repository,
    parse_repository_operation_query(
      query_input
    ),
  )

  facade_result = query_repository_operation_input(
    repository,
    query_input,
  )

  assert facade_result == direct_result


def test_phase129_4_existing_nu5_and_sigma11_handoffs_remain_available():
  nu5_result = (
    query_standard_repository_operation_input(
      "E(nu_5)"
    )
  )

  sigma11_result = (
    query_standard_repository_operation_input(
      "E(sigma_11)"
    )
  )

  assert nu5_result.found
  assert sigma11_result.found


def test_phase129_4_cli_query_e_nu_prime(
  capsys,
):
  exit_code = cli_main.main(
    [
      "query",
      "E(nu_prime)",
    ]
  )

  captured = capsys.readouterr()

  assert exit_code == 0
  assert captured.err == ""
  assert r"E\nu' \in \pi_{7}^{4}" in captured.out

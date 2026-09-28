import main as cli_main

from expression import (
  Composition,
  GeneratorSymbol,
  Suspension,
  Zero,
)
from homotopy_groups import (
  FiniteCyclicGroup,
  TodaPrimaryGroup,
  TodaPrimaryGroupZeroStatement,
)
from proof import (
  ProofRule,
  Relation,
  RelationType,
)
from repository_nu5_eta8_suspension_zero_specialization import (
  is_nu5_eta8_suspension_zero_operation_query,
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


def test_phase128_2_direct_lookup_still_misses():
  repository = (
    build_standard_production_proof_repository()
  )

  query = parse_repository_operation_query(
    "E(nu_5 o eta_8)"
  )

  result = query_repository_operation(
    repository,
    query,
  )

  assert not result.found
  assert result.matches == ()


def test_phase128_2_guard_accepts_only_exact_target_query():
  query = parse_repository_operation_query(
    "E(nu_5 o eta_8)"
  )

  assert (
    is_nu5_eta8_suspension_zero_operation_query(
      query
    )
  )

  for other in (
    "E(nu_5)",
    "E(nu_5 o eta_9)",
    "E(nu_6 o eta_8)",
    "H(nu_5 o eta_8)",
    "Delta(nu_5 o eta_8)",
  ):
    other_query = parse_repository_operation_query(
      other
    )

    assert not (
      is_nu5_eta8_suspension_zero_operation_query(
        other_query
      )
    )


def test_phase128_2_facade_handoff_derives_e_nu5_eta8_zero():
  result = (
    query_standard_repository_operation_input(
      "E(nu_5 o eta_8)"
    )
  )

  assert result.found
  assert len(result.matches) == 1

  match = result.matches[
    0
  ]

  assert (
    match.scope_node.root_entry.key
    == "standard.toda.prop58"
  )

  assert isinstance(
    match.statement,
    Relation,
  )

  assert (
    match.statement.relation_type
    is RelationType.ZERO
  )

  assert isinstance(
    match.statement.lhs,
    Suspension,
  )

  assert isinstance(
    match.statement.lhs.expression,
    Composition,
  )

  assert (
    match.statement.lhs
    .expression.left.generator
    == GeneratorSymbol(
      family="ν",
      index=5,
    )
  )

  assert (
    match.statement.lhs
    .expression.right.generator
    == GeneratorSymbol(
      family="η",
      index=8,
    )
  )

  assert isinstance(
    match.statement.rhs,
    Zero,
  )

  assert (
    match.match_kind
    is RepositoryOperationQueryMatchKind
    .SUSPENSION_RELATION
  )


def test_phase128_2_handoff_preserves_derived_pi10_6_zero_provenance():
  result = (
    query_standard_repository_operation_input(
      "E(nu_5 o eta_8)"
    )
  )

  root_step = (
    result.matches[
      0
    ].scope_node.proof_step
  )

  assert (
    root_step.rule
    is ProofRule.INFERENCE
  )

  assert len(
    root_step.premises
  ) == 1

  pi10_6_zero_step = (
    root_step.premises[
      0
    ]
  )

  assert (
    pi10_6_zero_step.rule
    is ProofRule.INFERENCE
  )

  assert (
    pi10_6_zero_step.conclusion
    == TodaPrimaryGroupZeroStatement(
      group=TodaPrimaryGroup(
        group_dimension=10,
        sphere_dimension=6,
      )
    )
  )


def test_phase128_2_pi10_6_zero_provenance_contains_pi9_5_nu5_eta8():
  result = (
    query_standard_repository_operation_input(
      "E(nu_5 o eta_8)"
    )
  )

  pi10_6_zero_step = (
    result.matches[
      0
    ].scope_node.proof_step.premises[
      0
    ]
  )

  matching_premises = tuple(
    premise
    for premise in pi10_6_zero_step.premises
    if (
      isinstance(
        premise.conclusion,
        Relation,
      )
      and premise.conclusion.lhs
      == TodaPrimaryGroup(
        group_dimension=9,
        sphere_dimension=5,
      )
      and isinstance(
        premise.conclusion.rhs,
        FiniteCyclicGroup,
      )
      and premise.conclusion.rhs.order
      == 2
    )
  )

  assert len(
    matching_premises
  ) == 1

  generator = (
    matching_premises[
      0
    ].conclusion.rhs.generator
  )

  assert isinstance(
    generator,
    Composition,
  )

  assert (
    generator.left.generator
    == GeneratorSymbol(
      family="ν",
      index=5,
    )
  )

  assert (
    generator.right.generator
    == GeneratorSymbol(
      family="η",
      index=8,
    )
  )


def test_phase128_2_query_proof_replays_existing_provenance():
  result = (
    query_standard_repository_operation_input(
      "E(nu_5 o eta_8)"
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

  replay = (
    build_repository_operation_query_proof_replay(
      presentation,
      max_depth=2,
    )
  )

  assert (
    replay.root_step.rule
    is ProofRule.INFERENCE
  )

  assert any(
    replay_step.depth == 1
    and replay_step.proof_step.conclusion
    == TodaPrimaryGroupZeroStatement(
      group=TodaPrimaryGroup(
        group_dimension=10,
        sphere_dimension=6,
      )
    )
    for replay_step in replay.steps
  )

  assert any(
    replay_step.depth == 2
    and isinstance(
      replay_step.proof_step.conclusion,
      Relation,
    )
    and replay_step.proof_step.conclusion.lhs
    == TodaPrimaryGroup(
      group_dimension=9,
      sphere_dimension=5,
    )
    for replay_step in replay.steps
  )


def test_phase128_2_handoff_does_not_mutate_repository():
  repository = (
    build_standard_production_proof_repository()
  )

  before = repository.entries()

  result = query_repository_operation_input(
    repository,
    "E(nu_5 o eta_8)",
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


def test_phase128_2_handoff_is_deterministic():
  first = (
    query_standard_repository_operation_input(
      "E(nu_5 o eta_8)"
    )
  )

  second = (
    query_standard_repository_operation_input(
      "E(nu_5 o eta_8)"
    )
  )

  assert len(
    first.matches
  ) == 1

  assert len(
    second.matches
  ) == 1

  assert (
    first.matches[
      0
    ].scope_node.root_entry.key
    == second.matches[
      0
    ].scope_node.root_entry.key
  )

  assert (
    first.matches[
      0
    ].scope_node.shortest_depth
    == second.matches[
      0
    ].scope_node.shortest_depth
  )

  assert (
    first.matches[
      0
    ].statement
    == second.matches[
      0
    ].statement
  )

  assert (
    first.matches[
      0
    ].match_kind
    is second.matches[
      0
    ].match_kind
  )


def test_phase128_2_existing_handoffs_remain_available():
  assert (
    query_standard_repository_operation_input(
      "E(nu_5)"
    ).found
  )

  assert (
    query_standard_repository_operation_input(
      "E(sigma_11)"
    ).found
  )


def test_phase128_2_cli_query_renders_zero_relation(
  capsys,
):
  exit_code = cli_main.main(
    [
      "query",
      "E(nu_5 o eta_8)",
    ]
  )

  captured = capsys.readouterr()

  assert exit_code == 0
  assert captured.err == ""
  assert r"\nu_{5}" in captured.out
  assert r"\eta_{8}" in captured.out
  assert "= 0" in captured.out

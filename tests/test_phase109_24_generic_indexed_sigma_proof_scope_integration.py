from expression import (
  GeneratorSymbol,
)
from homotopy_groups import (
  FiniteCyclicGroup,
  TodaPrimaryGroup,
)
from proof import (
  ProofRule,
  Relation,
  RelationType,
)
from repository_generator_applicability_facade import (
  explore_standard_repository_generator_applicability_input,
)
from repository_generator_known_group_identity_lookup import (
  find_standard_repository_generator_known_group_identity_input,
)
from repository_proof_scope import (
  build_repository_proof_scope,
)
from repository_proof_scope_facade import (
  explore_standard_repository_generator_proof_scope_input,
)
from standard_production_repository import (
  build_standard_production_proof_repository,
)


def _concrete_sigma_group_nodes(
  result,
  index,
):
  target = TodaPrimaryGroup(
    group_dimension=index + 7,
    sphere_dimension=index,
  )

  return tuple(
    node
    for node in result.scope.nodes
    if (
      isinstance(
        node.proof_step.conclusion,
        Relation,
      )
      and node.proof_step.conclusion.relation_type
      is RelationType.EQUALITY
      and node.proof_step.conclusion.lhs
      == target
      and isinstance(
        node.proof_step.conclusion.rhs,
        FiniteCyclicGroup,
      )
      and node.proof_step.conclusion.rhs.order
      == 16
      and getattr(
        node.proof_step.conclusion.rhs.generator,
        "generator",
        None,
      )
      == GeneratorSymbol(
        family="σ",
        index=index,
      )
    )
  )


def test_phase109_24_sigma11_recursive_proof_scope_now_has_occurrence():
  result = (
    explore_standard_repository_generator_proof_scope_input(
      "sigma_11"
    )
  )

  assert (
    len(
      result.occurrences
    )
    > 0
  )

  assert any(
    occurrence.matched_generator
    == GeneratorSymbol(
      family="σ",
      index=11,
    )
    for occurrence in result.occurrences
  )


def test_phase109_24_sigma11_scope_contains_exactly_one_specialized_group_node():
  result = (
    explore_standard_repository_generator_proof_scope_input(
      "sigma_11"
    )
  )

  nodes = _concrete_sigma_group_nodes(
    result,
    11,
  )

  assert len(
    nodes
  ) == 1


def test_phase109_24_sigma11_specialized_scope_node_preserves_symbolic_provenance():
  result = (
    explore_standard_repository_generator_proof_scope_input(
      "sigma_11"
    )
  )

  node = _concrete_sigma_group_nodes(
    result,
    11,
  )[
    0
  ]

  assert (
    node.shortest_depth
    > 0
  )

  assert (
    node.proof_step.rule
    is ProofRule.INFERENCE
  )

  assert len(
    node.proof_step.premises
  ) == 1

  symbolic_step = (
    node.proof_step.premises[
      0
    ]
  )

  assert isinstance(
    symbolic_step.conclusion,
    Relation,
  )

  assert (
    symbolic_step.conclusion.rhs.order
    == 16
  )


def test_phase109_24_sigma12_recursive_proof_scope_uses_same_generic_path():
  result = (
    explore_standard_repository_generator_proof_scope_input(
      "sigma_12"
    )
  )

  nodes = _concrete_sigma_group_nodes(
    result,
    12,
  )

  assert len(
    nodes
  ) == 1

  assert (
    len(
      result.occurrences
    )
    > 0
  )


def test_phase109_24_sigma100_recursive_proof_scope_uses_same_generic_path():
  result = (
    explore_standard_repository_generator_proof_scope_input(
      "sigma_100"
    )
  )

  nodes = _concrete_sigma_group_nodes(
    result,
    100,
  )

  assert len(
    nodes
  ) == 1


def test_phase109_24_sigma9_keeps_existing_concrete_scope_without_added_node():
  repository = (
    build_standard_production_proof_repository()
  )

  raw_scope = build_repository_proof_scope(
    repository
  )

  result = (
    explore_standard_repository_generator_proof_scope_input(
      "sigma_9"
    )
  )

  assert (
    len(
      result.scope.nodes
    )
    == len(
      raw_scope.nodes
    )
  )

  nodes = _concrete_sigma_group_nodes(
    result,
    9,
  )

  assert len(
    nodes
  ) == 1


def test_phase109_24_sigma7_remains_below_generic_specialization_boundary():
  result = (
    explore_standard_repository_generator_proof_scope_input(
      "sigma_7"
    )
  )

  assert (
    result.occurrences
    == ()
  )


def test_phase109_24_applicability_reuses_specialized_proof_scope():
  result = (
    explore_standard_repository_generator_applicability_input(
      "sigma_11"
    )
  )

  assert (
    len(
      result.proof_scope_exploration.occurrences
    )
    > 0
  )

  nodes = tuple(
    node
    for node in result.scope.nodes
    if (
      isinstance(
        node.proof_step.conclusion,
        Relation,
      )
      and node.proof_step.conclusion.lhs
      == TodaPrimaryGroup(
        group_dimension=18,
        sphere_dimension=11,
      )
    )
  )

  assert len(
    nodes
  ) == 1


def test_phase109_24_known_group_lookup_still_agrees_with_exploration_target():
  known_group_nodes = (
    find_standard_repository_generator_known_group_identity_input(
      "sigma_11"
    )
  )

  exploration = (
    explore_standard_repository_generator_proof_scope_input(
      "sigma_11"
    )
  )

  specialized_nodes = _concrete_sigma_group_nodes(
    exploration,
    11,
  )

  assert len(
    known_group_nodes
  ) == 1

  assert len(
    specialized_nodes
  ) == 1

  assert (
    known_group_nodes[
      0
    ].proof_step.conclusion
    == specialized_nodes[
      0
    ].proof_step.conclusion
  )


def test_phase109_24_standard_repository_roots_remain_unchanged():
  repository = (
    build_standard_production_proof_repository()
  )

  assert tuple(
    entry.key
    for entry in repository.entries()
  ) == (
    "standard.toda.prop56",
    "standard.toda.prop58",
    "standard.toda.prop511",
    "standard.toda.prop515",
  )

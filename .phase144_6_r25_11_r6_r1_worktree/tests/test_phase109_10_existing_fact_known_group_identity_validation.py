from functools import lru_cache

from expression import (
  GeneratorSymbol,
)
from generator_facts import (
  ETA_3_AMBIENT_GROUP_FACT,
  ETA_3_GENERATOR,
  GENERATOR_FACT_REPOSITORY,
  NU_7_AMBIENT_GROUP_FACT,
  NU_7_GENERATOR,
)
from homotopy_groups import (
  FiniteCyclicGroup,
  TodaPrimaryGroup,
)
from proof import (
  Relation,
  RelationType,
)
from repository_generator_known_group_identity_lookup import (
  find_standard_repository_generator_known_group_identity_input,
  find_standard_repository_generator_known_group_identity_nodes,
)


@lru_cache(maxsize=1)
def _phase109_10_eta3_nodes():
  return (
    find_standard_repository_generator_known_group_identity_nodes(
      ETA_3_GENERATOR
    )
  )


@lru_cache(maxsize=1)
def _phase109_10_nu7_nodes():
  return (
    find_standard_repository_generator_known_group_identity_nodes(
      NU_7_GENERATOR
    )
  )


def test_phase109_10_eta3_existing_ambient_fact_is_registered():
  fact = (
    GENERATOR_FACT_REPOSITORY
    .lookup_ambient_group(
      ETA_3_GENERATOR
    )
  )

  assert fact is ETA_3_AMBIENT_GROUP_FACT
  assert fact.group_dimension == 4
  assert fact.sphere_dimension == 3


def test_phase109_10_eta3_resolves_exactly_one_recursive_known_group_identity():
  nodes = _phase109_10_eta3_nodes()

  assert len(
    nodes
  ) == 1

  assert (
    nodes[
      0
    ].shortest_depth
    > 0
  )


def test_phase109_10_eta3_known_group_is_pi4_3_z2_eta3():
  node = (
    _phase109_10_eta3_nodes()[
      0
    ]
  )

  conclusion = (
    node.proof_step.conclusion
  )

  assert isinstance(
    conclusion,
    Relation,
  )
  assert (
    conclusion.relation_type
    is RelationType.EQUALITY
  )
  assert (
    conclusion.lhs
    == TodaPrimaryGroup(
      group_dimension=4,
      sphere_dimension=3,
    )
  )
  assert isinstance(
    conclusion.rhs,
    FiniteCyclicGroup,
  )
  assert (
    conclusion.rhs.order
    == 2
  )
  assert (
    conclusion.rhs
    .generator
    .generator
    == GeneratorSymbol(
      family="η",
      index=3,
    )
  )


def test_phase109_10_eta3_input_facade_matches_existing_generator_fact():
  nodes = (
    find_standard_repository_generator_known_group_identity_input(
      "eta_3"
    )
  )

  assert len(
    nodes
  ) == 1
  assert (
    nodes[
      0
    ].proof_step.conclusion
    == _phase109_10_eta3_nodes()[
      0
    ].proof_step.conclusion
  )


def test_phase109_10_nu7_existing_ambient_fact_is_registered():
  fact = (
    GENERATOR_FACT_REPOSITORY
    .lookup_ambient_group(
      NU_7_GENERATOR
    )
  )

  assert fact is NU_7_AMBIENT_GROUP_FACT
  assert fact.group_dimension == 10
  assert fact.sphere_dimension == 7


def test_phase109_10_nu7_resolves_exactly_one_recursive_known_group_identity():
  nodes = _phase109_10_nu7_nodes()

  assert len(
    nodes
  ) == 1

  assert (
    nodes[
      0
    ].shortest_depth
    > 0
  )


def test_phase109_10_nu7_known_group_is_pi10_7_z8_nu7():
  node = (
    _phase109_10_nu7_nodes()[
      0
    ]
  )

  conclusion = (
    node.proof_step.conclusion
  )

  assert isinstance(
    conclusion,
    Relation,
  )
  assert (
    conclusion.relation_type
    is RelationType.EQUALITY
  )
  assert (
    conclusion.lhs
    == TodaPrimaryGroup(
      group_dimension=10,
      sphere_dimension=7,
    )
  )
  assert isinstance(
    conclusion.rhs,
    FiniteCyclicGroup,
  )
  assert (
    conclusion.rhs.order
    == 8
  )
  assert (
    conclusion.rhs
    .generator
    .generator
    == GeneratorSymbol(
      family="ν",
      index=7,
    )
  )


def test_phase109_10_nu7_input_facade_matches_existing_generator_fact():
  nodes = (
    find_standard_repository_generator_known_group_identity_input(
      "nu_7"
    )
  )

  assert len(
    nodes
  ) == 1
  assert (
    nodes[
      0
    ].proof_step.conclusion
    == _phase109_10_nu7_nodes()[
      0
    ].proof_step.conclusion
  )

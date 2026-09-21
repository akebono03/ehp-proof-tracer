from functools import lru_cache

import pytest

from expression import (
  GeneratorSymbol,
  HomotopyElement,
)
from generator_facts import (
  NU_PRIME_AMBIENT_GROUP_FACT,
  NU_PRIME_GENERATOR,
)
from homotopy_groups import (
  FiniteCyclicGroup,
  TodaPrimaryGroup,
)
from proof import (
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
)
from proof_repository import (
  ProofRepository,
  ProofRepositoryEntry,
)
from repository_generator_known_group_identity_lookup import (
  find_repository_generator_known_group_identity_nodes,
  find_standard_repository_generator_known_group_identity_input,
)
from standard_production_repository import (
  build_standard_production_proof_repository,
)
from toda_group_lookup import (
  find_known_toda_group_results,
)
from toda_group_query import (
  TodaGroupQuery,
)


@lru_cache(maxsize=1)
def _phase109_3_data():
  repository = (
    build_standard_production_proof_repository()
  )

  initial_entries = (
    repository.entries()
  )

  nodes = (
    find_repository_generator_known_group_identity_nodes(
      repository,
      NU_PRIME_GENERATOR,
    )
  )

  final_entries = (
    repository.entries()
  )

  return {
    "repository": repository,
    "initial_entries": initial_entries,
    "nodes": nodes,
    "final_entries": final_entries,
  }


def test_phase109_3_nu_prime_has_one_recursive_known_group_identity():
  data = _phase109_3_data()

  assert len(
    data[
      "nodes"
    ]
  ) == 1


def test_phase109_3_nu_prime_identity_is_pi6_3_z4():
  data = _phase109_3_data()

  conclusion = (
    data[
      "nodes"
    ][
      0
    ]
    .proof_step
    .conclusion
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
      group_dimension=6,
      sphere_dimension=3,
    )
  )

  assert isinstance(
    conclusion.rhs,
    FiniteCyclicGroup,
  )
  assert conclusion.rhs.order == 4
  assert (
    conclusion.rhs.generator.generator
    == NU_PRIME_GENERATOR
  )


def test_phase109_3_nu_prime_identity_matches_registered_ambient_group():
  data = _phase109_3_data()

  conclusion = (
    data[
      "nodes"
    ][
      0
    ]
    .proof_step
    .conclusion
  )

  assert (
    conclusion.lhs.group_dimension
    == NU_PRIME_AMBIENT_GROUP_FACT.group_dimension
  )
  assert (
    conclusion.lhs.sphere_dimension
    == NU_PRIME_AMBIENT_GROUP_FACT.sphere_dimension
  )


def test_phase109_3_nu_prime_identity_is_derived_inside_proof_ancestry():
  data = _phase109_3_data()

  node = data[
    "nodes"
  ][
    0
  ]

  assert node.shortest_depth > 0
  assert (
    node.proof_step
    is not node.root_entry.step
  )
  assert (
    node.proof_step.rule
    is ProofRule.INFERENCE
  )


def test_phase109_3_existing_top_level_lookup_semantics_are_unchanged():
  data = _phase109_3_data()

  results = find_known_toda_group_results(
    data[
      "repository"
    ],
    TodaGroupQuery(
      n=3,
      k=3,
    ),
  )

  assert results == ()


def test_phase109_3_structurally_equal_duplicate_conclusions_are_deduplicated():
  target = TodaPrimaryGroup(
    group_dimension=6,
    sphere_dimension=3,
  )

  first_generator = HomotopyElement(
    name="ν′",
    dimension=3,
    source=6,
    target=3,
    generator=NU_PRIME_GENERATOR,
  )

  second_generator = HomotopyElement(
    name="ν′",
    dimension=3,
    source=6,
    target=3,
    generator=NU_PRIME_GENERATOR,
  )

  first_relation = Relation(
    lhs=target,
    rhs=FiniteCyclicGroup(
      order=4,
      generator=first_generator,
    ),
    relation_type=RelationType.EQUALITY,
  )

  second_relation = Relation(
    lhs=target,
    rhs=FiniteCyclicGroup(
      order=4,
      generator=second_generator,
    ),
    relation_type=RelationType.EQUALITY,
  )

  first_identity_step = ProofStep(
    conclusion=first_relation,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  second_identity_step = ProofStep(
    conclusion=second_relation,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  first_root_step = ProofStep(
    conclusion="first root",
    premises=(
      first_identity_step,
    ),
    rule=ProofRule.INFERENCE,
  )

  second_root_step = ProofStep(
    conclusion="second root",
    premises=(
      second_identity_step,
    ),
    rule=ProofRule.INFERENCE,
  )

  first_entry = ProofRepositoryEntry(
    key="phase109.3.first",
    step=first_root_step,
  )

  second_entry = ProofRepositoryEntry(
    key="phase109.3.second",
    step=second_root_step,
  )

  repository = ProofRepository()

  repository.register(
    first_entry
  )
  repository.register(
    second_entry
  )

  nodes = (
    find_repository_generator_known_group_identity_nodes(
      repository,
      NU_PRIME_GENERATOR,
    )
  )

  assert len(
    nodes
  ) == 1
  assert (
    nodes[
      0
    ].proof_step
    is first_identity_step
  )


def test_phase109_3_recursive_lookup_does_not_mutate_repository():
  data = _phase109_3_data()

  assert (
    data[
      "final_entries"
    ]
    == data[
      "initial_entries"
    ]
  )

  assert all(
    actual is expected
    for actual, expected in zip(
      data[
        "final_entries"
      ],
      data[
        "initial_entries"
      ],
    )
  )


def test_phase109_3_standard_input_facade_resolves_nu_prime():
  nodes = (
    find_standard_repository_generator_known_group_identity_input(
      "nu_prime"
    )
  )

  assert len(
    nodes
  ) == 1

  conclusion = (
    nodes[
      0
    ]
    .proof_step
    .conclusion
  )

  assert (
    conclusion.lhs
    == TodaPrimaryGroup(
      group_dimension=6,
      sphere_dimension=3,
    )
  )
  assert isinstance(
    conclusion.rhs,
    FiniteCyclicGroup,
  )
  assert conclusion.rhs.order == 4
  assert (
    conclusion.rhs.generator.generator
    == NU_PRIME_GENERATOR
  )


def test_phase109_3_missing_ambient_group_fact_returns_empty_tuple():
  data = _phase109_3_data()

  result = (
    find_repository_generator_known_group_identity_nodes(
      data[
        "repository"
      ],
      GeneratorSymbol(
        family="ν",
        index=5,
      ),
    )
  )

  assert result == ()


def test_phase109_3_lookup_rejects_non_repository():
  with pytest.raises(
    TypeError,
    match="repository must be a ProofRepository",
  ):
    find_repository_generator_known_group_identity_nodes(
      "not-a-repository",
      NU_PRIME_GENERATOR,
    )


def test_phase109_3_lookup_rejects_non_generator():
  data = _phase109_3_data()

  with pytest.raises(
    TypeError,
    match="generator must be a GeneratorSymbol",
  ):
    find_repository_generator_known_group_identity_nodes(
      data[
        "repository"
      ],
      "nu_prime",
    )

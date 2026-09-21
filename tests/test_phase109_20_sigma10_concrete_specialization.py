from expression import (
  GeneratorSymbol,
  ScalarSum,
  ScalarSymbol,
)
from generator_facts import (
  GENERATOR_FACT_REPOSITORY,
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
from repository_generator_known_group_identity_lookup import (
  find_standard_repository_generator_known_group_identity_input,
  find_standard_repository_generator_known_group_identity_nodes,
)
from repository_symbolic_sigma_specialization import (
  specialize_toda_prop515_sigma10_step,
)
from standard_production_repository import (
  build_standard_production_proof_repository,
)
from toda_prop515_upper_bootstrap import (
  build_toda_prop515_upper_bootstrap,
)


SIGMA_9 = GeneratorSymbol(
  family="σ",
  index=9,
)

SIGMA_10 = GeneratorSymbol(
  family="σ",
  index=10,
)

SIGMA_11 = GeneratorSymbol(
  family="σ",
  index=11,
)


def test_phase109_20_sigma10_still_has_no_explicit_ambient_group_fact():
  assert (
    GENERATOR_FACT_REPOSITORY
    .lookup_ambient_group(
      SIGMA_10
    )
    is None
  )


def test_phase109_20_specialization_boundary_builds_concrete_pi17_10_relation():
  upper_result = (
    build_toda_prop515_upper_bootstrap()
  )

  step = (
    specialize_toda_prop515_sigma10_step(
      upper_result.higher_step
    )
  )

  assert isinstance(
    step.conclusion,
    Relation,
  )

  assert (
    step.conclusion.relation_type
    is RelationType.EQUALITY
  )

  assert (
    step.conclusion.lhs
    == TodaPrimaryGroup(
      group_dimension=17,
      sphere_dimension=10,
    )
  )

  assert isinstance(
    step.conclusion.rhs,
    FiniteCyclicGroup,
  )

  assert (
    step.conclusion.rhs.order
    == 16
  )

  assert (
    step.conclusion.rhs
    .generator
    .generator
    == SIGMA_10
  )


def test_phase109_20_specialization_boundary_preserves_symbolic_provenance():
  upper_result = (
    build_toda_prop515_upper_bootstrap()
  )

  step = (
    specialize_toda_prop515_sigma10_step(
      upper_result.higher_step
    )
  )

  assert (
    step.rule
    is ProofRule.INFERENCE
  )

  assert (
    step.premises
    == (
      upper_result.higher_step,
    )
  )

  symbolic_relation = (
    step.premises[
      0
    ].conclusion
  )

  n = ScalarSymbol(
    name="n",
  )

  assert (
    symbolic_relation.lhs
    == TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=n,
        right=7,
      ),
      sphere_dimension=n,
    )
  )


def test_phase109_20_sigma10_resolves_one_recursive_known_group_identity():
  nodes = (
    find_standard_repository_generator_known_group_identity_nodes(
      SIGMA_10
    )
  )

  assert len(
    nodes
  ) == 1

  assert (
    nodes[
      0
    ].shortest_depth
    > 0
  )


def test_phase109_20_sigma10_known_group_is_pi17_10_z16_sigma10():
  conclusion = (
    find_standard_repository_generator_known_group_identity_nodes(
      SIGMA_10
    )[
      0
    ]
    .proof_step
    .conclusion
  )

  assert (
    conclusion
    == specialize_toda_prop515_sigma10_step(
      build_toda_prop515_upper_bootstrap()
      .higher_step
    ).conclusion
  )


def test_phase109_20_sigma10_input_facade_uses_specialization_boundary():
  nodes = (
    find_standard_repository_generator_known_group_identity_input(
      "sigma_10"
    )
  )

  assert len(
    nodes
  ) == 1

  assert (
    nodes[
      0
    ].proof_step.conclusion.lhs
    == TodaPrimaryGroup(
      group_dimension=17,
      sphere_dimension=10,
    )
  )


def test_phase109_20_sigma11_now_resolves_through_phase109_22_generalization():
  assert (
    GENERATOR_FACT_REPOSITORY
    .lookup_ambient_group(
      SIGMA_11
    )
    is None
  )

  nodes = (
    find_standard_repository_generator_known_group_identity_nodes(
      SIGMA_11
    )
  )

  assert len(
    nodes
  ) == 1

  assert (
    nodes[
      0
    ].proof_step.conclusion.lhs
    == TodaPrimaryGroup(
      group_dimension=18,
      sphere_dimension=11,
    )
  )


def test_phase109_20_sigma9_existing_concrete_fallback_still_works():
  nodes = (
    find_standard_repository_generator_known_group_identity_nodes(
      SIGMA_9
    )
  )

  assert len(
    nodes
  ) == 1

  assert (
    nodes[
      0
    ].proof_step.conclusion.lhs
    == TodaPrimaryGroup(
      group_dimension=16,
      sphere_dimension=9,
    )
  )


def test_phase109_20_standard_repository_root_entries_remain_unchanged():
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

from expression import (
  GeneratorSymbol,
  Suspension,
)
from generator_facts import (
  GENERATOR_FACT_REPOSITORY,
)
from homotopy_groups import (
  DirectSumGroup,
  FiniteCyclicGroup,
  FreeCyclicGroup,
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


SIGMA_8 = GeneratorSymbol(
  family="σ",
  index=8,
)

SIGMA_PRIME = GeneratorSymbol(
  family="σ",
  decoration="'",
)


def test_phase109_16_sigma8_still_has_no_explicit_ambient_group_fact():
  assert (
    GENERATOR_FACT_REPOSITORY
    .lookup_ambient_group(
      SIGMA_8
    )
    is None
  )


def test_phase109_16_sigma8_resolves_one_recursive_known_group_identity():
  nodes = (
    find_standard_repository_generator_known_group_identity_nodes(
      SIGMA_8
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


def test_phase109_16_sigma8_known_group_is_pi15_8_direct_sum():
  node = (
    find_standard_repository_generator_known_group_identity_nodes(
      SIGMA_8
    )[
      0
    ]
  )

  conclusion = (
    node
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
      group_dimension=15,
      sphere_dimension=8,
    )
  )

  assert isinstance(
    conclusion.rhs,
    DirectSumGroup,
  )


def test_phase109_16_sigma8_is_direct_free_summand_generator():
  conclusion = (
    find_standard_repository_generator_known_group_identity_nodes(
      SIGMA_8
    )[
      0
    ]
    .proof_step
    .conclusion
  )

  free_summands = tuple(
    summand
    for summand in conclusion.rhs.summands
    if isinstance(
      summand,
      FreeCyclicGroup,
    )
  )

  assert len(
    free_summands
  ) == 1

  assert (
    free_summands[
      0
    ].generator.generator
    == SIGMA_8
  )


def test_phase109_16_sigma_prime_occurrence_is_suspended_not_direct():
  conclusion = (
    find_standard_repository_generator_known_group_identity_nodes(
      SIGMA_8
    )[
      0
    ]
    .proof_step
    .conclusion
  )

  torsion_summands = tuple(
    summand
    for summand in conclusion.rhs.summands
    if isinstance(
      summand,
      FiniteCyclicGroup,
    )
  )

  assert len(
    torsion_summands
  ) == 1

  assert isinstance(
    torsion_summands[
      0
    ].generator,
    Suspension,
  )

  assert (
    torsion_summands[
      0
    ].generator.expression.generator
    == SIGMA_PRIME
  )

  assert (
    getattr(
      torsion_summands[
        0
      ].generator,
      "generator",
      None,
    )
    is None
  )


def test_phase109_16_sigma_prime_still_selects_pi14_7_not_pi15_8():
  nodes = (
    find_standard_repository_generator_known_group_identity_nodes(
      SIGMA_PRIME
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
      group_dimension=14,
      sphere_dimension=7,
    )
  )


def test_phase109_16_sigma8_input_facade_uses_direct_sum_fallback():
  nodes = (
    find_standard_repository_generator_known_group_identity_input(
      "sigma_8"
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
      group_dimension=15,
      sphere_dimension=8,
    )
  )


def test_phase109_16_sigma10_symbolic_specialization_remains_unsupported():
  sigma_10 = GeneratorSymbol(
    family="σ",
    index=10,
  )

  assert (
    GENERATOR_FACT_REPOSITORY
    .lookup_ambient_group(
      sigma_10
    )
    is None
  )

  assert (
    find_standard_repository_generator_known_group_identity_nodes(
      sigma_10
    )
    == ()
  )


def test_phase109_16_nu5_finite_cyclic_fallback_still_works():
  nu_5 = GeneratorSymbol(
    family="ν",
    index=5,
  )

  nodes = (
    find_standard_repository_generator_known_group_identity_nodes(
      nu_5
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
      group_dimension=8,
      sphere_dimension=5,
    )
  )


def test_phase109_16_decorated_sigma_finite_cyclic_fallback_still_works():
  for generator, expected_group in (
    (
      GeneratorSymbol(
        family="σ",
        decoration="'''",
      ),
      TodaPrimaryGroup(
        group_dimension=12,
        sphere_dimension=5,
      ),
    ),
    (
      GeneratorSymbol(
        family="σ",
        decoration="''",
      ),
      TodaPrimaryGroup(
        group_dimension=13,
        sphere_dimension=6,
      ),
    ),
    (
      SIGMA_PRIME,
      TodaPrimaryGroup(
        group_dimension=14,
        sphere_dimension=7,
      ),
    ),
  ):
    nodes = (
      find_standard_repository_generator_known_group_identity_nodes(
        generator
      )
    )

    assert len(
      nodes
    ) == 1

    assert (
      nodes[
        0
      ].proof_step.conclusion.lhs
      == expected_group
    )

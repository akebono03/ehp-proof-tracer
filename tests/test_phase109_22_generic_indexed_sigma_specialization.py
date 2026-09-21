import pytest

from expression import (
  GeneratorSymbol,
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
from repository_proof_scope import (
  build_repository_proof_scope,
)
from repository_symbolic_sigma_specialization import (
  is_toda_prop515_generic_sigma_specialization_generator,
  specialize_repository_proof_scope_for_generator,
  specialize_toda_prop515_sigma10_step,
  specialize_toda_prop515_sigma_index_step,
)
from standard_production_repository import (
  build_standard_production_proof_repository,
)
from toda_prop515_upper_bootstrap import (
  build_toda_prop515_upper_bootstrap,
)


@pytest.mark.parametrize(
  "index",
  (
    10,
    11,
    12,
    100,
  ),
)
def test_phase109_22_generic_specialization_accepts_indexed_sigma_n_at_least_10(
  index,
):
  assert (
    is_toda_prop515_generic_sigma_specialization_generator(
      GeneratorSymbol(
        family="σ",
        index=index,
      )
    )
  )


@pytest.mark.parametrize(
  "generator",
  (
    GeneratorSymbol(
      family="σ",
      index=9,
    ),
    GeneratorSymbol(
      family="σ",
      index=ScalarSymbol(
        name="n",
      ),
    ),
    GeneratorSymbol(
      family="σ",
      index=10,
      decoration="'",
    ),
    GeneratorSymbol(
      family="ν",
      index=10,
    ),
  ),
)
def test_phase109_22_generic_specialization_rejects_out_of_boundary_generators(
  generator,
):
  assert not (
    is_toda_prop515_generic_sigma_specialization_generator(
      generator
    )
  )


@pytest.mark.parametrize(
  "index",
  (
    10,
    11,
    12,
    100,
  ),
)
def test_phase109_22_generic_helper_builds_expected_finite_cyclic_group(
  index,
):
  upper_result = (
    build_toda_prop515_upper_bootstrap()
  )

  step = (
    specialize_toda_prop515_sigma_index_step(
      upper_result.higher_step,
      index,
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
      group_dimension=(
        index
        + 7
      ),
      sphere_dimension=index,
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
    == GeneratorSymbol(
      family="σ",
      index=index,
    )
  )


def test_phase109_22_generic_helper_preserves_symbolic_prop515_provenance():
  upper_result = (
    build_toda_prop515_upper_bootstrap()
  )

  step = (
    specialize_toda_prop515_sigma_index_step(
      upper_result.higher_step,
      11,
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


def test_phase109_22_sigma10_compatibility_wrapper_is_preserved():
  upper_result = (
    build_toda_prop515_upper_bootstrap()
  )

  assert (
    specialize_toda_prop515_sigma10_step(
      upper_result.higher_step
    ).conclusion
    == specialize_toda_prop515_sigma_index_step(
      upper_result.higher_step,
      10,
    ).conclusion
  )


@pytest.mark.parametrize(
  "index",
  (
    11,
    12,
    100,
  ),
)
def test_phase109_22_lookup_resolves_generic_indexed_sigma_group(
  index,
):
  generator = GeneratorSymbol(
    family="σ",
    index=index,
  )

  assert (
    GENERATOR_FACT_REPOSITORY
    .lookup_ambient_group(
      generator
    )
    is None
  )

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
    == TodaPrimaryGroup(
      group_dimension=(
        index
        + 7
      ),
      sphere_dimension=index,
    )
  )

  assert (
    nodes[
      0
    ].proof_step.conclusion.rhs.order
    == 16
  )

  assert (
    nodes[
      0
    ].proof_step.conclusion.rhs
    .generator.generator
    == generator
  )


@pytest.mark.parametrize(
  (
    "generator_input",
    "index",
  ),
  (
    (
      "sigma_11",
      11,
    ),
    (
      "σ_12",
      12,
    ),
    (
      "sigma_100",
      100,
    ),
  ),
)
def test_phase109_22_input_facade_resolves_generic_indexed_sigma_group(
  generator_input,
  index,
):
  nodes = (
    find_standard_repository_generator_known_group_identity_input(
      generator_input
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
      group_dimension=(
        index
        + 7
      ),
      sphere_dimension=index,
    )
  )


def test_phase109_22_scope_specialization_adds_exactly_one_node_for_sigma11():
  repository = (
    build_standard_production_proof_repository()
  )

  scope = build_repository_proof_scope(
    repository
  )

  specialized = (
    specialize_repository_proof_scope_for_generator(
      scope,
      GeneratorSymbol(
        family="σ",
        index=11,
      ),
    )
  )

  assert (
    len(
      specialized.nodes
    )
    == len(
      scope.nodes
    )
    + 1
  )


def test_phase109_22_scope_specialization_does_not_replace_sigma9_path():
  repository = (
    build_standard_production_proof_repository()
  )

  scope = build_repository_proof_scope(
    repository
  )

  specialized = (
    specialize_repository_proof_scope_for_generator(
      scope,
      GeneratorSymbol(
        family="σ",
        index=9,
      ),
    )
  )

  assert (
    specialized
    is scope
  )

  nodes = (
    find_standard_repository_generator_known_group_identity_nodes(
      GeneratorSymbol(
        family="σ",
        index=9,
      )
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


def test_phase109_22_symbolic_sigma_index_is_not_concretized_by_lookup():
  symbolic_sigma = GeneratorSymbol(
    family="σ",
    index=ScalarSymbol(
      name="n",
    ),
  )

  assert (
    find_standard_repository_generator_known_group_identity_nodes(
      symbolic_sigma
    )
    == ()
  )


def test_phase109_22_generic_helper_rejects_index_below_10():
  with pytest.raises(
    ValueError,
  ):
    specialize_toda_prop515_sigma_index_step(
      build_toda_prop515_upper_bootstrap()
      .higher_step,
      9,
    )


def test_phase109_22_generic_helper_rejects_non_integer_index():
  with pytest.raises(
    TypeError,
  ):
    specialize_toda_prop515_sigma_index_step(
      build_toda_prop515_upper_bootstrap()
      .higher_step,
      ScalarSymbol(
        name="n",
      ),
    )


def test_phase109_22_standard_repository_root_entries_remain_unchanged():
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

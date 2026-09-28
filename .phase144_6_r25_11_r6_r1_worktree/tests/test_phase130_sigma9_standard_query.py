from expression import (
  GeneratorSymbol,
)
from homotopy_groups import (
  FiniteCyclicGroup,
  TodaPrimaryGroup,
)
from proof import (
  Relation,
  RelationType,
)
from repository_proof_scope import (
  build_repository_proof_scope,
)
from standard_production_repository import (
  build_standard_production_proof_repository,
)
from toda_calculation import (
  build_known_toda_calculation_result,
  build_toda_calculation_result,
)
from toda_calculation_result import (
  TodaCalculationStatus,
)
from toda_group_query import TodaGroupQuery


def test_phase130_11_pi16_9_standard_query_is_found():
  repository = (
    build_standard_production_proof_repository()
  )

  result = (
    build_known_toda_calculation_result(
      repository,
      TodaGroupQuery(
        n=9,
        k=7,
      ),
    )
  )

  assert (
    result.status
    is TodaCalculationStatus.FOUND
  )
  assert len(
    result.candidates
  ) == 1


def test_phase130_11_pi16_9_is_z16_sigma9():
  repository = (
    build_standard_production_proof_repository()
  )

  result = (
    build_known_toda_calculation_result(
      repository,
      TodaGroupQuery(
        n=9,
        k=7,
      ),
    )
  )

  group_result = (
    result.candidates[
      0
    ].group_result
  )

  assert (
    group_result.target
    == TodaPrimaryGroup(
      group_dimension=16,
      sphere_dimension=9,
    )
  )
  assert isinstance(
    group_result.group_structure,
    FiniteCyclicGroup,
  )
  assert (
    group_result.group_structure.order
    == 16
  )
  assert (
    group_result.generators[
      0
    ].generator
    == GeneratorSymbol(
      family="σ",
      index=9,
    )
  )


def test_phase130_11_pi16_9_reuses_existing_concrete_proof_step():
  repository = (
    build_standard_production_proof_repository()
  )

  scope = build_repository_proof_scope(
    repository
  )

  target_nodes = tuple(
    node
    for node in scope.nodes
    if (
      node.root_entry.key
      == "standard.toda.prop515"
      and isinstance(
        node.proof_step.conclusion,
        Relation,
      )
      and (
        node.proof_step.conclusion.relation_type
        is RelationType.EQUALITY
      )
      and (
        node.proof_step.conclusion.lhs
        == TodaPrimaryGroup(
          group_dimension=16,
          sphere_dimension=9,
        )
      )
      and isinstance(
        node.proof_step.conclusion.rhs,
        FiniteCyclicGroup,
      )
      and (
        node.proof_step.conclusion.rhs.order
        == 16
      )
      and (
        getattr(
          node.proof_step.conclusion.rhs.generator,
          "generator",
          None,
        )
        == GeneratorSymbol(
          family="σ",
          index=9,
        )
      )
    )
  )

  assert len(
    target_nodes
  ) == 1

  result = (
    build_known_toda_calculation_result(
      repository,
      TodaGroupQuery(
        n=9,
        k=7,
      ),
    )
  )

  assert (
    result.candidates[
      0
    ].group_result.proof_step
    is target_nodes[
      0
    ].proof_step
  )


def test_phase130_11_pi16_9_keeps_prop515_provenance():
  repository = (
    build_standard_production_proof_repository()
  )

  result = (
    build_known_toda_calculation_result(
      repository,
      TodaGroupQuery(
        n=9,
        k=7,
      ),
    )
  )

  source_entry = (
    result.candidates[
      0
    ].group_result.source_entry
  )

  assert (
    source_entry.phase
    == "75"
  )
  assert (
    source_entry.theorem
    == "Toda Proposition 5.15"
  )


def test_phase130_11_existing_sigma_boundaries_remain_available():
  repository = (
    build_standard_production_proof_repository()
  )

  results = tuple(
    build_toda_calculation_result(
      repository,
      TodaGroupQuery(
        n=n,
        k=7,
      ),
    )
    for n in (
      8,
      9,
      10,
      11,
    )
  )

  assert all(
    result.status
    is TodaCalculationStatus.FOUND
    for result in results
  )


def test_phase130_11_repository_roots_remain_unchanged():
  repository = (
    build_standard_production_proof_repository()
  )

  before = tuple(
    entry.key
    for entry in repository.entries()
  )

  build_known_toda_calculation_result(
    repository,
    TodaGroupQuery(
      n=9,
      k=7,
    ),
  )

  after = tuple(
    entry.key
    for entry in repository.entries()
  )

  assert before == (
    "standard.toda.prop56",
    "standard.toda.prop58",
    "standard.toda.prop511",
    "standard.toda.prop515",
  )
  assert after == before

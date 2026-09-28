from expression import (
  Composition,
  GeneratorSymbol,
)
from homotopy_groups import (
  FiniteCyclicGroup,
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


def test_phase130_8_k4_n6_specializes_prop58_zero_group():
  repository = (
    build_standard_production_proof_repository()
  )

  result = (
    build_known_toda_calculation_result(
      repository,
      TodaGroupQuery(
        n=6,
        k=4,
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

  group_result = (
    result.candidates[
      0
    ].group_result
  )

  assert (
    group_result.group_structure
    is None
  )
  assert (
    group_result.generators
    == ()
  )
  assert (
    group_result.source_entry.phase
    == "68"
  )
  assert (
    group_result.source_entry.theorem
    == "Toda Proposition 5.8"
  )


def test_phase130_8_k4_concrete_boundary_remains_existing_result():
  repository = (
    build_standard_production_proof_repository()
  )

  result = (
    build_toda_calculation_result(
      repository,
      TodaGroupQuery(
        n=5,
        k=4,
      ),
    )
  )

  assert (
    result.status
    is TodaCalculationStatus.FOUND
  )
  assert (
    result.candidates[
      0
    ].group_result.source_entry.phase
    == "68"
  )
  assert (
    result.candidates[
      0
    ].group_result.source_entry.theorem
    == "Toda Proposition 5.8"
  )


def test_phase130_8_k5_n2_recovers_prop59_concrete_branch():
  repository = (
    build_standard_production_proof_repository()
  )

  result = (
    build_known_toda_calculation_result(
      repository,
      TodaGroupQuery(
        n=2,
        k=5,
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
  assert (
    result.candidates[
      0
    ].group_result.source_entry.phase
    == "70"
  )
  assert (
    result.candidates[
      0
    ].group_result.source_entry.theorem
    == "Toda Proposition 5.9"
  )


def test_phase130_8_k5_n6_recovers_prop59_concrete_boundary():
  repository = (
    build_standard_production_proof_repository()
  )

  result = (
    build_known_toda_calculation_result(
      repository,
      TodaGroupQuery(
        n=6,
        k=5,
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
  assert (
    result.candidates[
      0
    ].group_result.source_entry.phase
    == "70"
  )


def test_phase130_8_k5_n7_specializes_prop59_zero_group():
  repository = (
    build_standard_production_proof_repository()
  )

  result = (
    build_known_toda_calculation_result(
      repository,
      TodaGroupQuery(
        n=7,
        k=5,
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
  assert (
    result.candidates[
      0
    ].group_result.group_structure
    is None
  )
  assert (
    result.candidates[
      0
    ].group_result.source_entry.phase
    == "70"
  )


def test_phase130_8_k6_n5_remains_existing_nested_concrete_branch():
  repository = (
    build_standard_production_proof_repository()
  )

  result = (
    build_toda_calculation_result(
      repository,
      TodaGroupQuery(
        n=5,
        k=6,
      ),
    )
  )

  assert (
    result.status
    is TodaCalculationStatus.FOUND
  )
  assert (
    result.candidates[
      0
    ].group_result.source_entry.phase
    == "73"
  )


def test_phase130_8_k6_n8_remains_existing_nested_concrete_boundary():
  repository = (
    build_standard_production_proof_repository()
  )

  result = (
    build_toda_calculation_result(
      repository,
      TodaGroupQuery(
        n=8,
        k=6,
      ),
    )
  )

  assert (
    result.status
    is TodaCalculationStatus.FOUND
  )
  assert (
    result.candidates[
      0
    ].group_result.source_entry.phase
    == "73"
  )


def test_phase130_8_k6_n9_specializes_nu_squared_family():
  repository = (
    build_standard_production_proof_repository()
  )

  result = (
    build_known_toda_calculation_result(
      repository,
      TodaGroupQuery(
        n=9,
        k=6,
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

  group_result = (
    result.candidates[
      0
    ].group_result
  )

  assert isinstance(
    group_result.group_structure,
    FiniteCyclicGroup,
  )
  assert (
    group_result.group_structure.order
    == 2
  )
  assert isinstance(
    group_result.generators[
      0
    ],
    Composition,
  )
  assert (
    group_result.generators[
      0
    ].left.generator
    == GeneratorSymbol(
      family="ν",
      index=9,
    )
  )
  assert (
    group_result.generators[
      0
    ].right.generator
    == GeneratorSymbol(
      family="ν",
      index=12,
    )
  )
  assert (
    group_result.source_entry.phase
    == "73"
  )
  assert (
    group_result.source_entry.theorem
    == "Toda Proposition 5.11"
  )


def test_phase130_8_high_indices_specialize_k4_k5_k6():
  repository = (
    build_standard_production_proof_repository()
  )

  queries = (
    TodaGroupQuery(
      n=10,
      k=4,
    ),
    TodaGroupQuery(
      n=10,
      k=5,
    ),
    TodaGroupQuery(
      n=10,
      k=6,
    ),
  )

  results = tuple(
    build_known_toda_calculation_result(
      repository,
      query,
    )
    for query in queries
  )

  assert all(
    result.status
    is TodaCalculationStatus.FOUND
    for result in results
  )
  assert (
    results[
      0
    ].candidates[
      0
    ].group_result.group_structure
    is None
  )
  assert (
    results[
      1
    ].candidates[
      0
    ].group_result.group_structure
    is None
  )
  assert (
    results[
      2
    ].candidates[
      0
    ].group_result.group_structure.order
    == 2
  )


def test_phase130_8_repository_roots_remain_unchanged():
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
      n=10,
      k=5,
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

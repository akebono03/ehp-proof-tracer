from expression import (
  Composition,
)
from homotopy_groups import (
  FiniteCyclicGroup,
  FreeCyclicGroup,
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


def test_phase130_4_pi3_2_standard_query_recovers_existing_result():
  repository = (
    build_standard_production_proof_repository()
  )

  result = (
    build_known_toda_calculation_result(
      repository,
      TodaGroupQuery(
        n=2,
        k=1,
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
    FreeCyclicGroup,
  )
  assert (
    group_result.generators[
      0
    ].generator.family
    == "η"
  )
  assert (
    group_result.generators[
      0
    ].generator.index
    == 2
  )
  assert (
    group_result.source_entry.phase
    == "55"
  )
  assert (
    group_result.source_entry.theorem
    == "Toda Proposition 5.1"
  )


def test_phase130_4_pi4_3_standard_query_prefers_eta3_normalization():
  repository = (
    build_standard_production_proof_repository()
  )

  result = (
    build_known_toda_calculation_result(
      repository,
      TodaGroupQuery(
        n=3,
        k=1,
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
  assert (
    group_result.generators[
      0
    ].generator.family
    == "η"
  )
  assert (
    group_result.generators[
      0
    ].generator.index
    == 3
  )
  assert (
    group_result.source_entry.phase
    == "55"
  )
  assert (
    group_result.source_entry.theorem
    == "Toda Proposition 5.1"
  )


def test_phase130_4_pi4_2_standard_query_recovers_eta2_eta3():
  repository = (
    build_standard_production_proof_repository()
  )

  result = (
    build_known_toda_calculation_result(
      repository,
      TodaGroupQuery(
        n=2,
        k=2,
      ),
    )
  )

  assert (
    result.status
    is TodaCalculationStatus.FOUND
  )

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
    ].left.generator.index
    == 2
  )
  assert (
    group_result.generators[
      0
    ].right.generator.index
    == 3
  )
  assert (
    group_result.source_entry.phase
    == "59"
  )
  assert (
    group_result.source_entry.theorem
    == "Toda Proposition 5.3"
  )


def test_phase130_4_pi5_3_standard_query_recovers_eta3_eta4():
  repository = (
    build_standard_production_proof_repository()
  )

  result = (
    build_known_toda_calculation_result(
      repository,
      TodaGroupQuery(
        n=3,
        k=2,
      ),
    )
  )

  assert (
    result.status
    is TodaCalculationStatus.FOUND
  )

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
    ].left.generator.index
    == 3
  )
  assert (
    group_result.generators[
      0
    ].right.generator.index
    == 4
  )
  assert (
    group_result.source_entry.phase
    == "59"
  )
  assert (
    group_result.source_entry.theorem
    == "Toda Proposition 5.3"
  )


def test_phase130_4_custom_repository_does_not_gain_low_dimensional_fallback():
  from proof import (
    ProofRule,
    ProofStep,
  )
  from proof_repository import (
    ProofRepository,
    ProofRepositoryEntry,
  )

  repository = ProofRepository()

  repository.register(
    ProofRepositoryEntry(
      key="phase130.custom",
      step=ProofStep(
        conclusion="custom-root",
        premises=(),
        rule=ProofRule.GIVEN,
      ),
    )
  )

  result = (
    build_known_toda_calculation_result(
      repository,
      TodaGroupQuery(
        n=2,
        k=1,
      ),
    )
  )

  assert (
    result.status
    is TodaCalculationStatus.NOT_FOUND
  )


def test_phase130_4_existing_pi5_2_standard_query_remains_available():
  repository = (
    build_standard_production_proof_repository()
  )

  result = (
    build_toda_calculation_result(
      repository,
      TodaGroupQuery(
        n=2,
        k=3,
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
    ].group_result.source_entry.theorem
    == "Toda Proposition 5.6"
  )

import pytest

from proof_repository import (
  ProofRepository,
  ProofRepositoryEntry,
)
from test_phase65_prop56_integration import (
  build_phase65_9_data,
)
from test_phase68_prop58_integration import (
  build_phase68_11_data,
)
from test_phase73_prop511_finite_dimensional_integration import (
  build_phase73_8e_data,
)
from test_phase75_prop515_integration import (
  build_phase75_9_data,
)
from toda_calculation_goal import (
  TodaCalculationGoalDiscoveryStatus,
)
from toda_calculation_goal_discovery import (
  discover_concrete_toda_calculation_goal_candidates,
)
from toda_group_query import TodaGroupQuery


def make_phase95_10_entry(
  key,
  step,
  phase,
  theorem,
):
  return ProofRepositoryEntry(
    key=key,
    step=step,
    phase=phase,
    theorem=theorem,
  )


def test_phase95_10_empty_repository_returns_no_candidates():
  repository = ProofRepository()
  query = TodaGroupQuery(
    n=4,
    k=3,
  )

  result = (
    discover_concrete_toda_calculation_goal_candidates(
      repository,
      query,
    )
  )

  assert result.query is query
  assert result.candidates == ()
  assert (
    result.status
    is (
      TodaCalculationGoalDiscoveryStatus
      .NO_CANDIDATES
    )
  )


def test_phase95_10_discovers_single_candidate_from_repository():
  data = build_phase65_9_data()
  repository = ProofRepository()

  entry = make_phase95_10_entry(
    key="phase95.prop56",
    step=data[
      "integration_step"
    ],
    phase="65",
    theorem="Toda Proposition 5.6",
  )

  repository.register(
    entry
  )

  result = (
    discover_concrete_toda_calculation_goal_candidates(
      repository,
      TodaGroupQuery(
        n=4,
        k=3,
      ),
    )
  )

  assert len(
    result.candidates
  ) == 1
  assert (
    result.status
    is (
      TodaCalculationGoalDiscoveryStatus
      .UNIQUE_CANDIDATE
    )
  )
  assert (
    result.candidates[
      0
    ].goal
    is data[
      "pi7_4_step"
    ].conclusion
  )
  assert (
    result.candidates[
      0
    ].source.source_entry
    is entry
  )


def test_phase95_10_scans_multiple_aggregate_types():
  phase65 = build_phase65_9_data()
  phase68 = build_phase68_11_data()
  repository = ProofRepository()

  phase65_entry = make_phase95_10_entry(
    key="phase95.prop56",
    step=phase65[
      "integration_step"
    ],
    phase="65",
    theorem="Toda Proposition 5.6",
  )

  phase68_entry = make_phase95_10_entry(
    key="phase95.prop58",
    step=phase68[
      "integration_step"
    ],
    phase="68",
    theorem="Toda Proposition 5.8",
  )

  repository.register(
    phase65_entry
  )
  repository.register(
    phase68_entry
  )

  phase65_result = (
    discover_concrete_toda_calculation_goal_candidates(
      repository,
      TodaGroupQuery(
        n=4,
        k=3,
      ),
    )
  )

  phase68_result = (
    discover_concrete_toda_calculation_goal_candidates(
      repository,
      TodaGroupQuery(
        n=5,
        k=4,
      ),
    )
  )

  assert (
    phase65_result.candidates[
      0
    ].source.source_entry
    is phase65_entry
  )
  assert (
    phase68_result.candidates[
      0
    ].source.source_entry
    is phase68_entry
  )


def test_phase95_10_preserves_repository_registration_order_for_multiple_candidates():
  first_data = build_phase73_8e_data()
  second_data = build_phase73_8e_data()

  repository = ProofRepository()

  first_entry = make_phase95_10_entry(
    key="phase95.prop511.first",
    step=first_data[
      "final_step"
    ],
    phase="73",
    theorem=(
      "Toda Proposition 5.11 first"
    ),
  )

  second_entry = make_phase95_10_entry(
    key="phase95.prop511.second",
    step=second_data[
      "final_step"
    ],
    phase="73",
    theorem=(
      "Toda Proposition 5.11 second"
    ),
  )

  repository.register(
    first_entry
  )
  repository.register(
    second_entry
  )

  result = (
    discover_concrete_toda_calculation_goal_candidates(
      repository,
      TodaGroupQuery(
        n=4,
        k=6,
      ),
    )
  )

  assert (
    result.status
    is (
      TodaCalculationGoalDiscoveryStatus
      .MULTIPLE_CANDIDATES
    )
  )
  assert len(
    result.candidates
  ) == 2
  assert (
    result.candidates[
      0
    ].source.source_entry
    is first_entry
  )
  assert (
    result.candidates[
      1
    ].source.source_entry
    is second_entry
  )


def test_phase95_10_does_not_deduplicate_equal_goals_from_distinct_entries():
  data = build_phase73_8e_data()
  repository = ProofRepository()

  first_entry = make_phase95_10_entry(
    key="phase95.prop511.first",
    step=data[
      "final_step"
    ],
    phase="73",
    theorem=(
      "Toda Proposition 5.11 first"
    ),
  )

  second_entry = make_phase95_10_entry(
    key="phase95.prop511.second",
    step=data[
      "final_step"
    ],
    phase="73",
    theorem=(
      "Toda Proposition 5.11 second"
    ),
  )

  repository.register(
    first_entry
  )
  repository.register(
    second_entry
  )

  result = (
    discover_concrete_toda_calculation_goal_candidates(
      repository,
      TodaGroupQuery(
        n=4,
        k=6,
      ),
    )
  )

  assert len(
    result.candidates
  ) == 2
  assert (
    result.candidates[
      0
    ].goal
    is result.candidates[
      1
    ].goal
  )
  assert (
    result.candidates[
      0
    ].source.source_entry
    is not result.candidates[
      1
    ].source.source_entry
  )


def test_phase95_10_ignores_unrelated_repository_entries():
  aggregate = build_phase65_9_data()
  unrelated = build_phase75_9_data()
  repository = ProofRepository()

  unrelated_entry = make_phase95_10_entry(
    key="phase95.unrelated",
    step=unrelated[
      "pi12_5_step"
    ],
    phase="75",
    theorem=(
      "Toda Proposition 5.15 "
      "direct result"
    ),
  )

  aggregate_entry = make_phase95_10_entry(
    key="phase95.prop56",
    step=aggregate[
      "integration_step"
    ],
    phase="65",
    theorem="Toda Proposition 5.6",
  )

  repository.register(
    unrelated_entry
  )
  repository.register(
    aggregate_entry
  )

  result = (
    discover_concrete_toda_calculation_goal_candidates(
      repository,
      TodaGroupQuery(
        n=4,
        k=3,
      ),
    )
  )

  assert len(
    result.candidates
  ) == 1
  assert (
    result.candidates[
      0
    ].source.source_entry
    is aggregate_entry
  )


def test_phase95_10_preserves_nested_branch_provenance():
  data = build_phase73_8e_data()
  repository = ProofRepository()

  entry = make_phase95_10_entry(
    key="phase95.prop511",
    step=data[
      "final_step"
    ],
    phase="73",
    theorem="Toda Proposition 5.11",
  )

  repository.register(
    entry
  )

  result = (
    discover_concrete_toda_calculation_goal_candidates(
      repository,
      TodaGroupQuery(
        n=5,
        k=6,
      ),
    )
  )

  assert len(
    result.candidates
  ) == 1
  assert (
    result.candidates[
      0
    ].source.branch_name
    == (
      "nu_squared_finite_dimensional."
      "pi11_5_group_relation"
    )
  )


def test_phase95_10_does_not_instantiate_symbolic_higher_branch():
  data = build_phase75_9_data()
  repository = ProofRepository()

  entry = make_phase95_10_entry(
    key="phase95.prop515",
    step=data[
      "aggregate_step"
    ],
    phase="75",
    theorem="Toda Proposition 5.15",
  )

  repository.register(
    entry
  )

  result = (
    discover_concrete_toda_calculation_goal_candidates(
      repository,
      TodaGroupQuery(
        n=9,
        k=7,
      ),
    )
  )

  assert result.candidates == ()
  assert (
    result.status
    is (
      TodaCalculationGoalDiscoveryStatus
      .NO_CANDIDATES
    )
  )


def test_phase95_10_does_not_mutate_repository():
  data = build_phase68_11_data()
  repository = ProofRepository()

  entry = make_phase95_10_entry(
    key="phase95.prop58",
    step=data[
      "integration_step"
    ],
    phase="68",
    theorem="Toda Proposition 5.8",
  )

  repository.register(
    entry
  )

  before = repository.entries()

  discover_concrete_toda_calculation_goal_candidates(
    repository,
    TodaGroupQuery(
      n=5,
      k=4,
    ),
  )

  after = repository.entries()

  assert after is not before
  assert after == before
  assert all(
    actual is expected
    for actual, expected in zip(
      after,
      before,
    )
  )


def test_phase95_10_rejects_non_repository():
  with pytest.raises(
    TypeError,
    match=(
      "repository must be "
      "a ProofRepository"
    ),
  ):
    discover_concrete_toda_calculation_goal_candidates(
      "not-a-repository",
      TodaGroupQuery(
        n=4,
        k=3,
      ),
    )


def test_phase95_10_rejects_non_query():
  repository = ProofRepository()

  with pytest.raises(
    TypeError,
    match=(
      "query must be "
      "a TodaGroupQuery"
    ),
  ):
    discover_concrete_toda_calculation_goal_candidates(
      repository,
      "not-a-query",
    )

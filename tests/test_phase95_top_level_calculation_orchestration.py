from proof_repository import (
  ProofRepository,
  ProofRepositoryEntry,
)
from test_phase65_prop56_integration import (
  build_phase65_9_data,
)
from test_phase73_prop511_finite_dimensional_integration import (
  build_phase73_8e_data,
)
from test_phase75_prop515_integration import (
  build_phase75_9_data,
)
from toda_calculation import (
  build_toda_calculation_result,
)
from toda_calculation_result import (
  TodaCalculationStatus,
)
from toda_group_query import TodaGroupQuery


def make_phase95_18_entry(
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


def test_phase95_18_returns_not_found_when_direct_and_aggregate_paths_miss():
  repository = ProofRepository()

  result = build_toda_calculation_result(
    repository,
    TodaGroupQuery(
      n=9,
      k=7,
    ),
  )

  assert result.candidates == ()
  assert (
    result.status
    is TodaCalculationStatus.NOT_FOUND
  )


def test_phase95_18_uses_direct_result_without_aggregate_fallback():
  data = build_phase65_9_data()
  repository = ProofRepository()

  aggregate_entry = make_phase95_18_entry(
    key="phase95.prop56.aggregate",
    step=data[
      "integration_step"
    ],
    phase="65",
    theorem="Toda Proposition 5.6 aggregate",
  )

  direct_entry = make_phase95_18_entry(
    key="phase95.prop56.direct.pi7_4",
    step=data[
      "pi7_4_step"
    ],
    phase="65",
    theorem="Toda Proposition 5.6 direct",
  )

  repository.register(
    aggregate_entry
  )
  repository.register(
    direct_entry
  )

  result = build_toda_calculation_result(
    repository,
    TodaGroupQuery(
      n=4,
      k=3,
    ),
  )

  assert (
    result.status
    is TodaCalculationStatus.FOUND
  )
  assert len(
    result.candidates
  ) == 1

  candidate = result.candidates[
    0
  ]

  assert (
    candidate.group_result.source_entry
    is direct_entry
  )
  assert candidate.goal_source is None


def test_phase95_18_preserves_multiple_direct_results_without_fallback():
  data = build_phase65_9_data()
  repository = ProofRepository()

  aggregate_entry = make_phase95_18_entry(
    key="phase95.prop56.aggregate",
    step=data[
      "integration_step"
    ],
    phase="65",
    theorem="Toda Proposition 5.6 aggregate",
  )

  first_direct = make_phase95_18_entry(
    key="phase95.prop56.direct.first",
    step=data[
      "pi7_4_step"
    ],
    phase="65",
    theorem="Toda Proposition 5.6 direct first",
  )

  second_direct = make_phase95_18_entry(
    key="phase95.prop56.direct.second",
    step=data[
      "pi7_4_step"
    ],
    phase="65",
    theorem="Toda Proposition 5.6 direct second",
  )

  repository.register(
    aggregate_entry
  )
  repository.register(
    first_direct
  )
  repository.register(
    second_direct
  )

  result = build_toda_calculation_result(
    repository,
    TodaGroupQuery(
      n=4,
      k=3,
    ),
  )

  assert (
    result.status
    is TodaCalculationStatus.MULTIPLE_RESULTS
  )
  assert len(
    result.candidates
  ) == 2
  assert (
    result.candidates[
      0
    ].group_result.source_entry
    is first_direct
  )
  assert (
    result.candidates[
      1
    ].group_result.source_entry
    is second_direct
  )
  assert all(
    candidate.goal_source is None
    for candidate in result.candidates
  )


def test_phase95_18_falls_back_to_single_aggregate_branch():
  data = build_phase65_9_data()
  repository = ProofRepository()

  aggregate_entry = make_phase95_18_entry(
    key="phase95.prop56.aggregate",
    step=data[
      "integration_step"
    ],
    phase="65",
    theorem="Toda Proposition 5.6",
  )

  repository.register(
    aggregate_entry
  )

  result = build_toda_calculation_result(
    repository,
    TodaGroupQuery(
      n=4,
      k=3,
    ),
  )

  assert (
    result.status
    is TodaCalculationStatus.FOUND
  )
  assert len(
    result.candidates
  ) == 1

  candidate = result.candidates[
    0
  ]

  assert (
    candidate.group_result.proof_step
    is data[
      "pi7_4_step"
    ]
  )
  assert (
    candidate.goal_source
    .source_entry
    is aggregate_entry
  )
  assert (
    candidate.goal_source.branch_name
    == "pi7_4_group_relation"
  )
  assert (
    candidate.explanation.group_result
    is candidate.group_result
  )
  assert (
    candidate.explanation
    .recursive_provenance
    .root_step
    is data[
      "pi7_4_step"
    ]
  )


def test_phase95_18_falls_back_to_nested_phase73_branch():
  data = build_phase73_8e_data()
  repository = ProofRepository()

  aggregate_entry = make_phase95_18_entry(
    key="phase95.prop511.aggregate",
    step=data[
      "final_step"
    ],
    phase="73",
    theorem="Toda Proposition 5.11",
  )

  repository.register(
    aggregate_entry
  )

  result = build_toda_calculation_result(
    repository,
    TodaGroupQuery(
      n=5,
      k=6,
    ),
  )

  assert (
    result.status
    is TodaCalculationStatus.FOUND
  )

  candidate = result.candidates[
    0
  ]

  expected_step = (
    data[
      "phase73_8c"
    ][
      "pi11_5_step"
    ]
  )

  assert (
    candidate.group_result.proof_step
    is expected_step
  )
  assert (
    candidate.goal_source.branch_name
    == (
      "nu_squared_finite_dimensional."
      "pi11_5_group_relation"
    )
  )
  assert (
    candidate.explanation
    .dependency_result
    .root_step
    is expected_step
  )


def test_phase95_18_falls_back_to_zero_group_branch():
  data = build_phase75_9_data()
  repository = ProofRepository()

  aggregate_entry = make_phase95_18_entry(
    key="phase95.prop515.aggregate",
    step=data[
      "aggregate_step"
    ],
    phase="75",
    theorem="Toda Proposition 5.15",
  )

  repository.register(
    aggregate_entry
  )

  result = build_toda_calculation_result(
    repository,
    TodaGroupQuery(
      n=2,
      k=7,
    ),
  )

  assert (
    result.status
    is TodaCalculationStatus.FOUND
  )

  candidate = result.candidates[
    0
  ]

  assert (
    candidate.group_result.proof_step
    is data[
      "pi9_2_step"
    ]
  )
  assert (
    candidate.group_result.group_structure
    is None
  )
  assert (
    candidate.group_result.generators
    == ()
  )
  assert (
    candidate.group_result.generator_orders
    == ()
  )
  assert (
    candidate.goal_source.source_entry
    is aggregate_entry
  )


def test_phase95_18_preserves_multiple_aggregate_candidates_in_registration_order(
  monkeypatch,
):
  from types import SimpleNamespace

  import toda_calculation as calculation_module
  import toda_calculation_goal_discovery as discovery_module
  from test_phase95_minimal_calculation_result import (
    build_phase95_2_candidate,
  )
  from toda_calculation_goal import (
    TodaCalculationGoalCandidate,
    TodaCalculationGoalSource,
  )
  from toda_calculation_result import (
    TodaCalculationResult,
  )

  query = TodaGroupQuery(
    n=4,
    k=6,
  )

  first_base = build_phase95_2_candidate(
    "phase155.extreme.first",
    query,
  )
  second_base = build_phase95_2_candidate(
    "phase155.extreme.second",
    query,
  )

  first_entry = (
    first_base
    .group_result
    .source_entry
  )
  second_entry = (
    second_base
    .group_result
    .source_entry
  )

  repository = ProofRepository()
  repository.register(
    first_entry
  )
  repository.register(
    second_entry
  )

  first_source = TodaCalculationGoalSource(
    source_entry=first_entry,
    branch_name="synthetic_first",
  )
  second_source = TodaCalculationGoalSource(
    source_entry=second_entry,
    branch_name="synthetic_second",
  )

  goal_by_entry = {
    id(
      first_entry
    ): TodaCalculationGoalCandidate(
      target=query.target,
      goal=(
        first_base
        .group_result
        .proof_step
        .conclusion
      ),
      source=first_source,
    ),
    id(
      second_entry
    ): TodaCalculationGoalCandidate(
      target=query.target,
      goal=(
        second_base
        .group_result
        .proof_step
        .conclusion
      ),
      source=second_source,
    ),
  }

  def extract_one(
    entry,
    actual_query,
  ):
    assert actual_query is query
    return (
      goal_by_entry[
        id(
          entry
        )
      ],
    )

  monkeypatch.setattr(
    discovery_module,
    "extract_concrete_toda_calculation_goal_candidates",
    extract_one,
  )

  discovery = (
    discovery_module
    .discover_concrete_toda_calculation_goal_candidates(
      repository,
      query,
    )
  )

  assert tuple(
    candidate.source.source_entry
    for candidate in discovery.candidates
  ) == (
    first_entry,
    second_entry,
  )

  monkeypatch.setattr(
    calculation_module,
    "build_known_toda_calculation_result",
    lambda actual_repository, actual_query: (
      TodaCalculationResult(
        query=actual_query,
        candidates=(),
      )
    ),
  )
  monkeypatch.setattr(
    calculation_module,
    "discover_concrete_toda_calculation_goal_candidates",
    lambda actual_repository, actual_query: discovery,
  )

  result_by_source_entry_id = {
    id(
      first_entry
    ): (
      first_base
      .group_result
    ),
    id(
      second_entry
    ): (
      second_base
      .group_result
    ),
  }

  def normalize_one(
    goal_candidate,
  ):
    return (
      result_by_source_entry_id[
        id(
          goal_candidate
          .source
          .source_entry
        )
      ],
    )

  monkeypatch.setattr(
    calculation_module,
    "normalize_recovered_toda_calculation_goal_candidate",
    normalize_one,
  )

  result = (
    calculation_module
    .build_toda_calculation_result(
      repository,
      query,
    )
  )

  assert (
    result.status
    is TodaCalculationStatus.MULTIPLE_RESULTS
  )
  assert tuple(
    candidate.goal_source.source_entry
    for candidate in result.candidates
  ) == (
    first_entry,
    second_entry,
  )
  assert tuple(
    candidate.group_result
    for candidate in result.candidates
  ) == (
    first_base.group_result,
    second_base.group_result,
  )


def test_phase95_18_does_not_mutate_repository():
  data = build_phase73_8e_data()
  repository = ProofRepository()

  aggregate_entry = make_phase95_18_entry(
    key="phase95.prop511.aggregate",
    step=data[
      "final_step"
    ],
    phase="73",
    theorem="Toda Proposition 5.11",
  )

  repository.register(
    aggregate_entry
  )

  before = repository.entries()

  build_toda_calculation_result(
    repository,
    TodaGroupQuery(
      n=5,
      k=6,
    ),
  )

  after = repository.entries()

  assert after == before
  assert all(
    actual is expected
    for actual, expected in zip(
      after,
      before,
    )
  )

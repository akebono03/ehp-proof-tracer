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


def test_phase95_18_preserves_multiple_aggregate_candidates_in_registration_order():
  first_data = build_phase73_8e_data()
  second_data = build_phase73_8e_data()
  repository = ProofRepository()

  first_entry = make_phase95_18_entry(
    key="phase95.prop511.first",
    step=first_data[
      "final_step"
    ],
    phase="73",
    theorem="Toda Proposition 5.11 first",
  )

  second_entry = make_phase95_18_entry(
    key="phase95.prop511.second",
    step=second_data[
      "final_step"
    ],
    phase="73",
    theorem="Toda Proposition 5.11 second",
  )

  repository.register(
    first_entry
  )
  repository.register(
    second_entry
  )

  result = build_toda_calculation_result(
    repository,
    TodaGroupQuery(
      n=4,
      k=6,
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
    ].goal_source.source_entry
    is first_entry
  )
  assert (
    result.candidates[
      1
    ].goal_source.source_entry
    is second_entry
  )
  assert all(
    candidate.group_result.proof_step
    is first_data[
      "pi10_4_step"
    ]
    for candidate in result.candidates
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

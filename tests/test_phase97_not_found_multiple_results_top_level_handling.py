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
from test_phase95_actual_representative_top_level_capability import (
  build_phase95_20_data,
)
from toda_calculation_report import (
  build_toda_calculation_report_result,
)
from toda_calculation_result import (
  TodaCalculationStatus,
)
from toda_group_query import TodaGroupQuery


def test_phase97_4_not_found_returns_empty_top_level_result():
  repository = ProofRepository()

  result = (
    build_toda_calculation_report_result(
      repository,
      TodaGroupQuery(
        n=9,
        k=7,
      ),
    )
  )

  assert (
    result.status
    is TodaCalculationStatus.NOT_FOUND
  )
  assert (
    result.calculation_result
    .candidates
    == ()
  )
  assert result.candidates == ()


def test_phase97_4_found_returns_one_report_candidate():
  data = build_phase95_20_data()

  result = (
    build_toda_calculation_report_result(
      data[
        "repository"
      ],
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
  assert len(
    result.candidates
  ) == 1

  report_candidate = (
    result.candidates[
      0
    ]
  )

  assert (
    report_candidate.source_candidate
    is result
    .calculation_result
    .candidates[
      0
    ]
  )
  assert (
    report_candidate
    .presentation
    .source_candidate
    is report_candidate
    .source_candidate
  )
  assert (
    "# $\\pi_{9}^{5}$"
    in report_candidate.report
  )


def test_phase97_4_multiple_direct_results_preserve_identity_and_order():
  data = build_phase65_9_data()

  repository = ProofRepository()

  first_entry = ProofRepositoryEntry(
    key="phase97.direct.first",
    step=data[
      "pi7_4_step"
    ],
    phase="65",
    theorem="Toda Proposition 5.6 first",
  )

  second_entry = ProofRepositoryEntry(
    key="phase97.direct.second",
    step=data[
      "pi7_4_step"
    ],
    phase="65",
    theorem="Toda Proposition 5.6 second",
  )

  repository.register(
    first_entry
  )
  repository.register(
    second_entry
  )

  result = (
    build_toda_calculation_report_result(
      repository,
      TodaGroupQuery(
        n=4,
        k=3,
      ),
    )
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
    ].source_candidate
    is result
    .calculation_result
    .candidates[
      0
    ]
  )
  assert (
    result.candidates[
      1
    ].source_candidate
    is result
    .calculation_result
    .candidates[
      1
    ]
  )

  assert (
    result.candidates[
      0
    ].source_candidate
    .group_result
    .source_entry
    is first_entry
  )
  assert (
    result.candidates[
      1
    ].source_candidate
    .group_result
    .source_entry
    is second_entry
  )

  assert all(
    candidate
    .source_candidate
    .goal_source
    is None
    for candidate in result.candidates
  )

  first_report = (
    result.candidates[
      0
    ].report
  )
  second_report = (
    result.candidates[
      1
    ].report
  )

  assert first_report.startswith(
    "# $\\pi_"
  )
  assert second_report.startswith(
    "# $\\pi_"
  )


def test_phase97_4_multiple_aggregate_results_preserve_goal_source_order():
  first_data = build_phase73_8e_data()
  second_data = build_phase73_8e_data()

  repository = ProofRepository()

  first_entry = ProofRepositoryEntry(
    key="phase97.prop511.first",
    step=first_data[
      "final_step"
    ],
    phase="73",
    theorem="Toda Proposition 5.11 first",
  )

  second_entry = ProofRepositoryEntry(
    key="phase97.prop511.second",
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

  result = (
    build_toda_calculation_report_result(
      repository,
      TodaGroupQuery(
        n=4,
        k=6,
      ),
    )
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
    ].source_candidate
    .goal_source
    .source_entry
    is first_entry
  )
  assert (
    result.candidates[
      1
    ].source_candidate
    .goal_source
    .source_entry
    is second_entry
  )

  assert (
    result.candidates[
      0
    ].presentation
    .source
    .goal_source
    .repository_source
    .source_entry
    is first_entry
  )
  assert (
    result.candidates[
      1
    ].presentation
    .source
    .goal_source
    .repository_source
    .source_entry
    is second_entry
  )


def test_phase97_4_general_top_level_api_does_not_mutate_repository():
  data = build_phase95_20_data()

  repository = data[
    "repository"
  ]

  before = repository.entries()

  build_toda_calculation_report_result(
    repository,
    TodaGroupQuery(
      n=5,
      k=4,
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

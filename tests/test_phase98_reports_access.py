from proof_repository import (
  ProofRepository,
  ProofRepositoryEntry,
)
from test_phase65_prop56_integration import (
  build_phase65_9_data,
)
from test_phase95_actual_representative_top_level_capability import (
  build_phase95_20_data,
)
from toda_calculation_facade import (
  build_toda_report,
)
from toda_calculation_result import (
  TodaCalculationStatus,
)


def test_phase98_5_not_found_reports_is_empty_tuple():
  repository = ProofRepository()

  result = build_toda_report(
    repository,
    n=9,
    k=7,
  )

  assert (
    result.status
    is TodaCalculationStatus.NOT_FOUND
  )
  assert result.candidates == ()
  assert result.reports == ()


def test_phase98_5_found_reports_contains_the_single_report():
  data = build_phase95_20_data()

  result = build_toda_report(
    data[
      "repository"
    ],
    n=5,
    k=4,
  )

  assert (
    result.status
    is TodaCalculationStatus.FOUND
  )
  assert result.reports == (
    result.report,
  )
  assert (
    result.reports[
      0
    ]
    == result.candidates[
      0
    ].report
  )


def test_phase98_5_multiple_results_exposes_all_reports_in_candidate_order():
  data = build_phase65_9_data()

  repository = ProofRepository()

  first_entry = ProofRepositoryEntry(
    key="phase98.reports.first",
    step=data[
      "pi7_4_step"
    ],
    phase="65",
    theorem="Toda Proposition 5.6 first",
  )

  second_entry = ProofRepositoryEntry(
    key="phase98.reports.second",
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

  result = build_toda_report(
    repository,
    n=4,
    k=3,
  )

  assert (
    result.status
    is TodaCalculationStatus.MULTIPLE_RESULTS
  )
  assert len(
    result.reports
  ) == 2

  assert result.reports == tuple(
    candidate.report
    for candidate in result.candidates
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


def test_phase98_5_reports_access_preserves_candidate_identity():
  data = build_phase95_20_data()

  result = build_toda_report(
    data[
      "repository"
    ],
    n=5,
    k=4,
  )

  candidate = result.candidates[
    0
  ]
  source_candidate = (
    candidate.source_candidate
  )

  reports = result.reports

  assert len(
    reports
  ) == 1
  assert (
    result.candidates[
      0
    ]
    is candidate
  )
  assert (
    result.candidates[
      0
    ].source_candidate
    is source_candidate
  )
  assert (
    source_candidate
    is result
    .calculation_result
    .candidates[
      0
    ]
  )


def test_phase98_5_reports_access_does_not_mutate_repository():
  data = build_phase95_20_data()

  repository = data[
    "repository"
  ]

  result = build_toda_report(
    repository,
    n=5,
    k=4,
  )

  before = repository.entries()

  _ = result.reports

  after = repository.entries()

  assert after == before
  assert all(
    actual is expected
    for actual, expected in zip(
      after,
      before,
    )
  )

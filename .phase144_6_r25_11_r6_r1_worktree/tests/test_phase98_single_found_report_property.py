import pytest

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


def test_phase98_4_found_result_exposes_single_report_directly():
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
  assert (
    result.report
    == result.candidates[
      0
    ].report
  )
  assert (
    "# $\\pi_{9}^{5}$"
    in result.report
  )


def test_phase98_4_found_report_property_preserves_candidate_identity():
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

  before_source_candidate = (
    candidate.source_candidate
  )

  report = result.report

  assert isinstance(
    report,
    str,
  )
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
    is before_source_candidate
  )
  assert (
    before_source_candidate
    is result
    .calculation_result
    .candidates[
      0
    ]
  )


def test_phase98_4_not_found_report_property_rejects_fake_report():
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

  with pytest.raises(
    ValueError,
    match=(
      "report is available only when "
      "status is FOUND"
    ),
  ):
    _ = result.report


def test_phase98_4_multiple_results_report_property_rejects_silent_selection():
  data = build_phase65_9_data()

  repository = ProofRepository()

  first_entry = ProofRepositoryEntry(
    key="phase98.report.first",
    step=data[
      "pi7_4_step"
    ],
    phase="65",
    theorem="Toda Proposition 5.6 first",
  )

  second_entry = ProofRepositoryEntry(
    key="phase98.report.second",
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
    result.candidates
  ) == 2

  with pytest.raises(
    ValueError,
    match=(
      "report is available only when "
      "status is FOUND"
    ),
  ):
    _ = result.report

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


def test_phase98_4_report_property_does_not_mutate_repository():
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

  _ = result.report

  after = repository.entries()

  assert after == before
  assert all(
    actual is expected
    for actual, expected in zip(
      after,
      before,
    )
  )

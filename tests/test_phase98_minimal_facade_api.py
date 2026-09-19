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


def test_phase98_2_facade_builds_found_report_from_raw_n_k():
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
  assert result.query.n == 5
  assert result.query.k == 4
  assert (
    result.target.group_dimension
    == 9
  )
  assert (
    result.target.sphere_dimension
    == 5
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


def test_phase98_2_facade_preserves_not_found_semantics():
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
  assert (
    result.calculation_result
    .candidates
    == ()
  )
  assert result.candidates == ()


def test_phase98_2_facade_preserves_multiple_result_identity_and_order():
  data = build_phase65_9_data()

  repository = ProofRepository()

  first_entry = ProofRepositoryEntry(
    key="phase98.facade.first",
    step=data[
      "pi7_4_step"
    ],
    phase="65",
    theorem="Toda Proposition 5.6 first",
  )

  second_entry = ProofRepositoryEntry(
    key="phase98.facade.second",
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


def test_phase98_2_facade_does_not_mutate_repository():
  data = build_phase95_20_data()

  repository = data[
    "repository"
  ]

  before = repository.entries()

  build_toda_report(
    repository,
    n=5,
    k=4,
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


def test_phase98_2_facade_reuses_query_n_validation():
  repository = ProofRepository()

  with pytest.raises(
    ValueError,
    match="n must be positive",
  ):
    build_toda_report(
      repository,
      n=0,
      k=4,
    )


def test_phase98_2_facade_reuses_query_k_validation():
  repository = ProofRepository()

  with pytest.raises(
    ValueError,
    match="k must be nonnegative",
  ):
    build_toda_report(
      repository,
      n=5,
      k=-1,
    )


def test_phase98_2_facade_reuses_query_type_validation():
  repository = ProofRepository()

  with pytest.raises(
    TypeError,
    match="n must be an int",
  ):
    build_toda_report(
      repository,
      n=True,
      k=4,
    )

  with pytest.raises(
    TypeError,
    match="k must be an int",
  ):
    build_toda_report(
      repository,
      n=5,
      k=True,
    )

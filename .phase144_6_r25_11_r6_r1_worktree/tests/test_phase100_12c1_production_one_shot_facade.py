from proof_repository import ProofRepository
from toda_calculation_facade import (
  build_standard_toda_report,
  build_toda_report,
)
from toda_calculation_result import (
  TodaCalculationStatus,
)


def test_phase100_12c1_standard_one_shot_returns_found_report_for_pi12_5():
  result = build_standard_toda_report(
    n=5,
    k=7,
  )

  assert (
    result.status
    is TodaCalculationStatus.FOUND
  )
  assert result.query.n == 5
  assert result.query.k == 7
  assert (
    result.target.group_dimension
    == 12
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
    "# $\\pi_{12}^{5}$"
    in report_candidate.report
  )
  assert "## Result" in report_candidate.report
  assert "## Source" in report_candidate.report
  assert (
    "## Proof flow"
    in report_candidate.report
  )
  assert (
    "## Readable proof narrative"
    in report_candidate.report
  )


def test_phase100_12c1_standard_one_shot_preserves_prop515_provenance():
  result = build_standard_toda_report(
    n=5,
    k=7,
  )

  source = (
    result.candidates[
      0
    ]
    .presentation
    .source
    .goal_source
  )

  assert source is not None
  assert (
    source
    .repository_source
    .phase
    == "75"
  )
  assert (
    source
    .repository_source
    .theorem
    == "Toda Proposition 5.15"
  )
  assert (
    source.branch_name
    == "pi12_5_group_relation"
  )


def test_phase100_12c1_standard_one_shot_preserves_not_found_semantics():
  result = build_standard_toda_report(
    n=20,
    k=20,
  )

  assert (
    result.status
    is TodaCalculationStatus.NOT_FOUND
  )
  assert result.candidates == ()


def test_phase100_12c1_standard_one_shot_reuses_query_validation():
  try:
    build_standard_toda_report(
      n=0,
      k=7,
    )
  except ValueError as exc:
    assert (
      str(exc)
      == "n must be positive"
    )
  else:
    raise AssertionError(
      "expected ValueError"
    )


def test_phase100_12c1_existing_repository_explicit_facade_remains_available():
  repository = ProofRepository()

  result = build_toda_report(
    repository,
    n=5,
    k=7,
  )

  assert (
    result.status
    is TodaCalculationStatus.NOT_FOUND
  )
  assert result.candidates == ()

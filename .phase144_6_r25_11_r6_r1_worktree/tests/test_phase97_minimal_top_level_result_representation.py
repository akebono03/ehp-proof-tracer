import pytest

from test_phase95_actual_representative_top_level_capability import (
  build_phase95_20_data,
  get_single_candidate,
)
from toda_calculation_result import (
  TodaCalculationCandidate,
  TodaCalculationResult,
  TodaCalculationStatus,
)
from toda_calculation_report_result import (
  TodaCalculationReportCandidate,
  TodaCalculationReportResult,
)
from toda_end_to_end_presentation import (
  build_toda_end_to_end_candidate_presentation,
)
from toda_full_proof_report_renderer import (
  render_toda_full_proof_report_markdown,
)
from toda_group_query import TodaGroupQuery


def build_phase97_2_report_candidate(
  source_candidate,
  repository_entries,
):
  presentation = (
    build_toda_end_to_end_candidate_presentation(
      source_candidate,
      repository_entries,
    )
  )

  report = (
    render_toda_full_proof_report_markdown(
      presentation
    )
  )

  return TodaCalculationReportCandidate(
    source_candidate=source_candidate,
    presentation=presentation,
    report=report,
  )


def test_phase97_2_candidate_preserves_existing_objects_by_identity():
  data = build_phase95_20_data()

  source_candidate = get_single_candidate(
    data[
      "results"
    ][
      "pi9_5"
    ]
  )

  report_candidate = (
    build_phase97_2_report_candidate(
      source_candidate,
      data[
        "repository"
      ].entries(),
    )
  )

  assert (
    report_candidate.source_candidate
    is source_candidate
  )
  assert (
    report_candidate
    .presentation
    .source_candidate
    is source_candidate
  )
  assert isinstance(
    report_candidate.report,
    str,
  )
  assert (
    "## Readable proof narrative"
    in report_candidate.report
  )


def test_phase97_2_result_preserves_calculation_result_and_delegates_summary():
  data = build_phase95_20_data()

  calculation_result = (
    data[
      "results"
    ][
      "pi9_5"
    ]
  )

  source_candidate = get_single_candidate(
    calculation_result
  )

  report_candidate = (
    build_phase97_2_report_candidate(
      source_candidate,
      data[
        "repository"
      ].entries(),
    )
  )

  result = TodaCalculationReportResult(
    calculation_result=calculation_result,
    candidates=(
      report_candidate,
    ),
  )

  assert (
    result.calculation_result
    is calculation_result
  )
  assert (
    result.query
    is calculation_result.query
  )
  assert (
    result.target
    == calculation_result.target
  )
  assert (
    result.status
    is TodaCalculationStatus.FOUND
  )
  assert (
    result.candidates[
      0
    ]
    is report_candidate
  )


def test_phase97_2_not_found_result_preserves_empty_candidate_tuple():
  calculation_result = (
    TodaCalculationResult(
      query=TodaGroupQuery(
        n=9,
        k=7,
      ),
      candidates=(),
    )
  )

  result = TodaCalculationReportResult(
    calculation_result=calculation_result,
    candidates=(),
  )

  assert (
    result.status
    is TodaCalculationStatus.NOT_FOUND
  )
  assert result.candidates == ()


def test_phase97_2_multiple_results_preserve_candidate_identity_and_order():
  data = build_phase95_20_data()

  original = get_single_candidate(
    data[
      "results"
    ][
      "pi9_5"
    ]
  )

  first = TodaCalculationCandidate(
    group_result=original.group_result,
    explanation=original.explanation,
    goal_source=original.goal_source,
  )

  second = TodaCalculationCandidate(
    group_result=original.group_result,
    explanation=original.explanation,
    goal_source=original.goal_source,
  )

  calculation_result = (
    TodaCalculationResult(
      query=TodaGroupQuery(
        n=5,
        k=4,
      ),
      candidates=(
        first,
        second,
      ),
    )
  )

  repository_entries = (
    data[
      "repository"
    ].entries()
  )

  first_report = (
    build_phase97_2_report_candidate(
      first,
      repository_entries,
    )
  )

  second_report = (
    build_phase97_2_report_candidate(
      second,
      repository_entries,
    )
  )

  result = TodaCalculationReportResult(
    calculation_result=calculation_result,
    candidates=(
      first_report,
      second_report,
    ),
  )

  assert (
    result.status
    is TodaCalculationStatus.MULTIPLE_RESULTS
  )
  assert (
    result.candidates[
      0
    ].source_candidate
    is first
  )
  assert (
    result.candidates[
      1
    ].source_candidate
    is second
  )


def test_phase97_2_candidate_rejects_non_calculation_candidate():
  data = build_phase95_20_data()

  source_candidate = get_single_candidate(
    data[
      "results"
    ][
      "pi9_5"
    ]
  )

  presentation = (
    build_toda_end_to_end_candidate_presentation(
      source_candidate,
      data[
        "repository"
      ].entries(),
    )
  )

  with pytest.raises(
    TypeError,
    match=(
      "source_candidate must be "
      "a TodaCalculationCandidate"
    ),
  ):
    TodaCalculationReportCandidate(
      source_candidate="not-a-candidate",
      presentation=presentation,
      report="report",
    )


def test_phase97_2_candidate_rejects_non_presentation():
  data = build_phase95_20_data()

  source_candidate = get_single_candidate(
    data[
      "results"
    ][
      "pi9_5"
    ]
  )

  with pytest.raises(
    TypeError,
    match=(
      "presentation must be a "
      "TodaEndToEndCandidatePresentation"
    ),
  ):
    TodaCalculationReportCandidate(
      source_candidate=source_candidate,
      presentation="not-a-presentation",
      report="report",
    )


def test_phase97_2_candidate_rejects_presentation_source_identity_mismatch():
  data = build_phase95_20_data()

  original = get_single_candidate(
    data[
      "results"
    ][
      "pi9_5"
    ]
  )

  first = TodaCalculationCandidate(
    group_result=original.group_result,
    explanation=original.explanation,
    goal_source=original.goal_source,
  )

  second = TodaCalculationCandidate(
    group_result=original.group_result,
    explanation=original.explanation,
    goal_source=original.goal_source,
  )

  presentation = (
    build_toda_end_to_end_candidate_presentation(
      first,
      data[
        "repository"
      ].entries(),
    )
  )

  with pytest.raises(
    ValueError,
    match=(
      "presentation source identity must "
      "match source_candidate"
    ),
  ):
    TodaCalculationReportCandidate(
      source_candidate=second,
      presentation=presentation,
      report="report",
    )


def test_phase97_2_candidate_rejects_non_string_report():
  data = build_phase95_20_data()

  source_candidate = get_single_candidate(
    data[
      "results"
    ][
      "pi9_5"
    ]
  )

  presentation = (
    build_toda_end_to_end_candidate_presentation(
      source_candidate,
      data[
        "repository"
      ].entries(),
    )
  )

  with pytest.raises(
    TypeError,
    match="report must be a str",
  ):
    TodaCalculationReportCandidate(
      source_candidate=source_candidate,
      presentation=presentation,
      report=None,
    )


def test_phase97_2_result_rejects_non_calculation_result():
  with pytest.raises(
    TypeError,
    match=(
      "calculation_result must be "
      "a TodaCalculationResult"
    ),
  ):
    TodaCalculationReportResult(
      calculation_result=(
        "not-a-calculation-result"
      ),
      candidates=(),
    )


def test_phase97_2_result_rejects_non_tuple_candidates():
  calculation_result = (
    TodaCalculationResult(
      query=TodaGroupQuery(
        n=9,
        k=7,
      ),
      candidates=(),
    )
  )

  with pytest.raises(
    TypeError,
    match="candidates must be a tuple",
  ):
    TodaCalculationReportResult(
      calculation_result=calculation_result,
      candidates=[],
    )


def test_phase97_2_result_rejects_non_report_candidate_member():
  calculation_result = (
    TodaCalculationResult(
      query=TodaGroupQuery(
        n=9,
        k=7,
      ),
      candidates=(),
    )
  )

  with pytest.raises(
    TypeError,
    match=(
      "candidates must contain only "
      "TodaCalculationReportCandidate "
      "objects"
    ),
  ):
    TodaCalculationReportResult(
      calculation_result=calculation_result,
      candidates=(
        "not-a-report-candidate",
      ),
    )


def test_phase97_2_result_rejects_candidate_count_mismatch():
  data = build_phase95_20_data()

  calculation_result = (
    data[
      "results"
    ][
      "pi9_5"
    ]
  )

  with pytest.raises(
    ValueError,
    match=(
      "report candidates must match "
      "calculation_result candidates"
    ),
  ):
    TodaCalculationReportResult(
      calculation_result=calculation_result,
      candidates=(),
    )


def test_phase97_2_result_rejects_candidate_identity_mismatch():
  data = build_phase95_20_data()

  original = get_single_candidate(
    data[
      "results"
    ][
      "pi9_5"
    ]
  )

  first = TodaCalculationCandidate(
    group_result=original.group_result,
    explanation=original.explanation,
    goal_source=original.goal_source,
  )

  second = TodaCalculationCandidate(
    group_result=original.group_result,
    explanation=original.explanation,
    goal_source=original.goal_source,
  )

  calculation_result = (
    TodaCalculationResult(
      query=TodaGroupQuery(
        n=5,
        k=4,
      ),
      candidates=(
        first,
      ),
    )
  )

  wrong_report_candidate = (
    build_phase97_2_report_candidate(
      second,
      data[
        "repository"
      ].entries(),
    )
  )

  with pytest.raises(
    ValueError,
    match=(
      "report candidate identity must "
      "match calculation_result candidate "
      "identity in order"
    ),
  ):
    TodaCalculationReportResult(
      calculation_result=calculation_result,
      candidates=(
        wrong_report_candidate,
      ),
    )

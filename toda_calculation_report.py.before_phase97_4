from proof_repository import ProofRepository
from toda_calculation import (
  build_toda_calculation_result,
)
from toda_calculation_report_result import (
  TodaCalculationReportCandidate,
  TodaCalculationReportResult,
)
from toda_calculation_result import (
  TodaCalculationStatus,
)
from toda_end_to_end_presentation import (
  build_toda_end_to_end_candidate_presentation,
)
from toda_full_proof_report_renderer import (
  render_toda_full_proof_report_markdown,
)
from toda_group_query import TodaGroupQuery


def build_toda_found_calculation_report_result(
  repository: ProofRepository,
  query: TodaGroupQuery,
) -> TodaCalculationReportResult:
  calculation_result = (
    build_toda_calculation_result(
      repository,
      query,
    )
  )

  if (
    calculation_result.status
    is not TodaCalculationStatus.FOUND
  ):
    raise ValueError(
      "calculation result must have "
      "status FOUND"
    )

  source_candidate = (
    calculation_result.candidates[
      0
    ]
  )

  presentation = (
    build_toda_end_to_end_candidate_presentation(
      source_candidate,
      repository.entries(),
    )
  )

  report = (
    render_toda_full_proof_report_markdown(
      presentation
    )
  )

  report_candidate = (
    TodaCalculationReportCandidate(
      source_candidate=source_candidate,
      presentation=presentation,
      report=report,
    )
  )

  return TodaCalculationReportResult(
    calculation_result=calculation_result,
    candidates=(
      report_candidate,
    ),
  )

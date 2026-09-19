from proof_repository import ProofRepository
from toda_calculation_report import (
  build_toda_calculation_report_result,
)
from toda_calculation_report_result import (
  TodaCalculationReportResult,
)
from toda_group_query import TodaGroupQuery


def build_toda_report(
  repository: ProofRepository,
  n: int,
  k: int,
) -> TodaCalculationReportResult:
  query = TodaGroupQuery(
    n=n,
    k=k,
  )

  return build_toda_calculation_report_result(
    repository,
    query,
  )

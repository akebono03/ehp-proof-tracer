from proof_repository import ProofRepository
from standard_production_repository import (
  build_standard_production_proof_repository,
)
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


def build_standard_toda_report(
  n: int,
  k: int,
) -> TodaCalculationReportResult:
  repository = (
    build_standard_production_proof_repository()
  )

  return build_toda_report(
    repository,
    n=n,
    k=k,
  )

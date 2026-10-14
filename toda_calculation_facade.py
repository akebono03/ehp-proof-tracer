from __future__ import annotations
from toda_group_query import TodaGroupQuery


def build_toda_report(
  repository: ProofRepository,
  n: int,
  k: int,
) -> TodaCalculationReportResult:
  from toda_calculation_report import build_toda_calculation_report_result
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
  """Retired legacy standard entry; use the common typed search instead."""
  raise RuntimeError(
    "Legacy standard calculation is retired in Phase 165 R27-R24; "
    "use search_group_structure_automatically(n=n, k=k) "
    "and inspect COMPLETE, PARTIAL, or SEARCH_FAILED."
  )

def build_toda_partial_result(query: TodaGroupQuery):
    """Legacy-compatible entry; implementation lives in the independent typed facade."""
    from toda_typed_group_facade import build_toda_partial_result as run_typed_search
    return run_typed_search(query)



def build_standard_toda_partial_result(n: int, k: int):
    """Legacy-compatible entry; implementation lives in the independent typed facade."""
    from toda_typed_group_facade import build_standard_toda_partial_result as run_typed_search
    return run_typed_search(n, k)



from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from proof_repository import ProofRepository
    from toda_calculation_report_result import TodaCalculationReportResult

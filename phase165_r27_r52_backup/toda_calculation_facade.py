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
    """Search a group using the registry-backed prover, never legacy calculation."""
    if not isinstance(query, TodaGroupQuery):
        raise TypeError("query must be a TodaGroupQuery")
    from phase165_r52_r5_auto_search import search_group_structure_automatically
    return search_group_structure_automatically(n=query.n, k=query.k)


def build_standard_toda_partial_result(n: int, k: int):
    """Canonical partial-proof entry for public group-calculation callers."""
    return build_toda_partial_result(TodaGroupQuery(n=n, k=k))


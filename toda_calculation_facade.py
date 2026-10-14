from __future__ import annotations
from toda_group_query import TodaGroupQuery





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

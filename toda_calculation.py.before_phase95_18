from proof_repository import ProofRepository
from toda_calculation_result import (
  TodaCalculationCandidate,
  TodaCalculationResult,
)
from toda_explanation import (
  build_toda_representative_explanation,
)
from toda_group_lookup import (
  find_normalized_toda_group_results,
)
from toda_group_query import TodaGroupQuery


def build_known_toda_calculation_result(
  repository: ProofRepository,
  query: TodaGroupQuery,
) -> TodaCalculationResult:
  group_results = (
    find_normalized_toda_group_results(
      repository,
      query,
    )
  )

  candidates = tuple(
    TodaCalculationCandidate(
      group_result=group_result,
      explanation=(
        build_toda_representative_explanation(
          group_result
        )
      ),
    )
    for group_result in group_results
  )

  return TodaCalculationResult(
    query=query,
    candidates=candidates,
  )

from proof_repository import ProofRepository
from toda_calculation_goal_discovery import (
  discover_concrete_toda_calculation_goal_candidates,
)
from toda_calculation_goal_normalization import (
  normalize_recovered_toda_calculation_goal_candidate,
)
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


def build_toda_calculation_result(
  repository: ProofRepository,
  query: TodaGroupQuery,
) -> TodaCalculationResult:
  known_result = (
    build_known_toda_calculation_result(
      repository,
      query,
    )
  )

  if known_result.candidates:
    return known_result

  discovery_result = (
    discover_concrete_toda_calculation_goal_candidates(
      repository,
      query,
    )
  )

  candidates = []

  for goal_candidate in (
    discovery_result.candidates
  ):
    group_results = (
      normalize_recovered_toda_calculation_goal_candidate(
        goal_candidate
      )
    )

    for group_result in group_results:
      candidates.append(
        TodaCalculationCandidate(
          group_result=group_result,
          explanation=(
            build_toda_representative_explanation(
              group_result
            )
          ),
          goal_source=(
            goal_candidate.source
          ),
        )
      )

  return TodaCalculationResult(
    query=query,
    candidates=tuple(
      candidates
    ),
  )

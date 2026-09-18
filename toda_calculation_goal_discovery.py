from proof_repository import ProofRepository
from toda_calculation_goal import (
  TodaCalculationGoalDiscoveryResult,
)
from toda_calculation_goal_extraction import (
  extract_concrete_toda_calculation_goal_candidates,
)
from toda_group_query import TodaGroupQuery


def discover_concrete_toda_calculation_goal_candidates(
  repository: ProofRepository,
  query: TodaGroupQuery,
) -> TodaCalculationGoalDiscoveryResult:
  if not isinstance(
    repository,
    ProofRepository,
  ):
    raise TypeError(
      "repository must be a ProofRepository"
    )

  if not isinstance(
    query,
    TodaGroupQuery,
  ):
    raise TypeError(
      "query must be a TodaGroupQuery"
    )

  candidates = tuple(
    candidate
    for entry in repository.entries()
    for candidate in (
      extract_concrete_toda_calculation_goal_candidates(
        entry,
        query,
      )
    )
  )

  return TodaCalculationGoalDiscoveryResult(
    query=query,
    candidates=candidates,
  )

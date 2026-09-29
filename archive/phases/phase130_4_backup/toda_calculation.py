from expression import GeneratorSymbol
from proof_repository import (
  ProofRepository,
  ProofRepositoryEntry,
)
from repository_proof_scope import (
  build_repository_proof_scope,
)
from repository_symbolic_sigma_specialization import (
  specialize_repository_proof_scope_for_generator,
)
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
  is_toda_group_result_for_target,
)
from toda_group_query import TodaGroupQuery
from toda_group_result import (
  normalize_toda_group_result,
)


def _find_specialized_sigma_toda_group_results(
  repository: ProofRepository,
  query: TodaGroupQuery,
):
  if query.k != 7:
    return ()

  if query.n < 10:
    return ()

  scope = build_repository_proof_scope(
    repository
  )

  specialized_scope = (
    specialize_repository_proof_scope_for_generator(
      scope,
      GeneratorSymbol(
        family="σ",
        index=query.n,
      ),
    )
  )

  if specialized_scope is scope:
    return ()

  added_nodes = (
    specialized_scope.nodes[
      len(
        scope.nodes
      ):
    ]
  )

  results = []

  for node in added_nodes:
    if not is_toda_group_result_for_target(
      node.proof_step.conclusion,
      query.target,
    ):
      continue

    source_entry = node.root_entry

    specialized_entry = ProofRepositoryEntry(
      key=(
        f"{source_entry.key}::"
        f"sigma_{query.n}_specialization"
      ),
      step=node.proof_step,
      phase=source_entry.phase,
      theorem=source_entry.theorem,
    )

    results.append(
      normalize_toda_group_result(
        specialized_entry
      )
    )

  return tuple(
    results
  )


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

  if not group_results:
    group_results = (
      _find_specialized_sigma_toda_group_results(
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

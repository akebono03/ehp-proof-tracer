from proof_repository import ProofRepository
from repository_nu5_eta8_suspension_zero_specialization import (
  is_nu5_eta8_suspension_zero_operation_query,
  query_nu5_eta8_suspension_zero_handoff,
)
from repository_nu5_stable_bridge_specialization import (
  is_nu5_stable_bridge_operation_query,
  query_nu5_stable_bridge_handoff,
)
from repository_operation_query import (
  parse_repository_operation_query,
)
from repository_operation_query_lookup import (
  RepositoryOperationQueryResult,
  query_repository_operation,
)
from repository_sigma11_suspension_specialization import (
  is_sigma11_suspension_operation_query,
  query_sigma11_suspension_handoff,
)
from standard_production_repository import (
  build_standard_production_proof_repository,
)


def query_repository_operation_input(
  repository: ProofRepository,
  query_input: str,
) -> RepositoryOperationQueryResult:
  query = parse_repository_operation_query(
    query_input
  )

  direct_result = query_repository_operation(
    repository,
    query,
  )

  if direct_result.found:
    return direct_result

  if is_nu5_stable_bridge_operation_query(
    query
  ):
    return query_nu5_stable_bridge_handoff(
      repository,
      query,
    )

  if is_sigma11_suspension_operation_query(
    query
  ):
    return query_sigma11_suspension_handoff(
      repository,
      query,
    )

  if is_nu5_eta8_suspension_zero_operation_query(
    query
  ):
    return query_nu5_eta8_suspension_zero_handoff(
      repository,
      query,
    )

  return direct_result


def query_standard_repository_operation_input(
  query_input: str,
) -> RepositoryOperationQueryResult:
  repository = (
    build_standard_production_proof_repository()
  )

  return query_repository_operation_input(
    repository,
    query_input,
  )

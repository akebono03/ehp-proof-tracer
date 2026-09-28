from proof_repository import ProofRepository
from repository_operation_query import (
  parse_repository_operation_query,
)
from repository_operation_query_lookup import (
  RepositoryOperationQueryResult,
  query_repository_operation,
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

  return query_repository_operation(
    repository,
    query,
  )


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

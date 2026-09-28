from homotopy_groups import (
  DirectSumGroup,
  FiniteCyclicGroup,
  FreeCyclicGroup,
  TodaPrimaryGroup,
  TodaPrimaryGroupZeroStatement,
)
from proof import (
  Relation,
  RelationType,
)
from proof_repository import (
  ProofRepository,
  ProofRepositoryEntry,
)
from toda_group_query import (
  TodaGroupQuery,
)
from toda_group_result import (
  TodaGroupResult,
  normalize_toda_group_result,
)


def is_toda_group_result_for_target(
  conclusion,
  target: TodaPrimaryGroup,
) -> bool:
  if not isinstance(
    target,
    TodaPrimaryGroup,
  ):
    raise TypeError(
      "target must be a TodaPrimaryGroup"
    )

  if isinstance(
    conclusion,
    TodaPrimaryGroupZeroStatement,
  ):
    return (
      conclusion.group
      == target
    )

  if not isinstance(
    conclusion,
    Relation,
  ):
    return False

  return (
    conclusion.relation_type
    == RelationType.EQUALITY
    and conclusion.lhs
    == target
    and isinstance(
      conclusion.rhs,
      (
        FreeCyclicGroup,
        FiniteCyclicGroup,
        DirectSumGroup,
      ),
    )
  )


def find_known_toda_group_results(
  repository: ProofRepository,
  query: TodaGroupQuery,
) -> tuple[
  ProofRepositoryEntry,
  ...,
]:
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

  target = query.target

  return tuple(
    entry
    for entry in repository.entries()
    if is_toda_group_result_for_target(
      entry.step.conclusion,
      target,
    )
  )


def find_normalized_toda_group_results(
  repository: ProofRepository,
  query: TodaGroupQuery,
) -> tuple[
  TodaGroupResult,
  ...,
]:
  entries = find_known_toda_group_results(
    repository,
    query,
  )

  return tuple(
    normalize_toda_group_result(
      entry
    )
    for entry in entries
  )

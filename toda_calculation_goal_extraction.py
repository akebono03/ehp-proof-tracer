from proof_repository import ProofRepositoryEntry
from toda_calculation_goal import (
  TodaCalculationGoalCandidate,
  TodaCalculationGoalSource,
)
from toda_group_lookup import (
  is_toda_group_result_for_target,
)
from toda_group_query import TodaGroupQuery
from toda_rules import (
  TodaProp56FiniteDimensionalStatement,
  TodaProp58FiniteDimensionalStatement,
  TodaProp511FiniteDimensionalStatement,
  TodaProp511NuSquaredFiniteDimensionalStatement,
  TodaProp515FiniteDimensionalStatement,
)


def _candidate_for_branch(
  source_entry: ProofRepositoryEntry,
  query: TodaGroupQuery,
  branch_name: str,
  goal,
) -> TodaCalculationGoalCandidate | None:
  if not is_toda_group_result_for_target(
    goal,
    query.target,
  ):
    return None

  return TodaCalculationGoalCandidate(
    target=query.target,
    goal=goal,
    source=TodaCalculationGoalSource(
      source_entry=source_entry,
      branch_name=branch_name,
    ),
  )


def _extract_direct_branches(
  source_entry: ProofRepositoryEntry,
  query: TodaGroupQuery,
  statement,
  branch_names: tuple[str, ...],
) -> tuple[
  TodaCalculationGoalCandidate,
  ...,
]:
  candidates = []

  for branch_name in branch_names:
    candidate = _candidate_for_branch(
      source_entry,
      query,
      branch_name,
      getattr(
        statement,
        branch_name,
      ),
    )

    if candidate is not None:
      candidates.append(
        candidate
      )

  return tuple(
    candidates
  )


def _extract_prop511_nu_squared_branches(
  source_entry: ProofRepositoryEntry,
  query: TodaGroupQuery,
  statement: (
    TodaProp511NuSquaredFiniteDimensionalStatement
  ),
  prefix: str = "",
) -> tuple[
  TodaCalculationGoalCandidate,
  ...,
]:
  branch_names = (
    "pi11_5_group_relation",
    "pi12_6_group_relation",
    "pi13_7_group_relation",
    "pi14_8_group_relation",
  )

  candidates = []

  for branch_name in branch_names:
    source_name = (
      f"{prefix}.{branch_name}"
      if prefix
      else branch_name
    )

    candidate = _candidate_for_branch(
      source_entry,
      query,
      source_name,
      getattr(
        statement,
        branch_name,
      ),
    )

    if candidate is not None:
      candidates.append(
        candidate
      )

  return tuple(
    candidates
  )


def extract_concrete_toda_calculation_goal_candidates(
  source_entry: ProofRepositoryEntry,
  query: TodaGroupQuery,
) -> tuple[
  TodaCalculationGoalCandidate,
  ...,
]:
  if not isinstance(
    source_entry,
    ProofRepositoryEntry,
  ):
    raise TypeError(
      "source_entry must be "
      "a ProofRepositoryEntry"
    )

  if not isinstance(
    query,
    TodaGroupQuery,
  ):
    raise TypeError(
      "query must be a TodaGroupQuery"
    )

  statement = (
    source_entry
    .step
    .conclusion
  )

  if isinstance(
    statement,
    TodaProp56FiniteDimensionalStatement,
  ):
    return _extract_direct_branches(
      source_entry,
      query,
      statement,
      (
        "pi5_2_group_relation",
        "pi6_3_group_relation",
        "pi7_4_group_relation",
        "pi8_5_group_relation",
      ),
    )

  if isinstance(
    statement,
    TodaProp58FiniteDimensionalStatement,
  ):
    return _extract_direct_branches(
      source_entry,
      query,
      statement,
      (
        "pi6_2_group_relation",
        "pi7_3_group_relation",
        "pi8_4_group_relation",
        "pi9_5_group_relation",
      ),
    )

  if isinstance(
    statement,
    TodaProp511NuSquaredFiniteDimensionalStatement,
  ):
    return (
      _extract_prop511_nu_squared_branches(
        source_entry,
        query,
        statement,
      )
    )

  if isinstance(
    statement,
    TodaProp511FiniteDimensionalStatement,
  ):
    direct_candidates = (
      _extract_direct_branches(
        source_entry,
        query,
        statement,
        (
          "pi8_2_group_relation",
          "pi9_3_zero",
          "pi10_4_group_relation",
        ),
      )
    )

    nested_candidates = (
      _extract_prop511_nu_squared_branches(
        source_entry,
        query,
        (
          statement
          .nu_squared_finite_dimensional
        ),
        prefix=(
          "nu_squared_finite_dimensional"
        ),
      )
    )

    return (
      direct_candidates
      + nested_candidates
    )

  if isinstance(
    statement,
    TodaProp515FiniteDimensionalStatement,
  ):
    return _extract_direct_branches(
      source_entry,
      query,
      statement,
      (
        "pi9_2_zero",
        "pi10_3_zero",
        "pi11_4_zero",
        "pi12_5_group_relation",
        "pi13_6_group_relation",
        "pi14_7_group_relation",
        "pi15_8_group_relation",
      ),
    )

  return ()

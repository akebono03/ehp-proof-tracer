from proof_repository import ProofRepositoryEntry
from toda_calculation_goal import (
  TodaCalculationGoalCandidate,
)
from toda_calculation_goal_recovery import (
  recover_toda_calculation_goal_candidate_steps,
)
from toda_group_result import (
  TodaGroupResult,
  normalize_toda_group_result,
)


def normalize_recovered_toda_calculation_goal_candidate(
  candidate: TodaCalculationGoalCandidate,
) -> tuple[
  TodaGroupResult,
  ...,
]:
  if not isinstance(
    candidate,
    TodaCalculationGoalCandidate,
  ):
    raise TypeError(
      "candidate must be a "
      "TodaCalculationGoalCandidate"
    )

  if candidate.source is None:
    return ()

  recovered_steps = (
    recover_toda_calculation_goal_candidate_steps(
      candidate
    )
  )

  results = []

  for recovered_step in recovered_steps:
    if (
      recovered_step.conclusion
      != candidate.goal
    ):
      continue

    source_entry = (
      candidate
      .source
      .source_entry
    )

    ephemeral_entry = ProofRepositoryEntry(
      key=(
        f"{source_entry.key}::"
        f"{candidate.source.branch_name}"
      ),
      step=recovered_step,
      phase=source_entry.phase,
      theorem=source_entry.theorem,
    )

    results.append(
      normalize_toda_group_result(
        ephemeral_entry
      )
    )

  return tuple(
    results
  )

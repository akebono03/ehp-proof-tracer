from proof import ProofStep
from toda_calculation_goal import (
  TodaCalculationGoalCandidate,
)


def _identity_unique_steps(
  steps,
) -> tuple[
  ProofStep,
  ...,
]:
  unique = []
  seen_ids = set()

  for step in steps:
    step_id = id(
      step
    )

    if step_id in seen_ids:
      continue

    seen_ids.add(
      step_id
    )
    unique.append(
      step
    )

  return tuple(
    unique
  )


def recover_toda_calculation_goal_candidate_steps(
  candidate: TodaCalculationGoalCandidate,
) -> tuple[
  ProofStep,
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

  branch_parts = tuple(
    part
    for part in (
      candidate
      .source
      .branch_name
      .split(".")
    )
    if part
  )

  if not branch_parts:
    return ()

  current_steps = (
    candidate
    .source
    .source_entry
    .step,
  )

  for index, branch_part in enumerate(
    branch_parts
  ):
    next_steps = []

    for current_step in current_steps:
      current_statement = (
        current_step.conclusion
      )

      if not hasattr(
        current_statement,
        branch_part,
      ):
        continue

      branch_statement = getattr(
        current_statement,
        branch_part,
      )

      if (
        index
        == len(
          branch_parts
        ) - 1
        and branch_statement
        != candidate.goal
      ):
        continue

      next_steps.extend(
        premise
        for premise
        in current_step.premises
        if (
          isinstance(
            premise,
            ProofStep,
          )
          and premise.conclusion
          == branch_statement
        )
      )

    current_steps = (
      _identity_unique_steps(
        next_steps
      )
    )

    if not current_steps:
      return ()

  return current_steps

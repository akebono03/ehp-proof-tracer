from dataclasses import dataclass

from proof import (
  InferenceRunResult,
  ProofStep,
  find_goal_step,
  run_inference_until_stable_with_history,
)
from proof_repository import ProofRepository


@dataclass(frozen=True)
class RepositoryInferenceResult:
  inference_result: InferenceRunResult
  goal_step: ProofStep | None


def repository_available_steps(
  repository: ProofRepository,
) -> tuple[
  ProofStep,
  ...,
]:
  if not isinstance(
    repository,
    ProofRepository,
  ):
    raise TypeError(
      "repository must be a ProofRepository"
    )

  steps = []
  seen_step_ids = set()

  for entry in repository.entries():
    step_id = id(
      entry.step
    )

    if step_id in seen_step_ids:
      continue

    seen_step_ids.add(
      step_id
    )
    steps.append(
      entry.step
    )

  return tuple(
    steps
  )


def derive_goal_from_repository(
  repository: ProofRepository,
  inference_rules,
  goal,
  max_rounds=None,
) -> RepositoryInferenceResult:
  available_steps = (
    repository_available_steps(
      repository
    )
  )

  inference_result = (
    run_inference_until_stable_with_history(
      inference_rules,
      available_steps,
      max_rounds=max_rounds,
    )
  )

  goal_step = find_goal_step(
    inference_result.steps,
    goal,
  )

  return RepositoryInferenceResult(
    inference_result=inference_result,
    goal_step=goal_step,
  )

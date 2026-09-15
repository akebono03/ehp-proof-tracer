from proof import ProofStep
from proof_repository import ProofRepository


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

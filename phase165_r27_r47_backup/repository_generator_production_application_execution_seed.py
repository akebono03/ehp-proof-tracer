from proof_repository import (
  ProofRepository,
  ProofRepositoryEntry,
)
from repository_generator_production_application_recovery import (
  RepositoryGeneratorProductionApplicationRecovery,
  RepositoryGeneratorProductionApplicationRecoveryStatus,
)


def build_repository_generator_production_application_execution_seed_repository(
  recovery,
) -> ProofRepository:
  if not isinstance(
    recovery,
    RepositoryGeneratorProductionApplicationRecovery,
  ):
    raise TypeError(
      "recovery must be a "
      "RepositoryGeneratorProductionApplicationRecovery"
    )

  if (
    recovery.status
    is not RepositoryGeneratorProductionApplicationRecoveryStatus.UNIQUE
  ):
    raise ValueError(
      "recovery must have UNIQUE status"
    )

  premise_tuple = (
    recovery.premise_tuple
  )

  if premise_tuple is None:
    raise ValueError(
      "UNIQUE recovery must have a premise_tuple"
    )

  root_entry = (
    recovery.candidate.root_entry
  )

  repository = ProofRepository()

  for (
    premise_index,
    premise_step,
  ) in enumerate(
    premise_tuple
  ):
    repository.register(
      ProofRepositoryEntry(
        key=(
          f"{root_entry.key}::"
          "applicability-execution-seed::"
          f"{premise_index:03d}"
        ),
        step=premise_step,
        phase=root_entry.phase,
        theorem=root_entry.theorem,
      )
    )

  return repository

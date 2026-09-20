from proof_repository import (
  ProofRepository,
  ProofRepositoryEntry,
)
from repository_proof_scope_applicability import (
  RepositoryProofScopeApplicabilityCandidate,
)


def build_repository_generator_applicability_execution_seed_repository(
  candidate,
) -> ProofRepository:
  if not isinstance(
    candidate,
    RepositoryProofScopeApplicabilityCandidate,
  ):
    raise TypeError(
      "candidate must be a "
      "RepositoryProofScopeApplicabilityCandidate"
    )

  source_step = (
    candidate
    .candidate
    .source_step
  )
  root_entry = (
    candidate.root_entry
  )

  repository = ProofRepository()
  repository.register(
    ProofRepositoryEntry(
      key=(
        f"{root_entry.key}::"
        "applicability-execution-seed"
      ),
      step=source_step,
      phase=root_entry.phase,
      theorem=root_entry.theorem,
    )
  )

  return repository

from dataclasses import dataclass

from repository_proof_scope_applicability import (
  RepositoryProofScopeApplicabilityCandidate,
)


@dataclass(frozen=True)
class RepositoryGeneratorApplicabilityCandidateHandoff:
  candidate: RepositoryProofScopeApplicabilityCandidate
  goal: object

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.candidate,
      RepositoryProofScopeApplicabilityCandidate,
    ):
      raise TypeError(
        "candidate must be a "
        "RepositoryProofScopeApplicabilityCandidate"
      )

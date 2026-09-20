from dataclasses import dataclass

from repository_generator_applicability_facade import (
  RepositoryGeneratorApplicabilityExplorationResult,
)
from repository_proof_scope_applicability import (
  RepositoryProofScopeApplicabilityCandidate,
)


@dataclass(frozen=True)
class RepositoryGeneratorApplicabilitySelection:
  applicability_result: RepositoryGeneratorApplicabilityExplorationResult
  candidates: tuple[
    RepositoryProofScopeApplicabilityCandidate,
    ...,
  ]

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.applicability_result,
      RepositoryGeneratorApplicabilityExplorationResult,
    ):
      raise TypeError(
        "applicability_result must be a "
        "RepositoryGeneratorApplicabilityExplorationResult"
      )

    if not isinstance(
      self.candidates,
      tuple,
    ):
      raise TypeError(
        "candidates must be a tuple"
      )

    source_positions = {
      id(
        candidate
      ): index
      for index, candidate
      in enumerate(
        self.applicability_result.candidates
      )
    }

    selected_positions = []
    selected_candidate_ids = set()

    for candidate in self.candidates:
      if not isinstance(
        candidate,
        RepositoryProofScopeApplicabilityCandidate,
      ):
        raise TypeError(
          "candidates must contain only "
          "RepositoryProofScopeApplicabilityCandidate "
          "objects"
        )

      candidate_id = id(
        candidate
      )

      if candidate_id not in source_positions:
        raise ValueError(
          "each candidate must be an original "
          "candidate from applicability_result"
        )

      if candidate_id in selected_candidate_ids:
        raise ValueError(
          "candidates must not contain duplicate "
          "candidate identities"
        )

      selected_candidate_ids.add(
        candidate_id
      )
      selected_positions.append(
        source_positions[
          candidate_id
        ]
      )

    if selected_positions != sorted(
      selected_positions
    ):
      raise ValueError(
        "candidates must preserve applicability_result "
        "candidate order"
      )

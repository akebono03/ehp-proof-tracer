from dataclasses import dataclass
from enum import Enum

from repository_proof_scope_applicability import (
  RepositoryProofScopeApplicabilityCandidate,
)
from rule_catalog import (
  InferenceRuleCatalogEntry,
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


class RepositoryGeneratorApplicabilityHandoffValidationStatus(
  Enum
):
  READY = "ready"
  RULE_NOT_IN_EXECUTION_CATALOG = (
    "rule_not_in_execution_catalog"
  )
  RULE_NOT_FIXED_POINT_SAFE = (
    "rule_not_fixed_point_safe"
  )
  GOAL_INCOMPATIBLE = "goal_incompatible"


@dataclass(frozen=True)
class RepositoryGeneratorApplicabilityHandoffValidation:
  handoff: RepositoryGeneratorApplicabilityCandidateHandoff
  status: RepositoryGeneratorApplicabilityHandoffValidationStatus
  execution_entry: InferenceRuleCatalogEntry | None = None

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.handoff,
      RepositoryGeneratorApplicabilityCandidateHandoff,
    ):
      raise TypeError(
        "handoff must be a "
        "RepositoryGeneratorApplicabilityCandidateHandoff"
      )

    if not isinstance(
      self.status,
      RepositoryGeneratorApplicabilityHandoffValidationStatus,
    ):
      raise TypeError(
        "status must be a "
        "RepositoryGeneratorApplicabilityHandoffValidationStatus"
      )

    if (
      self.execution_entry is not None
      and not isinstance(
        self.execution_entry,
        InferenceRuleCatalogEntry,
      )
    ):
      raise TypeError(
        "execution_entry must be an "
        "InferenceRuleCatalogEntry or None"
      )

    if (
      self.status
      is RepositoryGeneratorApplicabilityHandoffValidationStatus.READY
    ):
      if self.execution_entry is None:
        raise ValueError(
          "READY validation requires an execution_entry"
        )

      return

    if self.execution_entry is not None:
      raise ValueError(
        "failed validation must not contain an execution_entry"
      )

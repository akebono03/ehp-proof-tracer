from dataclasses import dataclass
from enum import Enum

from proof import ProofStep
from repository_proof_scope import (
  build_repository_entry_proof_scope,
)
from repository_proof_scope_applicability import (
  RepositoryProofScopeApplicabilityCandidate,
)


class RepositoryGeneratorProductionApplicationRecoveryStatus(
  Enum
):
  NONE = "none"
  UNIQUE = "unique"
  AMBIGUOUS = "ambiguous"


@dataclass(frozen=True)
class RepositoryGeneratorProductionApplicationRecovery:
  candidate: RepositoryProofScopeApplicabilityCandidate
  goal: object
  applications: tuple[
    ProofStep,
    ...,
  ]

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

    if not isinstance(
      self.applications,
      tuple,
    ):
      raise TypeError(
        "applications must be a tuple"
      )

    for application in self.applications:
      if not isinstance(
        application,
        ProofStep,
      ):
        raise TypeError(
          "applications must contain only "
          "ProofStep objects"
        )

  @property
  def status(
    self,
  ) -> RepositoryGeneratorProductionApplicationRecoveryStatus:
    application_count = len(
      self.applications
    )

    if application_count == 0:
      return (
        RepositoryGeneratorProductionApplicationRecoveryStatus
        .NONE
      )

    if application_count == 1:
      return (
        RepositoryGeneratorProductionApplicationRecoveryStatus
        .UNIQUE
      )

    return (
      RepositoryGeneratorProductionApplicationRecoveryStatus
      .AMBIGUOUS
    )

  @property
  def unique_application(
    self,
  ) -> ProofStep | None:
    if (
      self.status
      is not RepositoryGeneratorProductionApplicationRecoveryStatus.UNIQUE
    ):
      return None

    return self.applications[
      0
    ]

  @property
  def premise_tuple(
    self,
  ) -> tuple[
    ProofStep,
    ...,
  ] | None:
    application = self.unique_application

    if application is None:
      return None

    return application.premises


def recover_repository_generator_production_application(
  candidate,
  goal,
) -> RepositoryGeneratorProductionApplicationRecovery:
  if not isinstance(
    candidate,
    RepositoryProofScopeApplicabilityCandidate,
  ):
    raise TypeError(
      "candidate must be a "
      "RepositoryProofScopeApplicabilityCandidate"
    )

  applicability_candidate = (
    candidate.candidate
  )
  premise_index = (
    applicability_candidate.premise_index
  )
  source_step = (
    applicability_candidate.source_step
  )
  inference_rule = (
    applicability_candidate.inference_rule
  )

  root_scope = (
    build_repository_entry_proof_scope(
      candidate.root_entry
    )
  )

  applications = []

  for node in root_scope:
    application = (
      node.proof_step
    )

    if (
      application.inference_rule
      is not inference_rule
    ):
      continue

    if application.conclusion != goal:
      continue

    if premise_index >= len(
      application.premises
    ):
      continue

    if (
      application.premises[
        premise_index
      ]
      is not source_step
    ):
      continue

    applications.append(
      application
    )

  return (
    RepositoryGeneratorProductionApplicationRecovery(
      candidate=candidate,
      goal=goal,
      applications=tuple(
        applications
      ),
    )
  )

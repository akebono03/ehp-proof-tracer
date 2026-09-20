from dataclasses import dataclass

from proof_repository import ProofRepository
from repository_generator_applicability_handoff import (
  RepositoryGeneratorApplicabilityCandidateHandoff,
  RepositoryGeneratorApplicabilityHandoffExecutionResult,
  RepositoryGeneratorApplicabilityHandoffSearchReport,
  RepositoryGeneratorApplicabilityHandoffValidation,
  RepositoryGeneratorApplicabilityHandoffValidationStatus,
  build_repository_generator_applicability_handoff_search_report,
  execute_repository_generator_applicability_handoff_search_report,
  validate_repository_generator_applicability_handoff,
)
from repository_generator_production_application_execution_seed import (
  build_repository_generator_production_application_execution_seed_repository,
)
from repository_generator_production_application_recovery import (
  RepositoryGeneratorProductionApplicationRecovery,
  RepositoryGeneratorProductionApplicationRecoveryStatus,
  recover_repository_generator_production_application,
)
from repository_proof_scope_applicability import (
  RepositoryProofScopeApplicabilityCandidate,
)
from rule_catalog import InferenceRuleCatalog


@dataclass(frozen=True)
class TwoPremiseProductionApplicationExecutionResult:
  candidate: RepositoryProofScopeApplicabilityCandidate
  goal: object
  recovery: RepositoryGeneratorProductionApplicationRecovery
  seed_repository: ProofRepository
  execution_catalog: InferenceRuleCatalog
  handoff: RepositoryGeneratorApplicabilityCandidateHandoff
  validation: RepositoryGeneratorApplicabilityHandoffValidation
  search_report: RepositoryGeneratorApplicabilityHandoffSearchReport
  execution: RepositoryGeneratorApplicabilityHandoffExecutionResult

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
      self.recovery,
      RepositoryGeneratorProductionApplicationRecovery,
    ):
      raise TypeError(
        "recovery must be a "
        "RepositoryGeneratorProductionApplicationRecovery"
      )

    if (
      self.recovery.candidate
      is not self.candidate
    ):
      raise ValueError(
        "recovery candidate must preserve "
        "candidate identity"
      )

    if (
      self.recovery.goal
      != self.goal
    ):
      raise ValueError(
        "recovery goal must match result goal"
      )

    if (
      self.recovery.status
      is not RepositoryGeneratorProductionApplicationRecoveryStatus.UNIQUE
    ):
      raise ValueError(
        "recovery must have UNIQUE status"
      )

    premise_tuple = (
      self.recovery.premise_tuple
    )

    if (
      premise_tuple is None
      or len(
        premise_tuple
      ) != 2
    ):
      raise ValueError(
        "recovery must contain exactly two premises"
      )

    if not isinstance(
      self.seed_repository,
      ProofRepository,
    ):
      raise TypeError(
        "seed_repository must be a ProofRepository"
      )

    if not isinstance(
      self.execution_catalog,
      InferenceRuleCatalog,
    ):
      raise TypeError(
        "execution_catalog must be an InferenceRuleCatalog"
      )

    if (
      self.handoff.candidate
      is not self.candidate
    ):
      raise ValueError(
        "handoff candidate must preserve candidate identity"
      )

    if (
      self.handoff.goal
      != self.goal
    ):
      raise ValueError(
        "handoff goal must match result goal"
      )

    if (
      self.validation.handoff
      is not self.handoff
    ):
      raise ValueError(
        "validation must preserve handoff identity"
      )

    if (
      self.validation.status
      is not RepositoryGeneratorApplicabilityHandoffValidationStatus.READY
    ):
      raise ValueError(
        "validation must be READY"
      )

    if (
      self.search_report.validation
      is not self.validation
    ):
      raise ValueError(
        "search_report must preserve validation identity"
      )

    if (
      self.execution.search_report
      is not self.search_report
    ):
      raise ValueError(
        "execution must preserve search_report identity"
      )


def execute_two_premise_repository_generator_production_application_candidate(
  candidate,
  goal,
  execution_catalog,
  max_depth=2,
  retry_policy=None,
) -> TwoPremiseProductionApplicationExecutionResult:
  if not isinstance(
    candidate,
    RepositoryProofScopeApplicabilityCandidate,
  ):
    raise TypeError(
      "candidate must be a "
      "RepositoryProofScopeApplicabilityCandidate"
    )

  if not isinstance(
    execution_catalog,
    InferenceRuleCatalog,
  ):
    raise TypeError(
      "execution_catalog must be an InferenceRuleCatalog"
    )

  recovery = (
    recover_repository_generator_production_application(
      candidate,
      goal,
    )
  )

  if (
    recovery.status
    is not RepositoryGeneratorProductionApplicationRecoveryStatus.UNIQUE
  ):
    raise ValueError(
      "production application recovery must be UNIQUE"
    )

  premise_tuple = (
    recovery.premise_tuple
  )

  if (
    premise_tuple is None
    or len(
      premise_tuple
    ) != 2
  ):
    raise ValueError(
      "production application must have exactly two premises"
    )

  seed_repository = (
    build_repository_generator_production_application_execution_seed_repository(
      recovery
    )
  )

  handoff = (
    RepositoryGeneratorApplicabilityCandidateHandoff(
      candidate=candidate,
      goal=goal,
    )
  )

  validation = (
    validate_repository_generator_applicability_handoff(
      handoff,
      execution_catalog,
    )
  )

  if (
    validation.status
    is not RepositoryGeneratorApplicabilityHandoffValidationStatus.READY
  ):
    raise ValueError(
      "two-premise production applicability handoff "
      "must validate as READY"
    )

  search_report = (
    build_repository_generator_applicability_handoff_search_report(
      validation,
      seed_repository,
      execution_catalog,
      max_depth=max_depth,
      retry_policy=retry_policy,
    )
  )

  execution = (
    execute_repository_generator_applicability_handoff_search_report(
      search_report,
      seed_repository,
    )
  )

  return TwoPremiseProductionApplicationExecutionResult(
    candidate=candidate,
    goal=goal,
    recovery=recovery,
    seed_repository=seed_repository,
    execution_catalog=execution_catalog,
    handoff=handoff,
    validation=validation,
    search_report=search_report,
    execution=execution,
  )

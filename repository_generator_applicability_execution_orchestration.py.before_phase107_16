from dataclasses import dataclass

from proof_repository import ProofRepository
from repository_generator_applicability_execution_entry import (
  build_first_qualified_production_execution_catalog,
)
from repository_generator_applicability_execution_seed import (
  build_repository_generator_applicability_execution_seed_repository,
)
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
from repository_proof_scope_applicability import (
  RepositoryProofScopeApplicabilityCandidate,
)
from rule_catalog import InferenceRuleCatalog


@dataclass(frozen=True)
class FirstQualifiedProductionApplicabilityExecutionResult:
  candidate: RepositoryProofScopeApplicabilityCandidate
  goal: object
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


def execute_first_qualified_production_applicability_candidate(
  candidate,
  goal,
  max_depth=2,
  retry_policy=None,
) -> FirstQualifiedProductionApplicabilityExecutionResult:
  if not isinstance(
    candidate,
    RepositoryProofScopeApplicabilityCandidate,
  ):
    raise TypeError(
      "candidate must be a "
      "RepositoryProofScopeApplicabilityCandidate"
    )

  seed_repository = (
    build_repository_generator_applicability_execution_seed_repository(
      candidate
    )
  )

  execution_catalog = (
    build_first_qualified_production_execution_catalog(
      candidate,
      goal,
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
      "qualified production applicability handoff "
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

  return FirstQualifiedProductionApplicabilityExecutionResult(
    candidate=candidate,
    goal=goal,
    seed_repository=seed_repository,
    execution_catalog=execution_catalog,
    handoff=handoff,
    validation=validation,
    search_report=search_report,
    execution=execution,
  )

from dataclasses import dataclass
from enum import Enum

from proof_repository import (
  ProofRepository,
)
from repository_inference import (
  BoundedProducerSearchReport,
  _build_bounded_producer_search_report_for_final_rule,
)
from repository_proof_scope_applicability import (
  RepositoryProofScopeApplicabilityCandidate,
)
from rule_catalog import (
  InferenceRuleCatalog,
  InferenceRuleCatalogEntry,
  find_goal_compatible_rule_entries,
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


@dataclass(frozen=True)
class RepositoryGeneratorApplicabilityHandoffSearchReport:
  validation: RepositoryGeneratorApplicabilityHandoffValidation
  report: BoundedProducerSearchReport

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.validation,
      RepositoryGeneratorApplicabilityHandoffValidation,
    ):
      raise TypeError(
        "validation must be a "
        "RepositoryGeneratorApplicabilityHandoffValidation"
      )

    if (
      self.validation.status
      is not RepositoryGeneratorApplicabilityHandoffValidationStatus.READY
    ):
      raise ValueError(
        "validation must be READY"
      )

    if not isinstance(
      self.report,
      BoundedProducerSearchReport,
    ):
      raise TypeError(
        "report must be a BoundedProducerSearchReport"
      )

    if (
      self.report.goal
      != self.validation.handoff.goal
    ):
      raise ValueError(
        "report goal must match handoff goal"
      )

    if self.report.search_result is None:
      return

    execution_entry = (
      self.validation.execution_entry
    )

    if execution_entry is None:
      raise ValueError(
        "READY validation requires an execution_entry"
      )

    if (
      self.report.search_result.final_rule
      is not execution_entry.rule
    ):
      raise ValueError(
        "search result final_rule must be "
        "validation execution_entry.rule"
      )


def validate_repository_generator_applicability_handoff(
  handoff,
  execution_catalog,
):
  if not isinstance(
    handoff,
    RepositoryGeneratorApplicabilityCandidateHandoff,
  ):
    raise TypeError(
      "handoff must be a "
      "RepositoryGeneratorApplicabilityCandidateHandoff"
    )

  if not isinstance(
    execution_catalog,
    InferenceRuleCatalog,
  ):
    raise TypeError(
      "execution_catalog must be an "
      "InferenceRuleCatalog"
    )

  selected_rule = (
    handoff
    .candidate
    .candidate
    .inference_rule
  )

  same_rule_entries = tuple(
    entry
    for entry in execution_catalog.entries()
    if entry.rule is selected_rule
  )

  if not same_rule_entries:
    return (
      RepositoryGeneratorApplicabilityHandoffValidation(
        handoff=handoff,
        status=(
          RepositoryGeneratorApplicabilityHandoffValidationStatus
          .RULE_NOT_IN_EXECUTION_CATALOG
        ),
      )
    )

  safe_same_rule_entries = tuple(
    entry
    for entry in same_rule_entries
    if entry.fixed_point_safe
  )

  if not safe_same_rule_entries:
    return (
      RepositoryGeneratorApplicabilityHandoffValidation(
        handoff=handoff,
        status=(
          RepositoryGeneratorApplicabilityHandoffValidationStatus
          .RULE_NOT_FIXED_POINT_SAFE
        ),
      )
    )

  same_rule_catalog = InferenceRuleCatalog()

  for entry in safe_same_rule_entries:
    same_rule_catalog.register(
      entry
    )

  goal_compatible_entries = (
    find_goal_compatible_rule_entries(
      same_rule_catalog,
      handoff.goal,
    )
  )

  if not goal_compatible_entries:
    return (
      RepositoryGeneratorApplicabilityHandoffValidation(
        handoff=handoff,
        status=(
          RepositoryGeneratorApplicabilityHandoffValidationStatus
          .GOAL_INCOMPATIBLE
        ),
      )
    )

  return RepositoryGeneratorApplicabilityHandoffValidation(
    handoff=handoff,
    status=(
      RepositoryGeneratorApplicabilityHandoffValidationStatus
      .READY
    ),
    execution_entry=goal_compatible_entries[
      0
    ],
  )


def build_repository_generator_applicability_handoff_search_report(
  validation,
  repository,
  execution_catalog,
  max_depth=2,
  retry_policy=None,
):
  if not isinstance(
    validation,
    RepositoryGeneratorApplicabilityHandoffValidation,
  ):
    raise TypeError(
      "validation must be a "
      "RepositoryGeneratorApplicabilityHandoffValidation"
    )

  if (
    validation.status
    is not RepositoryGeneratorApplicabilityHandoffValidationStatus.READY
  ):
    raise ValueError(
      "validation must be READY"
    )

  if not isinstance(
    repository,
    ProofRepository,
  ):
    raise TypeError(
      "repository must be a ProofRepository"
    )

  if not isinstance(
    execution_catalog,
    InferenceRuleCatalog,
  ):
    raise TypeError(
      "execution_catalog must be an "
      "InferenceRuleCatalog"
    )

  execution_entry = (
    validation.execution_entry
  )

  if execution_entry is None:
    raise ValueError(
      "READY validation requires an execution_entry"
    )

  report = (
    _build_bounded_producer_search_report_for_final_rule(
      repository,
      execution_catalog,
      validation.handoff.goal,
      execution_entry.rule,
      max_depth=max_depth,
      retry_policy=retry_policy,
    )
  )

  return (
    RepositoryGeneratorApplicabilityHandoffSearchReport(
      validation=validation,
      report=report,
    )
  )

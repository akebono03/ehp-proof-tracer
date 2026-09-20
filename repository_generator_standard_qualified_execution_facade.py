from dataclasses import dataclass

from proof import (
  ProofStep,
)
from proof_repository import (
  ProofRepositoryEntry,
)
from repository_generator_applicability_execution_orchestration import (
  FirstQualifiedProductionApplicabilityExecutionResult,
  execute_first_qualified_production_applicability_candidate,
)
from repository_generator_applicability_facade import (
  RepositoryGeneratorApplicabilityExplorationResult,
)
from repository_generator_qualified_execution_family import (
  RepositoryGeneratorQualifiedExecutionFamilyGrouping,
  group_qualified_repository_generator_execution_families,
)
from repository_generator_qualified_execution_family_selection import (
  RepositoryGeneratorQualifiedExecutionFamilySelection,
  select_qualified_repository_generator_execution_family_by_root_and_source,
)
from repository_generator_qualified_execution_selection import (
  RepositoryGeneratorQualifiedExecutionSelection,
  select_qualified_repository_generator_applicability_candidates,
)


@dataclass(frozen=True)
class StandardRepositoryGeneratorQualifiedExecutionFacadeResult:
  applicability_result: RepositoryGeneratorApplicabilityExplorationResult
  qualified_selection: RepositoryGeneratorQualifiedExecutionSelection
  family_grouping: RepositoryGeneratorQualifiedExecutionFamilyGrouping
  family_selection: RepositoryGeneratorQualifiedExecutionFamilySelection
  execution: FirstQualifiedProductionApplicabilityExecutionResult | None

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
      self.qualified_selection,
      RepositoryGeneratorQualifiedExecutionSelection,
    ):
      raise TypeError(
        "qualified_selection must be a "
        "RepositoryGeneratorQualifiedExecutionSelection"
      )

    if not isinstance(
      self.family_grouping,
      RepositoryGeneratorQualifiedExecutionFamilyGrouping,
    ):
      raise TypeError(
        "family_grouping must be a "
        "RepositoryGeneratorQualifiedExecutionFamilyGrouping"
      )

    if not isinstance(
      self.family_selection,
      RepositoryGeneratorQualifiedExecutionFamilySelection,
    ):
      raise TypeError(
        "family_selection must be a "
        "RepositoryGeneratorQualifiedExecutionFamilySelection"
      )

    if (
      self.qualified_selection.applicability_result
      is not self.applicability_result
    ):
      raise ValueError(
        "qualified_selection must preserve applicability_result identity"
      )

    if (
      self.family_grouping.selection
      is not self.qualified_selection
    ):
      raise ValueError(
        "family_grouping must preserve qualified_selection identity"
      )

    if (
      self.family_selection.grouping
      is not self.family_grouping
    ):
      raise ValueError(
        "family_selection must preserve family_grouping identity"
      )

    representative = (
      self.family_selection.representative
    )

    if representative is None:
      if self.execution is not None:
        raise ValueError(
          "execution must be None when no family group is selected"
        )

      return

    if not isinstance(
      self.execution,
      FirstQualifiedProductionApplicabilityExecutionResult,
    ):
      raise TypeError(
        "execution must be a "
        "FirstQualifiedProductionApplicabilityExecutionResult "
        "when a family group is selected"
      )

    if (
      self.execution.candidate
      is not representative
    ):
      raise ValueError(
        "execution candidate must be the selected family representative"
      )

  @property
  def selected_group(
    self,
  ):
    return (
      self.family_selection.selected_group
    )

  @property
  def representative(
    self,
  ):
    return (
      self.family_selection.representative
    )

  @property
  def executed(
    self,
  ) -> bool:
    return self.execution is not None


def execute_standard_repository_generator_applicability_result_by_root_and_source(
  applicability_result,
  root_entry,
  source_step,
  goal,
  max_depth=2,
  retry_policy=None,
) -> StandardRepositoryGeneratorQualifiedExecutionFacadeResult:
  if not isinstance(
    applicability_result,
    RepositoryGeneratorApplicabilityExplorationResult,
  ):
    raise TypeError(
      "applicability_result must be a "
      "RepositoryGeneratorApplicabilityExplorationResult"
    )

  if not isinstance(
    root_entry,
    ProofRepositoryEntry,
  ):
    raise TypeError(
      "root_entry must be a ProofRepositoryEntry"
    )

  if not isinstance(
    source_step,
    ProofStep,
  ):
    raise TypeError(
      "source_step must be a ProofStep"
    )

  qualified_selection = (
    select_qualified_repository_generator_applicability_candidates(
      applicability_result
    )
  )

  family_grouping = (
    group_qualified_repository_generator_execution_families(
      qualified_selection
    )
  )

  family_selection = (
    select_qualified_repository_generator_execution_family_by_root_and_source(
      family_grouping,
      root_entry,
      source_step,
    )
  )

  representative = (
    family_selection.representative
  )

  execution = None

  if representative is not None:
    execution = (
      execute_first_qualified_production_applicability_candidate(
        representative,
        goal,
        max_depth=max_depth,
        retry_policy=retry_policy,
      )
    )

  return StandardRepositoryGeneratorQualifiedExecutionFacadeResult(
    applicability_result=applicability_result,
    qualified_selection=qualified_selection,
    family_grouping=family_grouping,
    family_selection=family_selection,
    execution=execution,
  )

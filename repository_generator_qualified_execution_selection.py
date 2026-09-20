from dataclasses import dataclass
from enum import Enum

from repository_generator_applicability_execution_entry import (
  is_first_qualified_production_execution_candidate,
)
from repository_generator_applicability_facade import (
  RepositoryGeneratorApplicabilityExplorationResult,
)
from repository_generator_applicability_selection import (
  RepositoryGeneratorApplicabilitySelection,
)


class RepositoryGeneratorQualifiedExecutionSelectionStatus(
  Enum
):
  NONE = "none"
  UNIQUE = "unique"
  AMBIGUOUS = "ambiguous"


@dataclass(frozen=True)
class RepositoryGeneratorQualifiedExecutionSelection:
  selection: RepositoryGeneratorApplicabilitySelection

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.selection,
      RepositoryGeneratorApplicabilitySelection,
    ):
      raise TypeError(
        "selection must be a "
        "RepositoryGeneratorApplicabilitySelection"
      )

  @property
  def applicability_result(
    self,
  ) -> RepositoryGeneratorApplicabilityExplorationResult:
    return self.selection.applicability_result

  @property
  def candidates(
    self,
  ):
    return self.selection.candidates

  @property
  def status(
    self,
  ) -> RepositoryGeneratorQualifiedExecutionSelectionStatus:
    candidate_count = len(
      self.candidates
    )

    if candidate_count == 0:
      return (
        RepositoryGeneratorQualifiedExecutionSelectionStatus
        .NONE
      )

    if candidate_count == 1:
      return (
        RepositoryGeneratorQualifiedExecutionSelectionStatus
        .UNIQUE
      )

    return (
      RepositoryGeneratorQualifiedExecutionSelectionStatus
      .AMBIGUOUS
    )

  @property
  def unique_candidate(
    self,
  ):
    if (
      self.status
      is not RepositoryGeneratorQualifiedExecutionSelectionStatus.UNIQUE
    ):
      return None

    return self.candidates[
      0
    ]


def select_qualified_repository_generator_applicability_candidates(
  applicability_result,
) -> RepositoryGeneratorQualifiedExecutionSelection:
  if not isinstance(
    applicability_result,
    RepositoryGeneratorApplicabilityExplorationResult,
  ):
    raise TypeError(
      "applicability_result must be a "
      "RepositoryGeneratorApplicabilityExplorationResult"
    )

  candidates = tuple(
    candidate
    for candidate
    in applicability_result.candidates
    if (
      is_first_qualified_production_execution_candidate(
        candidate
      )
    )
  )

  selection = (
    RepositoryGeneratorApplicabilitySelection(
      applicability_result=applicability_result,
      candidates=candidates,
    )
  )

  return RepositoryGeneratorQualifiedExecutionSelection(
    selection=selection,
  )

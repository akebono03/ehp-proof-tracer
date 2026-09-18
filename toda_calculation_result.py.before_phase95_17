from dataclasses import dataclass
from enum import Enum

from homotopy_groups import TodaPrimaryGroup
from toda_explanation import (
  TodaRepresentativeExplanationResult,
)
from toda_group_query import TodaGroupQuery
from toda_group_result import TodaGroupResult


class TodaCalculationStatus(Enum):
  NOT_FOUND = "not_found"
  FOUND = "found"
  MULTIPLE_RESULTS = "multiple_results"


@dataclass(frozen=True)
class TodaCalculationCandidate:
  group_result: TodaGroupResult
  explanation: TodaRepresentativeExplanationResult

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.group_result,
      TodaGroupResult,
    ):
      raise TypeError(
        "group_result must be "
        "a TodaGroupResult"
      )

    if not isinstance(
      self.explanation,
      TodaRepresentativeExplanationResult,
    ):
      raise TypeError(
        "explanation must be "
        "a TodaRepresentativeExplanationResult"
      )

    if (
      self.explanation.group_result
      is not self.group_result
    ):
      raise ValueError(
        "explanation.group_result must be "
        "group_result"
      )


@dataclass(frozen=True)
class TodaCalculationResult:
  query: TodaGroupQuery
  candidates: tuple[
    TodaCalculationCandidate,
    ...,
  ]

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.query,
      TodaGroupQuery,
    ):
      raise TypeError(
        "query must be a TodaGroupQuery"
      )

    if not isinstance(
      self.candidates,
      tuple,
    ):
      raise TypeError(
        "candidates must be a tuple"
      )

    target = self.query.target

    for candidate in self.candidates:
      if not isinstance(
        candidate,
        TodaCalculationCandidate,
      ):
        raise TypeError(
          "candidates must contain only "
          "TodaCalculationCandidate objects"
        )

      if (
        candidate.group_result.target
        != target
      ):
        raise ValueError(
          "candidate target must match "
          "query target"
        )

  @property
  def target(
    self,
  ) -> TodaPrimaryGroup:
    return self.query.target

  @property
  def status(
    self,
  ) -> TodaCalculationStatus:
    if not self.candidates:
      return (
        TodaCalculationStatus
        .NOT_FOUND
      )

    if len(self.candidates) == 1:
      return (
        TodaCalculationStatus
        .FOUND
      )

    return (
      TodaCalculationStatus
      .MULTIPLE_RESULTS
    )

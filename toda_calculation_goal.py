from dataclasses import dataclass
from enum import Enum

from homotopy_groups import TodaPrimaryGroup
from proof_repository import ProofRepositoryEntry
from toda_group_lookup import (
  is_toda_group_result_for_target,
)
from toda_group_query import TodaGroupQuery


class TodaCalculationGoalDiscoveryStatus(
  Enum
):
  NO_CANDIDATES = "no_candidates"
  UNIQUE_CANDIDATE = "unique_candidate"
  MULTIPLE_CANDIDATES = (
    "multiple_candidates"
  )


@dataclass(frozen=True)
class TodaCalculationGoalSource:
  source_entry: ProofRepositoryEntry
  branch_name: str

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.source_entry,
      ProofRepositoryEntry,
    ):
      raise TypeError(
        "source_entry must be "
        "a ProofRepositoryEntry"
      )

    if not isinstance(
      self.branch_name,
      str,
    ):
      raise TypeError(
        "branch_name must be a str"
      )

    if not self.branch_name:
      raise ValueError(
        "branch_name must not be empty"
      )


@dataclass(frozen=True)
class TodaCalculationGoalCandidate:
  target: TodaPrimaryGroup
  goal: object
  source: (
    TodaCalculationGoalSource
    | None
  ) = None

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.target,
      TodaPrimaryGroup,
    ):
      raise TypeError(
        "target must be a TodaPrimaryGroup"
      )

    if not is_toda_group_result_for_target(
      self.goal,
      self.target,
    ):
      raise ValueError(
        "goal must be a normalizable "
        "Toda group result statement "
        "for target"
      )

    if (
      self.source is not None
      and not isinstance(
        self.source,
        TodaCalculationGoalSource,
      )
    ):
      raise TypeError(
        "source must be a "
        "TodaCalculationGoalSource "
        "or None"
      )


@dataclass(frozen=True)
class TodaCalculationGoalDiscoveryResult:
  query: TodaGroupQuery
  candidates: tuple[
    TodaCalculationGoalCandidate,
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

    for candidate in self.candidates:
      if not isinstance(
        candidate,
        TodaCalculationGoalCandidate,
      ):
        raise TypeError(
          "candidates must contain only "
          "TodaCalculationGoalCandidate "
          "objects"
        )

      if (
        candidate.target
        != self.query.target
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
  ) -> TodaCalculationGoalDiscoveryStatus:
    if not self.candidates:
      return (
        TodaCalculationGoalDiscoveryStatus
        .NO_CANDIDATES
      )

    if len(self.candidates) == 1:
      return (
        TodaCalculationGoalDiscoveryStatus
        .UNIQUE_CANDIDATE
      )

    return (
      TodaCalculationGoalDiscoveryStatus
      .MULTIPLE_CANDIDATES
    )

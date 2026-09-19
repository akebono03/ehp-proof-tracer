from dataclasses import dataclass

from homotopy_groups import TodaPrimaryGroup
from toda_calculation_result import (
  TodaCalculationCandidate,
  TodaCalculationResult,
  TodaCalculationStatus,
)
from toda_end_to_end_presentation import (
  TodaEndToEndCandidatePresentation,
)
from toda_group_query import TodaGroupQuery


@dataclass(frozen=True)
class TodaCalculationReportCandidate:
  source_candidate: TodaCalculationCandidate
  presentation: TodaEndToEndCandidatePresentation
  report: str

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.source_candidate,
      TodaCalculationCandidate,
    ):
      raise TypeError(
        "source_candidate must be "
        "a TodaCalculationCandidate"
      )

    if not isinstance(
      self.presentation,
      TodaEndToEndCandidatePresentation,
    ):
      raise TypeError(
        "presentation must be a "
        "TodaEndToEndCandidatePresentation"
      )

    if (
      self.presentation.source_candidate
      is not self.source_candidate
    ):
      raise ValueError(
        "presentation source identity must "
        "match source_candidate"
      )

    if not isinstance(
      self.report,
      str,
    ):
      raise TypeError(
        "report must be a str"
      )


@dataclass(frozen=True)
class TodaCalculationReportResult:
  calculation_result: TodaCalculationResult
  candidates: tuple[
    TodaCalculationReportCandidate,
    ...,
  ]

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.calculation_result,
      TodaCalculationResult,
    ):
      raise TypeError(
        "calculation_result must be "
        "a TodaCalculationResult"
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
        TodaCalculationReportCandidate,
      ):
        raise TypeError(
          "candidates must contain only "
          "TodaCalculationReportCandidate "
          "objects"
        )

    if (
      len(self.candidates)
      != len(
        self.calculation_result
        .candidates
      )
    ):
      raise ValueError(
        "report candidates must match "
        "calculation_result candidates"
      )

    for (
      report_candidate,
      calculation_candidate,
    ) in zip(
      self.candidates,
      self.calculation_result.candidates,
    ):
      if (
        report_candidate.source_candidate
        is not calculation_candidate
      ):
        raise ValueError(
          "report candidate identity must "
          "match calculation_result candidate "
          "identity in order"
        )

  @property
  def query(
    self,
  ) -> TodaGroupQuery:
    return self.calculation_result.query

  @property
  def target(
    self,
  ) -> TodaPrimaryGroup:
    return self.calculation_result.target

  @property
  def status(
    self,
  ) -> TodaCalculationStatus:
    return self.calculation_result.status

  @property
  def report(
    self,
  ) -> str:
    if (
      self.status
      is not TodaCalculationStatus.FOUND
    ):
      raise ValueError(
        "report is available only when "
        "status is FOUND"
      )

    return self.candidates[
      0
    ].report

  @property
  def reports(
    self,
  ) -> tuple[
    str,
    ...,
  ]:
    return tuple(
      candidate.report
      for candidate in self.candidates
    )

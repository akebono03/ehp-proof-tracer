from dataclasses import dataclass

from homotopy_groups import TodaPrimaryGroup
from toda_calculation_goal import (
  TodaCalculationGoalSource,
)
from toda_calculation_result import (
  TodaCalculationCandidate,
  TodaCalculationResult,
  TodaCalculationStatus,
)
from toda_ehp_exactness_provenance import (
  TodaEHPExactnessUseProvenanceResult,
)
from toda_ehp_result import (
  TodaEHPSequenceResult,
)
from toda_explanation import (
  TodaRepresentativeExplanationResult,
)
from toda_group_query import TodaGroupQuery
from toda_group_result import TodaGroupResult
from toda_proof_dependency import (
  TodaProofDependencyResult,
  TodaRecursiveProofProvenanceResult,
)


@dataclass(frozen=True)
class TodaCalculationPresentationCandidate:
  source_candidate: TodaCalculationCandidate

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

  @property
  def group_result(
    self,
  ) -> TodaGroupResult:
    return (
      self.source_candidate
      .group_result
    )

  @property
  def explanation(
    self,
  ) -> TodaRepresentativeExplanationResult:
    return (
      self.source_candidate
      .explanation
    )

  @property
  def ehp_result(
    self,
  ) -> TodaEHPSequenceResult | None:
    return (
      self.explanation
      .ehp_result
    )

  @property
  def exactness_provenance(
    self,
  ) -> (
    TodaEHPExactnessUseProvenanceResult
    | None
  ):
    return (
      self.explanation
      .exactness_provenance
    )

  @property
  def dependency_result(
    self,
  ) -> TodaProofDependencyResult:
    return (
      self.explanation
      .dependency_result
    )

  @property
  def recursive_provenance(
    self,
  ) -> TodaRecursiveProofProvenanceResult:
    return (
      self.explanation
      .recursive_provenance
    )

  @property
  def goal_source(
    self,
  ) -> TodaCalculationGoalSource | None:
    return (
      self.source_candidate
      .goal_source
    )


@dataclass(frozen=True)
class TodaCalculationPresentationResult:
  source_result: TodaCalculationResult
  candidates: tuple[
    TodaCalculationPresentationCandidate,
    ...,
  ]

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.source_result,
      TodaCalculationResult,
    ):
      raise TypeError(
        "source_result must be "
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
        TodaCalculationPresentationCandidate,
      ):
        raise TypeError(
          "candidates must contain only "
          "TodaCalculationPresentationCandidate "
          "objects"
        )

    if (
      len(self.candidates)
      != len(
        self.source_result
        .candidates
      )
    ):
      raise ValueError(
        "presentation candidates must match "
        "source_result candidates"
      )

    for (
      presentation_candidate,
      source_candidate,
    ) in zip(
      self.candidates,
      self.source_result.candidates,
    ):
      if (
        presentation_candidate
        .source_candidate
        is not source_candidate
      ):
        raise ValueError(
          "presentation candidate identity "
          "must match source_result candidate "
          "identity in order"
        )

  @property
  def query(
    self,
  ) -> TodaGroupQuery:
    return self.source_result.query

  @property
  def target(
    self,
  ) -> TodaPrimaryGroup:
    return self.source_result.target

  @property
  def status(
    self,
  ) -> TodaCalculationStatus:
    return self.source_result.status


def build_toda_calculation_presentation_result(
  calculation_result: TodaCalculationResult,
) -> TodaCalculationPresentationResult:
  if not isinstance(
    calculation_result,
    TodaCalculationResult,
  ):
    raise TypeError(
      "calculation_result must be "
      "a TodaCalculationResult"
    )

  candidates = tuple(
    TodaCalculationPresentationCandidate(
      source_candidate=candidate,
    )
    for candidate in (
      calculation_result
      .candidates
    )
  )

  return TodaCalculationPresentationResult(
    source_result=calculation_result,
    candidates=candidates,
  )

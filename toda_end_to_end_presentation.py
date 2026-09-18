from dataclasses import dataclass

from proof_repository import ProofRepositoryEntry
from toda_calculation_result import (
  TodaCalculationCandidate,
)
from toda_ehp_presentation import (
  TodaEHPExactnessPresentation,
  TodaEHPSequencePresentation,
  build_toda_ehp_exactness_presentation,
)
from toda_presentation import (
  TodaCalculationPresentationCandidate,
  TodaGroupResultPresentation,
  build_toda_group_result_presentation,
)
from toda_proof_flow_presentation import (
  TodaReadableProofFlowPresentation,
  build_toda_readable_proof_flow_presentation,
)
from toda_proof_presentation import (
  TodaCalculationCandidateSourcePresentation,
  TodaProofDependencyPresentationResult,
  build_toda_calculation_candidate_source_presentation,
  build_toda_proof_dependency_presentation_result,
)


@dataclass(frozen=True)
class TodaEndToEndCandidatePresentation:
  source_candidate: TodaCalculationCandidate
  calculation_candidate: (
    TodaCalculationPresentationCandidate
  )
  group: TodaGroupResultPresentation
  ehp: TodaEHPSequencePresentation | None
  exactness: (
    TodaEHPExactnessPresentation
    | None
  )
  dependencies: (
    TodaProofDependencyPresentationResult
  )
  proof_flow: (
    TodaReadableProofFlowPresentation
  )
  source: (
    TodaCalculationCandidateSourcePresentation
  )

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
      self.calculation_candidate,
      TodaCalculationPresentationCandidate,
    ):
      raise TypeError(
        "calculation_candidate must be "
        "a TodaCalculationPresentationCandidate"
      )

    if (
      self.calculation_candidate.source_candidate
      is not self.source_candidate
    ):
      raise ValueError(
        "calculation_candidate source identity "
        "must match source_candidate"
      )

    if not isinstance(
      self.group,
      TodaGroupResultPresentation,
    ):
      raise TypeError(
        "group must be a "
        "TodaGroupResultPresentation"
      )

    if (
      self.group.source_group_result
      is not self.source_candidate.group_result
    ):
      raise ValueError(
        "group source identity must match "
        "source_candidate.group_result"
      )

    explanation = (
      self.source_candidate.explanation
    )

    if explanation.ehp_result is None:
      if self.ehp is not None:
        raise ValueError(
          "ehp must be None when "
          "source explanation has no EHP result"
        )

      if self.exactness is not None:
        raise ValueError(
          "exactness must be None when "
          "source explanation has no "
          "exactness provenance"
        )
    else:
      if not isinstance(
        self.ehp,
        TodaEHPSequencePresentation,
      ):
        raise TypeError(
          "ehp must be a "
          "TodaEHPSequencePresentation"
        )

      if (
        self.ehp.source_result
        is not explanation.ehp_result
      ):
        raise ValueError(
          "ehp source identity must match "
          "source explanation"
        )

      if not isinstance(
        self.exactness,
        TodaEHPExactnessPresentation,
      ):
        raise TypeError(
          "exactness must be a "
          "TodaEHPExactnessPresentation"
        )

      if (
        self.exactness.source_provenance
        is not explanation.exactness_provenance
      ):
        raise ValueError(
          "exactness source identity must match "
          "source explanation"
        )

      if (
        self.exactness.sequence
        is not self.ehp
      ):
        raise ValueError(
          "exactness sequence must be "
          "the end-to-end EHP presentation"
        )

    if not isinstance(
      self.dependencies,
      TodaProofDependencyPresentationResult,
    ):
      raise TypeError(
        "dependencies must be a "
        "TodaProofDependencyPresentationResult"
      )

    if (
      self.dependencies.source_result
      is not explanation.dependency_result
    ):
      raise ValueError(
        "dependency source identity must match "
        "source explanation"
      )

    if not isinstance(
      self.proof_flow,
      TodaReadableProofFlowPresentation,
    ):
      raise TypeError(
        "proof_flow must be a "
        "TodaReadableProofFlowPresentation"
      )

    if (
      self.proof_flow.source_provenance
      is not explanation.recursive_provenance
    ):
      raise ValueError(
        "proof_flow source identity must match "
        "source explanation"
      )

    if (
      self.dependencies.root.source_step
      is not self.group
      .source_group_result
      .proof_step
    ):
      raise ValueError(
        "dependency root must match "
        "group proof step"
      )

    if (
      self.proof_flow.root.step.source_step
      is not self.group
      .source_group_result
      .proof_step
    ):
      raise ValueError(
        "proof flow root must match "
        "group proof step"
      )

    if not isinstance(
      self.source,
      TodaCalculationCandidateSourcePresentation,
    ):
      raise TypeError(
        "source must be a "
        "TodaCalculationCandidateSourcePresentation"
      )

    if (
      self.source.source_candidate
      is not self.source_candidate
    ):
      raise ValueError(
        "source presentation identity must "
        "match source_candidate"
      )


def _validate_repository_entries(
  repository_entries: tuple[
    ProofRepositoryEntry,
    ...,
  ],
) -> None:
  if not isinstance(
    repository_entries,
    tuple,
  ):
    raise TypeError(
      "repository_entries must be a tuple"
    )

  for entry in repository_entries:
    if not isinstance(
      entry,
      ProofRepositoryEntry,
    ):
      raise TypeError(
        "repository_entries must contain only "
        "ProofRepositoryEntry objects"
      )


def build_toda_end_to_end_candidate_presentation(
  candidate: TodaCalculationCandidate,
  repository_entries: tuple[
    ProofRepositoryEntry,
    ...,
  ] = (),
) -> TodaEndToEndCandidatePresentation:
  if not isinstance(
    candidate,
    TodaCalculationCandidate,
  ):
    raise TypeError(
      "candidate must be "
      "a TodaCalculationCandidate"
    )

  _validate_repository_entries(
    repository_entries
  )

  explanation = (
    candidate.explanation
  )

  exactness = None
  ehp = None

  if (
    explanation.exactness_provenance
    is not None
  ):
    exactness = (
      build_toda_ehp_exactness_presentation(
        explanation
        .exactness_provenance
      )
    )
    ehp = exactness.sequence

  return TodaEndToEndCandidatePresentation(
    source_candidate=candidate,
    calculation_candidate=(
      TodaCalculationPresentationCandidate(
        source_candidate=candidate,
      )
    ),
    group=(
      build_toda_group_result_presentation(
        candidate.group_result
      )
    ),
    ehp=ehp,
    exactness=exactness,
    dependencies=(
      build_toda_proof_dependency_presentation_result(
        explanation.dependency_result,
        repository_entries,
      )
    ),
    proof_flow=(
      build_toda_readable_proof_flow_presentation(
        explanation.recursive_provenance,
        repository_entries,
      )
    ),
    source=(
      build_toda_calculation_candidate_source_presentation(
        candidate
      )
    ),
  )

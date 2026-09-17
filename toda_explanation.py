from dataclasses import dataclass

from homotopy_groups import TodaPrimaryGroup
from toda_ehp_exactness_provenance import (
  TodaEHPExactnessUseProvenanceResult,
  extract_toda_ehp_exactness_use_provenance,
)
from toda_ehp_extraction import (
  extract_toda_ehp_sequence_result,
)
from toda_ehp_result import (
  TodaEHPSequenceResult,
)
from toda_group_result import TodaGroupResult
from toda_proof_dependency import (
  TodaProofDependency,
  TodaProofDependencyResult,
  TodaProofDependencyRole,
  extract_toda_proof_dependencies,
)


@dataclass(frozen=True)
class TodaRepresentativeExplanationResult:
  group_result: TodaGroupResult
  ehp_result: TodaEHPSequenceResult | None
  exactness_provenance: (
    TodaEHPExactnessUseProvenanceResult
    | None
  )
  dependency_result: TodaProofDependencyResult

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

    if (
      self.ehp_result is not None
      and not isinstance(
        self.ehp_result,
        TodaEHPSequenceResult,
      )
    ):
      raise TypeError(
        "ehp_result must be "
        "a TodaEHPSequenceResult "
        "or None"
      )

    if (
      self.exactness_provenance
      is not None
      and not isinstance(
        self.exactness_provenance,
        TodaEHPExactnessUseProvenanceResult,
      )
    ):
      raise TypeError(
        "exactness_provenance must be "
        "a TodaEHPExactnessUseProvenanceResult "
        "or None"
      )

    if not isinstance(
      self.dependency_result,
      TodaProofDependencyResult,
    ):
      raise TypeError(
        "dependency_result must be "
        "a TodaProofDependencyResult"
      )

    if (
      self.dependency_result.root_step
      is not self.group_result.proof_step
    ):
      raise ValueError(
        "dependency_result.root_step must be "
        "group_result.proof_step"
      )

    if self.ehp_result is None:
      if (
        self.exactness_provenance
        is not None
      ):
        raise ValueError(
          "exactness_provenance must be None "
          "when ehp_result is None"
        )
    else:
      if (
        self.ehp_result.target
        != self.group_result.target
      ):
        raise ValueError(
          "ehp_result and group_result "
          "must have the same target"
        )

      if (
        self.exactness_provenance
        is None
      ):
        raise ValueError(
          "exactness_provenance is required "
          "when ehp_result is present"
        )

      if (
        self.exactness_provenance.ehp_result
        is not self.ehp_result
      ):
        raise ValueError(
          "exactness_provenance.ehp_result "
          "must be ehp_result"
        )

  @property
  def target(
    self,
  ) -> TodaPrimaryGroup:
    return self.group_result.target

  def dependencies_for_role(
    self,
    role: TodaProofDependencyRole,
  ) -> tuple[
    TodaProofDependency,
    ...,
  ]:
    if not isinstance(
      role,
      TodaProofDependencyRole,
    ):
      raise TypeError(
        "role must be a "
        "TodaProofDependencyRole"
      )

    return tuple(
      dependency
      for dependency in (
        self.dependency_result
        .dependencies
      )
      if dependency.role == role
    )


def build_toda_representative_explanation(
  group_result: TodaGroupResult,
) -> TodaRepresentativeExplanationResult:
  if not isinstance(
    group_result,
    TodaGroupResult,
  ):
    raise TypeError(
      "group_result must be "
      "a TodaGroupResult"
    )

  ehp_result = (
    extract_toda_ehp_sequence_result(
      group_result
    )
  )

  exactness_provenance = None

  if ehp_result is not None:
    exactness_provenance = (
      extract_toda_ehp_exactness_use_provenance(
        group_result,
        ehp_result,
      )
    )

  dependency_result = (
    extract_toda_proof_dependencies(
      group_result
    )
  )

  return (
    TodaRepresentativeExplanationResult(
      group_result=group_result,
      ehp_result=ehp_result,
      exactness_provenance=(
        exactness_provenance
      ),
      dependency_result=(
        dependency_result
      ),
    )
  )

from enum import Enum

from homotopy_groups import (
  TodaPrimaryGroup,
)
from toda_group_proof_narrative_exactness_components import (
  TodaGroupProofNarrativeExactnessMethodComponent,
)
from toda_group_proof_narrative_exactness_relevance import (
  is_toda_group_proof_narrative_exactness_component_directly_relevant,
)


class TodaGroupProofNarrativeExactnessExposureClass(
  Enum
):
  OWNED_PRIMARY = "owned_primary"
  UNOWNED_RECURSIVE = "unowned_recursive"
  AMBIGUOUS_RELEVANT = "ambiguous_relevant"


def classify_toda_group_proof_narrative_exactness_component_exposure(
  relevant_groups: tuple[
    TodaPrimaryGroup,
    ...,
  ],
  components: tuple[
    TodaGroupProofNarrativeExactnessMethodComponent,
    ...,
  ],
  component: TodaGroupProofNarrativeExactnessMethodComponent,
) -> TodaGroupProofNarrativeExactnessExposureClass:
  if not isinstance(
    relevant_groups,
    tuple,
  ):
    raise TypeError(
      "relevant_groups must be a tuple"
    )

  for group in relevant_groups:
    if not isinstance(
      group,
      TodaPrimaryGroup,
    ):
      raise TypeError(
        "relevant_groups must contain only "
        "TodaPrimaryGroup objects"
      )

  if not isinstance(
    components,
    tuple,
  ):
    raise TypeError(
      "components must be a tuple"
    )

  for candidate in components:
    if not isinstance(
      candidate,
      TodaGroupProofNarrativeExactnessMethodComponent,
    ):
      raise TypeError(
        "components must contain only "
        "TodaGroupProofNarrativeExactnessMethodComponent "
        "objects"
      )

  if not isinstance(
    component,
    TodaGroupProofNarrativeExactnessMethodComponent,
  ):
    raise TypeError(
      "component must be a "
      "TodaGroupProofNarrativeExactnessMethodComponent"
    )

  if component not in components:
    raise ValueError(
      "component must appear in components"
    )

  directly_relevant = tuple(
    candidate
    for candidate in components
    if is_toda_group_proof_narrative_exactness_component_directly_relevant(
      relevant_groups,
      candidate,
    )
  )

  if len(
    directly_relevant
  ) == 1:
    if component == directly_relevant[
      0
    ]:
      return (
        TodaGroupProofNarrativeExactnessExposureClass
        .OWNED_PRIMARY
      )

    return (
      TodaGroupProofNarrativeExactnessExposureClass
      .UNOWNED_RECURSIVE
    )

  if not directly_relevant:
    return (
      TodaGroupProofNarrativeExactnessExposureClass
      .UNOWNED_RECURSIVE
    )

  if component in directly_relevant:
    return (
      TodaGroupProofNarrativeExactnessExposureClass
      .AMBIGUOUS_RELEVANT
    )

  return (
    TodaGroupProofNarrativeExactnessExposureClass
    .UNOWNED_RECURSIVE
  )

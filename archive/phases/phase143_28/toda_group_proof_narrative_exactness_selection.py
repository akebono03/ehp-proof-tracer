from homotopy_groups import (
  TodaPrimaryGroup,
)
from toda_group_proof_narrative_exactness_components import (
  TodaGroupProofNarrativeExactnessMethodComponent,
)
from toda_group_proof_narrative_exactness_relevance import (
  is_toda_group_proof_narrative_exactness_component_directly_relevant,
)


def select_toda_group_proof_narrative_primary_exactness_component(
  relevant_groups: tuple[
    TodaPrimaryGroup,
    ...,
  ],
  components: tuple[
    TodaGroupProofNarrativeExactnessMethodComponent,
    ...,
  ],
) -> (
  TodaGroupProofNarrativeExactnessMethodComponent
  | None
):
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

  for component in components:
    if not isinstance(
      component,
      TodaGroupProofNarrativeExactnessMethodComponent,
    ):
      raise TypeError(
        "components must contain only "
        "TodaGroupProofNarrativeExactnessMethodComponent "
        "objects"
      )

  directly_relevant = tuple(
    component
    for component in components
    if is_toda_group_proof_narrative_exactness_component_directly_relevant(
      relevant_groups,
      component,
    )
  )

  if len(
    directly_relevant
  ) != 1:
    return None

  return directly_relevant[
    0
  ]

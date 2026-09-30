from homotopy_groups import (
  TodaPrimaryGroup,
)
from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgument,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeBlock,
)
from toda_group_proof_narrative_exactness_components import (
  TodaGroupProofNarrativeExactnessMethodComponent,
  build_toda_group_proof_narrative_exactness_method_components,
)
from toda_group_proof_narrative_exactness_relevance import (
  is_toda_group_proof_narrative_exactness_component_directly_relevant,
)
from toda_group_proof_narrative_method_evidence import (
  extract_toda_group_proof_narrative_argument_method_evidence,
)
from toda_group_proof_narrative_relevant_groups import (
  extract_toda_group_proof_narrative_argument_relevant_groups,
)
from toda_group_proof_narrative_semantics import (
  TodaGroupProofNarrativeSemanticSidecar,
)
from toda_group_proof_presentation import (
  TodaGroupProofPresentation,
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


def select_toda_group_proof_narrative_argument_primary_exactness_component(
  presentation: TodaGroupProofPresentation,
  blocks: tuple[
    TodaGroupProofNarrativeBlock,
    ...,
  ],
  semantic_sidecar: TodaGroupProofNarrativeSemanticSidecar,
  arguments: tuple[
    TodaGroupProofNarrativeArgument,
    ...,
  ],
  argument_index: int,
) -> (
  TodaGroupProofNarrativeExactnessMethodComponent
  | None
):
  evidence = (
    extract_toda_group_proof_narrative_argument_method_evidence(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
      argument_index,
    )
  )
  argument = arguments[
    argument_index
  ]
  relevant_groups = (
    extract_toda_group_proof_narrative_argument_relevant_groups(
      presentation,
      blocks,
      argument,
    )
  )
  components = (
    build_toda_group_proof_narrative_exactness_method_components(
      evidence
    )
  )

  return (
    select_toda_group_proof_narrative_primary_exactness_component(
      relevant_groups,
      components,
    )
  )

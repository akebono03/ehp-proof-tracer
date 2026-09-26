from homotopy_groups import (
  TodaPrimaryGroup,
)
from toda_group_proof_narrative_exactness_components import (
  TodaGroupProofNarrativeExactnessMethodComponent,
)


def extract_toda_group_proof_narrative_exactness_component_terms(
  component: TodaGroupProofNarrativeExactnessMethodComponent,
) -> tuple[
  TodaPrimaryGroup,
  ...,
]:
  if not isinstance(
    component,
    TodaGroupProofNarrativeExactnessMethodComponent,
  ):
    raise TypeError(
      "component must be a "
      "TodaGroupProofNarrativeExactnessMethodComponent"
    )

  terms = []

  for window in component.windows:
    for term in (
      window.source_term,
      window.middle_term,
      window.target_term,
    ):
      if not isinstance(
        term,
        TodaPrimaryGroup,
      ):
        continue

      if term not in terms:
        terms.append(
          term
        )

  return tuple(
    terms
  )


def is_toda_group_proof_narrative_exactness_component_directly_relevant(
  relevant_groups: tuple[
    TodaPrimaryGroup,
    ...,
  ],
  component: TodaGroupProofNarrativeExactnessMethodComponent,
) -> bool:
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

  component_terms = (
    extract_toda_group_proof_narrative_exactness_component_terms(
      component
    )
  )

  return any(
    group in component_terms
    for group in relevant_groups
  )

from toda_group_proof_narrative_exactness_components import (
  TodaGroupProofNarrativeExactnessMethodComponent,
)


def render_toda_group_proof_narrative_exactness_method_transition(
  primary_component: (
    TodaGroupProofNarrativeExactnessMethodComponent
    | None
  ),
) -> str | None:
  if primary_component is None:
    return None

  if not isinstance(
    primary_component,
    TodaGroupProofNarrativeExactnessMethodComponent,
  ):
    raise TypeError(
      "primary_component must be a "
      "TodaGroupProofNarrativeExactnessMethodComponent "
      "or None"
    )

  return "そのために、次の完全列を考える."

from toda_group_proof_narrative_transitions import (
  TodaGroupProofNarrativeTransition,
  TodaGroupProofNarrativeTransitionRole,
)


def render_toda_group_proof_narrative_transition_connector(
  transition: TodaGroupProofNarrativeTransition,
) -> str | None:
  if not isinstance(
    transition,
    TodaGroupProofNarrativeTransition,
  ):
    raise TypeError(
      "transition must be a "
      "TodaGroupProofNarrativeTransition"
    )

  if (
    transition.role
    is TodaGroupProofNarrativeTransitionRole
    .DERIVATION
  ):
    return "以上より、"

  if (
    transition.role
    in (
      TodaGroupProofNarrativeTransitionRole
      .SUPPORT,
      TodaGroupProofNarrativeTransitionRole
      .CALCULATION_CHAIN,
    )
  ):
    return None

  raise ValueError(
    "unsupported NarrativeTransition role"
  )

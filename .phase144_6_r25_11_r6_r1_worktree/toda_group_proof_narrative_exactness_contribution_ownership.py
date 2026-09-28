from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeBlock,
  TodaGroupProofNarrativeMathematicalBlockRole,
)
from toda_group_proof_narrative_exactness_components import (
  TodaGroupProofNarrativeExactnessMethodComponent,
)
from toda_group_proof_narrative_exactness_display_contributions import (
  TodaGroupProofNarrativeExactnessDisplayContribution,
  TodaGroupProofNarrativeExactnessDisplayContributionKind,
)


def filter_toda_group_proof_narrative_exactness_body_contributions(
  block: TodaGroupProofNarrativeBlock,
  contributions: tuple[
    TodaGroupProofNarrativeExactnessDisplayContribution,
    ...,
  ],
  primary_component: (
    TodaGroupProofNarrativeExactnessMethodComponent
    | None
  ),
) -> tuple[
  TodaGroupProofNarrativeExactnessDisplayContribution,
  ...,
]:
  if not isinstance(
    block,
    TodaGroupProofNarrativeBlock,
  ):
    raise TypeError(
      "block must be a "
      "TodaGroupProofNarrativeBlock"
    )

  if (
    block.role
    is not TodaGroupProofNarrativeMathematicalBlockRole
    .EXACTNESS
  ):
    raise ValueError(
      "block must be an EXACTNESS block"
    )

  if not isinstance(
    contributions,
    tuple,
  ):
    raise TypeError(
      "contributions must be a tuple"
    )

  block_step_ids = {
    id(
      proof_step
    )
    for proof_step in block.steps
  }

  for contribution in contributions:
    if not isinstance(
      contribution,
      TodaGroupProofNarrativeExactnessDisplayContribution,
    ):
      raise TypeError(
        "contributions must contain only "
        "TodaGroupProofNarrativeExactnessDisplayContribution "
        "objects"
      )

    if id(
      contribution.proof_step
    ) not in block_step_ids:
      raise ValueError(
        "contribution proof_step must appear "
        "in block steps"
      )

  if (
    primary_component is not None
    and not isinstance(
      primary_component,
      TodaGroupProofNarrativeExactnessMethodComponent,
    )
  ):
    raise TypeError(
      "primary_component must be a "
      "TodaGroupProofNarrativeExactnessMethodComponent "
      "or None"
    )

  if primary_component is None:
    return contributions

  is_primary_evidence_block = any(
    evidence_block is block
    for evidence_block in primary_component.evidence_blocks
  )

  if not is_primary_evidence_block:
    return contributions

  return tuple(
    contribution
    for contribution in contributions
    if (
      contribution.kind
      is not TodaGroupProofNarrativeExactnessDisplayContributionKind
      .EXACTNESS_WINDOW
    )
  )

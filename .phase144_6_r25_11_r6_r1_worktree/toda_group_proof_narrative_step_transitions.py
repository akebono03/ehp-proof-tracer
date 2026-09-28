from dataclasses import dataclass
from enum import Enum

from proof import (
  ProofStep,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeBlock,
  TodaGroupProofNarrativeMathematicalBlockRole,
)
from toda_group_proof_presentation import (
  TodaGroupProofPresentation,
)


class TodaGroupProofNarrativeStepTransitionRole(
  Enum
):
  CALCULATION_CHAIN = "calculation_chain"


@dataclass(frozen=True)
class TodaGroupProofNarrativeStepTransition:
  role: TodaGroupProofNarrativeStepTransitionRole
  source_step: ProofStep
  target_step: ProofStep

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.role,
      TodaGroupProofNarrativeStepTransitionRole,
    ):
      raise TypeError(
        "role must be a "
        "TodaGroupProofNarrativeStepTransitionRole"
      )

    if not isinstance(
      self.source_step,
      ProofStep,
    ):
      raise TypeError(
        "source_step must be a ProofStep"
      )

    if not isinstance(
      self.target_step,
      ProofStep,
    ):
      raise TypeError(
        "target_step must be a ProofStep"
      )

    if self.source_step is self.target_step:
      raise ValueError(
        "source_step and target_step "
        "must be different ProofStep objects"
      )


def _validate_step_transition_inputs(
  presentation: TodaGroupProofPresentation,
  blocks: tuple[
    TodaGroupProofNarrativeBlock,
    ...,
  ],
) -> None:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a "
      "TodaGroupProofPresentation"
    )

  if not isinstance(
    blocks,
    tuple,
  ):
    raise TypeError(
      "blocks must be a tuple"
    )

  presentation_step_ids = {
    id(
      node.proof_step
    )
    for node in presentation.nodes
  }
  block_step_ids = set()

  for block in blocks:
    if not isinstance(
      block,
      TodaGroupProofNarrativeBlock,
    ):
      raise TypeError(
        "blocks must contain only "
        "TodaGroupProofNarrativeBlock objects"
      )

    for proof_step in block.steps:
      proof_step_id = id(
        proof_step
      )

      if proof_step_id not in presentation_step_ids:
        raise ValueError(
          "block proof steps must appear "
          "in presentation nodes"
        )

      if proof_step_id in block_step_ids:
        raise ValueError(
          "blocks must not contain duplicate "
          "ProofStep objects"
        )

      block_step_ids.add(
        proof_step_id
      )

  if block_step_ids != presentation_step_ids:
    raise ValueError(
      "blocks must cover presentation nodes "
      "exactly once"
    )


def extract_toda_group_proof_narrative_step_transitions(
  presentation: TodaGroupProofPresentation,
  blocks: tuple[
    TodaGroupProofNarrativeBlock,
    ...,
  ],
) -> tuple[
  TodaGroupProofNarrativeStepTransition,
  ...,
]:
  _validate_step_transition_inputs(
    presentation,
    blocks,
  )

  block_by_step_id = {
    id(
      proof_step
    ): block
    for block in blocks
    for proof_step in block.steps
  }
  transitions = []
  seen_keys = set()

  for edge in presentation.edges:
    source_step = edge.premise_step
    target_step = edge.parent_step
    source_block = block_by_step_id[
      id(
        source_step
      )
    ]
    target_block = block_by_step_id[
      id(
        target_step
      )
    ]

    if source_block is not target_block:
      continue

    if (
      source_block.role
      is not TodaGroupProofNarrativeMathematicalBlockRole
      .CALCULATION
    ):
      continue

    key = (
      id(
        source_step
      ),
      id(
        target_step
      ),
    )

    if key in seen_keys:
      continue

    seen_keys.add(
      key
    )
    transitions.append(
      TodaGroupProofNarrativeStepTransition(
        role=(
          TodaGroupProofNarrativeStepTransitionRole
          .CALCULATION_CHAIN
        ),
        source_step=source_step,
        target_step=target_step,
      )
    )

  return tuple(
    transitions
  )

from dataclasses import dataclass
from enum import Enum

from toda_group_proof_aggregate_statement_catalog import (
  is_toda_group_proof_aggregate_statement,
)
from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgument,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeBlock,
  TodaGroupProofNarrativeMathematicalBlockRole,
)
from toda_group_proof_presentation import (
  TodaGroupProofPresentation,
)


class TodaGroupProofNarrativeTransitionRole(
  Enum
):
  CALCULATION_CHAIN = "calculation_chain"
  SUPPORT = "support"
  DERIVATION = "derivation"


@dataclass(frozen=True)
class TodaGroupProofNarrativeTransition:
  role: TodaGroupProofNarrativeTransitionRole
  source_blocks: tuple[
    TodaGroupProofNarrativeBlock,
    ...,
  ]
  target_block: TodaGroupProofNarrativeBlock

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.role,
      TodaGroupProofNarrativeTransitionRole,
    ):
      raise TypeError(
        "role must be a "
        "TodaGroupProofNarrativeTransitionRole"
      )

    if not isinstance(
      self.source_blocks,
      tuple,
    ):
      raise TypeError(
        "source_blocks must be a tuple"
      )

    if not self.source_blocks:
      raise ValueError(
        "source_blocks must not be empty"
      )

    for block in self.source_blocks:
      if not isinstance(
        block,
        TodaGroupProofNarrativeBlock,
      ):
        raise TypeError(
          "source_blocks must contain only "
          "TodaGroupProofNarrativeBlock objects"
        )

    if len(
      {
        id(
          block
        )
        for block in self.source_blocks
      }
    ) != len(
      self.source_blocks
    ):
      raise ValueError(
        "source_blocks must not contain duplicates"
      )

    if not isinstance(
      self.target_block,
      TodaGroupProofNarrativeBlock,
    ):
      raise TypeError(
        "target_block must be a "
        "TodaGroupProofNarrativeBlock"
      )

    if any(
      block is self.target_block
      for block in self.source_blocks
    ):
      raise ValueError(
        "target_block must not appear in source_blocks"
      )


_DERIVATION_SOURCE_ROLES = frozenset(
  (
    TodaGroupProofNarrativeMathematicalBlockRole.CALCULATION,
    TodaGroupProofNarrativeMathematicalBlockRole.ORDER,
    TodaGroupProofNarrativeMathematicalBlockRole.EXACTNESS,
    TodaGroupProofNarrativeMathematicalBlockRole.MAP_PROPERTY,
    TodaGroupProofNarrativeMathematicalBlockRole.GROUP_STRUCTURE,
    TodaGroupProofNarrativeMathematicalBlockRole.MEMBERSHIP,
  )
)


def _validate_transition_inputs(
  presentation: TodaGroupProofPresentation,
  blocks: tuple[
    TodaGroupProofNarrativeBlock,
    ...,
  ],
  arguments: tuple[
    TodaGroupProofNarrativeArgument,
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

  if not isinstance(
    arguments,
    tuple,
  ):
    raise TypeError(
      "arguments must be a tuple"
    )

  block_ids = {
    id(
      block
    )
    for block in blocks
  }

  for block in blocks:
    if not isinstance(
      block,
      TodaGroupProofNarrativeBlock,
    ):
      raise TypeError(
        "blocks must contain only "
        "TodaGroupProofNarrativeBlock objects"
      )

  for argument in arguments:
    if not isinstance(
      argument,
      TodaGroupProofNarrativeArgument,
    ):
      raise TypeError(
        "arguments must contain only "
        "TodaGroupProofNarrativeArgument objects"
      )

    argument_blocks = (
      *argument.supporting_blocks,
      argument.conclusion_block,
    )

    if any(
      id(
        block
      ) not in block_ids
      for block in argument_blocks
    ):
      raise ValueError(
        "argument blocks must appear in blocks"
      )


def _block_index_by_step_id(
  blocks: tuple[
    TodaGroupProofNarrativeBlock,
    ...,
  ],
) -> dict[int, int]:
  return {
    id(
      proof_step
    ): block_index
    for block_index, block in enumerate(
      blocks
    )
    for proof_step in block.steps
  }


def _calculation_chain_transitions(
  presentation: TodaGroupProofPresentation,
  blocks: tuple[
    TodaGroupProofNarrativeBlock,
    ...,
  ],
) -> tuple[
  TodaGroupProofNarrativeTransition,
  ...,
]:
  block_index_by_step_id = (
    _block_index_by_step_id(
      blocks
    )
  )
  transitions = []
  seen_keys = set()

  for edge in presentation.edges:
    parent_index = block_index_by_step_id[
      id(
        edge.parent_step
      )
    ]
    premise_index = block_index_by_step_id[
      id(
        edge.premise_step
      )
    ]

    if parent_index == premise_index:
      continue

    parent_block = blocks[
      parent_index
    ]
    premise_block = blocks[
      premise_index
    ]

    if (
      parent_block.role
      is not TodaGroupProofNarrativeMathematicalBlockRole
      .CALCULATION
      or premise_block.role
      is not TodaGroupProofNarrativeMathematicalBlockRole
      .CALCULATION
    ):
      continue

    key = (
      id(
        premise_block
      ),
      id(
        parent_block
      ),
    )

    if key in seen_keys:
      continue

    seen_keys.add(
      key
    )
    transitions.append(
      TodaGroupProofNarrativeTransition(
        role=(
          TodaGroupProofNarrativeTransitionRole
          .CALCULATION_CHAIN
        ),
        source_blocks=(
          premise_block,
        ),
        target_block=parent_block,
      )
    )

  return tuple(
    transitions
  )


def _block_contains_aggregate_statement(
  block: TodaGroupProofNarrativeBlock,
) -> bool:
  return any(
    is_toda_group_proof_aggregate_statement(
      proof_step.conclusion
    )
    for proof_step in block.steps
  )


def _argument_transition_role(
  source_blocks: tuple[
    TodaGroupProofNarrativeBlock,
    ...,
  ],
) -> TodaGroupProofNarrativeTransitionRole:
  if any(
    (
      block.role in _DERIVATION_SOURCE_ROLES
      or _block_contains_aggregate_statement(
        block
      )
    )
    for block in source_blocks
  ):
    return (
      TodaGroupProofNarrativeTransitionRole
      .DERIVATION
    )

  return (
    TodaGroupProofNarrativeTransitionRole
    .SUPPORT
  )


def _argument_transitions(
  arguments: tuple[
    TodaGroupProofNarrativeArgument,
    ...,
  ],
) -> tuple[
  TodaGroupProofNarrativeTransition,
  ...,
]:
  transitions = []

  for argument in arguments:
    if not argument.supporting_blocks:
      continue

    transitions.append(
      TodaGroupProofNarrativeTransition(
        role=_argument_transition_role(
          argument.supporting_blocks
        ),
        source_blocks=argument.supporting_blocks,
        target_block=argument.conclusion_block,
      )
    )

  return tuple(
    transitions
  )


def extract_toda_group_proof_narrative_transitions(
  presentation: TodaGroupProofPresentation,
  blocks: tuple[
    TodaGroupProofNarrativeBlock,
    ...,
  ],
  arguments: tuple[
    TodaGroupProofNarrativeArgument,
    ...,
  ],
) -> tuple[
  TodaGroupProofNarrativeTransition,
  ...,
]:
  _validate_transition_inputs(
    presentation,
    blocks,
    arguments,
  )

  transitions = []
  seen_keys = set()

  for transition in (
    *_calculation_chain_transitions(
      presentation,
      blocks,
    ),
    *_argument_transitions(
      arguments
    ),
  ):
    key = (
      transition.role,
      tuple(
        id(
          block
        )
        for block in transition.source_blocks
      ),
      id(
        transition.target_block
      ),
    )

    if key in seen_keys:
      continue

    seen_keys.add(
      key
    )
    transitions.append(
      transition
    )

  return tuple(
    transitions
  )

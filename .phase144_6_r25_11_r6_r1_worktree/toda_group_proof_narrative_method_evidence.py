from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgument,
  _argument_direct_dependency_indices,
  _validate_argument_inputs,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeBlock,
  TodaGroupProofNarrativeMathematicalBlockRole,
)
from toda_group_proof_narrative_semantics import (
  TodaGroupProofNarrativeSemanticSidecar,
)
from toda_group_proof_presentation import (
  TodaGroupProofPresentation,
)


def extract_toda_group_proof_narrative_argument_method_evidence(
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
) -> tuple[
  TodaGroupProofNarrativeBlock,
  ...,
]:
  _validate_argument_inputs(
    presentation,
    blocks,
    semantic_sidecar,
  )

  if not isinstance(
    arguments,
    tuple,
  ):
    raise TypeError(
      "arguments must be a tuple"
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

  if (
    not isinstance(
      argument_index,
      int,
    )
    or isinstance(
      argument_index,
      bool,
    )
  ):
    raise TypeError(
      "argument_index must be an integer"
    )

  if not (
    0
    <= argument_index
    < len(
      arguments
    )
  ):
    raise ValueError(
      "argument_index is out of range"
    )

  block_index_by_identity = {
    id(
      block
    ): index
    for index, block in enumerate(
      blocks
    )
  }

  argument_conclusion_indices = []

  for argument in arguments:
    conclusion_index = block_index_by_identity.get(
      id(
        argument.conclusion_block
      )
    )

    if conclusion_index is None:
      raise ValueError(
        "argument conclusion_block must appear "
        "in blocks"
      )

    argument_conclusion_indices.append(
      conclusion_index
    )

  if len(
    set(
      argument_conclusion_indices
    )
  ) != len(
    argument_conclusion_indices
  ):
    raise ValueError(
      "arguments must have distinct "
      "conclusion blocks"
    )

  direct_dependencies = (
    _argument_direct_dependency_indices(
      presentation,
      blocks,
      semantic_sidecar,
    )
  )

  conclusion_index = argument_conclusion_indices[
    argument_index
  ]
  boundary_indices = set(
    argument_conclusion_indices
  )
  boundary_indices.discard(
    conclusion_index
  )

  visited = set()
  active = set()

  def visit(
    block_index: int,
  ) -> None:
    if block_index in boundary_indices:
      return

    if block_index in visited:
      return

    if block_index in active:
      return

    active.add(
      block_index
    )

    for dependency_index in direct_dependencies[
      block_index
    ]:
      visit(
        dependency_index
      )

    active.remove(
      block_index
    )
    visited.add(
      block_index
    )

  for dependency_index in direct_dependencies[
    conclusion_index
  ]:
    visit(
      dependency_index
    )

  return tuple(
    block
    for block_index, block in enumerate(
      blocks
    )
    if (
      block_index in visited
      and block.role
      is TodaGroupProofNarrativeMathematicalBlockRole
      .EXACTNESS
    )
  )

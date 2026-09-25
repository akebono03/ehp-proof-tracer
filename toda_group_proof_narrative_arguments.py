from dataclasses import dataclass
from enum import Enum

from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeBlock,
  TodaGroupProofNarrativeMathematicalBlockRole,
)
from toda_group_proof_narrative_semantics import (
  TodaGroupProofNarrativeSemanticSidecar,
  build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_presentation import (
  TodaGroupProofPresentation,
)


class TodaGroupProofNarrativeArgumentRole(
  Enum
):
  ESTABLISH_DEFINITION = "establish_definition"
  ESTABLISH_ORDER = "establish_order"
  ESTABLISH_GROUP_STRUCTURE = (
    "establish_group_structure"
  )


@dataclass(frozen=True)
class TodaGroupProofNarrativeArgument:
  role: TodaGroupProofNarrativeArgumentRole
  supporting_blocks: tuple[
    TodaGroupProofNarrativeBlock,
    ...,
  ]
  conclusion_block: TodaGroupProofNarrativeBlock

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.role,
      TodaGroupProofNarrativeArgumentRole,
    ):
      raise TypeError(
        "role must be a "
        "TodaGroupProofNarrativeArgumentRole"
      )

    if not isinstance(
      self.supporting_blocks,
      tuple,
    ):
      raise TypeError(
        "supporting_blocks must be a tuple"
      )

    for block in self.supporting_blocks:
      if not isinstance(
        block,
        TodaGroupProofNarrativeBlock,
      ):
        raise TypeError(
          "supporting_blocks must contain only "
          "TodaGroupProofNarrativeBlock objects"
        )

    if not isinstance(
      self.conclusion_block,
      TodaGroupProofNarrativeBlock,
    ):
      raise TypeError(
        "conclusion_block must be a "
        "TodaGroupProofNarrativeBlock"
      )

    if any(
      block is self.conclusion_block
      for block in self.supporting_blocks
    ):
      raise ValueError(
        "supporting_blocks must not contain "
        "conclusion_block"
      )

    if len(
      {
        id(
          block
        )
        for block in self.supporting_blocks
      }
    ) != len(
      self.supporting_blocks
    ):
      raise ValueError(
        "supporting_blocks must not contain "
        "duplicate blocks"
      )


_ARGUMENT_ROLE_BY_CONCLUSION_BLOCK_ROLE = {
  TodaGroupProofNarrativeMathematicalBlockRole.DEFINITION:
    TodaGroupProofNarrativeArgumentRole.ESTABLISH_DEFINITION,
  TodaGroupProofNarrativeMathematicalBlockRole.ORDER:
    TodaGroupProofNarrativeArgumentRole.ESTABLISH_ORDER,
  TodaGroupProofNarrativeMathematicalBlockRole.TARGET:
    TodaGroupProofNarrativeArgumentRole.ESTABLISH_GROUP_STRUCTURE,
}


def _validate_argument_inputs(
  presentation: TodaGroupProofPresentation,
  blocks: tuple[
    TodaGroupProofNarrativeBlock,
    ...,
  ],
  semantic_sidecar: TodaGroupProofNarrativeSemanticSidecar,
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
    semantic_sidecar,
    TodaGroupProofNarrativeSemanticSidecar,
  ):
    raise TypeError(
      "semantic_sidecar must be a "
      "TodaGroupProofNarrativeSemanticSidecar"
    )

  if semantic_sidecar.presentation is not presentation:
    raise ValueError(
      "semantic_sidecar must belong to presentation"
    )

  selected_step_ids = {
    id(
      node.proof_step
    )
    for node in presentation.nodes
  }
  seen_step_ids = set()

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
      step_id = id(
        proof_step
      )

      if step_id not in selected_step_ids:
        raise ValueError(
          "block proof steps must appear "
          "in presentation nodes"
        )

      if step_id in seen_step_ids:
        raise ValueError(
          "blocks must not contain duplicate "
          "ProofStep objects"
        )

      seen_step_ids.add(
        step_id
      )

  if seen_step_ids != selected_step_ids:
    raise ValueError(
      "blocks must cover presentation nodes "
      "exactly once"
    )


def _argument_direct_dependency_indices(
  presentation: TodaGroupProofPresentation,
  blocks: tuple[
    TodaGroupProofNarrativeBlock,
    ...,
  ],
  semantic_sidecar: TodaGroupProofNarrativeSemanticSidecar,
) -> tuple[
  tuple[int, ...],
  ...,
]:
  block_index_by_step_id = {
    id(
      proof_step
    ): block_index
    for block_index, block in enumerate(
      blocks
    )
    for proof_step in block.steps
  }

  dependencies = [
    []
    for _ in blocks
  ]

  def add_dependency(
    dependent_step,
    prerequisite_step,
  ) -> None:
    dependent_index = block_index_by_step_id[
      id(
        dependent_step
      )
    ]
    prerequisite_index = block_index_by_step_id[
      id(
        prerequisite_step
      )
    ]

    if dependent_index == prerequisite_index:
      return

    if prerequisite_index in dependencies[
      dependent_index
    ]:
      return

    dependencies[
      dependent_index
    ].append(
      prerequisite_index
    )

  for edge in presentation.edges:
    add_dependency(
      edge.parent_step,
      edge.premise_step,
    )

  for semantic in semantic_sidecar.dependency_semantics:
    add_dependency(
      semantic.dependent_step,
      semantic.prerequisite_step,
    )

  return tuple(
    tuple(
      dependency_indices
    )
    for dependency_indices in dependencies
  )


def _argument_dependency_closure_indices(
  direct_dependencies: tuple[
    tuple[int, ...],
    ...,
  ],
  conclusion_index: int,
) -> tuple[
  int,
  ...,
]:
  visited = set()
  active = set()

  def visit(
    block_index: int,
  ) -> None:
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

  visited.discard(
    conclusion_index
  )

  return tuple(
    block_index
    for block_index in range(
      len(
        direct_dependencies
      )
    )
    if block_index in visited
  )


def build_toda_group_proof_narrative_arguments(
  presentation: TodaGroupProofPresentation,
  blocks: tuple[
    TodaGroupProofNarrativeBlock,
    ...,
  ],
  semantic_sidecar: (
    TodaGroupProofNarrativeSemanticSidecar
    | None
  ) = None,
) -> tuple[
  TodaGroupProofNarrativeArgument,
  ...,
]:
  if semantic_sidecar is None:
    semantic_sidecar = (
      build_toda_group_proof_narrative_semantic_sidecar(
        presentation
      )
    )

  _validate_argument_inputs(
    presentation,
    blocks,
    semantic_sidecar,
  )

  direct_dependencies = (
    _argument_direct_dependency_indices(
      presentation,
      blocks,
      semantic_sidecar,
    )
  )

  arguments = []

  for conclusion_index, conclusion_block in enumerate(
    blocks
  ):
    argument_role = (
      _ARGUMENT_ROLE_BY_CONCLUSION_BLOCK_ROLE.get(
        conclusion_block.role
      )
    )

    if argument_role is None:
      continue

    supporting_indices = (
      _argument_dependency_closure_indices(
        direct_dependencies,
        conclusion_index,
      )
    )

    arguments.append(
      TodaGroupProofNarrativeArgument(
        role=argument_role,
        supporting_blocks=tuple(
          blocks[
            supporting_index
          ]
          for supporting_index in supporting_indices
        ),
        conclusion_block=conclusion_block,
      )
    )

  return tuple(
    arguments
  )

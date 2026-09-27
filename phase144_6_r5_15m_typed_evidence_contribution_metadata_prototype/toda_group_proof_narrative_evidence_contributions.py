from dataclasses import dataclass
from enum import Enum

from proof import (
  Relation,
  RelationType,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeBlock,
  TodaGroupProofNarrativeMathematicalBlockRole,
)
from toda_group_proof_presentation import (
  TodaGroupProofPresentation,
)
from toda_proof_dependency import (
  TodaProofEdge,
)


class TodaGroupProofNarrativeEvidenceContribution(
  Enum
):
  ESTABLISH_GROUP = "establish_group"
  ESTABLISH_MAP = "establish_map"
  ESTABLISH_ZERO = "establish_zero"
  ESTABLISH_ORDER = "establish_order"
  ESTABLISH_RELATION = "establish_relation"
  PROVIDE_REFERENCE = "provide_reference"
  PROVIDE_PRECONDITION = "provide_precondition"
  UNRESOLVED = "unresolved"


@dataclass(frozen=True)
class TodaGroupProofNarrativeEvidenceContributionSemantic:
  edge: TodaProofEdge
  contribution: (
    TodaGroupProofNarrativeEvidenceContribution
  )

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.edge,
      TodaProofEdge,
    ):
      raise TypeError(
        "edge must be a TodaProofEdge"
      )

    if not isinstance(
      self.contribution,
      TodaGroupProofNarrativeEvidenceContribution,
    ):
      raise TypeError(
        "contribution must be a "
        "TodaGroupProofNarrativeEvidenceContribution"
      )


@dataclass(frozen=True)
class TodaGroupProofNarrativeEvidenceContributionSidecar:
  presentation: TodaGroupProofPresentation
  edge_semantics: tuple[
    TodaGroupProofNarrativeEvidenceContributionSemantic,
    ...,
  ]

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.presentation,
      TodaGroupProofPresentation,
    ):
      raise TypeError(
        "presentation must be a "
        "TodaGroupProofPresentation"
      )

    if not isinstance(
      self.edge_semantics,
      tuple,
    ):
      raise TypeError(
        "edge_semantics must be a tuple"
      )

    allowed_edge_keys = {
      (
        id(
          edge.parent_step
        ),
        id(
          edge.premise_step
        ),
        edge.premise_index,
      )
      for edge in self.presentation.edges
    }

    seen_edge_keys = set()

    for semantic in self.edge_semantics:
      if not isinstance(
        semantic,
        TodaGroupProofNarrativeEvidenceContributionSemantic,
      ):
        raise TypeError(
          "edge_semantics must contain only "
          "TodaGroupProofNarrativeEvidenceContributionSemantic "
          "objects"
        )

      edge_key = (
        id(
          semantic.edge.parent_step
        ),
        id(
          semantic.edge.premise_step
        ),
        semantic.edge.premise_index,
      )

      if edge_key not in allowed_edge_keys:
        raise ValueError(
          "evidence contribution edge must appear "
          "in presentation edges"
        )

      if edge_key in seen_edge_keys:
        raise ValueError(
          "edge_semantics must not contain "
          "duplicate edges"
        )

      seen_edge_keys.add(
        edge_key
      )


def _block_by_step_id(
  blocks: tuple[
    TodaGroupProofNarrativeBlock,
    ...,
  ],
) -> dict[
  int,
  TodaGroupProofNarrativeBlock,
]:
  return {
    id(
      proof_step
    ): block
    for block in blocks
    for proof_step in block.steps
  }


def _contribution_for_premise_block(
  block: TodaGroupProofNarrativeBlock,
  edge: TodaProofEdge,
) -> TodaGroupProofNarrativeEvidenceContribution:
  role = block.role

  if (
    role
    is TodaGroupProofNarrativeMathematicalBlockRole
    .REFERENCE
  ):
    return (
      TodaGroupProofNarrativeEvidenceContribution
      .PROVIDE_REFERENCE
    )

  if (
    role
    is TodaGroupProofNarrativeMathematicalBlockRole
    .PRECONDITION
  ):
    return (
      TodaGroupProofNarrativeEvidenceContribution
      .PROVIDE_PRECONDITION
    )

  if (
    role
    is TodaGroupProofNarrativeMathematicalBlockRole
    .GROUP_STRUCTURE
  ):
    return (
      TodaGroupProofNarrativeEvidenceContribution
      .ESTABLISH_GROUP
    )

  if (
    role
    is TodaGroupProofNarrativeMathematicalBlockRole
    .MAP_PROPERTY
  ):
    return (
      TodaGroupProofNarrativeEvidenceContribution
      .ESTABLISH_MAP
    )

  if (
    role
    is TodaGroupProofNarrativeMathematicalBlockRole
    .ORDER
  ):
    return (
      TodaGroupProofNarrativeEvidenceContribution
      .ESTABLISH_ORDER
    )

  statement = (
    edge.premise_step.conclusion
  )

  if isinstance(
    statement,
    Relation,
  ):
    if (
      statement.relation_type
      is RelationType.ZERO
    ):
      return (
        TodaGroupProofNarrativeEvidenceContribution
        .ESTABLISH_ZERO
      )

    if (
      statement.relation_type
      is RelationType.ORDER
    ):
      return (
        TodaGroupProofNarrativeEvidenceContribution
        .ESTABLISH_ORDER
      )

    if (
      statement.relation_type
      is RelationType.EQUALITY
    ):
      return (
        TodaGroupProofNarrativeEvidenceContribution
        .ESTABLISH_RELATION
      )

  return (
    TodaGroupProofNarrativeEvidenceContribution
    .UNRESOLVED
  )


def build_toda_group_proof_narrative_evidence_contribution_sidecar(
  presentation: TodaGroupProofPresentation,
  blocks: tuple[
    TodaGroupProofNarrativeBlock,
    ...,
  ],
) -> TodaGroupProofNarrativeEvidenceContributionSidecar:
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

  block_by_step_id = (
    _block_by_step_id(
      blocks
    )
  )

  presentation_step_ids = {
    id(
      node.proof_step
    )
    for node in presentation.nodes
  }

  if (
    set(
      block_by_step_id
    )
    != presentation_step_ids
  ):
    raise ValueError(
      "blocks must cover presentation nodes "
      "exactly once"
    )

  edge_semantics = tuple(
    TodaGroupProofNarrativeEvidenceContributionSemantic(
      edge=edge,
      contribution=(
        _contribution_for_premise_block(
          block_by_step_id[
            id(
              edge.premise_step
            )
          ],
          edge,
        )
      ),
    )
    for edge in presentation.edges
  )

  return (
    TodaGroupProofNarrativeEvidenceContributionSidecar(
      presentation=presentation,
      edge_semantics=edge_semantics,
    )
  )

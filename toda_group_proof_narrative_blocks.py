from dataclasses import dataclass
from enum import Enum

from barratt_hilton_rules import (
  HomotopyGroupMembershipStatement,
)
from homotopy_groups import (
  TodaPrimaryGroup,
  TodaPrimaryGroupZeroStatement,
)
from proof import (
  ProofStep,
  Relation,
  RelationType,
)
from toda_group_proof_narrative_catalog import (
  DEFINITION_STATEMENT_TYPES,
  REFERENCE_STATEMENT_TYPES,
)
from toda_group_proof_narrative_semantics import (
  TodaGroupProofNarrativePremiseSemanticRole,
  TodaGroupProofNarrativeSemanticSidecar,
  TodaGroupProofNarrativeStepSemanticRole,
)
from toda_group_proof_presentation import (
  TodaGroupProofPresentation,
)
from toda_rules import (
  TodaDeltaImageUpToSignStatement,
  TodaDeltaInjectiveStatement,
  TodaDeltaZeroStatement,
  TodaHopfInvariantInjectiveStatement,
  TodaHopfInvariantIsomorphismStatement,
  TodaHopfInvariantSurjectiveStatement,
  TodaHopfInvariantZeroStatement,
  TodaIteratedSuspensionInjectiveStatement,
  TodaProp42ExactnessStatement,
  TodaProp44SuspensionInjectiveStatement,
  TodaSuspensionInjectiveStatement,
  TodaSuspensionIsomorphismStatement,
  TodaSuspensionSurjectiveStatement,
)


class TodaGroupProofNarrativeMathematicalBlockRole(
  Enum
):
  TARGET = "target"
  REFERENCE = "reference"
  PRECONDITION = "precondition"
  DEFINITION = "definition"
  MEMBERSHIP = "membership"
  CALCULATION = "calculation"
  EXACTNESS = "exactness"
  MAP_PROPERTY = "map_property"
  ORDER = "order"
  GROUP_STRUCTURE = "group_structure"
  CONCLUSION = "conclusion"
  OTHER = "other"


@dataclass(frozen=True)
class TodaGroupProofNarrativeBlock:
  role: TodaGroupProofNarrativeMathematicalBlockRole
  steps: tuple[
    ProofStep,
    ...,
  ]

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.role,
      TodaGroupProofNarrativeMathematicalBlockRole,
    ):
      raise TypeError(
        "role must be a "
        "TodaGroupProofNarrativeMathematicalBlockRole"
      )

    if not isinstance(
      self.steps,
      tuple,
    ):
      raise TypeError(
        "steps must be a tuple"
      )

    if not self.steps:
      raise ValueError(
        "steps must not be empty"
      )

    seen_step_ids = set()

    for proof_step in self.steps:
      if not isinstance(
        proof_step,
        ProofStep,
      ):
        raise TypeError(
          "steps must contain only ProofStep objects"
        )

      step_id = id(
        proof_step
      )

      if step_id in seen_step_ids:
        raise ValueError(
          "steps must not contain duplicate ProofStep objects"
        )

      seen_step_ids.add(
        step_id
      )


MAP_PROPERTY_STATEMENT_TYPES = (
  TodaDeltaInjectiveStatement,
  TodaDeltaZeroStatement,
  TodaHopfInvariantInjectiveStatement,
  TodaHopfInvariantIsomorphismStatement,
  TodaHopfInvariantSurjectiveStatement,
  TodaHopfInvariantZeroStatement,
  TodaIteratedSuspensionInjectiveStatement,
  TodaProp44SuspensionInjectiveStatement,
  TodaSuspensionInjectiveStatement,
  TodaSuspensionIsomorphismStatement,
  TodaSuspensionSurjectiveStatement,
)


def _selected_step_ids(
  presentation: TodaGroupProofPresentation,
) -> set[int]:
  return {
    id(
      node.proof_step
    )
    for node in presentation.nodes
  }


def _validate_semantic_sidecar(
  presentation: TodaGroupProofPresentation,
  semantic_sidecar: (
    TodaGroupProofNarrativeSemanticSidecar
    | None
  ),
) -> None:
  if semantic_sidecar is None:
    return

  if not isinstance(
    semantic_sidecar,
    TodaGroupProofNarrativeSemanticSidecar,
  ):
    raise TypeError(
      "semantic_sidecar must be a "
      "TodaGroupProofNarrativeSemanticSidecar "
      "or None"
    )

  if (
    semantic_sidecar.presentation
    is not presentation
  ):
    raise ValueError(
      "semantic_sidecar must belong to "
      "presentation"
    )


def _semantic_block_role_for_step(
  proof_step: ProofStep,
  semantic_sidecar: (
    TodaGroupProofNarrativeSemanticSidecar
    | None
  ),
) -> (
  TodaGroupProofNarrativeMathematicalBlockRole
  | None
):
  if semantic_sidecar is None:
    return None

  roles = set()

  for semantic in (
    semantic_sidecar.step_semantics
  ):
    if (
      semantic.proof_step
      is not proof_step
    ):
      continue

    if (
      semantic.role
      is TodaGroupProofNarrativeStepSemanticRole
      .DEFINITION_INTRODUCTION
    ):
      roles.add(
        TodaGroupProofNarrativeMathematicalBlockRole
        .DEFINITION
      )

  for semantic in (
    semantic_sidecar.premise_semantics
  ):
    if (
      semantic.edge.premise_step
      is not proof_step
    ):
      continue

    if (
      semantic.role
      is TodaGroupProofNarrativePremiseSemanticRole
      .PRECONDITION
    ):
      roles.add(
        TodaGroupProofNarrativeMathematicalBlockRole
        .PRECONDITION
      )

  if not roles:
    return None

  if len(
    roles
  ) != 1:
    raise ValueError(
      "conflicting narrative semantic roles "
      "for proof_step"
    )

  return next(
    iter(
      roles
    )
  )


def recognize_toda_group_proof_narrative_step_role(
  presentation: TodaGroupProofPresentation,
  proof_step: ProofStep,
  semantic_sidecar: (
    TodaGroupProofNarrativeSemanticSidecar
    | None
  ) = None,
) -> TodaGroupProofNarrativeMathematicalBlockRole:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a TodaGroupProofPresentation"
    )

  if not isinstance(
    proof_step,
    ProofStep,
  ):
    raise TypeError(
      "proof_step must be a ProofStep"
    )

  if id(
    proof_step
  ) not in _selected_step_ids(
    presentation
  ):
    raise ValueError(
      "proof_step must appear in presentation nodes"
    )

  _validate_semantic_sidecar(
    presentation,
    semantic_sidecar,
  )

  if proof_step is presentation.root_step:
    return (
      TodaGroupProofNarrativeMathematicalBlockRole.TARGET
    )

  semantic_role = (
    _semantic_block_role_for_step(
      proof_step,
      semantic_sidecar,
    )
  )

  if semantic_role is not None:
    return semantic_role

  statement = proof_step.conclusion

  if isinstance(
    statement,
    REFERENCE_STATEMENT_TYPES,
  ):
    return (
      TodaGroupProofNarrativeMathematicalBlockRole.REFERENCE
    )

  if isinstance(
    statement,
    TodaPrimaryGroupZeroStatement,
  ):
    return (
      TodaGroupProofNarrativeMathematicalBlockRole.GROUP_STRUCTURE
    )

  if isinstance(
    statement,
    TodaDeltaImageUpToSignStatement,
  ):
    return (
      TodaGroupProofNarrativeMathematicalBlockRole.MAP_PROPERTY
    )

  if isinstance(
    statement,
    DEFINITION_STATEMENT_TYPES,
  ):
    return (
      TodaGroupProofNarrativeMathematicalBlockRole.DEFINITION
    )

  if isinstance(
    statement,
    HomotopyGroupMembershipStatement,
  ):
    return (
      TodaGroupProofNarrativeMathematicalBlockRole.MEMBERSHIP
    )

  if isinstance(
    statement,
    TodaProp42ExactnessStatement,
  ):
    return (
      TodaGroupProofNarrativeMathematicalBlockRole.EXACTNESS
    )

  if isinstance(
    statement,
    MAP_PROPERTY_STATEMENT_TYPES,
  ):
    return (
      TodaGroupProofNarrativeMathematicalBlockRole.MAP_PROPERTY
    )

  if isinstance(
    statement,
    Relation,
  ):
    if statement.relation_type is RelationType.ORDER:
      return (
        TodaGroupProofNarrativeMathematicalBlockRole.ORDER
      )

    if (
      statement.relation_type
      is RelationType.EQUALITY
      and isinstance(
        statement.lhs,
        TodaPrimaryGroup,
      )
    ):
      return (
        TodaGroupProofNarrativeMathematicalBlockRole.GROUP_STRUCTURE
      )

    if statement.relation_type in (
      RelationType.EQUALITY,
      RelationType.ZERO,
    ):
      return (
        TodaGroupProofNarrativeMathematicalBlockRole.CALCULATION
      )

  return (
    TodaGroupProofNarrativeMathematicalBlockRole.OTHER
  )


def build_toda_group_proof_narrative_blocks(
  presentation: TodaGroupProofPresentation,
  semantic_sidecar: (
    TodaGroupProofNarrativeSemanticSidecar
    | None
  ) = None,
) -> tuple[
  TodaGroupProofNarrativeBlock,
  ...,
]:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a TodaGroupProofPresentation"
    )

  _validate_semantic_sidecar(
    presentation,
    semantic_sidecar,
  )

  ordered_steps = tuple(
    node.proof_step
    for node in presentation.nodes
  )

  role_by_step_id = {
    id(
      proof_step
    ): recognize_toda_group_proof_narrative_step_role(
      presentation,
      proof_step,
      semantic_sidecar=semantic_sidecar,
    )
    for proof_step in ordered_steps
  }

  neighbors_by_step_id = {
    id(
      proof_step
    ): set()
    for proof_step in ordered_steps
  }

  for edge in presentation.edges:
    parent_id = id(
      edge.parent_step
    )
    premise_id = id(
      edge.premise_step
    )

    if (
      role_by_step_id[
        parent_id
      ]
      is role_by_step_id[
        premise_id
      ]
    ):
      neighbors_by_step_id[
        parent_id
      ].add(
        premise_id
      )
      neighbors_by_step_id[
        premise_id
      ].add(
        parent_id
      )

  step_by_id = {
    id(
      proof_step
    ): proof_step
    for proof_step in ordered_steps
  }

  order_by_step_id = {
    id(
      proof_step
    ): index
    for index, proof_step in enumerate(
      ordered_steps
    )
  }

  visited_step_ids = set()
  blocks = []

  for proof_step in ordered_steps:
    start_id = id(
      proof_step
    )

    if start_id in visited_step_ids:
      continue

    role = role_by_step_id[
      start_id
    ]
    component_ids = []
    pending_ids = [
      start_id
    ]

    while pending_ids:
      current_id = pending_ids.pop()

      if current_id in visited_step_ids:
        continue

      visited_step_ids.add(
        current_id
      )
      component_ids.append(
        current_id
      )

      pending_ids.extend(
        neighbor_id
        for neighbor_id in neighbors_by_step_id[
          current_id
        ]
        if neighbor_id not in visited_step_ids
      )

    component_ids.sort(
      key=lambda step_id: order_by_step_id[
        step_id
      ]
    )

    blocks.append(
      TodaGroupProofNarrativeBlock(
        role=role,
        steps=tuple(
          step_by_id[
            step_id
          ]
          for step_id in component_ids
        ),
      )
    )

  return tuple(
    blocks
  )

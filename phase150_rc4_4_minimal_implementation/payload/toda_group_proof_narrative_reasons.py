from dataclasses import dataclass
from enum import Enum

from proof import (
  ProofStep,
)
from toda_group_proof_narrative_semantics import (
  TodaGroupProofNarrativeDependencySemanticRole,
  TodaGroupProofNarrativeSemanticSidecar,
)
from toda_group_proof_presentation import (
  TodaGroupProofPresentation,
)


class TodaGroupProofNarrativeReasonKind(
  Enum
):
  DEFINITION_APPLICABILITY = (
    "definition_applicability"
  )


@dataclass(frozen=True)
class TodaGroupProofNarrativeReason:
  kind: TodaGroupProofNarrativeReasonKind
  premise_steps: tuple[
    ProofStep,
    ...,
  ]
  conclusion_step: ProofStep
  owner_argument_index: int | None = None

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.kind,
      TodaGroupProofNarrativeReasonKind,
    ):
      raise TypeError(
        "kind must be a "
        "TodaGroupProofNarrativeReasonKind"
      )

    if not isinstance(
      self.premise_steps,
      tuple,
    ):
      raise TypeError(
        "premise_steps must be a tuple"
      )

    if not self.premise_steps:
      raise ValueError(
        "premise_steps must not be empty"
      )

    seen_step_ids = set()

    for proof_step in self.premise_steps:
      if not isinstance(
        proof_step,
        ProofStep,
      ):
        raise TypeError(
          "premise_steps must contain only "
          "ProofStep objects"
        )

      step_id = id(
        proof_step
      )

      if step_id in seen_step_ids:
        raise ValueError(
          "premise_steps must not contain "
          "duplicate ProofStep objects"
        )

      seen_step_ids.add(
        step_id
      )

    if not isinstance(
      self.conclusion_step,
      ProofStep,
    ):
      raise TypeError(
        "conclusion_step must be a ProofStep"
      )

    if id(
      self.conclusion_step
    ) in seen_step_ids:
      raise ValueError(
        "conclusion_step must not also be "
        "a premise step"
      )

    if (
      self.owner_argument_index
      is not None
      and (
        not isinstance(
          self.owner_argument_index,
          int,
        )
        or isinstance(
          self.owner_argument_index,
          bool,
        )
        or self.owner_argument_index < 0
      )
    ):
      raise TypeError(
        "owner_argument_index must be a "
        "non-negative integer or None"
      )


@dataclass(frozen=True)
class TodaGroupProofNarrativeReasonSidecar:
  presentation: TodaGroupProofPresentation
  reasons: tuple[
    TodaGroupProofNarrativeReason,
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
      self.reasons,
      tuple,
    ):
      raise TypeError(
        "reasons must be a tuple"
      )

    allowed_step_ids = {
      id(
        node.proof_step
      )
      for node in self.presentation.nodes
    }
    seen_reason_keys = set()

    for reason in self.reasons:
      if not isinstance(
        reason,
        TodaGroupProofNarrativeReason,
      ):
        raise TypeError(
          "reasons must contain only "
          "TodaGroupProofNarrativeReason objects"
        )

      reason_step_ids = (
        tuple(
          id(
            proof_step
          )
          for proof_step in reason.premise_steps
        )
        + (
          id(
            reason.conclusion_step
          ),
        )
      )

      if any(
        step_id not in allowed_step_ids
        for step_id in reason_step_ids
      ):
        raise ValueError(
          "reason proof steps must appear "
          "in presentation nodes"
        )

      reason_key = (
        reason.kind,
        tuple(
          id(
            proof_step
          )
          for proof_step in reason.premise_steps
        ),
        id(
          reason.conclusion_step
        ),
        reason.owner_argument_index,
      )

      if reason_key in seen_reason_keys:
        raise ValueError(
          "reasons must not contain "
          "duplicate reason relations"
        )

      seen_reason_keys.add(
        reason_key
      )


def build_toda_group_proof_narrative_reason_sidecar(
  presentation: TodaGroupProofPresentation,
  semantic_sidecar: TodaGroupProofNarrativeSemanticSidecar,
) -> TodaGroupProofNarrativeReasonSidecar:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a "
      "TodaGroupProofPresentation"
    )

  if not isinstance(
    semantic_sidecar,
    TodaGroupProofNarrativeSemanticSidecar,
  ):
    raise TypeError(
      "semantic_sidecar must be a "
      "TodaGroupProofNarrativeSemanticSidecar"
    )

  if (
    semantic_sidecar.presentation
    is not presentation
  ):
    raise ValueError(
      "semantic_sidecar must belong to "
      "presentation"
    )

  reasons = []

  for dependency in (
    semantic_sidecar.dependency_semantics
  ):
    if (
      dependency.role
      is not TodaGroupProofNarrativeDependencySemanticRole
      .PRECONDITION_FOR_DEFINITION
    ):
      continue

    reasons.append(
      TodaGroupProofNarrativeReason(
        kind=(
          TodaGroupProofNarrativeReasonKind
          .DEFINITION_APPLICABILITY
        ),
        premise_steps=(
          dependency.prerequisite_step,
        ),
        conclusion_step=(
          dependency.dependent_step
        ),
      )
    )

  return (
    TodaGroupProofNarrativeReasonSidecar(
      presentation=presentation,
      reasons=tuple(
        reasons
      ),
    )
  )

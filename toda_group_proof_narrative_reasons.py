from dataclasses import dataclass
from enum import Enum

from expression import (
  Multiple,
)
from proof import (
  ProofStep,
  Relation,
  RelationType,
)
from toda_rules import (
  TodaDeltaZeroStatement,
  TodaProp42ExactnessStatement,
  TodaSuspensionInjectiveStatement,
)
from toda_group_proof_narrative_semantics import (
  TodaGroupProofNarrativeDependencySemanticRole,
  TodaGroupProofNarrativeReferenceApplicationSemantic,
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
  EXACTNESS_TO_MAP_PROPERTY = (
    "exactness_to_map_property"
  )
  MULTIPLE_RELATION_TO_ORDER = (
    "multiple_relation_to_order"
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
  reference_application: (
    TodaGroupProofNarrativeReferenceApplicationSemantic | None
  ) = None

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
      self.reference_application is not None
      and not isinstance(
        self.reference_application,
        TodaGroupProofNarrativeReferenceApplicationSemantic,
      )
    ):
      raise TypeError(
        "reference_application must be a "
        "TodaGroupProofNarrativeReferenceApplicationSemantic or None"
      )

    if (
      self.reference_application is not None
      and self.reference_application.dependent_step
      is not self.conclusion_step
    ):
      raise ValueError(
        "reference_application must belong to conclusion_step"
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


def _exactness_to_map_property_reason(
  proof_step: ProofStep,
) -> TodaGroupProofNarrativeReason | None:
  conclusion = proof_step.conclusion

  if not isinstance(
    conclusion,
    TodaSuspensionInjectiveStatement,
  ):
    return None

  zero_premises = tuple(
    premise
    for premise in proof_step.premises
    if isinstance(
      premise.conclusion,
      TodaDeltaZeroStatement,
    )
  )
  exactness_premises = tuple(
    premise
    for premise in proof_step.premises
    if isinstance(
      premise.conclusion,
      TodaProp42ExactnessStatement,
    )
  )

  compatible_pairs = []

  for zero_premise in zero_premises:
    zero_map = zero_premise.conclusion.map

    for exactness_premise in exactness_premises:
      window = exactness_premise.conclusion.window

      if (
        zero_map.source_group
        != window.source_term
        or zero_map.target_group
        != window.middle_term
        or window.middle_term
        != conclusion.map.source_group
        or window.target_term
        != conclusion.map.target_group
        or getattr(
          window.first_map,
          "name",
          None,
        )
        != "Δ"
        or getattr(
          window.second_map,
          "name",
          None,
        )
        != "E"
      ):
        continue

      compatible_pairs.append(
        (
          zero_premise,
          exactness_premise,
        )
      )

  if len(
    compatible_pairs
  ) != 1:
    return None

  zero_premise, exactness_premise = (
    compatible_pairs[0]
  )

  return TodaGroupProofNarrativeReason(
    kind=(
      TodaGroupProofNarrativeReasonKind
      .EXACTNESS_TO_MAP_PROPERTY
    ),
    premise_steps=(
      zero_premise,
      exactness_premise,
    ),
    conclusion_step=proof_step,
  )


def _multiple_relation_to_order_reason(
  proof_step: ProofStep,
) -> TodaGroupProofNarrativeReason | None:
  conclusion = proof_step.conclusion

  if (
    not isinstance(conclusion, Relation)
    or conclusion.relation_type is not RelationType.ORDER
    or conclusion.rhs != 4
  ):
    return None

  order_premises = tuple(
    premise
    for premise in proof_step.premises
    if (
      isinstance(premise.conclusion, Relation)
      and premise.conclusion.relation_type is RelationType.ORDER
      and premise.conclusion.rhs == 2
    )
  )
  equality_premises = tuple(
    premise
    for premise in proof_step.premises
    if (
      isinstance(premise.conclusion, Relation)
      and premise.conclusion.relation_type is RelationType.EQUALITY
      and isinstance(premise.conclusion.lhs, Multiple)
      and premise.conclusion.lhs.coefficient == 2
    )
  )

  compatible_pairs = []

  for order_premise in order_premises:
    ordered_expression = order_premise.conclusion.lhs

    for equality_premise in equality_premises:
      equality = equality_premise.conclusion
      multiple = equality.lhs

      if (
        equality.rhs != ordered_expression
        or multiple.expression != conclusion.lhs
      ):
        continue

      compatible_pairs.append((order_premise, equality_premise))

  if len(compatible_pairs) != 1:
    return None

  order_premise, equality_premise = compatible_pairs[0]

  return TodaGroupProofNarrativeReason(
    kind=(
      TodaGroupProofNarrativeReasonKind
      .MULTIPLE_RELATION_TO_ORDER
    ),
    premise_steps=(order_premise, equality_premise),
    conclusion_step=proof_step,
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
  reference_applications_by_step_id = {}

  for application in semantic_sidecar.reference_application_semantics:
    reference_applications_by_step_id.setdefault(
      id(application.dependent_step),
      [],
    ).append(application)

  for dependency in (
    semantic_sidecar.dependency_semantics
  ):
    if (
      dependency.role
      is not TodaGroupProofNarrativeDependencySemanticRole
      .PRECONDITION_FOR_DEFINITION
    ):
      continue

    matching_applications = reference_applications_by_step_id.get(
      id(dependency.dependent_step),
      (),
    )
    reference_application = (
      matching_applications[0]
      if len(matching_applications) == 1
      else None
    )

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
        reference_application=reference_application,
      )
    )

  for node in presentation.nodes:
    exactness_reason = (
      _exactness_to_map_property_reason(
        node.proof_step
      )
    )

    if exactness_reason is not None:
      reasons.append(exactness_reason)

    multiple_order_reason = (
      _multiple_relation_to_order_reason(
        node.proof_step
      )
    )

    if multiple_order_reason is not None:
      reasons.append(multiple_order_reason)

  return (
    TodaGroupProofNarrativeReasonSidecar(
      presentation=presentation,
      reasons=tuple(
        reasons
      ),
    )
  )

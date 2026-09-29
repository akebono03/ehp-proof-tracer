from dataclasses import dataclass
from enum import Enum

from proof import (
  ProofStep,
  Relation,
)
from toda_group_proof_presentation import (
  TodaGroupProofPresentation,
)
from toda_rules import (
  TodaProp53FiniteDimensionalStatement,
)


class TodaGroupProofNarrativeHiddenBridgeSemanticRole(
  Enum
):
  TRANSPORT = "transport"
  INTEGRATION_PROVENANCE = (
    "integration_provenance"
  )


class TodaGroupProofNarrativeHiddenBridgeOperationKind(
  Enum
):
  SUSPENSION_STABILIZATION = (
    "suspension_stabilization"
  )


@dataclass(frozen=True)
class TodaGroupProofNarrativeHiddenBridgeSemantic:
  proof_step: ProofStep
  role: (
    TodaGroupProofNarrativeHiddenBridgeSemanticRole
  )
  reference_identity: str | None = None
  operation_kind: (
    TodaGroupProofNarrativeHiddenBridgeOperationKind
    | None
  ) = None

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.proof_step,
      ProofStep,
    ):
      raise TypeError(
        "proof_step must be a ProofStep"
      )

    if not isinstance(
      self.role,
      TodaGroupProofNarrativeHiddenBridgeSemanticRole,
    ):
      raise TypeError(
        "role must be a "
        "TodaGroupProofNarrativeHiddenBridgeSemanticRole"
      )

    if (
      self.reference_identity is not None
      and not isinstance(
        self.reference_identity,
        str,
      )
    ):
      raise TypeError(
        "reference_identity must be a str or None"
      )

    if (
      self.operation_kind is not None
      and not isinstance(
        self.operation_kind,
        TodaGroupProofNarrativeHiddenBridgeOperationKind,
      )
    ):
      raise TypeError(
        "operation_kind must be a "
        "TodaGroupProofNarrativeHiddenBridgeOperationKind "
        "or None"
      )


_TRANSPORT_RULE_NAMES = frozenset(
  {
    (
      "Toda Proposition 5.3 n=3 "
      "pi_5^3 finite-cyclic transport"
    ),
    (
      "Toda Proposition 5.3 n=4 "
      "pi_6^4 finite-cyclic transport"
    ),
    (
      "Toda Proposition 5.3 "
      "eta_4 squared stable transport"
    ),
  }
)


_STABLE_TRANSPORT_RULE_NAME = (
  "Toda Proposition 5.3 "
  "eta_4 squared stable transport"
)


def _inference_rule_name(
  proof_step: ProofStep,
) -> str | None:
  inference_rule = (
    proof_step.inference_rule
  )

  if inference_rule is None:
    return None

  return inference_rule.name


def classify_toda_group_proof_narrative_hidden_bridge_step(
  proof_step: ProofStep,
) -> (
  TodaGroupProofNarrativeHiddenBridgeSemanticRole
  | None
):
  if not isinstance(
    proof_step,
    ProofStep,
  ):
    raise TypeError(
      "proof_step must be a ProofStep"
    )

  rule_name = _inference_rule_name(
    proof_step
  )

  if (
    isinstance(
      proof_step.conclusion,
      Relation,
    )
    and rule_name
    in _TRANSPORT_RULE_NAMES
  ):
    return (
      TodaGroupProofNarrativeHiddenBridgeSemanticRole
      .TRANSPORT
    )

  if isinstance(
    proof_step.conclusion,
    TodaProp53FiniteDimensionalStatement,
  ):
    return (
      TodaGroupProofNarrativeHiddenBridgeSemanticRole
      .INTEGRATION_PROVENANCE
    )

  return None


def _hidden_bridge_reference_identity(
  proof_step: ProofStep,
  role: TodaGroupProofNarrativeHiddenBridgeSemanticRole,
) -> str | None:
  if (
    role
    is TodaGroupProofNarrativeHiddenBridgeSemanticRole
    .TRANSPORT
  ):
    return "Proposition 5.3"

  return None


def _hidden_bridge_operation_kind(
  proof_step: ProofStep,
  role: TodaGroupProofNarrativeHiddenBridgeSemanticRole,
) -> (
  TodaGroupProofNarrativeHiddenBridgeOperationKind
  | None
):
  if (
    role
    is TodaGroupProofNarrativeHiddenBridgeSemanticRole
    .TRANSPORT
    and _inference_rule_name(
      proof_step
    )
    == _STABLE_TRANSPORT_RULE_NAME
  ):
    return (
      TodaGroupProofNarrativeHiddenBridgeOperationKind
      .SUSPENSION_STABILIZATION
    )

  return None


def build_toda_group_proof_narrative_hidden_bridge_semantics(
  presentation: TodaGroupProofPresentation,
) -> tuple[
  TodaGroupProofNarrativeHiddenBridgeSemantic,
  ...,
]:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a "
      "TodaGroupProofPresentation"
    )

  semantics = []

  for node in presentation.nodes:
    proof_step = node.proof_step
    role = (
      classify_toda_group_proof_narrative_hidden_bridge_step(
        proof_step
      )
    )

    if role is None:
      continue

    semantics.append(
      TodaGroupProofNarrativeHiddenBridgeSemantic(
        proof_step=proof_step,
        role=role,
        reference_identity=(
          _hidden_bridge_reference_identity(
            proof_step,
            role,
          )
        ),
        operation_kind=(
          _hidden_bridge_operation_kind(
            proof_step,
            role,
          )
        ),
      )
    )

  return tuple(
    semantics
  )

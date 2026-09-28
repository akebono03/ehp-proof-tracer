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


@dataclass(frozen=True)
class TodaGroupProofNarrativeHiddenBridgeSemantic:
  proof_step: ProofStep
  role: (
    TodaGroupProofNarrativeHiddenBridgeSemanticRole
  )

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
    role = (
      classify_toda_group_proof_narrative_hidden_bridge_step(
        node.proof_step
      )
    )

    if role is None:
      continue

    semantics.append(
      TodaGroupProofNarrativeHiddenBridgeSemantic(
        proof_step=node.proof_step,
        role=role,
      )
    )

  return tuple(
    semantics
  )

from dataclasses import dataclass
from enum import Enum

from proof import ProofStep
from toda_group_proof_presentation import TodaGroupProofPresentation
from toda_rules import (
  Toda48Pi16_9OrderAndE4InjectiveStatement,
  Toda515Sigma8TransportedDecompositionStatement,
  TodaLemma514Sigma8Statement,
  TodaProp515Pi12_5HopfIsomorphismStatement,
  TodaProp56Pi8_5QuotientStatement,
)


class TodaGroupProofNarrativeAggregateSemanticKind(Enum):
  GROUP_ORDER_TRANSPORT = "group_order_transport"
  MAP_TRANSPORT = "map_transport"
  GROUP_DECOMPOSITION_TRANSPORT = "group_decomposition_transport"
  RELATION_AGGREGATE = "relation_aggregate"


@dataclass(frozen=True)
class TodaGroupProofNarrativeAggregateStepSemantic:
  proof_step: ProofStep
  kind: TodaGroupProofNarrativeAggregateSemanticKind

  def __post_init__(self) -> None:
    if not isinstance(self.proof_step, ProofStep):
      raise TypeError("proof_step must be a ProofStep")

    if not isinstance(
      self.kind,
      TodaGroupProofNarrativeAggregateSemanticKind,
    ):
      raise TypeError(
        "kind must be a "
        "TodaGroupProofNarrativeAggregateSemanticKind"
      )


@dataclass(frozen=True)
class TodaGroupProofNarrativeAggregateSemanticSidecar:
  presentation: TodaGroupProofPresentation
  step_semantics: tuple[
    TodaGroupProofNarrativeAggregateStepSemantic,
    ...,
  ]

  def __post_init__(self) -> None:
    if not isinstance(
      self.presentation,
      TodaGroupProofPresentation,
    ):
      raise TypeError(
        "presentation must be a TodaGroupProofPresentation"
      )

    if not isinstance(self.step_semantics, tuple):
      raise TypeError("step_semantics must be a tuple")

    allowed_step_ids = {
      id(node.proof_step)
      for node in self.presentation.nodes
    }
    seen_step_ids = set()

    for semantic in self.step_semantics:
      if not isinstance(
        semantic,
        TodaGroupProofNarrativeAggregateStepSemantic,
      ):
        raise TypeError(
          "step_semantics must contain only "
          "TodaGroupProofNarrativeAggregateStepSemantic objects"
        )

      step_id = id(semantic.proof_step)

      if step_id not in allowed_step_ids:
        raise ValueError(
          "aggregate semantic proof_step must appear "
          "in presentation nodes"
        )

      if step_id in seen_step_ids:
        raise ValueError(
          "step_semantics must not contain duplicate proof steps"
        )

      seen_step_ids.add(step_id)


_AGGREGATE_SEMANTIC_KIND_BY_STATEMENT_TYPE = {
  TodaProp56Pi8_5QuotientStatement: (
    TodaGroupProofNarrativeAggregateSemanticKind
    .GROUP_ORDER_TRANSPORT
  ),
  Toda48Pi16_9OrderAndE4InjectiveStatement: (
    TodaGroupProofNarrativeAggregateSemanticKind
    .GROUP_ORDER_TRANSPORT
  ),
  TodaProp515Pi12_5HopfIsomorphismStatement: (
    TodaGroupProofNarrativeAggregateSemanticKind
    .MAP_TRANSPORT
  ),
  Toda515Sigma8TransportedDecompositionStatement: (
    TodaGroupProofNarrativeAggregateSemanticKind
    .GROUP_DECOMPOSITION_TRANSPORT
  ),
  TodaLemma514Sigma8Statement: (
    TodaGroupProofNarrativeAggregateSemanticKind
    .RELATION_AGGREGATE
  ),
}


def build_toda_group_proof_narrative_aggregate_semantic_sidecar(
  presentation: TodaGroupProofPresentation,
) -> TodaGroupProofNarrativeAggregateSemanticSidecar:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a TodaGroupProofPresentation"
    )

  step_semantics = []

  for node in presentation.nodes:
    proof_step = node.proof_step
    kind = _AGGREGATE_SEMANTIC_KIND_BY_STATEMENT_TYPE.get(
      type(proof_step.conclusion)
    )

    if kind is None:
      continue

    step_semantics.append(
      TodaGroupProofNarrativeAggregateStepSemantic(
        proof_step=proof_step,
        kind=kind,
      )
    )

  return TodaGroupProofNarrativeAggregateSemanticSidecar(
    presentation=presentation,
    step_semantics=tuple(step_semantics),
  )

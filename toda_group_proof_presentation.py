from dataclasses import dataclass

from proof import ProofStep
from proof_repository import ProofRepositoryEntry
from toda_group_result_proof_replay import (
  TodaGroupResultProofReplayResult,
  TodaGroupResultProofReplayStep,
)
from toda_proof_dependency import (
  TodaProofEdge,
  extract_toda_recursive_proof_provenance,
)


@dataclass(frozen=True)
class TodaGroupProofPresentation:
  source_replay: TodaGroupResultProofReplayResult
  edges: tuple[
    TodaProofEdge,
    ...,
  ]

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.source_replay,
      TodaGroupResultProofReplayResult,
    ):
      raise TypeError(
        "source_replay must be a "
        "TodaGroupResultProofReplayResult"
      )

    if not isinstance(
      self.edges,
      tuple,
    ):
      raise TypeError(
        "edges must be a tuple"
      )

    allowed_step_ids = {
      id(
        node.proof_step
      )
      for node in self.nodes
    }

    seen_edge_keys: set[
      tuple[
        int,
        int,
        int,
      ]
    ] = set()

    for edge in self.edges:
      if not isinstance(
        edge,
        TodaProofEdge,
      ):
        raise TypeError(
          "edges must contain only "
          "TodaProofEdge objects"
        )

      if (
        id(
          edge.parent_step
        )
        not in allowed_step_ids
      ):
        raise ValueError(
          "edge parent_step must appear "
          "in presentation nodes"
        )

      if (
        id(
          edge.premise_step
        )
        not in allowed_step_ids
      ):
        raise ValueError(
          "edge premise_step must appear "
          "in presentation nodes"
        )

      edge_key = (
        id(
          edge.parent_step
        ),
        id(
          edge.premise_step
        ),
        edge.premise_index,
      )

      if edge_key in seen_edge_keys:
        raise ValueError(
          "edges must not contain "
          "duplicate proof edges"
        )

      seen_edge_keys.add(
        edge_key
      )

  @property
  def nodes(
    self,
  ) -> tuple[
    TodaGroupResultProofReplayStep,
    ...,
  ]:
    return self.source_replay.steps

  @property
  def root_step(
    self,
  ) -> ProofStep:
    return self.source_replay.root_step

  @property
  def source_entry(
    self,
  ) -> ProofRepositoryEntry:
    return self.source_replay.source_entry

  @property
  def max_depth(
    self,
  ) -> int:
    return self.source_replay.max_depth


def build_toda_group_proof_presentation(
  replay: TodaGroupResultProofReplayResult,
) -> TodaGroupProofPresentation:
  if not isinstance(
    replay,
    TodaGroupResultProofReplayResult,
  ):
    raise TypeError(
      "replay must be a "
      "TodaGroupResultProofReplayResult"
    )

  provenance = (
    extract_toda_recursive_proof_provenance(
      replay.group_result
    )
  )

  allowed_step_ids = {
    id(
      replay_step.proof_step
    )
    for replay_step in replay.steps
  }

  edges = tuple(
    edge
    for edge in provenance.edges
    if (
      id(
        edge.parent_step
      )
      in allowed_step_ids
      and id(
        edge.premise_step
      )
      in allowed_step_ids
    )
  )

  return TodaGroupProofPresentation(
    source_replay=replay,
    edges=edges,
  )

from dataclasses import dataclass

from proof_repository import ProofRepositoryEntry
from toda_proof_dependency import (
  TodaProofEdge,
  TodaProofNode,
  TodaRecursiveProofProvenanceResult,
)
from toda_proof_presentation import (
  TodaProofStepPresentation,
  build_toda_proof_step_presentation,
)


@dataclass(frozen=True)
class TodaProofFlowNodePresentation:
  source_node: TodaProofNode
  step: TodaProofStepPresentation
  incoming_use_count: int

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.source_node,
      TodaProofNode,
    ):
      raise TypeError(
        "source_node must be "
        "a TodaProofNode"
      )

    if not isinstance(
      self.step,
      TodaProofStepPresentation,
    ):
      raise TypeError(
        "step must be a "
        "TodaProofStepPresentation"
      )

    if (
      self.step.source_step
      is not self.source_node.proof_step
    ):
      raise ValueError(
        "step source identity must match "
        "source_node.proof_step"
      )

    if (
      self.step.role
      is not self.source_node.role
    ):
      raise ValueError(
        "step role must match "
        "source_node.role"
      )

    if (
      isinstance(
        self.incoming_use_count,
        bool,
      )
      or not isinstance(
        self.incoming_use_count,
        int,
      )
    ):
      raise TypeError(
        "incoming_use_count must be an int"
      )

    if self.incoming_use_count < 0:
      raise ValueError(
        "incoming_use_count must be "
        "non-negative"
      )

  @property
  def shortest_depth(
    self,
  ) -> int:
    return self.source_node.shortest_depth

  @property
  def is_shared_dependency(
    self,
  ) -> bool:
    return self.incoming_use_count > 1


@dataclass(frozen=True)
class TodaProofFlowEdgePresentation:
  source_edge: TodaProofEdge
  parent: TodaProofFlowNodePresentation
  premise: TodaProofFlowNodePresentation

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.source_edge,
      TodaProofEdge,
    ):
      raise TypeError(
        "source_edge must be "
        "a TodaProofEdge"
      )

    if not isinstance(
      self.parent,
      TodaProofFlowNodePresentation,
    ):
      raise TypeError(
        "parent must be a "
        "TodaProofFlowNodePresentation"
      )

    if not isinstance(
      self.premise,
      TodaProofFlowNodePresentation,
    ):
      raise TypeError(
        "premise must be a "
        "TodaProofFlowNodePresentation"
      )

    if (
      self.parent.step.source_step
      is not self.source_edge.parent_step
    ):
      raise ValueError(
        "parent identity must match "
        "source_edge.parent_step"
      )

    if (
      self.premise.step.source_step
      is not self.source_edge.premise_step
    ):
      raise ValueError(
        "premise identity must match "
        "source_edge.premise_step"
      )

  @property
  def premise_index(
    self,
  ) -> int:
    return self.source_edge.premise_index


@dataclass(frozen=True)
class TodaReadableProofFlowPresentation:
  source_provenance: TodaRecursiveProofProvenanceResult
  nodes: tuple[
    TodaProofFlowNodePresentation,
    ...,
  ]
  edges: tuple[
    TodaProofFlowEdgePresentation,
    ...,
  ]

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.source_provenance,
      TodaRecursiveProofProvenanceResult,
    ):
      raise TypeError(
        "source_provenance must be "
        "a TodaRecursiveProofProvenanceResult"
      )

    if not isinstance(
      self.nodes,
      tuple,
    ):
      raise TypeError(
        "nodes must be a tuple"
      )

    if not isinstance(
      self.edges,
      tuple,
    ):
      raise TypeError(
        "edges must be a tuple"
      )

    source_node_ids = {
      id(node.proof_step)
      for node in (
        self.source_provenance.nodes
      )
    }

    if len(
      self.nodes
    ) != len(
      self.source_provenance.nodes
    ):
      raise ValueError(
        "nodes must contain each source "
        "provenance node exactly once"
      )

    seen_step_ids: set[int] = set()

    for node in self.nodes:
      if not isinstance(
        node,
        TodaProofFlowNodePresentation,
      ):
        raise TypeError(
          "nodes must contain only "
          "TodaProofFlowNodePresentation "
          "objects"
        )

      step_id = id(
        node.step.source_step
      )

      if step_id in seen_step_ids:
        raise ValueError(
          "nodes must not duplicate "
          "ProofStep identity"
        )

      if step_id not in source_node_ids:
        raise ValueError(
          "presentation node must come from "
          "source provenance"
        )

      seen_step_ids.add(
        step_id
      )

    if seen_step_ids != source_node_ids:
      raise ValueError(
        "nodes must cover all source "
        "provenance nodes"
      )

    if (
      len(self.edges)
      != len(
        self.source_provenance.edges
      )
    ):
      raise ValueError(
        "edges must match source_provenance "
        "edges"
      )

    for (
      presented_edge,
      source_edge,
    ) in zip(
      self.edges,
      self.source_provenance.edges,
    ):
      if not isinstance(
        presented_edge,
        TodaProofFlowEdgePresentation,
      ):
        raise TypeError(
          "edges must contain only "
          "TodaProofFlowEdgePresentation "
          "objects"
        )

      if (
        presented_edge.source_edge
        is not source_edge
      ):
        raise ValueError(
          "edge identity must match "
          "source_provenance in order"
        )

  @property
  def root(
    self,
  ) -> TodaProofFlowNodePresentation:
    return next(
      node
      for node in self.nodes
      if (
        node.step.source_step
        is self.source_provenance.root_step
      )
    )


def _validate_repository_entries(
  repository_entries: tuple[
    ProofRepositoryEntry,
    ...,
  ],
) -> None:
  if not isinstance(
    repository_entries,
    tuple,
  ):
    raise TypeError(
      "repository_entries must be a tuple"
    )

  for entry in repository_entries:
    if not isinstance(
      entry,
      ProofRepositoryEntry,
    ):
      raise TypeError(
        "repository_entries must contain only "
        "ProofRepositoryEntry objects"
      )


def _dependency_first_source_nodes(
  provenance: TodaRecursiveProofProvenanceResult,
) -> tuple[
  TodaProofNode,
  ...,
]:
  node_by_step_id = {
    id(node.proof_step): node
    for node in provenance.nodes
  }

  outgoing_edges_by_parent_id: dict[
    int,
    list[
      TodaProofEdge
    ],
  ] = {}

  for edge in provenance.edges:
    outgoing_edges_by_parent_id.setdefault(
      id(edge.parent_step),
      [],
    ).append(
      edge
    )

  ordered: list[
    TodaProofNode
  ] = []

  visited_ids: set[int] = set()
  active_ids: set[int] = set()

  def visit(
    node: TodaProofNode,
  ) -> None:
    step_id = id(
      node.proof_step
    )

    if step_id in visited_ids:
      return

    if step_id in active_ids:
      return

    active_ids.add(
      step_id
    )

    for edge in (
      outgoing_edges_by_parent_id.get(
        step_id,
        (),
      )
    ):
      premise_id = id(
        edge.premise_step
      )

      premise_node = (
        node_by_step_id[
          premise_id
        ]
      )

      visit(
        premise_node
      )

    active_ids.remove(
      step_id
    )

    if step_id in visited_ids:
      return

    visited_ids.add(
      step_id
    )

    ordered.append(
      node
    )

  root_node = node_by_step_id[
    id(
      provenance.root_step
    )
  ]

  visit(
    root_node
  )

  for node in provenance.nodes:
    visit(
      node
    )

  return tuple(
    ordered
  )


def build_toda_readable_proof_flow_presentation(
  provenance: TodaRecursiveProofProvenanceResult,
  repository_entries: tuple[
    ProofRepositoryEntry,
    ...,
  ] = (),
) -> TodaReadableProofFlowPresentation:
  if not isinstance(
    provenance,
    TodaRecursiveProofProvenanceResult,
  ):
    raise TypeError(
      "provenance must be "
      "a TodaRecursiveProofProvenanceResult"
    )

  _validate_repository_entries(
    repository_entries
  )

  incoming_use_count_by_step_id: dict[
    int,
    int,
  ] = {
    id(node.proof_step): 0
    for node in provenance.nodes
  }

  for edge in provenance.edges:
    premise_id = id(
      edge.premise_step
    )

    incoming_use_count_by_step_id[
      premise_id
    ] += 1

  source_nodes = (
    _dependency_first_source_nodes(
      provenance
    )
  )

  nodes = tuple(
    TodaProofFlowNodePresentation(
      source_node=source_node,
      step=(
        build_toda_proof_step_presentation(
          source_node.proof_step,
          repository_entries,
        )
      ),
      incoming_use_count=(
        incoming_use_count_by_step_id[
          id(
            source_node.proof_step
          )
        ]
      ),
    )
    for source_node in source_nodes
  )

  node_by_step_id = {
    id(node.step.source_step): node
    for node in nodes
  }

  edges = tuple(
    TodaProofFlowEdgePresentation(
      source_edge=edge,
      parent=(
        node_by_step_id[
          id(
            edge.parent_step
          )
        ]
      ),
      premise=(
        node_by_step_id[
          id(
            edge.premise_step
          )
        ]
      ),
    )
    for edge in provenance.edges
  )

  return TodaReadableProofFlowPresentation(
    source_provenance=provenance,
    nodes=nodes,
    edges=edges,
  )

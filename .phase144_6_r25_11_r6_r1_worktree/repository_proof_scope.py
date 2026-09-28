from dataclasses import dataclass

from proof import ProofStep
from proof_repository import (
  ProofRepository,
  ProofRepositoryEntry,
)


@dataclass(frozen=True)
class RepositoryProofScopeNode:
  root_entry: ProofRepositoryEntry
  proof_step: ProofStep
  shortest_depth: int

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.root_entry,
      ProofRepositoryEntry,
    ):
      raise TypeError(
        "root_entry must be a ProofRepositoryEntry"
      )

    if not isinstance(
      self.proof_step,
      ProofStep,
    ):
      raise TypeError(
        "proof_step must be a ProofStep"
      )

    if (
      isinstance(
        self.shortest_depth,
        bool,
      )
      or not isinstance(
        self.shortest_depth,
        int,
      )
    ):
      raise TypeError(
        "shortest_depth must be an int"
      )

    if self.shortest_depth < 0:
      raise ValueError(
        "shortest_depth must be non-negative"
      )

    if (
      self.shortest_depth == 0
      and self.proof_step
      is not self.root_entry.step
    ):
      raise ValueError(
        "depth-zero proof_step must be "
        "root_entry.step"
      )

    if (
      self.proof_step
      is self.root_entry.step
      and self.shortest_depth != 0
    ):
      raise ValueError(
        "root_entry.step must have depth zero"
      )


@dataclass(frozen=True)
class RepositoryProofScopeResult:
  repository: ProofRepository
  nodes: tuple[
    RepositoryProofScopeNode,
    ...,
  ]

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.repository,
      ProofRepository,
    ):
      raise TypeError(
        "repository must be a ProofRepository"
      )

    if not isinstance(
      self.nodes,
      tuple,
    ):
      raise TypeError(
        "nodes must be a tuple"
      )

    registered_entries = (
      self.repository.entries()
    )

    node_keys = set()

    for node in self.nodes:
      if not isinstance(
        node,
        RepositoryProofScopeNode,
      ):
        raise TypeError(
          "nodes must contain only "
          "RepositoryProofScopeNode objects"
        )

      if not any(
        node.root_entry is entry
        for entry in registered_entries
      ):
        raise ValueError(
          "node root_entry must be registered "
          "in repository"
        )

      node_key = (
        id(
          node.root_entry
        ),
        id(
          node.proof_step
        ),
      )

      if node_key in node_keys:
        raise ValueError(
          "nodes must not repeat the same "
          "root_entry/proof_step identity pair"
        )

      node_keys.add(
        node_key
      )


def build_repository_entry_proof_scope(
  entry: ProofRepositoryEntry,
) -> tuple[
  RepositoryProofScopeNode,
  ...,
]:
  if not isinstance(
    entry,
    ProofRepositoryEntry,
  ):
    raise TypeError(
      "entry must be a ProofRepositoryEntry"
    )

  queue: list[
    tuple[
      ProofStep,
      int,
    ]
  ] = [
    (
      entry.step,
      0,
    ),
  ]

  seen_step_ids: set[int] = set()
  nodes = []
  queue_index = 0

  while queue_index < len(
    queue
  ):
    (
      proof_step,
      depth,
    ) = queue[
      queue_index
    ]

    queue_index += 1

    proof_step_id = id(
      proof_step
    )

    if proof_step_id in seen_step_ids:
      continue

    seen_step_ids.add(
      proof_step_id
    )

    nodes.append(
      RepositoryProofScopeNode(
        root_entry=entry,
        proof_step=proof_step,
        shortest_depth=depth,
      )
    )

    for premise in proof_step.premises:
      if isinstance(
        premise,
        ProofStep,
      ):
        queue.append(
          (
            premise,
            depth + 1,
          )
        )

  return tuple(
    nodes
  )


def build_repository_proof_scope(
  repository: ProofRepository,
) -> RepositoryProofScopeResult:
  if not isinstance(
    repository,
    ProofRepository,
  ):
    raise TypeError(
      "repository must be a ProofRepository"
    )

  nodes = []

  for entry in repository.entries():
    nodes.extend(
      build_repository_entry_proof_scope(
        entry
      )
    )

  return RepositoryProofScopeResult(
    repository=repository,
    nodes=tuple(
      nodes
    ),
  )

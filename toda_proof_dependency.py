from dataclasses import dataclass
from enum import Enum

from homotopy_groups import (
  DirectSumGroup,
  FiniteCyclicGroup,
  FreeCyclicGroup,
  TodaEHPExactnessWindow,
  TodaPrimaryGroup,
  TodaPrimaryGroupZeroStatement,
)
from proof import (
  LiteratureStatement,
  ProofStep,
  Relation,
  RelationType,
)
from toda_group_result import TodaGroupResult
from toda_rules import (
  TodaDeltaImageUpToSignStatement,
  TodaDeltaInjectiveStatement,
  TodaHopfInvariantZeroStatement,
  TodaNuFamilyDefinitionStatement,
  TodaProp42ExactnessStatement,
  TodaSuspensionSurjectiveStatement,
)


class TodaProofDependencyRole(Enum):
  EHP_EXACTNESS = "ehp_exactness"
  EHP_WINDOW = "ehp_window"
  GROUP_STRUCTURE = "group_structure"
  RELATION = "relation"
  ORDER = "order"
  MAP_PROPERTY = "map_property"
  DEFINITION = "definition"
  LITERATURE = "literature"
  OTHER = "other"


def classify_toda_proof_step_role(
  proof_step: ProofStep,
) -> TodaProofDependencyRole:
  if not isinstance(
    proof_step,
    ProofStep,
  ):
    raise TypeError(
      "proof_step must be a ProofStep"
    )

  conclusion = (
    proof_step.conclusion
  )

  if isinstance(
    conclusion,
    TodaProp42ExactnessStatement,
  ):
    return (
      TodaProofDependencyRole
      .EHP_EXACTNESS
    )

  if isinstance(
    conclusion,
    TodaEHPExactnessWindow,
  ):
    return (
      TodaProofDependencyRole
      .EHP_WINDOW
    )

  if isinstance(
    conclusion,
    TodaPrimaryGroupZeroStatement,
  ):
    return (
      TodaProofDependencyRole
      .GROUP_STRUCTURE
    )

  if isinstance(
    conclusion,
    Relation,
  ):
    if (
      conclusion.relation_type
      == RelationType.ORDER
    ):
      return (
        TodaProofDependencyRole
        .ORDER
      )

    if (
      conclusion.relation_type
      == RelationType.EQUALITY
      and isinstance(
        conclusion.lhs,
        TodaPrimaryGroup,
      )
      and isinstance(
        conclusion.rhs,
        (
          FreeCyclicGroup,
          FiniteCyclicGroup,
          DirectSumGroup,
        ),
      )
    ):
      return (
        TodaProofDependencyRole
        .GROUP_STRUCTURE
      )

    return (
      TodaProofDependencyRole
      .RELATION
    )

  if isinstance(
    conclusion,
    (
      TodaDeltaImageUpToSignStatement,
      TodaDeltaInjectiveStatement,
      TodaHopfInvariantZeroStatement,
      TodaSuspensionSurjectiveStatement,
    ),
  ):
    return (
      TodaProofDependencyRole
      .MAP_PROPERTY
    )

  if isinstance(
    conclusion,
    TodaNuFamilyDefinitionStatement,
  ):
    return (
      TodaProofDependencyRole
      .DEFINITION
    )

  if isinstance(
    conclusion,
    LiteratureStatement,
  ):
    return (
      TodaProofDependencyRole
      .LITERATURE
    )

  return (
    TodaProofDependencyRole
    .OTHER
  )


@dataclass(frozen=True)
class TodaProofDependency:
  proof_step: ProofStep
  depth: int
  role: TodaProofDependencyRole = (
    TodaProofDependencyRole.OTHER
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

    if (
      isinstance(
        self.depth,
        bool,
      )
      or not isinstance(
        self.depth,
        int,
      )
    ):
      raise TypeError(
        "depth must be an int"
      )

    if self.depth <= 0:
      raise ValueError(
        "depth must be positive"
      )

    if not isinstance(
      self.role,
      TodaProofDependencyRole,
    ):
      raise TypeError(
        "role must be a "
        "TodaProofDependencyRole"
      )

  @property
  def is_direct(
    self,
  ) -> bool:
    return self.depth == 1


@dataclass(frozen=True)
class TodaProofDependencyResult:
  root_step: ProofStep
  dependencies: tuple[
    TodaProofDependency,
    ...,
  ]

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.root_step,
      ProofStep,
    ):
      raise TypeError(
        "root_step must be a ProofStep"
      )

    if not isinstance(
      self.dependencies,
      tuple,
    ):
      raise TypeError(
        "dependencies must be a tuple"
      )

    seen_step_ids: set[int] = set()

    for dependency in (
      self.dependencies
    ):
      if not isinstance(
        dependency,
        TodaProofDependency,
      ):
        raise TypeError(
          "dependencies must contain only "
          "TodaProofDependency objects"
        )

      if (
        dependency.proof_step
        is self.root_step
      ):
        raise ValueError(
          "root_step must not appear "
          "in dependencies"
        )

      step_id = id(
        dependency.proof_step
      )

      if step_id in seen_step_ids:
        raise ValueError(
          "dependencies must not contain "
          "the same ProofStep more than once"
        )

      seen_step_ids.add(
        step_id
      )


@dataclass(frozen=True)
class TodaProofNode:
  proof_step: ProofStep
  shortest_depth: int
  role: TodaProofDependencyRole = (
    TodaProofDependencyRole.OTHER
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

    if not isinstance(
      self.role,
      TodaProofDependencyRole,
    ):
      raise TypeError(
        "role must be a "
        "TodaProofDependencyRole"
      )


@dataclass(frozen=True)
class TodaProofEdge:
  parent_step: ProofStep
  premise_step: ProofStep
  premise_index: int

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.parent_step,
      ProofStep,
    ):
      raise TypeError(
        "parent_step must be a ProofStep"
      )

    if not isinstance(
      self.premise_step,
      ProofStep,
    ):
      raise TypeError(
        "premise_step must be a ProofStep"
      )

    if (
      isinstance(
        self.premise_index,
        bool,
      )
      or not isinstance(
        self.premise_index,
        int,
      )
    ):
      raise TypeError(
        "premise_index must be an int"
      )

    if self.premise_index < 0:
      raise ValueError(
        "premise_index must be non-negative"
      )

    if self.premise_index >= len(
      self.parent_step.premises
    ):
      raise ValueError(
        "premise_index must refer to "
        "parent_step.premises"
      )

    if (
      self.parent_step.premises[
        self.premise_index
      ]
      is not self.premise_step
    ):
      raise ValueError(
        "premise_step must be the "
        "ProofStep at premise_index"
      )


@dataclass(frozen=True)
class TodaRecursiveProofProvenanceResult:
  root_step: ProofStep
  nodes: tuple[
    TodaProofNode,
    ...,
  ]
  edges: tuple[
    TodaProofEdge,
    ...,
  ]

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.root_step,
      ProofStep,
    ):
      raise TypeError(
        "root_step must be a ProofStep"
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

    node_step_ids: set[int] = set()
    root_node_count = 0

    for node in self.nodes:
      if not isinstance(
        node,
        TodaProofNode,
      ):
        raise TypeError(
          "nodes must contain only "
          "TodaProofNode objects"
        )

      step_id = id(
        node.proof_step
      )

      if step_id in node_step_ids:
        raise ValueError(
          "nodes must not contain "
          "the same ProofStep more than once"
        )

      node_step_ids.add(
        step_id
      )

      if node.proof_step is self.root_step:
        root_node_count += 1

        if node.shortest_depth != 0:
          raise ValueError(
            "root node shortest_depth "
            "must be zero"
          )
      elif node.shortest_depth <= 0:
        raise ValueError(
          "non-root node shortest_depth "
          "must be positive"
        )

    if root_node_count != 1:
      raise ValueError(
        "nodes must contain root_step "
        "exactly once"
      )

    seen_edges: set[
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
        id(edge.parent_step)
        not in node_step_ids
      ):
        raise ValueError(
          "edge parent_step must appear "
          "in nodes"
        )

      if (
        id(edge.premise_step)
        not in node_step_ids
      ):
        raise ValueError(
          "edge premise_step must appear "
          "in nodes"
        )

      edge_key = (
        id(edge.parent_step),
        id(edge.premise_step),
        edge.premise_index,
      )

      if edge_key in seen_edges:
        raise ValueError(
          "edges must not contain "
          "duplicate proof edges"
        )

      seen_edges.add(
        edge_key
      )

def extract_toda_proof_dependencies(
  group_result: TodaGroupResult,
) -> TodaProofDependencyResult:
  if not isinstance(
    group_result,
    TodaGroupResult,
  ):
    raise TypeError(
      "group_result must be "
      "a TodaGroupResult"
    )

  root_step = (
    group_result.proof_step
  )

  queue: list[
    tuple[
      ProofStep,
      int,
    ]
  ] = []

  for premise in (
    root_step.premises
  ):
    if isinstance(
      premise,
      ProofStep,
    ):
      queue.append(
        (
          premise,
          1,
        )
      )

  seen_step_ids: set[int] = {
    id(
      root_step
    ),
  }

  dependencies: list[
    TodaProofDependency
  ] = []

  queue_index = 0

  while queue_index < len(
    queue
  ):
    (
      step,
      depth,
    ) = queue[
      queue_index
    ]

    queue_index += 1

    step_id = id(
      step
    )

    if step_id in seen_step_ids:
      continue

    seen_step_ids.add(
      step_id
    )

    dependencies.append(
      TodaProofDependency(
        proof_step=step,
        depth=depth,
        role=(
          classify_toda_proof_step_role(
            step
          )
        ),
      )
    )

    for premise in (
      step.premises
    ):
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

  return TodaProofDependencyResult(
    root_step=root_step,
    dependencies=tuple(
      dependencies
    ),
  )


def extract_toda_recursive_proof_provenance(
  group_result: TodaGroupResult,
) -> TodaRecursiveProofProvenanceResult:
  if not isinstance(
    group_result,
    TodaGroupResult,
  ):
    raise TypeError(
      "group_result must be "
      "a TodaGroupResult"
    )

  root_step = (
    group_result.proof_step
  )

  queue: list[
    tuple[
      ProofStep,
      int,
    ]
  ] = [
    (
      root_step,
      0,
    ),
  ]

  seen_step_ids: set[int] = set()

  nodes: list[
    TodaProofNode
  ] = []

  edges: list[
    TodaProofEdge
  ] = []

  queue_index = 0

  while queue_index < len(
    queue
  ):
    (
      step,
      depth,
    ) = queue[
      queue_index
    ]

    queue_index += 1

    step_id = id(
      step
    )

    if step_id in seen_step_ids:
      continue

    seen_step_ids.add(
      step_id
    )

    nodes.append(
      TodaProofNode(
        proof_step=step,
        shortest_depth=depth,
        role=(
          classify_toda_proof_step_role(
            step
          )
        ),
      )
    )

    for (
      premise_index,
      premise,
    ) in enumerate(
      step.premises
    ):
      if not isinstance(
        premise,
        ProofStep,
      ):
        continue

      edges.append(
        TodaProofEdge(
          parent_step=step,
          premise_step=premise,
          premise_index=(
            premise_index
          ),
        )
      )

      queue.append(
        (
          premise,
          depth + 1,
        )
      )

  return (
    TodaRecursiveProofProvenanceResult(
      root_step=root_step,
      nodes=tuple(
        nodes
      ),
      edges=tuple(
        edges
      ),
    )
  )

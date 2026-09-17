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

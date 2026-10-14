from dataclasses import dataclass

from proof import ProofStep
from repository_operation_query_lookup import (
  RepositoryOperationQueryMatch,
)
from repository_operation_query_presentation import (
  RepositoryOperationQueryPresentation,
  RepositoryOperationQueryPresentationItem,
)


@dataclass(frozen=True)
class RepositoryOperationQueryProofReplayStep:
  depth: int
  proof_step: ProofStep

  def __post_init__(
    self,
  ) -> None:
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

    if self.depth < 0:
      raise ValueError(
        "depth must be nonnegative"
      )

    if not isinstance(
      self.proof_step,
      ProofStep,
    ):
      raise TypeError(
        "proof_step must be a ProofStep"
      )


@dataclass(frozen=True)
class RepositoryOperationQueryProofReplayResult:
  source_presentation: RepositoryOperationQueryPresentation
  source_item: RepositoryOperationQueryPresentationItem
  source_match: RepositoryOperationQueryMatch
  root_step: ProofStep
  steps: tuple[
    RepositoryOperationQueryProofReplayStep,
    ...,
  ]
  max_depth: int

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.source_presentation,
      RepositoryOperationQueryPresentation,
    ):
      raise TypeError(
        "source_presentation must be a "
        "RepositoryOperationQueryPresentation"
      )

    if not isinstance(
      self.source_item,
      RepositoryOperationQueryPresentationItem,
    ):
      raise TypeError(
        "source_item must be a "
        "RepositoryOperationQueryPresentationItem"
      )

    if not any(
      self.source_item is item
      for item in self.source_presentation.items
    ):
      raise ValueError(
        "source_item must belong to source_presentation"
      )

    if not isinstance(
      self.source_match,
      RepositoryOperationQueryMatch,
    ):
      raise TypeError(
        "source_match must be a "
        "RepositoryOperationQueryMatch"
      )

    if not any(
      self.source_match is match
      for match in self.source_item.matches
    ):
      raise ValueError(
        "source_match must belong to source_item"
      )

    if not isinstance(
      self.root_step,
      ProofStep,
    ):
      raise TypeError(
        "root_step must be a ProofStep"
      )

    if (
      self.root_step
      is not self.source_match.scope_node.proof_step
    ):
      raise ValueError(
        "root_step must preserve source_match "
        "proof-step identity"
      )

    _validate_max_depth(
      self.max_depth
    )

    if not isinstance(
      self.steps,
      tuple,
    ):
      raise TypeError(
        "steps must be a tuple"
      )

    if not self.steps:
      raise ValueError(
        "steps must not be empty"
      )

    for step in self.steps:
      if not isinstance(
        step,
        RepositoryOperationQueryProofReplayStep,
      ):
        raise TypeError(
          "steps must contain only "
          "RepositoryOperationQueryProofReplayStep values"
        )

      if step.depth > self.max_depth:
        raise ValueError(
          "replay step depth must not exceed max_depth"
        )

    if (
      self.steps[
        0
      ].depth
      != 0
      or self.steps[
        0
      ].proof_step
      is not self.root_step
    ):
      raise ValueError(
        "steps must begin with root_step at depth zero"
      )

    proof_step_ids = tuple(
      id(
        step.proof_step
      )
      for step in self.steps
    )

    if len(
      set(
        proof_step_ids
      )
    ) != len(
      proof_step_ids
    ):
      raise ValueError(
        "steps must not repeat ProofStep identity"
      )


def _validate_max_depth(
  max_depth,
) -> None:
  if (
    isinstance(
      max_depth,
      bool,
    )
    or not isinstance(
      max_depth,
      int,
    )
  ):
    raise TypeError(
      "max_depth must be an int"
    )

  if max_depth < 0:
    raise ValueError(
      "max_depth must be nonnegative"
    )


def _collect_operation_query_proof_replay_steps(
  root_step: ProofStep,
  max_depth: int,
) -> tuple[
  RepositoryOperationQueryProofReplayStep,
  ...,
]:
  if not isinstance(
    root_step,
    ProofStep,
  ):
    raise TypeError(
      "root_step must be a ProofStep"
    )

  _validate_max_depth(
    max_depth
  )

  collected = []
  seen_step_ids = set()

  def visit(
    step: ProofStep,
    depth: int,
  ) -> None:
    step_id = id(
      step
    )

    if step_id in seen_step_ids:
      return

    seen_step_ids.add(
      step_id
    )

    collected.append(
      RepositoryOperationQueryProofReplayStep(
        depth=depth,
        proof_step=step,
      )
    )

    if depth >= max_depth:
      return

    for premise in step.premises:
      if not isinstance(
        premise,
        ProofStep,
      ):
        continue

      visit(
        premise,
        depth + 1,
      )

  visit(
    root_step,
    0,
  )

  return tuple(
    collected
  )


def build_repository_operation_query_proof_replay(
  presentation: RepositoryOperationQueryPresentation,
  fact_number: int | None = None,
  max_depth: int = 1,
) -> RepositoryOperationQueryProofReplayResult:
  if not isinstance(
    presentation,
    RepositoryOperationQueryPresentation,
  ):
    raise TypeError(
      "presentation must be a "
      "RepositoryOperationQueryPresentation"
    )

  _validate_max_depth(
    max_depth
  )

  if not presentation.items:
    raise ValueError(
      "operation query proof replay requires "
      "at least one presentation item"
    )

  if fact_number is None:
    if len(
      presentation.items
    ) != 1:
      raise ValueError(
        "fact_number is required when multiple "
        "repository facts are available"
      )

    item = presentation.items[
      0
    ]
  else:
    if (
      isinstance(
        fact_number,
        bool,
      )
      or not isinstance(
        fact_number,
        int,
      )
    ):
      raise TypeError(
        "fact_number must be an int or None"
      )

    if fact_number <= 0:
      raise ValueError(
        "fact_number must be positive"
      )

    if fact_number > len(
      presentation.items
    ):
      raise ValueError(
        "fact_number exceeds repository fact count"
      )

    item = presentation.items[
      fact_number - 1
    ]

  source_match = (
    item.primary_match
  )

  root_step = (
    source_match
    .scope_node
    .proof_step
  )

  steps = (
    _collect_operation_query_proof_replay_steps(
      root_step,
      max_depth,
    )
  )

  return RepositoryOperationQueryProofReplayResult(
    source_presentation=presentation,
    source_item=item,
    source_match=source_match,
    root_step=root_step,
    steps=steps,
    max_depth=max_depth,
  )

from dataclasses import dataclass

from proof import ProofStep
from proof_repository import ProofRepositoryEntry
from toda_group_result import TodaGroupResult
from toda_proof_dependency import (
  TodaProofDependencyRole,
  extract_toda_recursive_proof_provenance,
)


@dataclass(frozen=True)
class TodaGroupResultProofReplayStep:
  depth: int
  proof_step: ProofStep
  role: TodaProofDependencyRole

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

    if not isinstance(
      self.role,
      TodaProofDependencyRole,
    ):
      raise TypeError(
        "role must be a TodaProofDependencyRole"
      )


@dataclass(frozen=True)
class TodaGroupResultProofReplayResult:
  group_result: TodaGroupResult
  source_entry: ProofRepositoryEntry
  root_step: ProofStep
  steps: tuple[
    TodaGroupResultProofReplayStep,
    ...,
  ]
  max_depth: int

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.group_result,
      TodaGroupResult,
    ):
      raise TypeError(
        "group_result must be a TodaGroupResult"
      )

    if not isinstance(
      self.source_entry,
      ProofRepositoryEntry,
    ):
      raise TypeError(
        "source_entry must be a ProofRepositoryEntry"
      )

    if (
      self.source_entry
      is not self.group_result.source_entry
    ):
      raise ValueError(
        "source_entry must preserve group_result source identity"
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
      is not self.group_result.proof_step
    ):
      raise ValueError(
        "root_step must preserve group_result proof-step identity"
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
        TodaGroupResultProofReplayStep,
      ):
        raise TypeError(
          "steps must contain only "
          "TodaGroupResultProofReplayStep objects"
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


def build_toda_group_result_proof_replay(
  group_result: TodaGroupResult,
  max_depth: int = 1,
) -> TodaGroupResultProofReplayResult:
  if not isinstance(
    group_result,
    TodaGroupResult,
  ):
    raise TypeError(
      "group_result must be a TodaGroupResult"
    )

  _validate_max_depth(
    max_depth
  )

  provenance = (
    extract_toda_recursive_proof_provenance(
      group_result
    )
  )

  steps = tuple(
    TodaGroupResultProofReplayStep(
      depth=node.shortest_depth,
      proof_step=node.proof_step,
      role=node.role,
    )
    for node in provenance.nodes
    if node.shortest_depth <= max_depth
  )

  return TodaGroupResultProofReplayResult(
    group_result=group_result,
    source_entry=group_result.source_entry,
    root_step=group_result.proof_step,
    steps=steps,
    max_depth=max_depth,
  )

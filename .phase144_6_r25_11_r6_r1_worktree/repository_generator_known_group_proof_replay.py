from dataclasses import dataclass

from expression import (
  GeneratorSymbol,
)
from generator_input import (
  resolve_generator_input,
)
from proof import (
  ProofStep,
)
from repository_generator_known_group_identity_lookup import (
  find_standard_repository_generator_known_group_identity_nodes,
)
from repository_proof_scope import (
  RepositoryProofScopeNode,
)


@dataclass(frozen=True)
class RepositoryGeneratorKnownGroupProofReplayStep:
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
class RepositoryGeneratorKnownGroupProofReplayResult:
  generator: GeneratorSymbol
  source_node: RepositoryProofScopeNode
  root_step: ProofStep
  steps: tuple[
    RepositoryGeneratorKnownGroupProofReplayStep,
    ...,
  ]
  max_depth: int

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.generator,
      GeneratorSymbol,
    ):
      raise TypeError(
        "generator must be a GeneratorSymbol"
      )

    if not isinstance(
      self.source_node,
      RepositoryProofScopeNode,
    ):
      raise TypeError(
        "source_node must be a RepositoryProofScopeNode"
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
      is not self.source_node.proof_step
    ):
      raise ValueError(
        "root_step must preserve source_node proof-step identity"
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
        RepositoryGeneratorKnownGroupProofReplayStep,
      ):
        raise TypeError(
          "steps must contain only "
          "RepositoryGeneratorKnownGroupProofReplayStep objects"
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


def _collect_known_group_proof_replay_steps(
  root_step: ProofStep,
  max_depth: int,
) -> tuple[
  RepositoryGeneratorKnownGroupProofReplayStep,
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
      RepositoryGeneratorKnownGroupProofReplayStep(
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


def build_standard_repository_generator_known_group_proof_replay_input(
  generator_input: str,
  max_depth: int = 1,
) -> RepositoryGeneratorKnownGroupProofReplayResult:
  if not isinstance(
    generator_input,
    str,
  ):
    raise TypeError(
      "generator_input must be a str"
    )

  _validate_max_depth(
    max_depth
  )

  generator = resolve_generator_input(
    generator_input
  )

  nodes = (
    find_standard_repository_generator_known_group_identity_nodes(
      generator
    )
  )

  if len(
    nodes
  ) != 1:
    raise ValueError(
      "known-group proof replay requires exactly one "
      "known-group identity"
    )

  source_node = nodes[
    0
  ]

  root_step = (
    source_node.proof_step
  )

  steps = (
    _collect_known_group_proof_replay_steps(
      root_step,
      max_depth,
    )
  )

  return RepositoryGeneratorKnownGroupProofReplayResult(
    generator=generator,
    source_node=source_node,
    root_step=root_step,
    steps=steps,
    max_depth=max_depth,
  )

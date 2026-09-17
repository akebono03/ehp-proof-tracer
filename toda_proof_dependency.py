from dataclasses import dataclass

from proof import ProofStep


@dataclass(frozen=True)
class TodaProofDependency:
  proof_step: ProofStep
  depth: int

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

from dataclasses import dataclass

from proof import ProofStep
from toda_ehp_result import (
  TodaEHPExactnessWindowResult,
  TodaEHPSequenceResult,
)
from toda_group_result import TodaGroupResult
from toda_rules import (
  TodaProp42ExactnessStatement,
)


@dataclass(frozen=True)
class TodaEHPExactnessUseResult:
  window_result: TodaEHPExactnessWindowResult
  exactness_step: ProofStep
  consumer_steps: tuple[
    ProofStep,
    ...,
  ]

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.window_result,
      TodaEHPExactnessWindowResult,
    ):
      raise TypeError(
        "window_result must be "
        "a TodaEHPExactnessWindowResult"
      )

    if not isinstance(
      self.exactness_step,
      ProofStep,
    ):
      raise TypeError(
        "exactness_step must be a ProofStep"
      )

    conclusion = (
      self.exactness_step.conclusion
    )

    if not isinstance(
      conclusion,
      TodaProp42ExactnessStatement,
    ):
      raise ValueError(
        "exactness_step must conclude "
        "TodaProp42ExactnessStatement"
      )

    if (
      conclusion.window
      is not self.window_result.window
    ):
      raise ValueError(
        "exactness_step window must be "
        "window_result.window"
      )

    if not isinstance(
      self.consumer_steps,
      tuple,
    ):
      raise TypeError(
        "consumer_steps must be a tuple"
      )

    for consumer_step in (
      self.consumer_steps
    ):
      if not isinstance(
        consumer_step,
        ProofStep,
      ):
        raise TypeError(
          "consumer_steps must contain "
          "only ProofStep objects"
        )

      if not any(
        premise
        is self.exactness_step
        for premise in (
          consumer_step.premises
        )
      ):
        raise ValueError(
          "each consumer step must use "
          "exactness_step directly"
        )


@dataclass(frozen=True)
class TodaEHPExactnessUseProvenanceResult:
  ehp_result: TodaEHPSequenceResult
  uses: tuple[
    TodaEHPExactnessUseResult,
    ...,
  ]

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.ehp_result,
      TodaEHPSequenceResult,
    ):
      raise TypeError(
        "ehp_result must be "
        "a TodaEHPSequenceResult"
      )

    if not isinstance(
      self.uses,
      tuple,
    ):
      raise TypeError(
        "uses must be a tuple"
      )

    for use in self.uses:
      if not isinstance(
        use,
        TodaEHPExactnessUseResult,
      ):
        raise TypeError(
          "uses must contain only "
          "TodaEHPExactnessUseResult objects"
        )

    if tuple(
      use.window_result.window
      for use in self.uses
    ) != tuple(
      window_result.window
      for window_result in (
        self.ehp_result.windows
      )
    ):
      raise ValueError(
        "uses must match ehp_result windows "
        "in order"
      )


def _collect_reachable_proof_steps(
  proof_step: ProofStep,
) -> tuple[
  ProofStep,
  ...,
]:
  if not isinstance(
    proof_step,
    ProofStep,
  ):
    raise TypeError(
      "proof_step must be a ProofStep"
    )

  steps: list[
    ProofStep
  ] = []

  visited_ids: set[int] = set()

  def visit(
    step: ProofStep,
  ) -> None:
    step_id = id(
      step
    )

    if step_id in visited_ids:
      return

    visited_ids.add(
      step_id
    )

    steps.append(
      step
    )

    for premise in (
      step.premises
    ):
      if isinstance(
        premise,
        ProofStep,
      ):
        visit(
          premise
        )

  visit(
    proof_step
  )

  return tuple(
    steps
  )


def extract_toda_ehp_exactness_use_provenance(
  group_result: TodaGroupResult,
  ehp_result: TodaEHPSequenceResult,
) -> TodaEHPExactnessUseProvenanceResult:
  if not isinstance(
    group_result,
    TodaGroupResult,
  ):
    raise TypeError(
      "group_result must be "
      "a TodaGroupResult"
    )

  if not isinstance(
    ehp_result,
    TodaEHPSequenceResult,
  ):
    raise TypeError(
      "ehp_result must be "
      "a TodaEHPSequenceResult"
    )

  if (
    group_result.target
    != ehp_result.target
  ):
    raise ValueError(
      "group_result and ehp_result "
      "must have the same target"
    )

  reachable_steps = (
    _collect_reachable_proof_steps(
      group_result.proof_step
    )
  )

  uses = []

  for window_result in (
    ehp_result.windows
  ):
    matching_steps = tuple(
      step
      for step in reachable_steps
      if (
        isinstance(
          step.conclusion,
          TodaProp42ExactnessStatement,
        )
        and (
          step.conclusion.window
          is window_result.window
        )
      )
    )

    if len(
      matching_steps
    ) != 1:
      raise ValueError(
        "each EHP window must have "
        "exactly one reachable "
        "exactness proof step"
      )

    exactness_step = (
      matching_steps[
        0
      ]
    )

    consumer_steps = tuple(
      step
      for step in reachable_steps
      if any(
        premise
        is exactness_step
        for premise in (
          step.premises
        )
      )
    )

    uses.append(
      TodaEHPExactnessUseResult(
        window_result=window_result,
        exactness_step=exactness_step,
        consumer_steps=consumer_steps,
      )
    )

  return (
    TodaEHPExactnessUseProvenanceResult(
      ehp_result=ehp_result,
      uses=tuple(
        uses
      ),
    )
  )

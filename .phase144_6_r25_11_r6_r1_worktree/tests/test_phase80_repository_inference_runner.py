from dataclasses import dataclass

import pytest

from proof import (
  InferenceRule,
  InferenceTerminationReason,
  PremisePattern,
  ProofRule,
  ProofStep,
)
from proof_repository import (
  ProofRepository,
  ProofRepositoryEntry,
)
from repository_inference import (
  RepositoryInferenceResult,
  derive_goal_from_repository,
)


@dataclass(frozen=True)
class Phase80RunnerSourceStatement:
  value: str


@dataclass(frozen=True)
class Phase80RunnerGoalStatement:
  value: str


def make_source_step(
  value,
):
  return ProofStep(
    conclusion=Phase80RunnerSourceStatement(
      value=value,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )


def make_rule():
  return InferenceRule(
    name="phase80_repository_runner",
    premise_patterns=(
      PremisePattern(
        statement_type=(
          Phase80RunnerSourceStatement
        ),
      ),
    ),
    conclusion_builder=(
      lambda premises: (
        Phase80RunnerGoalStatement(
          value=(
            premises[0]
            .conclusion
            .value
          ),
        )
      )
    ),
  )


def test_phase80_4_derives_goal_from_repository():
  repository = ProofRepository()

  source_step = make_source_step(
    "A"
  )

  repository.register(
    ProofRepositoryEntry(
      key="phase80.source",
      step=source_step,
    )
  )

  goal = Phase80RunnerGoalStatement(
    value="A",
  )

  result = derive_goal_from_repository(
    repository,
    (make_rule(),),
    goal,
  )

  assert isinstance(
    result,
    RepositoryInferenceResult,
  )
  assert result.goal_step is not None
  assert result.goal_step.conclusion == goal
  assert (
    result.goal_step.rule
    == ProofRule.INFERENCE
  )


def test_phase80_4_goal_step_is_exact_step_from_inference_result():
  repository = ProofRepository()

  source_step = make_source_step(
    "A"
  )

  repository.register(
    ProofRepositoryEntry(
      key="phase80.source",
      step=source_step,
    )
  )

  result = derive_goal_from_repository(
    repository,
    (make_rule(),),
    Phase80RunnerGoalStatement(
      value="A",
    ),
  )

  assert result.goal_step is not None
  assert any(
    step is result.goal_step
    for step in (
      result
      .inference_result
      .steps
    )
  )


def test_phase80_4_preserves_repository_step_identity_in_inference_result():
  repository = ProofRepository()

  source_step = make_source_step(
    "A"
  )

  repository.register(
    ProofRepositoryEntry(
      key="phase80.source",
      step=source_step,
    )
  )

  result = derive_goal_from_repository(
    repository,
    (make_rule(),),
    Phase80RunnerGoalStatement(
      value="A",
    ),
  )

  assert (
    result
    .inference_result
    .steps[0]
    is source_step
  )


def test_phase80_4_missing_goal_returns_none_after_fixed_point():
  repository = ProofRepository()

  repository.register(
    ProofRepositoryEntry(
      key="phase80.source",
      step=make_source_step(
        "A"
      ),
    )
  )

  result = derive_goal_from_repository(
    repository,
    (make_rule(),),
    Phase80RunnerGoalStatement(
      value="missing",
    ),
  )

  assert result.goal_step is None
  assert (
    result
    .inference_result
    .termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )


def test_phase80_4_existing_repository_goal_is_detected_without_new_inference():
  repository = ProofRepository()

  existing_goal_step = ProofStep(
    conclusion=Phase80RunnerGoalStatement(
      value="A",
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  repository.register(
    ProofRepositoryEntry(
      key="phase80.goal",
      step=existing_goal_step,
    )
  )

  result = derive_goal_from_repository(
    repository,
    (),
    Phase80RunnerGoalStatement(
      value="A",
    ),
  )

  assert (
    result.goal_step
    is existing_goal_step
  )
  assert (
    result
    .inference_result
    .termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )


def test_phase80_4_max_rounds_is_forwarded_to_inference_runner():
  repository = ProofRepository()

  repository.register(
    ProofRepositoryEntry(
      key="phase80.source",
      step=make_source_step(
        "A"
      ),
    )
  )

  result = derive_goal_from_repository(
    repository,
    (make_rule(),),
    Phase80RunnerGoalStatement(
      value="A",
    ),
    max_rounds=0,
  )

  assert result.goal_step is None
  assert (
    result
    .inference_result
    .termination_reason
    == InferenceTerminationReason.MAX_ROUNDS
  )


def test_phase80_4_does_not_register_derived_goal_back_into_repository():
  repository = ProofRepository()

  source_entry = ProofRepositoryEntry(
    key="phase80.source",
    step=make_source_step(
      "A"
    ),
  )

  repository.register(
    source_entry
  )

  before_entries = (
    repository.entries()
  )

  result = derive_goal_from_repository(
    repository,
    (make_rule(),),
    Phase80RunnerGoalStatement(
      value="A",
    ),
  )

  assert result.goal_step is not None
  assert (
    repository.entries()
    == before_entries
  )


def test_phase80_4_rejects_non_repository_via_existing_bridge_validation():
  with pytest.raises(
    TypeError,
    match=(
      "repository must be "
      "a ProofRepository"
    ),
  ):
    derive_goal_from_repository(
      "not-a-repository",
      (),
      Phase80RunnerGoalStatement(
        value="A",
      ),
    )


def test_phase80_4_rejects_invalid_inference_rules_via_existing_runner_validation():
  repository = ProofRepository()

  with pytest.raises(
    TypeError,
    match=(
      "inference_rules must be "
      "an InferenceRule or a "
      "tuple/list of InferenceRule"
    ),
  ):
    derive_goal_from_repository(
      repository,
      "not-rules",
      Phase80RunnerGoalStatement(
        value="A",
      ),
    )

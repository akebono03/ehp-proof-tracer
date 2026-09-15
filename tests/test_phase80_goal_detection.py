from dataclasses import dataclass

import pytest

from proof import (
  InferenceRule,
  PremisePattern,
  ProofRule,
  ProofStep,
  find_goal_step,
  run_inference_until_stable_with_history,
)


@dataclass(frozen=True)
class Phase80GoalStatement:
  value: str


@dataclass(frozen=True)
class Phase80GoalDerivedStatement:
  value: str


def make_step(
  value,
  rule=ProofRule.GIVEN,
):
  return ProofStep(
    conclusion=Phase80GoalStatement(
      value=value,
    ),
    premises=(),
    rule=rule,
  )


def test_phase80_3_single_step_match_returns_exact_step():
  step = make_step(
    "A"
  )

  found = find_goal_step(
    step,
    Phase80GoalStatement(
      value="A",
    ),
  )

  assert found is step


def test_phase80_3_tuple_match_returns_exact_existing_step():
  first_step = make_step(
    "A"
  )
  second_step = make_step(
    "B"
  )

  found = find_goal_step(
    (
      first_step,
      second_step,
    ),
    Phase80GoalStatement(
      value="B",
    ),
  )

  assert found is second_step


def test_phase80_3_list_input_is_supported():
  first_step = make_step(
    "A"
  )
  second_step = make_step(
    "B"
  )

  found = find_goal_step(
    [
      first_step,
      second_step,
    ],
    Phase80GoalStatement(
      value="A",
    ),
  )

  assert found is first_step


def test_phase80_3_missing_goal_returns_none():
  step = make_step(
    "A"
  )

  assert (
    find_goal_step(
      (step,),
      Phase80GoalStatement(
        value="missing",
      ),
    )
    is None
  )


def test_phase80_3_goal_uses_structural_equality_not_object_identity():
  conclusion = Phase80GoalStatement(
    value="A",
  )
  structurally_equal_goal = (
    Phase80GoalStatement(
      value="A",
    )
  )
  step = ProofStep(
    conclusion=conclusion,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert (
    structurally_equal_goal
    is not conclusion
  )

  assert (
    find_goal_step(
      (step,),
      structurally_equal_goal,
    )
    is step
  )


def test_phase80_3_same_conclusion_multiple_steps_returns_first_match():
  shared_conclusion = (
    Phase80GoalStatement(
      value="A",
    )
  )

  first_step = ProofStep(
    conclusion=shared_conclusion,
    premises=(),
    rule=ProofRule.GIVEN,
  )
  second_step = ProofStep(
    conclusion=shared_conclusion,
    premises=(
      first_step,
    ),
    rule=ProofRule.INFERENCE,
  )

  found = find_goal_step(
    (
      first_step,
      second_step,
    ),
    Phase80GoalStatement(
      value="A",
    ),
  )

  assert found is first_step


def test_phase80_3_fixed_point_result_can_find_newly_derived_goal():
  source_step = make_step(
    "source"
  )

  rule = InferenceRule(
    name="phase80_goal_detection_test",
    premise_patterns=(
      PremisePattern(
        statement_type=(
          Phase80GoalStatement
        ),
      ),
    ),
    conclusion_builder=(
      lambda premises: (
        Phase80GoalDerivedStatement(
          value=(
            premises[0]
            .conclusion
            .value
          ),
        )
      )
    ),
  )

  result = (
    run_inference_until_stable_with_history(
      (rule,),
      (source_step,),
    )
  )

  goal = Phase80GoalDerivedStatement(
    value="source",
  )

  found = find_goal_step(
    result.steps,
    goal,
  )

  assert found is not None
  assert found.conclusion == goal
  assert found.rule == ProofRule.INFERENCE
  assert found.premises == (
    source_step,
  )


def test_phase80_3_rejects_non_step_container():
  with pytest.raises(
    TypeError,
    match=(
      "steps must be a ProofStep "
      "or a tuple/list of ProofStep"
    ),
  ):
    find_goal_step(
      "not-steps",
      Phase80GoalStatement(
        value="A",
      ),
    )


def test_phase80_3_rejects_container_with_non_proof_step():
  with pytest.raises(
    TypeError,
    match=(
      "steps must contain "
      "only ProofStep objects"
    ),
  ):
    find_goal_step(
      (
        make_step(
          "A"
        ),
        "not-a-step",
      ),
      Phase80GoalStatement(
        value="A",
      ),
    )

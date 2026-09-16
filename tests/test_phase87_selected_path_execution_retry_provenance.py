import pytest

from repository_inference import (
  BoundedProducerSearchStatus,
  FiniteProducerRetryPolicy,
  execute_depth_two_producer_search,
  repository_available_steps,
)

from test_phase87_selection_side_finite_retry import (
  Phase87SelectionAStatement,
  Phase87SelectionGoalStatement,
  build_phase87_3_data,
)


def test_phase87_5_without_retry_policy_preserves_ambiguity_execution_boundary():
  data = build_phase87_3_data()

  result = execute_depth_two_producer_search(
    data["repository"],
    data["catalog"],
    data["goal"],
    max_depth=2,
  )

  assert result.report.status is (
    BoundedProducerSearchStatus
    .AMBIGUOUS_PRODUCER
  )
  assert result.report.search_result is None
  assert result.repository_inference_result is None


def test_phase87_5_one_attempt_returns_retry_exhausted_without_execution():
  data = build_phase87_3_data()

  result = execute_depth_two_producer_search(
    data["repository"],
    data["catalog"],
    data["goal"],
    max_depth=2,
    retry_policy=FiniteProducerRetryPolicy(
      max_attempts=1,
    ),
  )

  assert result.report.status is (
    BoundedProducerSearchStatus
    .PRODUCER_RETRY_EXHAUSTED
  )
  assert result.report.search_result is None
  assert result.repository_inference_result is None


def test_phase87_5_two_attempts_execute_selected_second_candidate_and_derive_goal():
  data = build_phase87_3_data()

  result = execute_depth_two_producer_search(
    data["repository"],
    data["catalog"],
    data["goal"],
    max_depth=2,
    retry_policy=FiniteProducerRetryPolicy(
      max_attempts=2,
    ),
  )

  assert result.report.status is (
    BoundedProducerSearchStatus.SUCCESS
  )
  assert result.report.search_result is not None
  assert result.repository_inference_result is not None

  assert tuple(
    node.producer_rule
    for node
    in result.report.search_result.producer_nodes
  ) == (
    data["second_a_rule"],
  )

  goal_step = (
    result.repository_inference_result.goal_step
  )

  assert goal_step is not None
  assert goal_step.conclusion == data["goal"]
  assert isinstance(
    goal_step.conclusion,
    Phase87SelectionGoalStatement,
  )


def test_phase87_5_retry_execution_preserves_selected_path_provenance():
  data = build_phase87_3_data()

  result = execute_depth_two_producer_search(
    data["repository"],
    data["catalog"],
    data["goal"],
    max_depth=2,
    retry_policy=FiniteProducerRetryPolicy(
      max_attempts=2,
    ),
  )

  repository_result = (
    result.repository_inference_result
  )

  assert repository_result is not None

  steps = (
    repository_result
    .inference_result
    .steps
  )

  a_step = next(
    step
    for step in steps
    if isinstance(
      step.conclusion,
      Phase87SelectionAStatement,
    )
  )

  goal_step = repository_result.goal_step

  assert goal_step is not None

  assert a_step.premises == ()
  assert a_step.inference_rule is data[
    "second_a_rule"
  ]

  assert goal_step.premises == (
    a_step,
  )
  assert goal_step.inference_rule is data[
    "final_rule"
  ]


def test_phase87_5_failed_retry_candidate_is_not_executed():
  data = build_phase87_3_data()

  result = execute_depth_two_producer_search(
    data["repository"],
    data["catalog"],
    data["goal"],
    max_depth=2,
    retry_policy=FiniteProducerRetryPolicy(
      max_attempts=2,
    ),
  )

  repository_result = (
    result.repository_inference_result
  )

  assert repository_result is not None

  executed_rules = tuple(
    step.inference_rule
    for step
    in repository_result.inference_result.steps
    if step.inference_rule is not None
  )

  assert data[
    "second_a_rule"
  ] in executed_rules
  assert data[
    "final_rule"
  ] in executed_rules

  assert data[
    "first_a_rule"
  ] not in executed_rules
  assert data[
    "b_rule"
  ] not in executed_rules
  assert data[
    "c_rule"
  ] not in executed_rules


def test_phase87_5_retry_execution_preserves_repository():
  data = build_phase87_3_data()

  initial_steps = repository_available_steps(
    data["repository"]
  )

  result = execute_depth_two_producer_search(
    data["repository"],
    data["catalog"],
    data["goal"],
    max_depth=2,
    retry_policy=FiniteProducerRetryPolicy(
      max_attempts=2,
    ),
  )

  assert result.report.status is (
    BoundedProducerSearchStatus.SUCCESS
  )

  assert repository_available_steps(
    data["repository"]
  ) == initial_steps


@pytest.mark.parametrize(
  "invalid_retry_policy",
  (
    1,
    "retry",
    object(),
  ),
)
def test_phase87_5_execution_rejects_invalid_retry_policy(
  invalid_retry_policy,
):
  data = build_phase87_3_data()

  with pytest.raises(
    TypeError,
    match=(
      "retry_policy must be a "
      "FiniteProducerRetryPolicy or None"
    ),
  ):
    execute_depth_two_producer_search(
      data["repository"],
      data["catalog"],
      data["goal"],
      retry_policy=invalid_retry_policy,
    )

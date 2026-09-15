from proof import (
  ProofRule,
  ProofStep,
)
from proof_repository import (
  ProofRepository,
  ProofRepositoryEntry,
)
from repository_inference import (
  BoundedProducerExecutionResult,
  BoundedProducerSearchStatus,
  execute_depth_two_producer_search,
  repository_available_steps,
)
from rule_catalog import (
  InferenceRuleCatalog,
)
from test_phase85_execution_failure_diagnostics import (
  Phase85ExecutionGoalStatement,
  _search_result,
)


def test_phase85_7_executes_successful_search_result():
  data = _search_result()

  result = execute_depth_two_producer_search(
    data[
      "repository"
    ],
    data[
      "catalog"
    ],
    data[
      "goal"
    ],
  )

  assert isinstance(
    result,
    BoundedProducerExecutionResult,
  )

  assert result.report.status is (
    BoundedProducerSearchStatus.SUCCESS
  )

  assert result.report.search_result is not None

  assert (
    result.repository_inference_result
    is not None
  )

  assert (
    result.repository_inference_result
    .goal_step
    is not None
  )

  assert (
    result.repository_inference_result
    .goal_step
    .conclusion
    == data[
      "goal"
    ]
  )


def test_phase85_7_executes_report_selected_rules():
  data = _search_result()

  result = execute_depth_two_producer_search(
    data[
      "repository"
    ],
    data[
      "catalog"
    ],
    data[
      "goal"
    ],
  )

  search_result = result.report.search_result

  assert search_result is not None

  assert (
    search_result.final_rule
    is data[
      "final_rule"
    ]
  )

  assert any(
    node.producer_rule
    is data[
      "producer_rule"
    ]
    for node
    in search_result.producer_nodes
  )

  inference_result = (
    result.repository_inference_result
  )

  assert inference_result is not None

  assert any(
    step.conclusion
    == data[
      "goal"
    ]
    for step
    in inference_result
    .inference_result
    .steps
  )


def test_phase85_7_returns_existing_goal_without_search_execution():
  goal = Phase85ExecutionGoalStatement(
    name="requested",
  )

  goal_step = ProofStep(
    conclusion=goal,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  repository = ProofRepository()

  repository.register(
    ProofRepositoryEntry(
      key="phase85.execution.existing_goal",
      step=goal_step,
      phase="85",
      theorem=(
        "integrated bounded search execution"
      ),
    )
  )

  result = execute_depth_two_producer_search(
    repository,
    InferenceRuleCatalog(),
    goal,
  )

  assert result.report.status is (
    BoundedProducerSearchStatus
    .GOAL_ALREADY_AVAILABLE
  )

  assert result.report.search_result is None
  assert result.report.diagnostic is None

  assert (
    result.repository_inference_result
    is not None
  )

  assert (
    result.repository_inference_result
    .goal_step
    is goal_step
  )


def test_phase85_7_search_failure_does_not_execute():
  data = _search_result()

  result = execute_depth_two_producer_search(
    data[
      "repository"
    ],
    InferenceRuleCatalog(),
    data[
      "goal"
    ],
  )

  assert result.report.status is (
    BoundedProducerSearchStatus
    .NO_FINAL_RULE
  )

  assert result.report.search_result is None
  assert result.report.diagnostic is not None

  assert (
    result.repository_inference_result
    is None
  )


def test_phase85_7_execution_failure_does_not_return_proof_result():
  data = _search_result(
    producer_applicable=False,
  )

  result = execute_depth_two_producer_search(
    data[
      "repository"
    ],
    data[
      "catalog"
    ],
    data[
      "goal"
    ],
  )

  assert result.report.status is (
    BoundedProducerSearchStatus
    .PRODUCER_NOT_APPLICABLE
  )

  assert result.report.search_result is not None
  assert result.report.diagnostic is not None

  assert (
    result.repository_inference_result
    is None
  )


def test_phase85_7_goal_not_derived_does_not_execute():
  data = _search_result(
    derive_requested_goal=False,
  )

  result = execute_depth_two_producer_search(
    data[
      "repository"
    ],
    data[
      "catalog"
    ],
    data[
      "goal"
    ],
  )

  assert result.report.status is (
    BoundedProducerSearchStatus
    .GOAL_NOT_DERIVED
  )

  assert result.report.search_result is not None
  assert result.report.diagnostic is not None

  assert (
    result.repository_inference_result
    is None
  )


def test_phase85_7_does_not_mutate_repository():
  data = _search_result()

  initial_steps = repository_available_steps(
    data[
      "repository"
    ]
  )

  result = execute_depth_two_producer_search(
    data[
      "repository"
    ],
    data[
      "catalog"
    ],
    data[
      "goal"
    ],
  )

  assert result.report.status is (
    BoundedProducerSearchStatus.SUCCESS
  )

  assert repository_available_steps(
    data[
      "repository"
    ]
  ) == initial_steps



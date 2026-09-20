
from repository_generator_applicability_handoff import (
  execute_repository_generator_applicability_handoff_search_report,
)
from repository_inference import (
  BoundedProducerSearchStatus,
)
from test_phase104_4m_ready_search_report_execution_adapter import (
  _build_fixture,
)


def test_phase104_4o_preserves_final_rule_identity_end_to_end():
  data = _build_fixture()

  search_report = data[
    "search_report"
  ]
  validation = search_report.validation

  result = (
    execute_repository_generator_applicability_handoff_search_report(
      search_report,
      data[
        "repository"
      ],
    )
  )

  assert result.search_report is search_report
  assert (
    result.execution_result.report
    is search_report.report
  )

  search_result = (
    search_report
    .report
    .search_result
  )
  assert search_result is not None

  candidate_rule = (
    validation
    .handoff
    .candidate
    .candidate
    .inference_rule
  )

  execution_entry = (
    validation.execution_entry
  )
  assert execution_entry is not None

  repository_result = (
    result
    .execution_result
    .repository_inference_result
  )
  assert repository_result is not None

  goal_step = repository_result.goal_step
  assert goal_step is not None

  assert (
    candidate_rule
    is execution_entry.rule
  )
  assert (
    execution_entry.rule
    is search_result.final_rule
  )
  assert (
    search_result.final_rule
    is goal_step.inference_rule
  )


def test_phase104_4o_preserves_selected_producer_proof_step_provenance():
  data = _build_fixture()

  search_report = data[
    "search_report"
  ]

  result = (
    execute_repository_generator_applicability_handoff_search_report(
      search_report,
      data[
        "repository"
      ],
    )
  )

  search_result = (
    search_report
    .report
    .search_result
  )
  assert search_result is not None

  assert len(
    search_result.producer_nodes
  ) == 1

  producer_node = (
    search_result.producer_nodes[
      0
    ]
  )

  repository_result = (
    result
    .execution_result
    .repository_inference_result
  )
  assert repository_result is not None

  producer_steps = tuple(
    step
    for step
    in repository_result.inference_result.steps
    if (
      step.inference_rule
      is producer_node.producer_rule
    )
  )

  assert len(
    producer_steps
  ) == 1

  producer_step = producer_steps[
    0
  ]

  source_step = (
    search_report
    .validation
    .handoff
    .candidate
    .scope_node
    .proof_step
  )

  assert (
    producer_node.producer_rule
    is data[
      "producer_rule"
    ]
  )
  assert (
    producer_step.inference_rule
    is producer_node.producer_rule
  )
  assert producer_step.premises == (
    source_step,
  )

  goal_step = repository_result.goal_step
  assert goal_step is not None

  assert (
    goal_step.inference_rule
    is search_result.final_rule
  )
  assert goal_step.premises == (
    producer_step,
  )


def test_phase104_4o_goal_already_available_preserves_validation_without_execution():
  data = _build_fixture(
    goal_already_available=True,
  )

  search_report = data[
    "search_report"
  ]

  assert search_report.report.status is (
    BoundedProducerSearchStatus
    .GOAL_ALREADY_AVAILABLE
  )

  validation = search_report.validation
  candidate_rule = (
    validation
    .handoff
    .candidate
    .candidate
    .inference_rule
  )

  execution_entry = (
    validation.execution_entry
  )
  assert execution_entry is not None
  assert (
    candidate_rule
    is execution_entry.rule
  )

  result = (
    execute_repository_generator_applicability_handoff_search_report(
      search_report,
      data[
        "repository"
      ],
    )
  )

  assert result.search_report is search_report
  assert (
    result.execution_result.report
    is search_report.report
  )

  repository_result = (
    result
    .execution_result
    .repository_inference_result
  )
  assert repository_result is not None

  goal_step = repository_result.goal_step
  assert goal_step is not None
  assert goal_step.inference_rule is None

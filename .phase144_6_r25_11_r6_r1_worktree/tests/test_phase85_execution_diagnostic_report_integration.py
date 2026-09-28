from proof import (
  ProofRule,
  ProofStep,
)
from proof_repository import (
  ProofRepository,
  ProofRepositoryEntry,
)
from repository_inference import (
  BoundedProducerSearchStatus,
  build_depth_two_producer_search_report,
  repository_available_steps,
)
from rule_catalog import (
  InferenceRuleCatalog,
)
from test_phase85_execution_failure_diagnostics import (
  Phase85ExecutionGoalStatement,
  _search_result,
)


def test_phase85_6_reports_success():
  data = _search_result()

  report = build_depth_two_producer_search_report(
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

  assert report.status is (
    BoundedProducerSearchStatus.SUCCESS
  )
  assert report.goal == data[
    "goal"
  ]
  assert report.search_result is not None
  assert (
    report.search_result.final_rule
    is data[
      "final_rule"
    ]
  )
  assert report.diagnostic is None


def test_phase85_6_reports_goal_already_available():
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
      key="phase85.report.goal",
      step=goal_step,
      phase="85",
      theorem=(
        "execution diagnostic report integration"
      ),
    )
  )

  report = build_depth_two_producer_search_report(
    repository,
    InferenceRuleCatalog(),
    goal,
  )

  assert report.status is (
    BoundedProducerSearchStatus
    .GOAL_ALREADY_AVAILABLE
  )
  assert report.goal == goal
  assert report.search_result is None
  assert report.diagnostic is None


def test_phase85_6_integrates_search_failure():
  data = _search_result()

  report = build_depth_two_producer_search_report(
    data[
      "repository"
    ],
    InferenceRuleCatalog(),
    data[
      "goal"
    ],
  )

  assert report.status is (
    BoundedProducerSearchStatus
    .NO_FINAL_RULE
  )
  assert report.search_result is None
  assert report.diagnostic is not None
  assert report.diagnostic.status is (
    BoundedProducerSearchStatus
    .NO_FINAL_RULE
  )
  assert report.diagnostic.goal == data[
    "goal"
  ]


def test_phase85_6_integrates_producer_execution_failure():
  data = _search_result(
    producer_applicable=False,
  )

  report = build_depth_two_producer_search_report(
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

  assert report.status is (
    BoundedProducerSearchStatus
    .PRODUCER_NOT_APPLICABLE
  )
  assert report.search_result is not None
  assert report.diagnostic is not None
  assert report.diagnostic.status is (
    BoundedProducerSearchStatus
    .PRODUCER_NOT_APPLICABLE
  )
  assert (
    report.diagnostic.final_rule
    is data[
      "final_rule"
    ]
  )
  assert report.diagnostic.producer_candidates == (
    data[
      "producer_rule"
    ],
  )


def test_phase85_6_integrates_final_rule_execution_failure():
  data = _search_result(
    final_applicable=False,
  )

  report = build_depth_two_producer_search_report(
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

  assert report.status is (
    BoundedProducerSearchStatus
    .FINAL_RULE_NOT_APPLICABLE
  )
  assert report.search_result is not None
  assert report.diagnostic is not None
  assert report.diagnostic.status is (
    BoundedProducerSearchStatus
    .FINAL_RULE_NOT_APPLICABLE
  )
  assert (
    report.diagnostic.final_rule
    is data[
      "final_rule"
    ]
  )


def test_phase85_6_integrates_goal_not_derived():
  data = _search_result(
    derive_requested_goal=False,
  )

  report = build_depth_two_producer_search_report(
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

  assert report.status is (
    BoundedProducerSearchStatus
    .GOAL_NOT_DERIVED
  )
  assert report.search_result is not None
  assert report.diagnostic is not None
  assert report.diagnostic.status is (
    BoundedProducerSearchStatus
    .GOAL_NOT_DERIVED
  )
  assert (
    report.diagnostic.final_rule
    is data[
      "final_rule"
    ]
  )


def test_phase85_6_report_building_does_not_mutate_repository():
  data = _search_result(
    producer_applicable=False,
  )

  initial_steps = repository_available_steps(
    data[
      "repository"
    ]
  )

  build_depth_two_producer_search_report(
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

  assert repository_available_steps(
    data[
      "repository"
    ]
  ) == initial_steps



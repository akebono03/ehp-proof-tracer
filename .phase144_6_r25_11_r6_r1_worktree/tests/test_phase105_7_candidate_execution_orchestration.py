import pytest

from repository_generator_applicability_execution_orchestration import (
  FirstQualifiedProductionApplicabilityExecutionResult,
  execute_first_qualified_production_applicability_candidate,
)
from repository_generator_applicability_handoff import (
  RepositoryGeneratorApplicabilityHandoffValidationStatus,
)
from repository_inference import (
  BoundedProducerSearchStatus,
)
from test_phase105_5_minimal_production_execution_seed_adapter import (
  build_phase105_5_actual_data,
)


def test_phase105_7_orchestration_returns_composed_result():
  data = build_phase105_5_actual_data()

  result = (
    execute_first_qualified_production_applicability_candidate(
      data[
        "candidate"
      ],
      data[
        "goal"
      ],
    )
  )

  assert isinstance(
    result,
    FirstQualifiedProductionApplicabilityExecutionResult,
  )


def test_phase105_7_orchestration_preserves_candidate_and_goal():
  data = build_phase105_5_actual_data()

  result = (
    execute_first_qualified_production_applicability_candidate(
      data[
        "candidate"
      ],
      data[
        "goal"
      ],
    )
  )

  assert result.candidate is data[
    "candidate"
  ]
  assert result.goal == data[
    "goal"
  ]
  assert result.handoff.candidate is data[
    "candidate"
  ]
  assert result.handoff.goal == data[
    "goal"
  ]


def test_phase105_7_orchestration_builds_exact_source_seed():
  data = build_phase105_5_actual_data()

  result = (
    execute_first_qualified_production_applicability_candidate(
      data[
        "candidate"
      ],
      data[
        "goal"
      ],
    )
  )

  entries = result.seed_repository.entries()

  assert len(
    entries
  ) == 1
  assert entries[
    0
  ].step is data[
    "source_step"
  ]


def test_phase105_7_orchestration_builds_single_qualified_execution_entry():
  data = build_phase105_5_actual_data()

  result = (
    execute_first_qualified_production_applicability_candidate(
      data[
        "candidate"
      ],
      data[
        "goal"
      ],
    )
  )

  entries = result.execution_catalog.entries()

  assert len(
    entries
  ) == 1

  execution_entry = entries[
    0
  ]

  assert execution_entry.fixed_point_safe is True
  assert (
    execution_entry.rule
    is data[
      "candidate"
    ].candidate.inference_rule
  )


def test_phase105_7_orchestration_reaches_ready_and_success_without_producers():
  data = build_phase105_5_actual_data()

  result = (
    execute_first_qualified_production_applicability_candidate(
      data[
        "candidate"
      ],
      data[
        "goal"
      ],
    )
  )

  assert result.validation.status is (
    RepositoryGeneratorApplicabilityHandoffValidationStatus.READY
  )

  assert result.search_report.report.status is (
    BoundedProducerSearchStatus.SUCCESS
  )

  search_result = (
    result.search_report.report.search_result
  )
  assert search_result is not None
  assert search_result.producer_nodes == ()


def test_phase105_7_orchestration_derives_goal_with_full_provenance():
  data = build_phase105_5_actual_data()

  result = (
    execute_first_qualified_production_applicability_candidate(
      data[
        "candidate"
      ],
      data[
        "goal"
      ],
    )
  )

  repository_result = (
    result
    .execution
    .execution_result
    .repository_inference_result
  )
  assert repository_result is not None

  goal_step = repository_result.goal_step
  assert goal_step is not None
  assert goal_step.conclusion == data[
    "goal"
  ]
  assert goal_step.premises == (
    data[
      "source_step"
    ],
  )

  execution_entry = (
    result.validation.execution_entry
  )
  assert execution_entry is not None

  search_result = (
    result.search_report.report.search_result
  )
  assert search_result is not None

  assert (
    data[
      "candidate"
    ].candidate.inference_rule
    is execution_entry.rule
    is search_result.final_rule
    is goal_step.inference_rule
  )


def test_phase105_7_orchestration_preserves_intermediate_identity_chain():
  data = build_phase105_5_actual_data()

  result = (
    execute_first_qualified_production_applicability_candidate(
      data[
        "candidate"
      ],
      data[
        "goal"
      ],
    )
  )

  assert (
    result.validation.handoff
    is result.handoff
  )
  assert (
    result.search_report.validation
    is result.validation
  )
  assert (
    result.execution.search_report
    is result.search_report
  )
  assert (
    result.execution.execution_result.report
    is result.search_report.report
  )


def test_phase105_7_orchestration_does_not_mutate_standard_repository():
  data = build_phase105_5_actual_data()

  before_entries = (
    data[
      "production_repository"
    ].entries()
  )

  execute_first_qualified_production_applicability_candidate(
    data[
      "candidate"
    ],
    data[
      "goal"
    ],
  )

  assert (
    data[
      "production_repository"
    ].entries()
    == before_entries
  )


def test_phase105_7_orchestration_rejects_non_candidate():
  data = build_phase105_5_actual_data()

  with pytest.raises(
    TypeError,
    match=(
      "candidate must be a "
      "RepositoryProofScopeApplicabilityCandidate"
    ),
  ):
    execute_first_qualified_production_applicability_candidate(
      object(),
      data[
        "goal"
      ],
    )

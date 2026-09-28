from dataclasses import replace

import pytest

from repository_generator_applicability_handoff import (
  RepositoryGeneratorApplicabilityHandoffValidationStatus,
)
from repository_generator_two_premise_execution_integration import (
  TwoPremiseProductionApplicationExecutionResult,
  execute_two_premise_repository_generator_production_application_candidate,
)
from repository_inference import (
  BoundedProducerSearchStatus,
  repository_available_steps,
)
from rule_catalog import (
  InferenceRuleCatalog,
)
from test_phase107_5_exact_production_application_premise_tuple_recovery import (
  build_phase107_5_actual_data,
)


def _build_phase107_9_execution_catalog(
  data,
):
  candidate = data[
    "candidates"
  ][
    0
  ]

  discovery_entry = (
    candidate
    .candidate
    .catalog_entry
  )

  execution_entry = replace(
    discovery_entry,
    key=(
      "phase107.9.execution."
      "pi6-2-eta2-nu-prime"
    ),
    fixed_point_safe=True,
    goal_compatibility=(
      lambda candidate_goal:
      candidate_goal
      == data[
        "goal"
      ]
    ),
  )

  execution_catalog = (
    InferenceRuleCatalog()
  )
  execution_catalog.register(
    execution_entry
  )

  return (
    execution_catalog,
    execution_entry,
  )


def test_phase107_9_integration_rejects_non_candidate():
  data = build_phase107_5_actual_data()

  execution_catalog, _ = (
    _build_phase107_9_execution_catalog(
      data
    )
  )

  with pytest.raises(
    TypeError,
    match=(
      "candidate must be a "
      "RepositoryProofScopeApplicabilityCandidate"
    ),
  ):
    execute_two_premise_repository_generator_production_application_candidate(
      object(),
      data[
        "goal"
      ],
      execution_catalog,
    )


def test_phase107_9_integration_rejects_non_catalog():
  data = build_phase107_5_actual_data()

  with pytest.raises(
    TypeError,
    match=(
      "execution_catalog must be an "
      "InferenceRuleCatalog"
    ),
  ):
    execute_two_premise_repository_generator_production_application_candidate(
      data[
        "candidates"
      ][
        0
      ],
      data[
        "goal"
      ],
      object(),
    )


@pytest.mark.parametrize(
  "candidate_index",
  (
    0,
    1,
  ),
)
def test_phase107_9_actual_two_premise_execution_reaches_ready_and_success(
  candidate_index,
):
  data = build_phase107_5_actual_data()

  execution_catalog, _ = (
    _build_phase107_9_execution_catalog(
      data
    )
  )

  result = (
    execute_two_premise_repository_generator_production_application_candidate(
      data[
        "candidates"
      ][
        candidate_index
      ],
      data[
        "goal"
      ],
      execution_catalog,
    )
  )

  assert isinstance(
    result,
    TwoPremiseProductionApplicationExecutionResult,
  )

  assert result.validation.status is (
    RepositoryGeneratorApplicabilityHandoffValidationStatus.READY
  )

  assert result.search_report.report.status is (
    BoundedProducerSearchStatus.SUCCESS
  )

  search_result = (
    result
    .search_report
    .report
    .search_result
  )

  assert search_result is not None
  assert search_result.producer_nodes == ()


@pytest.mark.parametrize(
  "candidate_index",
  (
    0,
    1,
  ),
)
def test_phase107_9_search_uses_exact_recovered_premise_tuple(
  candidate_index,
):
  data = build_phase107_5_actual_data()

  execution_catalog, _ = (
    _build_phase107_9_execution_catalog(
      data
    )
  )

  result = (
    execute_two_premise_repository_generator_production_application_candidate(
      data[
        "candidates"
      ][
        candidate_index
      ],
      data[
        "goal"
      ],
      execution_catalog,
    )
  )

  premise_tuple = (
    result.recovery.premise_tuple
  )

  assert premise_tuple is not None

  seed_steps = (
    repository_available_steps(
      result.seed_repository
    )
  )

  assert seed_steps == premise_tuple

  search_result = (
    result
    .search_report
    .report
    .search_result
  )
  assert search_result is not None

  assert (
    search_result
    .final_availability
    .matched_steps
    == premise_tuple
  )

  assert (
    search_result
    .final_availability
    .missing_indices
    == ()
  )


@pytest.mark.parametrize(
  "candidate_index",
  (
    0,
    1,
  ),
)
def test_phase107_9_execution_rederives_goal_with_exact_provenance(
  candidate_index,
):
  data = build_phase107_5_actual_data()

  execution_catalog, execution_entry = (
    _build_phase107_9_execution_catalog(
      data
    )
  )

  result = (
    execute_two_premise_repository_generator_production_application_candidate(
      data[
        "candidates"
      ][
        candidate_index
      ],
      data[
        "goal"
      ],
      execution_catalog,
    )
  )

  repository_result = (
    result
    .execution
    .execution_result
    .repository_inference_result
  )

  assert repository_result is not None

  goal_step = (
    repository_result.goal_step
  )

  assert goal_step is not None

  assert (
    goal_step.conclusion
    == data[
      "goal"
    ]
  )

  assert (
    goal_step
    is not data[
      "target_step"
    ]
  )

  premise_tuple = (
    result.recovery.premise_tuple
  )

  assert premise_tuple is not None
  assert goal_step.premises == premise_tuple

  assert all(
    actual is expected
    for actual, expected
    in zip(
      goal_step.premises,
      premise_tuple,
    )
  )

  search_result = (
    result
    .search_report
    .report
    .search_result
  )
  assert search_result is not None

  assert (
    data[
      "candidates"
    ][
      candidate_index
    ]
    .candidate
    .inference_rule
    is execution_entry.rule
    is search_result.final_rule
    is goal_step.inference_rule
  )


def test_phase107_9_integration_preserves_intermediate_identity_chain():
  data = build_phase107_5_actual_data()

  execution_catalog, _ = (
    _build_phase107_9_execution_catalog(
      data
    )
  )

  candidate = (
    data[
      "candidates"
    ][
      0
    ]
  )

  result = (
    execute_two_premise_repository_generator_production_application_candidate(
      candidate,
      data[
        "goal"
      ],
      execution_catalog,
    )
  )

  assert result.candidate is candidate
  assert result.recovery.candidate is candidate
  assert result.handoff.candidate is candidate

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
    result
    .execution
    .execution_result
    .report
    is result
    .search_report
    .report
  )


def test_phase107_9_integration_rejects_non_unique_recovery():
  data = build_phase107_5_actual_data()

  execution_catalog, _ = (
    _build_phase107_9_execution_catalog(
      data
    )
  )

  with pytest.raises(
    ValueError,
    match=(
      "production application recovery "
      "must be UNIQUE"
    ),
  ):
    execute_two_premise_repository_generator_production_application_candidate(
      data[
        "candidates"
      ][
        0
      ],
      object(),
      execution_catalog,
    )


def test_phase107_9_integration_rejects_non_ready_handoff():
  data = build_phase107_5_actual_data()

  empty_execution_catalog = (
    InferenceRuleCatalog()
  )

  with pytest.raises(
    ValueError,
    match=(
      "two-premise production applicability handoff "
      "must validate as READY"
    ),
  ):
    execute_two_premise_repository_generator_production_application_candidate(
      data[
        "candidates"
      ][
        0
      ],
      data[
        "goal"
      ],
      empty_execution_catalog,
    )


def test_phase107_9_integration_does_not_mutate_standard_repository():
  data = build_phase107_5_actual_data()

  before_entries = (
    data[
      "repository"
    ].entries()
  )

  execution_catalog, _ = (
    _build_phase107_9_execution_catalog(
      data
    )
  )

  execute_two_premise_repository_generator_production_application_candidate(
    data[
      "candidates"
    ][
      0
    ],
    data[
      "goal"
    ],
    execution_catalog,
  )

  assert (
    data[
      "repository"
    ].entries()
    == before_entries
  )

import pytest

from repository_generator_applicability_execution_entry import (
  build_second_qualified_production_execution_catalog,
)
from repository_generator_applicability_execution_orchestration import (
  FirstQualifiedProductionApplicabilityExecutionResult,
  execute_second_qualified_production_applicability_candidate,
)
from repository_generator_qualified_execution_dispatch import (
  QualifiedProductionApplicabilityExecutionDispatchResult,
  execute_qualified_production_applicability_candidate,
)
from repository_generator_two_premise_execution_integration import (
  TwoPremiseProductionApplicationExecutionResult,
)
from repository_inference import (
  BoundedProducerSearchStatus,
)
from test_phase105_5_minimal_production_execution_seed_adapter import (
  build_phase105_5_actual_data,
)
from test_phase107_5_exact_production_application_premise_tuple_recovery import (
  build_phase107_5_actual_data,
)


_FIRST_FAMILY = (
  "toda_58_delta_iota9_nu4_nu_prime_inference_rule"
)

_SECOND_FAMILY = (
  "toda_lemma57_pi6_2_eta2_nu_prime_inference_rule"
)


def test_phase107_16_second_execution_catalog_preserves_rule_identity():
  data = build_phase107_5_actual_data()

  candidate = (
    data[
      "candidates"
    ][
      0
    ]
  )

  catalog = (
    build_second_qualified_production_execution_catalog(
      candidate,
      data[
        "goal"
      ],
    )
  )

  entries = catalog.entries()

  assert len(
    entries
  ) == 1

  entry = entries[
    0
  ]

  assert entry.fixed_point_safe is True
  assert (
    entry.rule
    is candidate.candidate.inference_rule
  )


def test_phase107_16_second_orchestration_executes_exact_two_premise_path():
  data = build_phase107_5_actual_data()

  candidate = (
    data[
      "candidates"
    ][
      0
    ]
  )

  result = (
    execute_second_qualified_production_applicability_candidate(
      candidate,
      data[
        "goal"
      ],
    )
  )

  assert isinstance(
    result,
    TwoPremiseProductionApplicationExecutionResult,
  )

  assert result.candidate is candidate
  assert result.goal == data[
    "goal"
  ]

  search_result = (
    result
    .search_report
    .report
    .search_result
  )

  assert search_result is not None
  assert search_result.producer_nodes == ()

  repository_result = (
    result
    .execution
    .execution_result
    .repository_inference_result
  )

  assert repository_result is not None
  assert repository_result.goal_step is not None

  premise_tuple = (
    result.recovery.premise_tuple
  )

  assert premise_tuple is not None
  assert (
    repository_result.goal_step.premises
    == premise_tuple
  )


def test_phase107_16_dispatch_routes_first_family_to_existing_orchestration():
  data = build_phase105_5_actual_data()

  result = (
    execute_qualified_production_applicability_candidate(
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
    QualifiedProductionApplicabilityExecutionDispatchResult,
  )

  assert result.family_name == _FIRST_FAMILY
  assert (
    result.candidate
    is data[
      "candidate"
    ]
  )
  assert isinstance(
    result.execution,
    FirstQualifiedProductionApplicabilityExecutionResult,
  )

  assert (
    result.execution.candidate
    is data[
      "candidate"
    ]
  )

  assert (
    result.execution
    .search_report
    .report
    .status
    is BoundedProducerSearchStatus.SUCCESS
  )


@pytest.mark.parametrize(
  "candidate_index",
  (
    0,
    1,
  ),
)
def test_phase107_16_dispatch_routes_second_family_to_two_premise_orchestration(
  candidate_index,
):
  data = build_phase107_5_actual_data()

  candidate = (
    data[
      "candidates"
    ][
      candidate_index
    ]
  )

  result = (
    execute_qualified_production_applicability_candidate(
      candidate,
      data[
        "goal"
      ],
    )
  )

  assert result.family_name == _SECOND_FAMILY
  assert result.candidate is candidate
  assert isinstance(
    result.execution,
    TwoPremiseProductionApplicationExecutionResult,
  )

  assert (
    result.execution.candidate
    is candidate
  )

  assert (
    result.execution
    .search_report
    .report
    .status
    is BoundedProducerSearchStatus.SUCCESS
  )

  search_result = (
    result.execution
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
def test_phase107_16_second_dispatch_preserves_exact_recovered_provenance(
  candidate_index,
):
  data = build_phase107_5_actual_data()

  candidate = (
    data[
      "candidates"
    ][
      candidate_index
    ]
  )

  result = (
    execute_qualified_production_applicability_candidate(
      candidate,
      data[
        "goal"
      ],
    )
  )

  execution = result.execution

  assert isinstance(
    execution,
    TwoPremiseProductionApplicationExecutionResult,
  )

  repository_result = (
    execution
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
    goal_step
    is not data[
      "target_step"
    ]
  )

  premise_tuple = (
    execution.recovery.premise_tuple
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

  assert (
    goal_step.inference_rule
    is candidate.candidate.inference_rule
  )


def test_phase107_16_dispatch_rejects_non_candidate():
  data = build_phase105_5_actual_data()

  with pytest.raises(
    TypeError,
    match=(
      "candidate must be a "
      "RepositoryProofScopeApplicabilityCandidate"
    ),
  ):
    execute_qualified_production_applicability_candidate(
      object(),
      data[
        "goal"
      ],
    )


def test_phase107_16_second_orchestration_rejects_first_family_candidate():
  data = build_phase105_5_actual_data()

  with pytest.raises(
    ValueError,
    match=(
      "candidate rule is not the second qualified "
      "production execution rule"
    ),
  ):
    execute_second_qualified_production_applicability_candidate(
      data[
        "candidate"
      ],
      data[
        "goal"
      ],
    )


def test_phase107_16_dispatch_does_not_mutate_standard_repositories():
  first_data = build_phase105_5_actual_data()
  second_data = build_phase107_5_actual_data()

  first_before = (
    first_data[
      "production_repository"
    ].entries()
  )
  second_before = (
    second_data[
      "repository"
    ].entries()
  )

  execute_qualified_production_applicability_candidate(
    first_data[
      "candidate"
    ],
    first_data[
      "goal"
    ],
  )

  execute_qualified_production_applicability_candidate(
    second_data[
      "candidates"
    ][
      0
    ],
    second_data[
      "goal"
    ],
  )

  assert (
    first_data[
      "production_repository"
    ].entries()
    == first_before
  )

  assert (
    second_data[
      "repository"
    ].entries()
    == second_before
  )

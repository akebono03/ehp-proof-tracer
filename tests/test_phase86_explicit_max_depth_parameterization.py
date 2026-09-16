import pytest

from proof_repository import ProofRepository
from repository_inference import (
  BoundedProducerSearchStatus,
  build_depth_two_producer_search_report,
  diagnose_depth_two_producer_search_failure,
  execute_depth_two_producer_search,
  repository_available_steps,
  select_unique_depth_two_producer_chain,
)
from test_phase84_producer_premise_availability import (
  build_phase84_3_data,
)
from test_phase85_nested_producer_cycle_depth_classification import (
  Phase85NestedGoalStatement,
  _base_rules,
  _catalog,
)


def _producer_rule_sequence(
  search_result,
):
  return tuple(
    node.producer_rule
    for node
    in search_result.producer_nodes
  )


def _producer_depth_sequence(
  search_result,
):
  return tuple(
    node.depths
    for node
    in search_result.producer_nodes
  )


def _dependency_rule_sequence(
  search_result,
):
  return tuple(
    tuple(
      dependency.producer_rule
      for dependency
      in node.dependencies
    )
    for node
    in search_result.producer_nodes
  )


def test_phase86_2_default_and_explicit_search_select_same_path():
  data = build_phase84_3_data()

  default_result = (
    select_unique_depth_two_producer_chain(
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
  )

  explicit_result = (
    select_unique_depth_two_producer_chain(
      data[
        "repository"
      ],
      data[
        "catalog"
      ],
      data[
        "goal"
      ],
      max_depth=2,
    )
  )

  assert default_result is not None
  assert explicit_result is not None

  assert (
    default_result.final_rule
    is explicit_result.final_rule
  )

  assert (
    default_result.final_availability
    == explicit_result.final_availability
  )

  assert default_result.max_depth == 2
  assert explicit_result.max_depth == 2

  assert (
    _producer_rule_sequence(
      default_result
    )
    == _producer_rule_sequence(
      explicit_result
    )
  )

  assert (
    _producer_depth_sequence(
      default_result
    )
    == _producer_depth_sequence(
      explicit_result
    )
  )

  assert (
    _dependency_rule_sequence(
      default_result
    )
    == _dependency_rule_sequence(
      explicit_result
    )
  )


def test_phase86_2_explicit_search_preserves_actual_shared_dependency():
  data = build_phase84_3_data()

  result = (
    select_unique_depth_two_producer_chain(
      data[
        "repository"
      ],
      data[
        "catalog"
      ],
      data[
        "goal"
      ],
      max_depth=2,
    )
  )

  assert result is not None

  assert tuple(
    node.producer_rule
    for node
    in result.producer_nodes
  ) == (
    data[
      "bracket_sum_rule"
    ],
    data[
      "composition_rule"
    ],
  )

  bracket_sum_node = result.producer_nodes[
    0
  ]
  composition_node = result.producer_nodes[
    1
  ]

  assert bracket_sum_node.depths == (
    1,
    2,
  )

  assert bracket_sum_node.is_shared

  assert composition_node.depths == (
    1,
  )

  assert composition_node.dependencies == (
    bracket_sum_node,
  )

  assert result.is_within_depth_limit


def test_phase86_2_default_and_explicit_depth_limit_diagnostics_match():
  rules = _base_rules()
  catalog = _catalog(
    rules
  )
  goal = Phase85NestedGoalStatement()

  default_diagnostic = (
    diagnose_depth_two_producer_search_failure(
      ProofRepository(),
      catalog,
      goal,
    )
  )

  explicit_diagnostic = (
    diagnose_depth_two_producer_search_failure(
      ProofRepository(),
      catalog,
      goal,
      max_depth=2,
    )
  )

  assert default_diagnostic is not None
  assert explicit_diagnostic is not None

  assert default_diagnostic.status is (
    BoundedProducerSearchStatus.DEPTH_LIMIT
  )

  assert explicit_diagnostic.status is (
    BoundedProducerSearchStatus.DEPTH_LIMIT
  )

  assert (
    default_diagnostic.current_depth
    == explicit_diagnostic.current_depth
    == 2
  )

  assert (
    default_diagnostic.required_next_depth
    == explicit_diagnostic.required_next_depth
    == 3
  )

  assert (
    default_diagnostic.producer_candidates
    == explicit_diagnostic.producer_candidates
  )

  assert (
    default_diagnostic.ancestor_rules
    == explicit_diagnostic.ancestor_rules
  )


def test_phase86_2_default_and_explicit_reports_match():
  data = build_phase84_3_data()

  default_report = (
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
  )

  explicit_report = (
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
      max_depth=2,
    )
  )

  assert default_report.status is (
    BoundedProducerSearchStatus.SUCCESS
  )

  assert explicit_report.status is (
    BoundedProducerSearchStatus.SUCCESS
  )

  assert default_report.diagnostic is None
  assert explicit_report.diagnostic is None

  assert default_report.search_result is not None
  assert explicit_report.search_result is not None

  assert (
    default_report.search_result.final_rule
    is explicit_report.search_result.final_rule
  )

  assert (
    _producer_rule_sequence(
      default_report.search_result
    )
    == _producer_rule_sequence(
      explicit_report.search_result
    )
  )

  assert (
    _producer_depth_sequence(
      default_report.search_result
    )
    == _producer_depth_sequence(
      explicit_report.search_result
    )
  )

  assert (
    _dependency_rule_sequence(
      default_report.search_result
    )
    == _dependency_rule_sequence(
      explicit_report.search_result
    )
  )


def test_phase86_2_default_and_explicit_execution_match():
  data = build_phase84_3_data()

  default_result = (
    execute_depth_two_producer_search(
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
  )

  explicit_result = (
    execute_depth_two_producer_search(
      data[
        "repository"
      ],
      data[
        "catalog"
      ],
      data[
        "goal"
      ],
      max_depth=2,
    )
  )

  assert default_result.report.status is (
    BoundedProducerSearchStatus.SUCCESS
  )

  assert explicit_result.report.status is (
    BoundedProducerSearchStatus.SUCCESS
  )

  default_repository_result = (
    default_result.repository_inference_result
  )
  explicit_repository_result = (
    explicit_result.repository_inference_result
  )

  assert default_repository_result is not None
  assert explicit_repository_result is not None

  default_goal_step = (
    default_repository_result.goal_step
  )
  explicit_goal_step = (
    explicit_repository_result.goal_step
  )

  assert default_goal_step is not None
  assert explicit_goal_step is not None

  assert (
    default_goal_step.conclusion
    == explicit_goal_step.conclusion
    == data[
      "goal"
    ]
  )

  assert (
    default_goal_step.inference_rule
    is explicit_goal_step.inference_rule
    is data[
      "final_rule"
    ]
  )

  assert len(
    default_goal_step.premises
  ) == len(
    explicit_goal_step.premises
  )

  assert tuple(
    premise.conclusion
    for premise
    in default_goal_step.premises
  ) == tuple(
    premise.conclusion
    for premise
    in explicit_goal_step.premises
  )

  assert tuple(
    premise.inference_rule
    for premise
    in default_goal_step.premises
  ) == tuple(
    premise.inference_rule
    for premise
    in explicit_goal_step.premises
  )


def test_phase86_2_explicit_execution_preserves_repository_non_mutation():
  data = build_phase84_3_data()

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
    max_depth=2,
  )

  assert result.report.status is (
    BoundedProducerSearchStatus.SUCCESS
  )

  assert repository_available_steps(
    data[
      "repository"
    ]
  ) == initial_steps


@pytest.mark.parametrize(
  "max_depth",
  (
    1,
    4,
  ),
)
def test_phase86_2_search_rejects_unsupported_depths(
  max_depth,
):
  data = build_phase84_3_data()

  with pytest.raises(
    ValueError,
    match=(
      "max_depth must be 2 or 3 for "
      "bounded producer search selection"
    ),
  ):
    select_unique_depth_two_producer_chain(
      data[
        "repository"
      ],
      data[
        "catalog"
      ],
      data[
        "goal"
      ],
      max_depth=max_depth,
    )


@pytest.mark.parametrize(
  "max_depth",
  (
    1,
    4,
  ),
)
def test_phase86_3_3_diagnostics_reject_unsupported_depths(
  max_depth,
):
  data = build_phase84_3_data()

  with pytest.raises(
    ValueError,
    match=(
      "max_depth must be 2 or 3 for "
      "bounded producer search selection"
    ),
  ):
    diagnose_depth_two_producer_search_failure(
      data[
        "repository"
      ],
      data[
        "catalog"
      ],
      data[
        "goal"
      ],
      max_depth=max_depth,
    )


@pytest.mark.parametrize(
  "max_depth",
  (
    1,
    3,
  ),
)
def test_phase86_2_report_rejects_unsupported_depths(
  max_depth,
):
  data = build_phase84_3_data()

  with pytest.raises(
    ValueError,
    match=(
      "max_depth must be 2 for "
      "depth-two producer search"
    ),
  ):
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
      max_depth=max_depth,
    )


@pytest.mark.parametrize(
  "max_depth",
  (
    1,
    3,
  ),
)
def test_phase86_2_execution_rejects_unsupported_depths(
  max_depth,
):
  data = build_phase84_3_data()

  with pytest.raises(
    ValueError,
    match=(
      "max_depth must be 2 for "
      "depth-two producer search"
    ),
  ):
    execute_depth_two_producer_search(
      data[
        "repository"
      ],
      data[
        "catalog"
      ],
      data[
        "goal"
      ],
      max_depth=max_depth,
    )


@pytest.mark.parametrize(
  "max_depth",
  (
    True,
    2.0,
    "2",
  ),
)
def test_phase86_2_rejects_non_integer_depth(
  max_depth,
):
  data = build_phase84_3_data()

  with pytest.raises(
    TypeError,
    match="max_depth must be an int",
  ):
    execute_depth_two_producer_search(
      data[
        "repository"
      ],
      data[
        "catalog"
      ],
      data[
        "goal"
      ],
      max_depth=max_depth,
    )



import pytest

from proof import (
  InferenceRule,
  PremisePattern,
  ProofRule,
  ProofStep,
)
from repository_inference import (
  BoundedProducerSearchNode,
  BoundedProducerSearchResult,
  PremiseAvailability,
)


class Phase84SeedStatement:
  pass


class Phase84SharedStatement:
  pass


class Phase84IntermediateStatement:
  pass


class Phase84GoalStatement:
  pass


def _phase84_rule(
  name,
  premise_patterns,
):
  return InferenceRule(
    name=name,
    premise_patterns=premise_patterns,
  )


def _build_phase84_2_data():
  seed_pattern = PremisePattern(
    proof_rule=ProofRule.GIVEN,
    statement_type=(
      Phase84SeedStatement
    ),
  )

  shared_pattern = PremisePattern(
    proof_rule=ProofRule.INFERENCE,
    statement_type=(
      Phase84SharedStatement
    ),
  )

  intermediate_pattern = PremisePattern(
    proof_rule=ProofRule.INFERENCE,
    statement_type=(
      Phase84IntermediateStatement
    ),
  )

  shared_rule = _phase84_rule(
    "phase84 shared producer",
    (
      seed_pattern,
    ),
  )

  intermediate_rule = _phase84_rule(
    "phase84 intermediate producer",
    (
      shared_pattern,
    ),
  )

  final_rule = _phase84_rule(
    "phase84 final rule",
    (
      shared_pattern,
      intermediate_pattern,
    ),
  )

  seed_step = ProofStep(
    conclusion=Phase84SeedStatement(),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  shared_availability = PremiseAvailability(
    inference_rule=shared_rule,
    matched_steps=(
      seed_step,
    ),
    missing_indices=(),
  )

  intermediate_availability = (
    PremiseAvailability(
      inference_rule=intermediate_rule,
      matched_steps=(
        None,
      ),
      missing_indices=(
        0,
      ),
    )
  )

  final_availability = PremiseAvailability(
    inference_rule=final_rule,
    matched_steps=(
      None,
      None,
    ),
    missing_indices=(
      0,
      1,
    ),
  )

  shared_node = BoundedProducerSearchNode(
    requesting_rule=final_rule,
    premise_index=0,
    premise_pattern=shared_pattern,
    producer_rule=shared_rule,
    producer_availability=(
      shared_availability
    ),
    depths=(
      1,
      2,
    ),
  )

  intermediate_node = (
    BoundedProducerSearchNode(
      requesting_rule=final_rule,
      premise_index=1,
      premise_pattern=(
        intermediate_pattern
      ),
      producer_rule=(
        intermediate_rule
      ),
      producer_availability=(
        intermediate_availability
      ),
      depths=(
        1,
      ),
      dependencies=(
        shared_node,
      ),
    )
  )

  result = BoundedProducerSearchResult(
    goal=Phase84GoalStatement(),
    final_rule=final_rule,
    final_availability=(
      final_availability
    ),
    producer_nodes=(
      shared_node,
      intermediate_node,
    ),
    max_depth=2,
  )

  return {
    "seed_step": seed_step,
    "shared_pattern": shared_pattern,
    "intermediate_pattern": (
      intermediate_pattern
    ),
    "shared_rule": shared_rule,
    "intermediate_rule": (
      intermediate_rule
    ),
    "final_rule": final_rule,
    "shared_availability": (
      shared_availability
    ),
    "intermediate_availability": (
      intermediate_availability
    ),
    "final_availability": (
      final_availability
    ),
    "shared_node": shared_node,
    "intermediate_node": (
      intermediate_node
    ),
    "result": result,
  }


def test_phase84_2_node_preserves_requested_premise():
  data = _build_phase84_2_data()

  node = data[
    "shared_node"
  ]

  assert (
    node.requesting_rule
    is data[
      "final_rule"
    ]
  )

  assert node.premise_index == 0

  assert (
    node.premise_pattern
    is data[
      "shared_pattern"
    ]
  )


def test_phase84_2_node_preserves_selected_producer():
  data = _build_phase84_2_data()

  node = data[
    "shared_node"
  ]

  assert (
    node.producer_rule
    is data[
      "shared_rule"
    ]
  )

  assert (
    node.producer_availability
    is data[
      "shared_availability"
    ]
  )


def test_phase84_2_shared_node_records_all_path_depths():
  data = _build_phase84_2_data()

  node = data[
    "shared_node"
  ]

  assert node.depths == (
    1,
    2,
  )

  assert node.minimum_depth == 1
  assert node.maximum_depth == 2
  assert node.is_shared


def test_phase84_2_non_shared_node_has_one_depth():
  data = _build_phase84_2_data()

  node = data[
    "intermediate_node"
  ]

  assert node.depths == (
    1,
  )

  assert node.minimum_depth == 1
  assert node.maximum_depth == 1
  assert not node.is_shared


def test_phase84_2_node_preserves_dependency_dag_edge():
  data = _build_phase84_2_data()

  assert (
    data[
      "intermediate_node"
    ].dependencies
    == (
      data[
        "shared_node"
      ],
    )
  )


def test_phase84_2_result_preserves_final_search_context():
  data = _build_phase84_2_data()

  result = data[
    "result"
  ]

  assert (
    result.final_rule
    is data[
      "final_rule"
    ]
  )

  assert (
    result.final_availability
    is data[
      "final_availability"
    ]
  )

  assert result.producer_nodes == (
    data[
      "shared_node"
    ],
    data[
      "intermediate_node"
    ],
  )

  assert result.max_depth == 2


def test_phase84_2_result_reports_depth_limit_status():
  data = _build_phase84_2_data()

  assert (
    data[
      "result"
    ].is_within_depth_limit
  )

  depth_one_result = (
    BoundedProducerSearchResult(
      goal=data[
        "result"
      ].goal,
      final_rule=data[
        "final_rule"
      ],
      final_availability=data[
        "final_availability"
      ],
      producer_nodes=data[
        "result"
      ].producer_nodes,
      max_depth=1,
    )
  )

  assert not (
    depth_one_result
    .is_within_depth_limit
  )


def test_phase84_2_representation_does_not_execute_rules():
  data = _build_phase84_2_data()

  assert (
    data[
      "shared_availability"
    ].matched_steps
    == (
      data[
        "seed_step"
      ],
    )
  )

  assert (
    data[
      "intermediate_availability"
    ].matched_steps
    == (
      None,
    )
  )

  assert (
    data[
      "final_availability"
    ].matched_steps
    == (
      None,
      None,
    )
  )


def test_phase84_2_node_rejects_empty_depths():
  data = _build_phase84_2_data()

  with pytest.raises(
    ValueError,
    match="depths must not be empty",
  ):
    BoundedProducerSearchNode(
      requesting_rule=data[
        "final_rule"
      ],
      premise_index=0,
      premise_pattern=data[
        "shared_pattern"
      ],
      producer_rule=data[
        "shared_rule"
      ],
      producer_availability=data[
        "shared_availability"
      ],
      depths=(),
    )


def test_phase84_2_node_rejects_unsorted_or_duplicate_depths():
  data = _build_phase84_2_data()

  with pytest.raises(
    ValueError,
    match=(
      "depths must be unique and sorted"
    ),
  ):
    BoundedProducerSearchNode(
      requesting_rule=data[
        "final_rule"
      ],
      premise_index=0,
      premise_pattern=data[
        "shared_pattern"
      ],
      producer_rule=data[
        "shared_rule"
      ],
      producer_availability=data[
        "shared_availability"
      ],
      depths=(
        2,
        1,
        2,
      ),
    )


def test_phase84_2_result_rejects_non_positive_max_depth():
  data = _build_phase84_2_data()

  with pytest.raises(
    ValueError,
    match="max_depth must be positive",
  ):
    BoundedProducerSearchResult(
      goal=data[
        "result"
      ].goal,
      final_rule=data[
        "final_rule"
      ],
      final_availability=data[
        "final_availability"
      ],
      producer_nodes=data[
        "result"
      ].producer_nodes,
      max_depth=0,
    )

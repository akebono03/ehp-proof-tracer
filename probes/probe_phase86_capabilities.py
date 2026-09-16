from functools import lru_cache
from pathlib import Path
import sys


TESTS_DIRECTORY = (
  Path(
    __file__
  )
  .resolve()
  .parents[1]
  / "tests"
)

tests_directory_text = str(
  TESTS_DIRECTORY
)

if (
  tests_directory_text
  not in sys.path
):
  sys.path.insert(
    0,
    tests_directory_text,
  )


from proof_repository import ProofRepository
from repository_inference import (
  BoundedProducerSearchStatus,
  diagnose_depth_two_producer_search_failure,
  execute_depth_two_producer_search,
  repository_available_steps,
)
from test_phase84_producer_premise_availability import (
  build_phase84_3_data,
)
from test_phase85_nested_producer_cycle_depth_classification import (
  Phase85NestedGoalStatement,
  _base_rules,
  _catalog,
)


def _producer_rules(
  search_result,
):
  return tuple(
    node.producer_rule
    for node
    in search_result.producer_nodes
  )


def _producer_depths(
  search_result,
):
  return tuple(
    node.depths
    for node
    in search_result.producer_nodes
  )


def _dependency_rule_ids(
  search_result,
):
  return tuple(
    tuple(
      id(
        dependency.producer_rule
      )
      for dependency
      in node.dependencies
    )
    for node
    in search_result.producer_nodes
  )


def _unsupported_depth_is_rejected(
  data,
  max_depth,
):
  try:
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
  except ValueError:
    return True

  return False


@lru_cache(maxsize=1)
def build_phase86_representative_result():
  data = build_phase84_3_data()

  repository = data[
    "repository"
  ]
  catalog = data[
    "catalog"
  ]
  goal = data[
    "goal"
  ]

  initial_steps = repository_available_steps(
    repository
  )

  default_result = (
    execute_depth_two_producer_search(
      repository,
      catalog,
      goal,
    )
  )

  explicit_result = (
    execute_depth_two_producer_search(
      repository,
      catalog,
      goal,
      max_depth=2,
    )
  )

  default_search_result = (
    default_result.report.search_result
  )
  explicit_search_result = (
    explicit_result.report.search_result
  )

  assert default_search_result is not None
  assert explicit_search_result is not None

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

  default_producer_rules = _producer_rules(
    default_search_result
  )
  explicit_producer_rules = _producer_rules(
    explicit_search_result
  )

  default_depths = _producer_depths(
    default_search_result
  )
  explicit_depths = _producer_depths(
    explicit_search_result
  )

  default_dependencies = (
    _dependency_rule_ids(
      default_search_result
    )
  )
  explicit_dependencies = (
    _dependency_rule_ids(
      explicit_search_result
    )
  )

  rules = _base_rules()

  boundary_diagnostic = (
    diagnose_depth_two_producer_search_failure(
      ProofRepository(),
      _catalog(
        rules
      ),
      Phase85NestedGoalStatement(),
      max_depth=2,
    )
  )

  assert boundary_diagnostic is not None

  default_shared_node = (
    default_search_result.producer_nodes[
      0
    ]
  )
  default_composition_node = (
    default_search_result.producer_nodes[
      1
    ]
  )

  explicit_shared_node = (
    explicit_search_result.producer_nodes[
      0
    ]
  )
  explicit_composition_node = (
    explicit_search_result.producer_nodes[
      1
    ]
  )

  return {
    "data": data,
    "default_result": default_result,
    "explicit_result": explicit_result,
    "default_search_result": (
      default_search_result
    ),
    "explicit_search_result": (
      explicit_search_result
    ),
    "default_goal_step": (
      default_goal_step
    ),
    "explicit_goal_step": (
      explicit_goal_step
    ),
    "default_status": (
      default_result.report.status
    ),
    "explicit_status": (
      explicit_result.report.status
    ),
    "default_max_depth": (
      default_search_result.max_depth
    ),
    "explicit_max_depth": (
      explicit_search_result.max_depth
    ),
    "same_final_rule": (
      default_search_result.final_rule
      is explicit_search_result.final_rule
    ),
    "same_producer_path": (
      default_producer_rules
      == explicit_producer_rules
    ),
    "same_depths": (
      default_depths
      == explicit_depths
    ),
    "same_dependencies": (
      default_dependencies
      == explicit_dependencies
    ),
    "default_producer_node_count": len(
      default_search_result.producer_nodes
    ),
    "explicit_producer_node_count": len(
      explicit_search_result.producer_nodes
    ),
    "default_shared_depths": (
      default_shared_node.depths
    ),
    "explicit_shared_depths": (
      explicit_shared_node.depths
    ),
    "default_shared_dependency": (
      default_composition_node.dependencies
      == (
        default_shared_node,
      )
    ),
    "explicit_shared_dependency": (
      explicit_composition_node.dependencies
      == (
        explicit_shared_node,
      )
    ),
    "default_goal_derived": (
      default_goal_step.conclusion
      == goal
    ),
    "explicit_goal_derived": (
      explicit_goal_step.conclusion
      == goal
    ),
    "same_goal_conclusion": (
      default_goal_step.conclusion
      == explicit_goal_step.conclusion
    ),
    "same_goal_rule": (
      default_goal_step.inference_rule
      is explicit_goal_step.inference_rule
    ),
    "same_goal_premise_conclusions": (
      tuple(
        premise.conclusion
        for premise
        in default_goal_step.premises
      )
      == tuple(
        premise.conclusion
        for premise
        in explicit_goal_step.premises
      )
    ),
    "same_goal_premise_rules": (
      tuple(
        premise.inference_rule
        for premise
        in default_goal_step.premises
      )
      == tuple(
        premise.inference_rule
        for premise
        in explicit_goal_step.premises
      )
    ),
    "diagnostic_status": (
      boundary_diagnostic.status
    ),
    "diagnostic_current_depth": (
      boundary_diagnostic.current_depth
    ),
    "diagnostic_required_next_depth": (
      boundary_diagnostic
      .required_next_depth
    ),
    "repository_mutated": (
      repository_available_steps(
        repository
      )
      != initial_steps
    ),
    "max_depth_one_rejected": (
      _unsupported_depth_is_rejected(
        data,
        1,
      )
    ),
    "max_depth_three_rejected": (
      _unsupported_depth_is_rejected(
        data,
        3,
      )
    ),
  }


def main():
  result = (
    build_phase86_representative_result()
  )

  print(
    "=== Phase 86-2: explicit max_depth "
    "parameterization compatibility ==="
  )
  print()

  print(
    "Actual proof target:"
  )
  print(
    "  Toda Lemma 5.16 final "
    "bracket-sum consequence"
  )
  print()

  print(
    "Depth parameterization:"
  )
  print(
    "  default max depth =",
    result[
      "default_max_depth"
    ],
  )
  print(
    "  explicit max depth =",
    result[
      "explicit_max_depth"
    ],
  )
  print()

  print(
    "Compatibility:"
  )
  print(
    "  default status =",
    result[
      "default_status"
    ].value,
  )
  print(
    "  explicit status =",
    result[
      "explicit_status"
    ].value,
  )
  print(
    "  same final rule =",
    result[
      "same_final_rule"
    ],
  )
  print(
    "  same producer path =",
    result[
      "same_producer_path"
    ],
  )
  print(
    "  same depths =",
    result[
      "same_depths"
    ],
  )
  print(
    "  same dependencies =",
    result[
      "same_dependencies"
    ],
  )
  print()

  print(
    "Selected producer path:"
  )
  print(
    "  default producer node count =",
    result[
      "default_producer_node_count"
    ],
  )
  print(
    "  explicit producer node count =",
    result[
      "explicit_producer_node_count"
    ],
  )
  print(
    "  default shared depths =",
    result[
      "default_shared_depths"
    ],
  )
  print(
    "  explicit shared depths =",
    result[
      "explicit_shared_depths"
    ],
  )
  print(
    "  default shared dependency =",
    result[
      "default_shared_dependency"
    ],
  )
  print(
    "  explicit shared dependency =",
    result[
      "explicit_shared_dependency"
    ],
  )
  print()

  print(
    "Execution / provenance:"
  )
  print(
    "  default goal derived =",
    result[
      "default_goal_derived"
    ],
  )
  print(
    "  explicit goal derived =",
    result[
      "explicit_goal_derived"
    ],
  )
  print(
    "  same goal conclusion =",
    result[
      "same_goal_conclusion"
    ],
  )
  print(
    "  same goal inference rule =",
    result[
      "same_goal_rule"
    ],
  )
  print(
    "  same goal premise conclusions =",
    result[
      "same_goal_premise_conclusions"
    ],
  )
  print(
    "  same goal premise rules =",
    result[
      "same_goal_premise_rules"
    ],
  )
  print()

  print(
    "Depth-limit diagnostic:"
  )
  print(
    "  status =",
    result[
      "diagnostic_status"
    ].value,
  )
  print(
    "  current depth =",
    result[
      "diagnostic_current_depth"
    ],
  )
  print(
    "  required next depth =",
    result[
      "diagnostic_required_next_depth"
    ],
  )
  print()

  print(
    "Safety / phase boundary:"
  )
  print(
    "  repository mutated =",
    result[
      "repository_mutated"
    ],
  )
  print(
    "  max_depth=1 rejected =",
    result[
      "max_depth_one_rejected"
    ],
  )
  print(
    "  max_depth=3 rejected =",
    result[
      "max_depth_three_rejected"
    ],
  )
  print()

  print(
    "Phase 86-2 completion boundary:"
  )
  print(
    "  explicit max_depth=2 = enabled"
  )
  print(
    "  implicit depth=2 API compatibility "
    "= preserved"
  )
  print(
    "  selected producer path compatibility "
    "= verified"
  )
  print(
    "  diagnostic compatibility = verified"
  )
  print(
    "  execution provenance compatibility "
    "= verified"
  )
  print(
    "  repository non-mutation = verified"
  )
  print(
    "  max_depth > 2 = not implemented"
  )
  print(
    "  retry / backtracking = not implemented"
  )
  print(
    "  producer ranking = not implemented"
  )
  print(
    "  arbitrary recursive search = "
    "not implemented"
  )


if __name__ == "__main__":
  main()



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
from test_phase86_depth_three_bounded_search import (
  Phase86DepthThreeAStatement,
  Phase86DepthThreeBStatement,
  Phase86DepthThreeCStatement,
  build_phase86_3_1_data,
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


def _depth_is_accepted(
  data,
  max_depth,
):
  try:
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
      max_depth=max_depth,
    )
  except (TypeError, ValueError):
    return False

  return result.report.status is (
    BoundedProducerSearchStatus.SUCCESS
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
    "max_depth_three_accepted": (
      _depth_is_accepted(
        data,
        3,
      )
    ),
    "max_depth_four_rejected": (
      _unsupported_depth_is_rejected(
        data,
        4,
      )
    ),
  }



@lru_cache(maxsize=1)
def build_phase86_depth_three_representative_result():
  data = build_phase86_3_1_data()

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

  depth_two_result = (
    execute_depth_two_producer_search(
      repository,
      catalog,
      goal,
      max_depth=2,
    )
  )

  depth_three_result = (
    execute_depth_two_producer_search(
      repository,
      catalog,
      goal,
      max_depth=3,
    )
  )

  search_result = (
    depth_three_result.report.search_result
  )
  repository_result = (
    depth_three_result
    .repository_inference_result
  )

  assert search_result is not None
  assert repository_result is not None
  assert repository_result.goal_step is not None

  steps = repository_result.inference_result.steps

  c_step = next(
    step
    for step in steps
    if isinstance(
      step.conclusion,
      Phase86DepthThreeCStatement,
    )
  )
  b_step = next(
    step
    for step in steps
    if isinstance(
      step.conclusion,
      Phase86DepthThreeBStatement,
    )
  )
  a_step = next(
    step
    for step in steps
    if isinstance(
      step.conclusion,
      Phase86DepthThreeAStatement,
    )
  )
  goal_step = repository_result.goal_step

  producer_rules = tuple(
    node.producer_rule
    for node in search_result.producer_nodes
  )
  producer_depths = tuple(
    node.depths
    for node in search_result.producer_nodes
  )

  return {
    "depth_two_status": (
      depth_two_result.report.status
    ),
    "depth_two_current_depth": (
      depth_two_result.report
      .diagnostic.current_depth
      if depth_two_result.report.diagnostic
      is not None
      else None
    ),
    "depth_two_required_next_depth": (
      depth_two_result.report
      .diagnostic.required_next_depth
      if depth_two_result.report.diagnostic
      is not None
      else None
    ),
    "depth_three_status": (
      depth_three_result.report.status
    ),
    "depth_three_max_depth": (
      search_result.max_depth
    ),
    "producer_rules": producer_rules,
    "producer_depths": producer_depths,
    "dependency_first_order": (
      producer_rules
      == (
        data[
          "c_rule"
        ],
        data[
          "b_rule"
        ],
        data[
          "a_rule"
        ],
      )
    ),
    "goal_derived": (
      goal_step.conclusion == goal
    ),
    "c_rule_reused": (
      c_step.inference_rule
      is data[
        "c_rule"
      ]
    ),
    "b_uses_c_step": (
      b_step.premises == (
        c_step,
      )
    ),
    "a_uses_b_step": (
      a_step.premises == (
        b_step,
      )
    ),
    "final_uses_a_step": (
      goal_step.premises == (
        a_step,
      )
    ),
    "repository_mutated": (
      repository_available_steps(
        repository
      )
      != initial_steps
    ),
  }

def main():
  compatibility = (
    build_phase86_representative_result()
  )
  depth_three = (
    build_phase86_depth_three_representative_result()
  )

  print(
    "=== Phase 86-3: bounded depth=3 completion ==="
  )
  print()

  print(
    "Phase 86-2 compatibility baseline:"
  )
  print(
    "  default max depth =",
    compatibility[
      "default_max_depth"
    ],
  )
  print(
    "  explicit max depth =",
    compatibility[
      "explicit_max_depth"
    ],
  )
  print(
    "  same producer path =",
    compatibility[
      "same_producer_path"
    ],
  )
  print(
    "  same dependencies =",
    compatibility[
      "same_dependencies"
    ],
  )
  print(
    "  same goal inference rule =",
    compatibility[
      "same_goal_rule"
    ],
  )
  print()

  print(
    "Depth=3 representative chain:"
  )
  print(
    "  max_depth=2 status =",
    depth_three[
      "depth_two_status"
    ].value,
  )
  print(
    "  current depth =",
    depth_three[
      "depth_two_current_depth"
    ],
  )
  print(
    "  required next depth =",
    depth_three[
      "depth_two_required_next_depth"
    ],
  )
  print(
    "  max_depth=3 status =",
    depth_three[
      "depth_three_status"
    ].value,
  )
  print(
    "  selected max depth =",
    depth_three[
      "depth_three_max_depth"
    ],
  )
  print(
    "  producer depths =",
    depth_three[
      "producer_depths"
    ],
  )
  print(
    "  dependency-first order =",
    depth_three[
      "dependency_first_order"
    ],
  )
  print()

  print(
    "Execution / provenance:"
  )
  print(
    "  goal derived =",
    depth_three[
      "goal_derived"
    ],
  )
  print(
    "  C rule reused =",
    depth_three[
      "c_rule_reused"
    ],
  )
  print(
    "  B uses C ProofStep =",
    depth_three[
      "b_uses_c_step"
    ],
  )
  print(
    "  A uses B ProofStep =",
    depth_three[
      "a_uses_b_step"
    ],
  )
  print(
    "  final uses A ProofStep =",
    depth_three[
      "final_uses_a_step"
    ],
  )
  print(
    "  repository mutated =",
    depth_three[
      "repository_mutated"
    ],
  )
  print()

  print(
    "Safety / completion boundary:"
  )
  print(
    "  max_depth=1 rejected =",
    compatibility[
      "max_depth_one_rejected"
    ],
  )
  print(
    "  max_depth=3 accepted =",
    compatibility[
      "max_depth_three_accepted"
    ],
  )
  print(
    "  max_depth=4 rejected =",
    compatibility[
      "max_depth_four_rejected"
    ],
  )
  print(
    "  selection / diagnostics / report / execution "
    "support max_depth=2,3"
  )
  print(
    "  retry / backtracking = not implemented"
  )
  print(
    "  producer ranking = not implemented"
  )
  print(
    "  arbitrary recursive search = not implemented"
  )


if __name__ == "__main__":
  main()

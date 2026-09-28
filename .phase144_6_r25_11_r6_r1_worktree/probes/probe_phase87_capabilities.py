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


from repository_inference import (
  BoundedProducerSearchStatus,
  FiniteProducerRetryPolicy,
  execute_depth_two_producer_search,
  repository_available_steps,
)
from test_phase87_selection_side_finite_retry import (
  Phase87SelectionAStatement,
  build_phase87_3_data,
)


@lru_cache(maxsize=1)
def build_phase87_representative_result():
  data = build_phase87_3_data()

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

  no_policy_result = (
    execute_depth_two_producer_search(
      repository,
      catalog,
      goal,
      max_depth=2,
    )
  )

  one_attempt_result = (
    execute_depth_two_producer_search(
      repository,
      catalog,
      goal,
      max_depth=2,
      retry_policy=FiniteProducerRetryPolicy(
        max_attempts=1,
      ),
    )
  )

  two_attempt_result = (
    execute_depth_two_producer_search(
      repository,
      catalog,
      goal,
      max_depth=2,
      retry_policy=FiniteProducerRetryPolicy(
        max_attempts=2,
      ),
    )
  )

  search_result = (
    two_attempt_result.report.search_result
  )
  repository_result = (
    two_attempt_result
    .repository_inference_result
  )

  assert search_result is not None
  assert repository_result is not None
  assert repository_result.goal_step is not None

  steps = repository_result.inference_result.steps

  a_step = next(
    step
    for step in steps
    if isinstance(
      step.conclusion,
      Phase87SelectionAStatement,
    )
  )
  goal_step = repository_result.goal_step

  executed_rules = tuple(
    step.inference_rule
    for step in steps
    if step.inference_rule is not None
  )

  return {
    "no_policy_status": (
      no_policy_result.report.status
    ),
    "one_attempt_status": (
      one_attempt_result.report.status
    ),
    "two_attempt_status": (
      two_attempt_result.report.status
    ),
    "selected_rules": tuple(
      node.producer_rule
      for node
      in search_result.producer_nodes
    ),
    "selected_second_candidate": (
      tuple(
        node.producer_rule
        for node
        in search_result.producer_nodes
      )
      == (
        data[
          "second_a_rule"
        ],
      )
    ),
    "goal_derived": (
      goal_step.conclusion
      == goal
    ),
    "selected_rule_reused": (
      a_step.inference_rule
      is data[
        "second_a_rule"
      ]
    ),
    "final_uses_selected_step": (
      goal_step.premises
      == (
        a_step,
      )
    ),
    "final_rule_reused": (
      goal_step.inference_rule
      is data[
        "final_rule"
      ]
    ),
    "failed_first_candidate_executed": (
      data[
        "first_a_rule"
      ]
      in executed_rules
    ),
    "failed_b_branch_executed": (
      data[
        "b_rule"
      ]
      in executed_rules
    ),
    "failed_c_branch_executed": (
      data[
        "c_rule"
      ]
      in executed_rules
    ),
    "repository_mutated": (
      repository_available_steps(
        repository
      )
      != initial_steps
    ),
  }


def main():
  result = (
    build_phase87_representative_result()
  )

  print(
    "=== Phase 87: finite producer retry completion ==="
  )
  print()

  print(
    "Ambiguity / retry boundary:"
  )
  print(
    "  no policy status =",
    result[
      "no_policy_status"
    ].value,
  )
  print(
    "  max_attempts=1 status =",
    result[
      "one_attempt_status"
    ].value,
  )
  print(
    "  max_attempts=2 status =",
    result[
      "two_attempt_status"
    ].value,
  )
  print()

  print(
    "Selected path:"
  )
  print(
    "  second producer selected =",
    result[
      "selected_second_candidate"
    ],
  )
  print(
    "  goal derived =",
    result[
      "goal_derived"
    ],
  )
  print()

  print(
    "Execution / provenance:"
  )
  print(
    "  selected producer rule reused =",
    result[
      "selected_rule_reused"
    ],
  )
  print(
    "  final uses selected ProofStep =",
    result[
      "final_uses_selected_step"
    ],
  )
  print(
    "  final rule reused =",
    result[
      "final_rule_reused"
    ],
  )
  print(
    "  failed first candidate executed =",
    result[
      "failed_first_candidate_executed"
    ],
  )
  print(
    "  failed B branch executed =",
    result[
      "failed_b_branch_executed"
    ],
  )
  print(
    "  failed C branch executed =",
    result[
      "failed_c_branch_executed"
    ],
  )
  print(
    "  repository mutated =",
    result[
      "repository_mutated"
    ],
  )
  print()

  print(
    "Completion boundary:"
  )
  print(
    "  finite explicit retry = implemented"
  )
  print(
    "  catalog-order attempts = implemented"
  )
  print(
    "  retry exhaustion diagnostic = implemented"
  )
  print(
    "  selected-path execution = implemented"
  )
  print(
    "  general backtracking = not implemented"
  )
  print(
    "  producer ranking = not implemented"
  )
  print(
    "  proof-cost model = not implemented"
  )
  print(
    "  best-proof selection = not implemented"
  )
  print(
    "  DFS / BFS / A* = not implemented"
  )


if __name__ == "__main__":
  main()

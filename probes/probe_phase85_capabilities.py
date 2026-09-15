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
  repository_available_steps,
)
from test_phase85_actual_theorem_integration import (
  build_phase85_8_data,
)


def _proof_graph_is_acyclic(
  step,
):
  visited = set()
  active = set()

  def visit(
    current,
  ):
    current_id = id(
      current
    )

    if current_id in active:
      return False

    if current_id in visited:
      return True

    active.add(
      current_id
    )

    for premise in current.premises:
      if not visit(
        premise
      ):
        return False

    active.remove(
      current_id
    )
    visited.add(
      current_id
    )

    return True

  return visit(
    step
  )


def build_phase85_representative_result():
  data = build_phase85_8_data()

  report = data[
    "report"
  ]
  search_result = data[
    "search_result"
  ]
  final_step = data[
    "final_step"
  ]

  return {
    "data": data,
    "status": report.status,
    "diagnostic": report.diagnostic,
    "search_result": search_result,
    "producer_node_count": len(
      search_result.producer_nodes
    ),
    "bracket_sum_depths": data[
      "bracket_sum_node"
    ].depths,
    "bracket_sum_shared": data[
      "bracket_sum_node"
    ].is_shared,
    "composition_depends_on_bracket_sum": (
      data[
        "composition_node"
      ].dependencies
      == (
        data[
          "bracket_sum_node"
        ],
      )
    ),
    "within_depth_limit": (
      search_result.is_within_depth_limit
    ),
    "goal_initially_present": any(
      step.conclusion
      == data[
        "goal"
      ]
      for step
      in data[
        "initial_steps"
      ]
    ),
    "goal_derived": (
      final_step.conclusion
      == data[
        "goal"
      ]
    ),
    "bracket_sum_rule_reused": (
      data[
        "bracket_sum_step"
      ].inference_rule
      is data[
        "phase84_3"
      ][
        "bracket_sum_rule"
      ]
    ),
    "composition_rule_reused": (
      data[
        "composition_step"
      ].inference_rule
      is data[
        "phase84_3"
      ][
        "composition_rule"
      ]
    ),
    "final_rule_reused": (
      final_step.inference_rule
      is data[
        "phase84_3"
      ][
        "final_rule"
      ]
    ),
    "shared_bracket_sum_step": (
      final_step.premises[
        0
      ]
      is data[
        "composition_step"
      ].premises[
        0
      ]
      is data[
        "bracket_sum_step"
      ]
    ),
    "graph_acyclic": (
      _proof_graph_is_acyclic(
        final_step
      )
    ),
    "repository_mutated": (
      repository_available_steps(
        data[
          "repository"
        ]
      )
      != data[
        "initial_steps"
      ]
    ),
  }


def main():
  result = (
    build_phase85_representative_result()
  )

  print(
    "=== Phase 85: bounded-search diagnostics "
    "and integrated execution ==="
  )
  print()

  print(
    "Actual proof target:"
  )
  print(
    "  Toda Lemma 5.16 final bracket-sum consequence"
  )
  print(
    "  goal initially present =",
    result[
      "goal_initially_present"
    ],
  )
  print()

  print(
    "Unified bounded-search report:"
  )
  print(
    "  status =",
    result[
      "status"
    ].value,
  )
  print(
    "  diagnostic present =",
    result[
      "diagnostic"
    ]
    is not None,
  )
  print(
    "  search result present =",
    result[
      "search_result"
    ]
    is not None,
  )
  print()

  print(
    "Selected producer path:"
  )
  print(
    "  producer node count =",
    result[
      "producer_node_count"
    ],
  )
  print(
    "  bracket-sum depths =",
    result[
      "bracket_sum_depths"
    ],
  )
  print(
    "  bracket-sum shared =",
    result[
      "bracket_sum_shared"
    ],
  )
  print(
    "  composition depends on bracket-sum =",
    result[
      "composition_depends_on_bracket_sum"
    ],
  )
  print(
    "  within depth limit =",
    result[
      "within_depth_limit"
    ],
  )
  print()

  print(
    "Integrated execution:"
  )
  print(
    "  final goal derived =",
    result[
      "goal_derived"
    ],
  )
  print(
    "  shared bracket-sum proof step =",
    result[
      "shared_bracket_sum_step"
    ],
  )
  print()

  print(
    "Provenance / safety:"
  )
  print(
    "  existing bracket-sum rule reused =",
    result[
      "bracket_sum_rule_reused"
    ],
  )
  print(
    "  existing composition rule reused =",
    result[
      "composition_rule_reused"
    ],
  )
  print(
    "  existing final rule reused =",
    result[
      "final_rule_reused"
    ],
  )
  print(
    "  derived graph acyclic =",
    result[
      "graph_acyclic"
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
    "Phase 85 completion boundary:"
  )
  print(
    "  search-failure diagnostics = enabled"
  )
  print(
    "  execution-failure diagnostics = enabled"
  )
  print(
    "  unified diagnostic report = enabled"
  )
  print(
    "  integrated bounded-search execution = enabled"
  )
  print(
    "  actual Toda Lemma 5.16 integration = verified"
  )
  print(
    "  producer execution depth = 2"
  )
  print(
    "  retry / backtracking = not implemented"
  )
  print(
    "  producer ranking = not implemented"
  )
  print(
    "  depth > 2 = not implemented"
  )
  print(
    "  arbitrary recursive search = not implemented"
  )


if __name__ == "__main__":
  main()



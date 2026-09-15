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


from proof import ProofRule
from repository_inference import (
  repository_available_steps,
  select_unique_depth_two_producer_chain,
)
from test_phase84_actual_theorem_integration import (
  build_phase84_6_data,
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


def build_phase84_representative_result():
  data = build_phase84_6_data()
  phase84_3 = data[
    "phase84_3"
  ]

  search_result = (
    select_unique_depth_two_producer_chain(
      data[
        "repository"
      ],
      phase84_3[
        "catalog"
      ],
      data[
        "goal"
      ],
    )
  )

  assert search_result is not None

  bracket_sum_node = next(
    node
    for node in search_result.producer_nodes
    if (
      node.producer_rule
      is phase84_3[
        "bracket_sum_rule"
      ]
    )
  )

  composition_node = next(
    node
    for node in search_result.producer_nodes
    if (
      node.producer_rule
      is phase84_3[
        "composition_rule"
      ]
    )
  )

  bracket_sum_step = data[
    "bracket_sum_step"
  ]
  composition_step = data[
    "composition_step"
  ]
  final_step = data[
    "final_step"
  ]
  initial_steps = data[
    "initial_steps"
  ]

  return {
    "data": data,
    "search_result": search_result,
    "bracket_sum_node": bracket_sum_node,
    "composition_node": composition_node,
    "goal_initially_present": any(
      step.conclusion
      == data[
        "goal"
      ]
      for step in initial_steps
    ),
    "bracket_sum_initially_present": any(
      step.conclusion
      == bracket_sum_step.conclusion
      for step in initial_steps
    ),
    "composition_initially_present": any(
      step.conclusion
      == composition_step.conclusion
      for step in initial_steps
    ),
    "bracket_sum_derived": (
      bracket_sum_step.rule
      == ProofRule.INFERENCE
    ),
    "composition_derived": (
      composition_step.rule
      == ProofRule.INFERENCE
    ),
    "final_derived": (
      final_step.rule
      == ProofRule.INFERENCE
    ),
    "bracket_sum_rule_reused": (
      bracket_sum_step.inference_rule
      is phase84_3[
        "bracket_sum_rule"
      ]
    ),
    "composition_rule_reused": (
      composition_step.inference_rule
      is phase84_3[
        "composition_rule"
      ]
    ),
    "final_rule_reused": (
      final_step.inference_rule
      is phase84_3[
        "final_rule"
      ]
    ),
    "shared_bracket_sum_step": (
      final_step.premises[
        0
      ]
      is composition_step.premises[
        0
      ]
      is bracket_sum_step
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
      != initial_steps
    ),
  }


def main():
  result = (
    build_phase84_representative_result()
  )
  search_result = result[
    "search_result"
  ]
  bracket_sum_node = result[
    "bracket_sum_node"
  ]
  composition_node = result[
    "composition_node"
  ]

  print(
    "=== Phase 84: bounded depth=2 producer search ==="
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
    "Bounded producer-chain selection:"
  )
  print(
    "  producer node count =",
    len(
      search_result.producer_nodes
    ),
  )
  print(
    "  bracket-sum depths =",
    bracket_sum_node.depths,
  )
  print(
    "  bracket-sum shared =",
    bracket_sum_node.is_shared,
  )
  print(
    "  composition depths =",
    composition_node.depths,
  )
  print(
    "  composition depends on bracket-sum =",
    composition_node.dependencies
    == (
      bracket_sum_node,
    ),
  )
  print(
    "  within depth limit =",
    search_result.is_within_depth_limit,
  )
  print()

  print(
    "Bounded depth=2 execution:"
  )
  print(
    "  bracket-sum initially present =",
    result[
      "bracket_sum_initially_present"
    ],
  )
  print(
    "  composition initially present =",
    result[
      "composition_initially_present"
    ],
  )
  print(
    "  bracket-sum derived =",
    result[
      "bracket_sum_derived"
    ],
  )
  print(
    "  composition derived =",
    result[
      "composition_derived"
    ],
  )
  print(
    "  final goal derived =",
    result[
      "final_derived"
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
    "Phase 84 completion boundary:"
  )
  print(
    "  producer execution depth = 2"
  )
  print(
    "  unique producer policy = enabled"
  )
  print(
    "  shared dependency reuse = enabled"
  )
  print(
    "  cycle / ambiguity stop = enabled"
  )
  print(
    "  depth > 2 = not implemented"
  )
  print(
    "  arbitrary recursive search = not implemented"
  )
  print(
    "  DFS / BFS / A* = not implemented"
  )
  print(
    "  proof ranking / cost model = not implemented"
  )


if __name__ == "__main__":
  main()

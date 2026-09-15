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
  all_missing_premises_uniquely_producible,
  repository_available_steps,
)
from test_phase83_actual_theorem_integration import (
  build_phase83_5_data,
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


def build_phase83_representative_result():
  data = build_phase83_5_data()

  initial_steps = data[
    "initial_steps"
  ]
  lookups = data[
    "lookups"
  ]
  first_step = data[
    "first_step"
  ]
  second_step = data[
    "second_step"
  ]
  final_step = data[
    "final_step"
  ]

  return {
    "data": data,
    "initial_steps": initial_steps,
    "availability": data[
      "detections"
    ][
      0
    ],
    "lookups": lookups,
    "all_unique": (
      all_missing_premises_uniquely_producible(
        lookups
      )
    ),
    "goal_initially_present": any(
      step.conclusion
      == data[
        "goal"
      ]
      for step in initial_steps
    ),
    "first_initially_present": any(
      step.conclusion
      == first_step.conclusion
      for step in initial_steps
    ),
    "second_initially_present": any(
      step.conclusion
      == second_step.conclusion
      for step in initial_steps
    ),
    "first_is_inference": (
      first_step.rule
      == ProofRule.INFERENCE
    ),
    "second_is_inference": (
      second_step.rule
      == ProofRule.INFERENCE
    ),
    "final_is_inference": (
      final_step.rule
      == ProofRule.INFERENCE
    ),
    "first_rule_reused": (
      first_step.inference_rule
      is data[
        "first_rule"
      ]
    ),
    "second_rule_reused": (
      second_step.inference_rule
      is data[
        "second_rule"
      ]
    ),
    "final_rule_reused": (
      final_step.inference_rule
      is data[
        "final_rule"
      ]
    ),
    "final_uses_both_intermediates": (
      final_step.premises
      == (
        first_step,
        second_step,
      )
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
    build_phase83_representative_result()
  )

  availability = result[
    "availability"
  ]
  lookups = result[
    "lookups"
  ]

  print(
    "=== Phase 83: multiple one-level producers ==="
  )
  print()

  print(
    "Actual proof target:"
  )
  print(
    "  Toda Lemma 5.16 Theorem 3.6 bracket-sum containment"
  )
  print(
    "  goal initially present =",
    result[
      "goal_initially_present"
    ],
  )
  print()

  print(
    "Final-rule premise analysis:"
  )
  print(
    "  missing premise count =",
    len(
      availability.missing_indices
    ),
  )

  for lookup in lookups:
    print(
      "  missing premise",
      lookup.premise_index,
      "=",
      lookup.premise_pattern.statement_type.__name__,
    )
    print(
      "    safe producer candidates =",
      len(
        lookup.producer_rules
      ),
    )

  print(
    "  all missing premises uniquely producible =",
    result[
      "all_unique"
    ],
  )
  print()

  print(
    "Multiple one-level producer execution:"
  )
  print(
    "  first intermediate initially present =",
    result[
      "first_initially_present"
    ],
  )
  print(
    "  second intermediate initially present =",
    result[
      "second_initially_present"
    ],
  )
  print(
    "  first intermediate derived =",
    result[
      "first_is_inference"
    ],
  )
  print(
    "  second intermediate derived =",
    result[
      "second_is_inference"
    ],
  )
  print(
    "  final goal derived =",
    result[
      "final_is_inference"
    ],
  )
  print(
    "  final uses both new intermediates =",
    result[
      "final_uses_both_intermediates"
    ],
  )
  print()

  print(
    "Provenance / safety:"
  )
  print(
    "  existing first producer rule reused =",
    result[
      "first_rule_reused"
    ],
  )
  print(
    "  existing second producer rule reused =",
    result[
      "second_rule_reused"
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
    "Phase 83 completion boundary:"
  )
  print(
    "  multiple missing-premise lookup = enabled"
  )
  print(
    "  all-unique producer policy = enabled"
  )
  print(
    "  multiple one-level producers = enabled"
  )
  print(
    "  producer execution depth = 1"
  )
  print(
    "  final-rule retry = enabled"
  )
  print(
    "  recursive producer search = not implemented"
  )
  print(
    "  depth > 1 = not implemented"
  )
  print(
    "  DFS / BFS / A* = not implemented"
  )
  print(
    "  proof ranking / cost model = not implemented"
  )


if __name__ == "__main__":
  main()

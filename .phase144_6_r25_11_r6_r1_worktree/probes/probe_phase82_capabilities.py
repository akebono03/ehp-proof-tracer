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
  detect_missing_premises,
  repository_available_steps,
)
from rule_catalog import (
  find_premise_producer_rules,
)
from test_phase82_actual_theorem_integration import (
  build_phase82_5_data,
)


def _collect_ancestors(
  step,
):
  ancestors = []
  seen = set()
  stack = list(
    step.premises
  )

  while stack:
    current = stack.pop()
    current_id = id(
      current
    )

    if current_id in seen:
      continue

    seen.add(
      current_id
    )
    ancestors.append(
      current
    )
    stack.extend(
      current.premises
    )

  return tuple(
    ancestors
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


def build_phase82_representative_result():
  data = build_phase82_5_data()

  repository = data[
    "repository"
  ]
  catalog = data[
    "catalog"
  ]
  initial_steps = (
    repository_available_steps(
      repository
    )
  )

  final_rule = data[
    "phase82_3"
  ][
    "final_rule"
  ]

  availability = (
    detect_missing_premises(
      final_rule,
      initial_steps,
    )
  )

  if len(
    availability.missing_patterns
  ) != 1:
    raise RuntimeError(
      "Phase 82 representative final rule "
      "must have exactly one missing premise"
    )

  missing_pattern = (
    availability.missing_patterns[
      0
    ]
  )

  producer_rules = (
    find_premise_producer_rules(
      catalog,
      missing_pattern,
    )
  )

  if len(
    producer_rules
  ) != 1:
    raise RuntimeError(
      "Phase 82 representative missing premise "
      "must have exactly one safe producer"
    )

  intermediate_step = data[
    "intermediate_step"
  ]
  final_step = data[
    "final_step"
  ]

  final_ancestors = (
    _collect_ancestors(
      final_step
    )
  )

  return {
    "data": data,
    "initial_steps": initial_steps,
    "availability": availability,
    "missing_pattern": missing_pattern,
    "producer_rules": producer_rules,
    "intermediate_step": intermediate_step,
    "final_step": final_step,
    "goal_initially_present": any(
      step.conclusion
      == data[
        "goal"
      ]
      for step in initial_steps
    ),
    "intermediate_initially_present": any(
      step.conclusion
      == intermediate_step.conclusion
      for step in initial_steps
    ),
    "intermediate_is_inference": (
      intermediate_step.rule
      == ProofRule.INFERENCE
    ),
    "final_is_inference": (
      final_step.rule
      == ProofRule.INFERENCE
    ),
    "producer_rule_reused": (
      intermediate_step.inference_rule
      is data[
        "phase82_3"
      ][
        "producer_rule"
      ]
    ),
    "final_rule_reused": (
      final_step.inference_rule
      is final_rule
    ),
    "final_uses_new_intermediate": (
      final_step.premises[
        1
      ]
      is intermediate_step
    ),
    "goal_absent_from_ancestors": all(
      ancestor.conclusion
      != final_step.conclusion
      for ancestor in final_ancestors
    ),
    "graph_acyclic": (
      _proof_graph_is_acyclic(
        final_step
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
  result = (
    build_phase82_representative_result()
  )

  data = result[
    "data"
  ]
  availability = result[
    "availability"
  ]

  print(
    "=== Phase 82: one-level goal-directed proof search ==="
  )
  print()

  print(
    "Actual proof target:"
  )
  print(
    "  Toda Lemma 5.16 final consequence"
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
      availability.missing_patterns
    ),
  )
  print(
    "  missing premise index =",
    availability.missing_indices[
      0
    ],
  )
  print(
    "  missing statement type =",
    result[
      "missing_pattern"
    ].statement_type.__name__,
  )
  print()

  print(
    "One-level producer lookup:"
  )
  print(
    "  safe producer candidates =",
    len(
      result[
        "producer_rules"
      ]
    ),
  )
  print(
    "  unique producer selected =",
    len(
      result[
        "producer_rules"
      ]
    )
    == 1,
  )
  print(
    "  existing Phase 77 producer reused =",
    result[
      "producer_rule_reused"
    ],
  )
  print()

  print(
    "Two-step forward execution:"
  )
  print(
    "  intermediate initially present =",
    result[
      "intermediate_initially_present"
    ],
  )
  print(
    "  intermediate derived =",
    result[
      "intermediate_step"
    ]
    is not None,
  )
  print(
    "  intermediate is INFERENCE =",
    result[
      "intermediate_is_inference"
    ],
  )
  print(
    "  final goal derived =",
    result[
      "final_step"
    ]
    is not None,
  )
  print(
    "  final is INFERENCE =",
    result[
      "final_is_inference"
    ],
  )
  print(
    "  existing Phase 77 final rule reused =",
    result[
      "final_rule_reused"
    ],
  )
  print(
    "  final uses newly derived intermediate =",
    result[
      "final_uses_new_intermediate"
    ],
  )
  print()

  print(
    "Provenance / safety:"
  )
  print(
    "  goal absent from ancestry =",
    result[
      "goal_absent_from_ancestors"
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
    "Phase 82 completion boundary:"
  )
  print(
    "  missing-premise detection = enabled"
  )
  print(
    "  one-level producer lookup = enabled"
  )
  print(
    "  unique-producer safety policy = enabled"
  )
  print(
    "  one-level intermediate generation = enabled"
  )
  print(
    "  final-rule retry = enabled"
  )
  print(
    "  recursive producer search = not implemented"
  )
  print(
    "  arbitrary-depth backward chaining = not implemented"
  )
  print(
    "  DFS / BFS / A* = not implemented"
  )
  print(
    "  proof ranking / cost model = not implemented"
  )
  print(
    "  persistent search cache = not implemented"
  )
  print(
    "  automatic proof narrative = not implemented"
  )


if __name__ == "__main__":
  main()

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


from test_phase80_actual_proof_integration import (
  build_phase80_5_data,
)
from repository_inference import (
  derive_goal_from_repository,
  repository_available_steps,
)
from proof import ProofRule


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


def build_phase80_representative_result():
  data = build_phase80_5_data()

  initial_steps = (
    repository_available_steps(
      data[
        "repository"
      ]
    )
  )

  initial_goal_present = any(
    step.conclusion
    == data[
      "goal"
    ]
    for step in initial_steps
  )

  result = derive_goal_from_repository(
    data[
      "repository"
    ],
    (
      data[
        "final_rule"
      ],
    ),
    data[
      "goal"
    ],
  )

  goal_step = result.goal_step

  if goal_step is None:
    raise RuntimeError(
      "Phase 80 representative goal "
      "was not derived"
    )

  ancestors = _collect_ancestors(
    goal_step
  )

  return {
    "data": data,
    "initial_steps": initial_steps,
    "initial_goal_present": (
      initial_goal_present
    ),
    "result": result,
    "goal_step": goal_step,
    "ancestors": ancestors,
    "goal_is_new_step": (
      goal_step
      is not data[
        "original_final_step"
      ]
    ),
    "exact_repository_premises": (
      goal_step.premises
      == (
        data[
          "bracket_sum_step"
        ],
        data[
          "composition_step"
        ],
      )
      and (
        goal_step.premises[0]
        is data[
          "bracket_sum_step"
        ]
      )
      and (
        goal_step.premises[1]
        is data[
          "composition_step"
        ]
      )
    ),
    "final_is_inference": (
      goal_step.rule
      == ProofRule.INFERENCE
    ),
    "goal_absent_from_ancestors": (
      all(
        ancestor.conclusion
        != goal_step.conclusion
        for ancestor in ancestors
      )
    ),
    "graph_acyclic": (
      _proof_graph_is_acyclic(
        goal_step
      )
    ),
  }


def main():
  result = (
    build_phase80_representative_result()
  )

  data = result[
    "data"
  ]
  inference_result = result[
    "result"
  ].inference_result

  print(
    "=== Phase 80: repository-assisted "
    "automatic inference ==="
  )
  print()

  print(
    "Actual proof target:"
  )
  print(
    "  Toda Lemma 5.16 final conclusion"
  )
  print()

  print(
    "Initial repository:"
  )
  print(
    "  actual Phase 77 bracket-sum premise"
  )
  print(
    "  actual Phase 77 scaled-composition premise"
  )
  print(
    "  registered initial steps =",
    len(
      result[
        "initial_steps"
      ]
    ),
  )
  print(
    "  goal initially present =",
    result[
      "initial_goal_present"
    ],
  )
  print()

  print(
    "Repository-assisted inference:"
  )
  print(
    "  goal derived =",
    result[
      "goal_step"
    ]
    is not None,
  )
  print(
    "  new ProofStep created =",
    result[
      "goal_is_new_step"
    ],
  )
  print(
    "  final is INFERENCE =",
    result[
      "final_is_inference"
    ],
  )
  print(
    "  exact repository premises =",
    result[
      "exact_repository_premises"
    ],
  )
  print(
    "  existing Phase 77 rule reused =",
    (
      result[
        "goal_step"
      ].inference_rule
      is data[
        "final_rule"
      ]
    ),
  )
  print(
    "  termination =",
    inference_result
    .termination_reason
    .value,
  )
  print()

  print(
    "Applicability / non-circularity:"
  )
  print(
    "  goal absent from initial ancestry =",
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
    bool(
      data[
        "repository"
      ].find_by_conclusion(
        data[
          "goal"
        ]
      )
    ),
  )
  print()

  print(
    "Phase 80 boundary:"
  )
  print(
    "  repository-assisted inference = enabled"
  )
  print(
    "  rule set = explicitly supplied"
  )
  print(
    "  automatic rule selection = not implemented"
  )
  print(
    "  backward proof search = not implemented"
  )
  print(
    "  persistent repository = not implemented"
  )
  print(
    "  automatic proof narrative = not implemented"
  )


if __name__ == "__main__":
  main()

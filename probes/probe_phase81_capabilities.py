from functools import lru_cache
from pathlib import Path
import sys

from proof import ProofRule


TESTS_DIR = (
  Path(__file__).resolve().parents[1]
  / "tests"
)

if str(TESTS_DIR) not in sys.path:
  sys.path.insert(
    0,
    str(TESTS_DIR),
  )

from test_phase81_rule_selection_regression import (
  build_phase81_6_data,
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


def _rule_names(rules):
  return tuple(
    rule.name
    for rule in rules
  )


@lru_cache(maxsize=1)
def build_phase81_representative_result():
  data = build_phase81_6_data()

  goal_step = data[
    "goal_step"
  ]

  phase80 = data[
    "phase80"
  ]

  compatible_entries = data[
    "compatible_entries"
  ]

  compatible_rules = data[
    "compatible_rules"
  ]

  selected_rule = (
    goal_step.inference_rule
  )

  repository = data[
    "repository"
  ]

  goal = data[
    "goal"
  ]

  initial_goal_present = bool(
    repository.find_by_conclusion(
      goal
    )
  )

  correct_rule_match_count = sum(
    1
    for match in data[
      "matches"
    ]
    if (
      match.inference_rule
      is data[
        "final_rule"
      ]
    )
  )

  wrong_rule_match_count = sum(
    1
    for match in data[
      "matches"
    ]
    if (
      match.inference_rule
      is not data[
        "final_rule"
      ]
    )
  )

  accepted_goal_count = sum(
    1
    for application_result
    in data[
      "application_results"
    ]
    if (
      application_result.accepted
      and (
        application_result
        .candidate_step
        .conclusion
        == goal
      )
    )
  )

  return {
    "data": data,
    "goal": goal,
    "goal_step": goal_step,
    "phase80": phase80,
    "compatible_entries": (
      compatible_entries
    ),
    "compatible_rules": (
      compatible_rules
    ),
    "compatible_rule_names": (
      _rule_names(
        compatible_rules
      )
    ),
    "selected_rule": selected_rule,
    "initial_goal_present": (
      initial_goal_present
    ),
    "correct_rule_match_count": (
      correct_rule_match_count
    ),
    "wrong_rule_match_count": (
      wrong_rule_match_count
    ),
    "accepted_goal_count": (
      accepted_goal_count
    ),
  }


def print_phase81_result(
  result,
):
  print(
    "=== Phase 81: automatic rule selection ==="
  )
  print()
  print(
    "Actual proof target:"
  )
  print(
    "  Toda Lemma 5.16 final consequence"
  )
  print()
  print(
    "Goal statement type:"
  )
  print(
    "  "
    + type(
      result[
        "goal"
      ]
    ).__name__
  )
  print()


def print_phase81_catalog_selection(
  result,
):
  data = result[
    "data"
  ]

  print(
    "Rule catalog / candidate selection:"
  )
  print(
    "  catalog entries = "
    + str(
      len(
        data[
          "catalog"
        ].entries()
      )
    )
  )
  print(
    "  goal-compatible safe entries = "
    + str(
      len(
        result[
          "compatible_entries"
        ]
      )
    )
  )
  print(
    "  execution rules after alias dedup = "
    + str(
      len(
        result[
          "compatible_rules"
        ]
      )
    )
  )
  print(
    "  unsafe candidate excluded = "
    + str(
      data[
        "unsafe_rule"
      ]
      not in result[
        "compatible_rules"
      ]
    )
  )
  print(
    "  unrelated conclusion type excluded = "
    + str(
      data[
        "unrelated_rule"
      ]
      not in result[
        "compatible_rules"
      ]
    )
  )
  print(
    "  actual rule alias deduplicated = "
    + str(
      result[
        "compatible_rules"
      ].count(
        data[
          "final_rule"
        ]
      )
      == 1
    )
  )
  print()


def print_phase81_applicability(
  result,
):
  data = result[
    "data"
  ]

  print(
    "Applicability filtering:"
  )
  print(
    "  correct rule matches = "
    + str(
      result[
        "correct_rule_match_count"
      ]
    )
  )
  print(
    "  wrong rule matches = "
    + str(
      result[
        "wrong_rule_match_count"
      ]
    )
  )
  print(
    "  wrong-guard candidate rejected = "
    + str(
      all(
        match.inference_rule
        is not data[
          "wrong_guard_rule"
        ]
        for match in data[
          "matches"
        ]
      )
    )
  )
  print(
    "  missing-premise candidate rejected = "
    + str(
      all(
        match.inference_rule
        is not data[
          "missing_premise_rule"
        ]
        for match in data[
          "matches"
        ]
      )
    )
  )
  print()


def print_phase81_derivation(
  result,
):
  data = result[
    "data"
  ]
  goal_step = result[
    "goal_step"
  ]

  print(
    "Repository-assisted derivation:"
  )
  print(
    "  goal initially present = "
    + str(
      result[
        "initial_goal_present"
      ]
    )
  )
  print(
    "  goal derived = "
    + str(
      goal_step.conclusion
      == result[
        "goal"
      ]
    )
  )
  print(
    "  final is INFERENCE = "
    + str(
      goal_step.rule
      == ProofRule.INFERENCE
    )
  )
  print(
    "  selected existing Phase 77 rule = "
    + str(
      result[
        "selected_rule"
      ]
      is data[
        "final_rule"
      ]
    )
  )
  print(
    "  exact repository premises retained = "
    + str(
      goal_step.premises
      == (
        result[
          "phase80"
        ][
          "bracket_sum_step"
        ],
        result[
          "phase80"
        ][
          "composition_step"
        ],
      )
    )
  )
  print(
    "  accepted goal proofs = "
    + str(
      result[
        "accepted_goal_count"
      ]
    )
  )
  print(
    "  goal absent from ancestry = "
    + str(
      all(
        ancestor.conclusion
        != result[
          "goal"
        ]
        for ancestor in data[
          "ancestors"
        ]
      )
    )
  )
  print(
    "  graph acyclic = "
    + str(
      _proof_graph_is_acyclic(
        goal_step
      )
    )
  )
  print(
    "  repository mutated = "
    + str(
      bool(
        data[
          "repository"
        ].find_by_conclusion(
          result[
            "goal"
          ]
        )
      )
    )
  )
  print()


def print_phase81_boundary():
  print(
    "Phase 81 completion boundary:"
  )
  print(
    "  automatic goal-compatible rule selection = enabled"
  )
  print(
    "  fixed-point-safe catalog filtering = enabled"
  )
  print(
    "  repository-assisted actual theorem inference = enabled"
  )
  print(
    "  rule applicability still owned by premise patterns / match_guard"
  )
  print(
    "  multi-step unknown-premise search = not implemented"
  )
  print(
    "  backward chaining = not implemented"
  )
  print(
    "  proof ranking = not implemented"
  )
  print(
    "  persistent repository = not implemented"
  )
  print(
    "  automatic proof narrative = not implemented"
  )


def main():
  result = (
    build_phase81_representative_result()
  )

  print_phase81_result(
    result
  )
  print_phase81_catalog_selection(
    result
  )
  print_phase81_applicability(
    result
  )
  print_phase81_derivation(
    result
  )
  print_phase81_boundary()


if __name__ == "__main__":
  main()

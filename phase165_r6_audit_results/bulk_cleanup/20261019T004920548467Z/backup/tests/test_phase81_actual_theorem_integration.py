from functools import lru_cache

from proof import (
  InferenceTerminationReason,
  ProofRule,
)
from repository_inference import (
  derive_goal_from_repository_with_catalog,
  repository_available_steps,
)
from rule_catalog import (
  InferenceRuleCatalog,
  InferenceRuleCatalogEntry,
  find_goal_compatible_rules,
)
from test_phase80_actual_proof_integration import (
  build_phase80_5_data,
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


@lru_cache(maxsize=1)
def build_phase81_5_data():
  phase80 = build_phase80_5_data()

  catalog = InferenceRuleCatalog()

  catalog_entry = (
    InferenceRuleCatalogEntry(
      key=(
        "phase77."
        "toda_lemma516_final"
      ),
      rule=phase80[
        "final_rule"
      ],
      conclusion_type=type(
        phase80[
          "goal"
        ]
      ),
      fixed_point_safe=True,
    )
  )

  catalog.register(
    catalog_entry
  )

  initial_steps = (
    repository_available_steps(
      phase80[
        "repository"
      ]
    )
  )

  repository_entries_before = (
    phase80[
      "repository"
    ].entries()
  )

  compatible_rules = (
    find_goal_compatible_rules(
      catalog,
      phase80[
        "goal"
      ],
    )
  )

  result = (
    derive_goal_from_repository_with_catalog(
      phase80[
        "repository"
      ],
      catalog,
      phase80[
        "goal"
      ],
    )
  )

  goal_step = result.goal_step

  if goal_step is None:
    raise RuntimeError(
      "Phase 81-5 actual Toda "
      "Lemma 5.16 goal was not derived"
    )

  ancestors = (
    _collect_ancestors(
      goal_step
    )
  )

  return {
    "phase80": phase80,
    "catalog": catalog,
    "catalog_entry": catalog_entry,
    "initial_steps": initial_steps,
    "repository_entries_before": (
      repository_entries_before
    ),
    "compatible_rules": (
      compatible_rules
    ),
    "result": result,
    "goal_step": goal_step,
    "ancestors": ancestors,
  }


def test_phase81_5_actual_goal_is_absent_initially():
  data = build_phase81_5_data()

  goal = data[
    "phase80"
  ][
    "goal"
  ]

  assert all(
    step.conclusion
    != goal
    for step in data[
      "initial_steps"
    ]
  )


def test_phase81_5_catalog_selects_actual_phase77_final_rule():
  data = build_phase81_5_data()

  assert (
    data[
      "compatible_rules"
    ]
    == (
      data[
        "phase80"
      ][
        "final_rule"
      ],
    )
  )

  assert (
    data[
      "compatible_rules"
    ][0]
    is data[
      "phase80"
    ][
      "final_rule"
    ]
  )


def test_phase81_5_derives_actual_toda_lemma516_goal():
  data = build_phase81_5_data()

  assert (
    data[
      "goal_step"
    ].conclusion
    == data[
      "phase80"
    ][
      "goal"
    ]
  )


def test_phase81_5_creates_new_final_step():
  data = build_phase81_5_data()

  assert (
    data[
      "goal_step"
    ]
    is not data[
      "phase80"
    ][
      "original_final_step"
    ]
  )


def test_phase81_5_final_step_is_inference():
  data = build_phase81_5_data()

  assert (
    data[
      "goal_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase81_5_final_step_records_automatically_selected_rule():
  data = build_phase81_5_data()

  assert (
    data[
      "goal_step"
    ].inference_rule
    is data[
      "phase80"
    ][
      "final_rule"
    ]
  )


def test_phase81_5_final_step_uses_exact_repository_premises():
  data = build_phase81_5_data()

  goal_step = data[
    "goal_step"
  ]

  phase80 = data[
    "phase80"
  ]

  assert (
    goal_step.premises
    == (
      phase80[
        "bracket_sum_step"
      ],
      phase80[
        "composition_step"
      ],
    )
  )

  assert (
    goal_step.premises[0]
    is phase80[
      "bracket_sum_step"
    ]
  )

  assert (
    goal_step.premises[1]
    is phase80[
      "composition_step"
    ]
  )


def test_phase81_5_actual_inference_reaches_fixed_point():
  data = build_phase81_5_data()

  assert (
    data[
      "result"
    ]
    .inference_result
    .termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )


def test_phase81_5_goal_is_absent_from_ancestors():
  data = build_phase81_5_data()

  goal_conclusion = (
    data[
      "goal_step"
    ].conclusion
  )

  assert all(
    ancestor.conclusion
    != goal_conclusion
    for ancestor in data[
      "ancestors"
    ]
  )


def test_phase81_5_derived_graph_is_acyclic():
  data = build_phase81_5_data()

  assert (
    _proof_graph_is_acyclic(
      data[
        "goal_step"
      ]
    )
  )


def test_phase81_5_repository_remains_unchanged():
  data = build_phase81_5_data()

  repository = data[
    "phase80"
  ][
    "repository"
  ]

  assert (
    repository.entries()
    == data[
      "repository_entries_before"
    ]
  )


def test_phase81_5_final_goal_is_not_registered_back_into_repository():
  data = build_phase81_5_data()

  repository = data[
    "phase80"
  ][
    "repository"
  ]

  assert (
    repository.find_by_conclusion(
      data[
        "phase80"
      ][
        "goal"
      ]
    )
    == ()
  )



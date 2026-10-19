from dataclasses import dataclass
from functools import lru_cache

import pytest

from proof import InferenceRule
from rule_catalog import (
  InferenceRuleCatalog,
  InferenceRuleCatalogEntry,
  find_goal_compatible_rule_entries,
  find_goal_compatible_rules,
)
from test_phase88_realistic_catalog_collision_observability import (
  build_phase88_4_data,
)
from toda_rules import (
  TodaDeltaImageUpToSignStatement,
)


@dataclass(frozen=True)
class Phase88GoalCompatibilityStatement:
  value: str


@lru_cache(maxsize=1)
def build_phase88_7_data():
  phase88_4 = build_phase88_4_data()

  catalog = InferenceRuleCatalog()
  entries = []

  for index, (
    rule,
    goal,
  ) in enumerate(
    zip(
      phase88_4[
        "rules"
      ],
      phase88_4[
        "goals"
      ],
    )
  ):
    entry = InferenceRuleCatalogEntry(
      key=(
        "phase88.goal-compatible."
        f"{index}"
      ),
      rule=rule,
      conclusion_type=(
        TodaDeltaImageUpToSignStatement
      ),
      fixed_point_safe=True,
      goal_compatibility=(
        lambda candidate_goal,
        expected_goal=goal:
        candidate_goal
        == expected_goal
      ),
    )

    catalog.register(
      entry
    )
    entries.append(
      entry
    )

  return {
    "phase88_4": phase88_4,
    "catalog": catalog,
    "entries": tuple(
      entries
    ),
    "rules": phase88_4[
      "rules"
    ],
    "goals": phase88_4[
      "goals"
    ],
  }


def test_phase88_7_goal_compatibility_defaults_to_none():
  entry = InferenceRuleCatalogEntry(
    key="phase88.default",
    rule=InferenceRule(
      name="phase88 default rule",
    ),
    conclusion_type=(
      Phase88GoalCompatibilityStatement
    ),
    fixed_point_safe=True,
  )

  assert (
    entry.goal_compatibility
    is None
  )


def test_phase88_7_rejects_non_callable_goal_compatibility():
  with pytest.raises(
    TypeError,
    match=(
      "goal_compatibility must be "
      "callable or None"
    ),
  ):
    InferenceRuleCatalogEntry(
      key="phase88.invalid",
      rule=InferenceRule(
        name="phase88 invalid rule",
      ),
      conclusion_type=(
        Phase88GoalCompatibilityStatement
      ),
      fixed_point_safe=True,
      goal_compatibility=True,
    )


def test_phase88_7_goal_compatibility_must_return_bool():
  catalog = InferenceRuleCatalog()

  catalog.register(
    InferenceRuleCatalogEntry(
      key="phase88.invalid-result",
      rule=InferenceRule(
        name=(
          "phase88 invalid result rule"
        ),
      ),
      conclusion_type=(
        Phase88GoalCompatibilityStatement
      ),
      fixed_point_safe=True,
      goal_compatibility=(
        lambda goal: "yes"
      ),
    )
  )

  goal = (
    Phase88GoalCompatibilityStatement(
      value="goal",
    )
  )

  with pytest.raises(
    TypeError,
    match=(
      "goal_compatibility must "
      "return a bool"
    ),
  ):
    find_goal_compatible_rules(
      catalog,
      goal,
    )


def test_phase88_7_none_preserves_phase88_4_type_only_collision():
  data = build_phase88_7_data()
  phase88_4 = data[
    "phase88_4"
  ]

  assert phase88_4[
    "goal_candidates"
  ] == (
    phase88_4[
      "rules"
    ],
    phase88_4[
      "rules"
    ],
    phase88_4[
      "rules"
    ],
  )


def test_phase88_7_actual_goals_select_one_matching_entry_each():
  data = build_phase88_7_data()

  selected_entries = tuple(
    find_goal_compatible_rule_entries(
      data[
        "catalog"
      ],
      goal,
    )
    for goal in data[
      "goals"
    ]
  )

  assert selected_entries == (
    (
      data[
        "entries"
      ][0],
    ),
    (
      data[
        "entries"
      ][1],
    ),
    (
      data[
        "entries"
      ][2],
    ),
  )


def test_phase88_7_actual_goals_select_one_matching_rule_each():
  data = build_phase88_7_data()

  selected_rules = tuple(
    find_goal_compatible_rules(
      data[
        "catalog"
      ],
      goal,
    )
    for goal in data[
      "goals"
    ]
  )

  assert selected_rules == (
    (
      data[
        "rules"
      ][0],
    ),
    (
      data[
        "rules"
      ][1],
    ),
    (
      data[
        "rules"
      ][2],
    ),
  )


def test_phase88_7_goal_compatibility_preserves_registration_order():
  data = build_phase88_7_data()

  assert data[
    "catalog"
  ].entries() == data[
    "entries"
  ]

  assert data[
    "catalog"
  ].rules() == data[
    "rules"
  ]

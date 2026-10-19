from functools import lru_cache

from proof import (
  InferenceRule,
  PremisePattern,
)
from repository_inference import (
  detect_missing_premises,
  find_missing_premise_producer_lookups,
)
from rule_catalog import (
  InferenceRuleCatalog,
  InferenceRuleCatalogEntry,
  find_premise_producer_candidate_entries,
  find_premise_producer_rule_entries,
  find_premise_producer_rules,
)
from test_phase88_goal_side_compatibility import (
  build_phase88_7_data,
)
from toda_rules import (
  TodaDeltaImageUpToSignStatement,
)


@lru_cache(maxsize=1)
def build_phase88_11_data():
  phase88_7 = build_phase88_7_data()

  lookups = []

  for goal in phase88_7[
    "goals"
  ]:
    requesting_rule = InferenceRule(
      name=(
        "phase88 producer-side "
        "goal compatibility requester"
      ),
      premise_patterns=(
        PremisePattern(
          statement_type=(
            TodaDeltaImageUpToSignStatement
          ),
          statement_pattern=goal,
        ),
      ),
    )

    availability = detect_missing_premises(
      requesting_rule,
      (),
    )

    lookup = (
      find_missing_premise_producer_lookups(
        availability,
        phase88_7[
          "catalog"
        ],
      )[0]
    )

    lookups.append(
      lookup
    )

  return {
    "phase88_7": phase88_7,
    "catalog": phase88_7[
      "catalog"
    ],
    "entries": phase88_7[
      "entries"
    ],
    "rules": phase88_7[
      "rules"
    ],
    "goals": phase88_7[
      "goals"
    ],
    "lookups": tuple(
      lookups
    ),
  }


def test_phase88_11_requested_statements_are_actual_delta_goals():
  data = build_phase88_11_data()

  assert tuple(
    lookup.requested_statement
    for lookup in data[
      "lookups"
    ]
  ) == data[
    "goals"
  ]


def test_phase88_11_each_actual_requested_statement_selects_one_rule():
  data = build_phase88_11_data()

  assert tuple(
    lookup.producer_rules
    for lookup in data[
      "lookups"
    ]
  ) == (
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


def test_phase88_11_rule_entry_lookup_filters_by_requested_statement():
  data = build_phase88_11_data()

  selected = tuple(
    find_premise_producer_rule_entries(
      data[
        "catalog"
      ],
      lookup.premise_pattern,
      requested_statement=(
        lookup.requested_statement
      ),
    )
    for lookup in data[
      "lookups"
    ]
  )

  assert selected == (
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


def test_phase88_11_candidate_entry_lookup_filters_by_requested_statement():
  data = build_phase88_11_data()

  selected = tuple(
    find_premise_producer_candidate_entries(
      data[
        "catalog"
      ],
      lookup.premise_pattern,
      requested_statement=(
        lookup.requested_statement
      ),
    )
    for lookup in data[
      "lookups"
    ]
  )

  assert selected == (
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


def test_phase88_11_none_requested_statement_preserves_type_only_semantics():
  data = build_phase88_11_data()

  pattern = data[
    "lookups"
  ][0].premise_pattern

  assert (
    find_premise_producer_rules(
      data[
        "catalog"
      ],
      pattern,
      requested_statement=None,
    )
    == data[
      "rules"
    ]
  )


def test_phase88_11_entry_without_goal_compatibility_remains_compatible():
  data = build_phase88_11_data()

  always_available_rule = InferenceRule(
    name=(
      "phase88 no goal compatibility "
      "producer"
    ),
  )

  catalog = InferenceRuleCatalog()

  catalog.register(
    InferenceRuleCatalogEntry(
      key="phase88.no-filter",
      rule=always_available_rule,
      conclusion_type=(
        TodaDeltaImageUpToSignStatement
      ),
      fixed_point_safe=True,
    )
  )

  pattern = data[
    "lookups"
  ][0].premise_pattern

  assert (
    find_premise_producer_rules(
      catalog,
      pattern,
      requested_statement=(
        data[
          "goals"
        ][2]
      ),
    )
    == (
      always_available_rule,
    )
  )


def test_phase88_11_producer_lookup_does_not_change_requested_statement():
  data = build_phase88_11_data()

  for lookup, goal in zip(
    data[
      "lookups"
    ],
    data[
      "goals"
    ],
  ):
    assert (
      lookup.requested_statement
      == goal
    )


def test_phase88_11_registration_order_is_preserved_after_filtering():
  data = build_phase88_11_data()

  all_rules = (
    find_premise_producer_rules(
      data[
        "catalog"
      ],
      data[
        "lookups"
      ][0].premise_pattern,
      requested_statement=None,
    )
  )

  assert all_rules == data[
    "rules"
  ]

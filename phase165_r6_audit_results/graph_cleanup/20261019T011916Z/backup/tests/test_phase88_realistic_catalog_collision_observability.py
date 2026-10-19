from functools import lru_cache

from proof import PremisePattern
from repository_inference import (
  BoundedProducerSearchStatus,
)
from rule_catalog import (
  InferenceRuleCatalog,
  InferenceRuleCatalogEntry,
  find_goal_compatible_rules,
  find_premise_producer_rules,
)
from test_phase52_delta_direct_bridge import (
  build_phase52_2_data,
)
from test_phase66_delta_iota9_nu_expression import (
  build_phase66_3_data,
)
from test_phase76_delta_iota17 import (
  build_phase76_4_data,
)
from test_phase85_actual_theorem_integration import (
  build_phase85_8_data,
)
from toda_rules import (
  TodaDeltaImageUpToSignStatement,
  toda_516_delta_iota17_generator_inference_rule,
  toda_58_delta_iota9_nu4_nu_prime_inference_rule,
  toda_delta_iota5_two_eta2_up_to_sign_inference_rule,
)


@lru_cache(maxsize=1)
def build_phase88_4_data():
  phase52 = build_phase52_2_data()
  phase66 = build_phase66_3_data()
  phase76 = build_phase76_4_data()
  phase85 = build_phase85_8_data()

  iota5_rule = (
    toda_delta_iota5_two_eta2_up_to_sign_inference_rule()
  )
  iota9_rule = (
    toda_58_delta_iota9_nu4_nu_prime_inference_rule()
  )
  iota17_rule = (
    toda_516_delta_iota17_generator_inference_rule()
  )

  rules = (
    iota5_rule,
    iota9_rule,
    iota17_rule,
  )

  catalog_entries = (
    InferenceRuleCatalogEntry(
      key="phase88.realistic.delta-iota5",
      rule=iota5_rule,
      conclusion_type=(
        TodaDeltaImageUpToSignStatement
      ),
      fixed_point_safe=True,
    ),
    InferenceRuleCatalogEntry(
      key="phase88.realistic.delta-iota9",
      rule=iota9_rule,
      conclusion_type=(
        TodaDeltaImageUpToSignStatement
      ),
      fixed_point_safe=True,
    ),
    InferenceRuleCatalogEntry(
      key="phase88.realistic.delta-iota17",
      rule=iota17_rule,
      conclusion_type=(
        TodaDeltaImageUpToSignStatement
      ),
      fixed_point_safe=True,
    ),
  )

  catalog = InferenceRuleCatalog()
  alias_catalog = InferenceRuleCatalog()

  for entry in catalog_entries:
    catalog.register(entry)
    alias_catalog.register(entry)

  alias_entry = InferenceRuleCatalogEntry(
    key="phase88.realistic.delta-iota5-alias",
    rule=iota5_rule,
    conclusion_type=(
      TodaDeltaImageUpToSignStatement
    ),
    fixed_point_safe=True,
  )
  alias_catalog.register(alias_entry)

  goals = (
    phase52[
      "delta_two_eta_2_up_to_sign"
    ],
    phase66[
      "expected_statement"
    ],
    phase76[
      "expected_final"
    ],
  )

  delta_pattern = PremisePattern(
    statement_type=(
      TodaDeltaImageUpToSignStatement
    ),
  )

  goal_candidates = tuple(
    find_goal_compatible_rules(
      catalog,
      goal,
    )
    for goal in goals
  )

  producer_candidates = (
    find_premise_producer_rules(
      catalog,
      delta_pattern,
    )
  )

  alias_producer_candidates = (
    find_premise_producer_rules(
      alias_catalog,
      delta_pattern,
    )
  )

  return {
    "phase52": phase52,
    "phase66": phase66,
    "phase76": phase76,
    "phase85": phase85,
    "rules": rules,
    "catalog_entries": catalog_entries,
    "catalog": catalog,
    "alias_entry": alias_entry,
    "alias_catalog": alias_catalog,
    "goals": goals,
    "delta_pattern": delta_pattern,
    "goal_candidates": goal_candidates,
    "producer_candidates": producer_candidates,
    "alias_producer_candidates": (
      alias_producer_candidates
    ),
  }


def test_phase88_4_uses_three_distinct_actual_delta_goals():
  data = build_phase88_4_data()

  assert all(
    isinstance(
      goal,
      TodaDeltaImageUpToSignStatement,
    )
    for goal in data[
      "goals"
    ]
  )

  assert len(
    set(
      data[
        "goals"
      ]
    )
  ) == 3


def test_phase88_4_catalog_registration_order_is_deterministic():
  data = build_phase88_4_data()

  assert tuple(
    entry.key
    for entry in data[
      "catalog"
    ].entries()
  ) == (
    "phase88.realistic.delta-iota5",
    "phase88.realistic.delta-iota9",
    "phase88.realistic.delta-iota17",
  )


def test_phase88_4_catalog_preserves_three_distinct_rule_identities():
  data = build_phase88_4_data()

  assert data[
    "catalog"
  ].rules() == data[
    "rules"
  ]

  assert len(
    {
      id(rule)
      for rule in data[
        "rules"
      ]
    }
  ) == 3


def test_phase88_4_each_actual_goal_observes_same_type_collision():
  data = build_phase88_4_data()

  assert data[
    "goal_candidates"
  ] == (
    data[
      "rules"
    ],
    data[
      "rules"
    ],
    data[
      "rules"
    ],
  )


def test_phase88_4_producer_lookup_observes_three_actual_candidates():
  data = build_phase88_4_data()

  assert data[
    "producer_candidates"
  ] == data[
    "rules"
  ]


def test_phase88_4_same_rule_alias_does_not_add_producer_candidate():
  data = build_phase88_4_data()

  assert len(
    data[
      "alias_catalog"
    ].entries()
  ) == 4

  assert (
    data[
      "alias_entry"
    ].rule
    is data[
      "rules"
    ][0]
  )

  assert data[
    "alias_producer_candidates"
  ] == data[
    "rules"
  ]


def test_phase88_4_existing_narrow_toda_lemma516_search_still_succeeds():
  data = build_phase88_4_data()
  phase85 = data[
    "phase85"
  ]

  assert phase85[
    "report"
  ].status is (
    BoundedProducerSearchStatus.SUCCESS
  )

  assert phase85[
    "final_step"
  ].conclusion == phase85[
    "goal"
  ]

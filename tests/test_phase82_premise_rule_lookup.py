from functools import lru_cache

import pytest

from proof import (
  PremisePattern,
  ProofRule,
)
from rule_catalog import (
  InferenceRuleCatalog,
  InferenceRuleCatalogEntry,
  find_premise_producer_rule_entries,
  find_premise_producer_rules,
)
from test_phase82_missing_premise_detection import (
  build_phase82_2_data,
)
from toda_rules import (
  TodaLemma516BracketSumContainmentStatement,
  TodaLemma516ScaledCompositionBridgeStatement,
)


@lru_cache(maxsize=1)
def build_phase82_3_data():
  phase82_2 = (
    build_phase82_2_data()
  )

  phase77 = phase82_2[
    "phase77"
  ]

  final_rule = phase82_2[
    "final_rule"
  ]

  producer_rule = (
    phase77[
      "composition_step"
    ].inference_rule
  )

  assert producer_rule is not None

  missing_pattern = (
    phase82_2[
      "direct_detection"
    ].missing_patterns[
      0
    ]
  )

  catalog = InferenceRuleCatalog()

  final_entry = (
    InferenceRuleCatalogEntry(
      key=(
        "phase82."
        "toda_lemma516_final"
      ),
      rule=final_rule,
      conclusion_type=(
        TodaLemma516BracketSumContainmentStatement
      ),
      fixed_point_safe=True,
    )
  )

  producer_entry = (
    InferenceRuleCatalogEntry(
      key=(
        "phase82."
        "scaled_composition_producer"
      ),
      rule=producer_rule,
      conclusion_type=(
        TodaLemma516ScaledCompositionBridgeStatement
      ),
      fixed_point_safe=True,
    )
  )

  producer_alias_entry = (
    InferenceRuleCatalogEntry(
      key=(
        "phase82."
        "scaled_composition_producer_alias"
      ),
      rule=producer_rule,
      conclusion_type=(
        TodaLemma516ScaledCompositionBridgeStatement
      ),
      fixed_point_safe=True,
    )
  )

  unsafe_producer_entry = (
    InferenceRuleCatalogEntry(
      key=(
        "phase82."
        "unsafe_scaled_composition"
      ),
      rule=producer_rule,
      conclusion_type=(
        TodaLemma516ScaledCompositionBridgeStatement
      ),
      fixed_point_safe=False,
    )
  )

  unrelated_entry = (
    InferenceRuleCatalogEntry(
      key=(
        "phase82."
        "unrelated_final_type"
      ),
      rule=final_rule,
      conclusion_type=(
        TodaLemma516BracketSumContainmentStatement
      ),
      fixed_point_safe=True,
    )
  )

  for entry in (
    final_entry,
    producer_entry,
    producer_alias_entry,
    unsafe_producer_entry,
    unrelated_entry,
  ):
    catalog.register(
      entry
    )

  producer_entries = (
    find_premise_producer_rule_entries(
      catalog,
      missing_pattern,
    )
  )

  producer_rules = (
    find_premise_producer_rules(
      catalog,
      missing_pattern,
    )
  )

  return {
    "phase82_2": phase82_2,
    "phase77": phase77,
    "catalog": catalog,
    "final_rule": final_rule,
    "producer_rule": producer_rule,
    "missing_pattern": (
      missing_pattern
    ),
    "final_entry": final_entry,
    "producer_entry": (
      producer_entry
    ),
    "producer_alias_entry": (
      producer_alias_entry
    ),
    "unsafe_producer_entry": (
      unsafe_producer_entry
    ),
    "unrelated_entry": (
      unrelated_entry
    ),
    "producer_entries": (
      producer_entries
    ),
    "producer_rules": (
      producer_rules
    ),
  }


def test_phase82_3_missing_pattern_is_scaled_composition():
  data = build_phase82_3_data()

  pattern = data[
    "missing_pattern"
  ]

  assert (
    pattern.statement_type
    is
    TodaLemma516ScaledCompositionBridgeStatement
  )

  assert (
    pattern.proof_rule
    == ProofRule.INFERENCE
  )


def test_phase82_3_actual_producer_is_existing_phase77_rule():
  data = build_phase82_3_data()

  assert (
    data[
      "producer_rule"
    ]
    is data[
      "phase77"
    ][
      "composition_step"
    ].inference_rule
  )


def test_phase82_3_finds_safe_producer_entries_by_exact_type():
  data = build_phase82_3_data()

  entries = data[
    "producer_entries"
  ]

  assert (
    data[
      "producer_entry"
    ]
    in entries
  )

  assert (
    data[
      "producer_alias_entry"
    ]
    in entries
  )


def test_phase82_3_preserves_catalog_aliases_at_entry_level():
  data = build_phase82_3_data()

  entries = data[
    "producer_entries"
  ]

  assert entries == (
    data[
      "producer_entry"
    ],
    data[
      "producer_alias_entry"
    ],
  )


def test_phase82_3_deduplicates_producer_rules_by_identity():
  data = build_phase82_3_data()

  assert (
    data[
      "producer_rules"
    ]
    == (
      data[
        "producer_rule"
      ],
    )
  )


def test_phase82_3_excludes_unsafe_producer():
  data = build_phase82_3_data()

  assert (
    data[
      "unsafe_producer_entry"
    ]
    not in data[
      "producer_entries"
    ]
  )


def test_phase82_3_excludes_unrelated_conclusion_type():
  data = build_phase82_3_data()

  assert (
    data[
      "unrelated_entry"
    ]
    not in data[
      "producer_entries"
    ]
  )


def test_phase82_3_final_rule_is_not_selected_as_producer():
  data = build_phase82_3_data()

  assert all(
    entry.rule
    is not data[
      "final_rule"
    ]
    for entry in data[
      "producer_entries"
    ]
  )


def test_phase82_3_no_matching_producer_returns_empty():
  data = build_phase82_3_data()

  unmatched_pattern = PremisePattern(
    proof_rule=ProofRule.INFERENCE,
    statement_type=dict,
  )

  assert (
    find_premise_producer_rule_entries(
      data[
        "catalog"
      ],
      unmatched_pattern,
    )
    == ()
  )

  assert (
    find_premise_producer_rules(
      data[
        "catalog"
      ],
      unmatched_pattern,
    )
    == ()
  )


def test_phase82_3_lookup_does_not_execute_producer_rule():
  data = build_phase82_3_data()

  phase82_2 = data[
    "phase82_2"
  ]

  composition_conclusion = (
    data[
      "phase77"
    ][
      "composition_step"
    ].conclusion
  )

  initial_steps = tuple(
    entry.step
    for entry
    in phase82_2[
      "repository"
    ].entries()
  )

  assert all(
    step.conclusion
    != composition_conclusion
    for step in initial_steps
  )

  find_premise_producer_rules(
    data[
      "catalog"
    ],
    data[
      "missing_pattern"
    ],
  )

  final_steps = tuple(
    entry.step
    for entry
    in phase82_2[
      "repository"
    ].entries()
  )

  assert (
    final_steps
    == initial_steps
  )

  assert all(
    step.conclusion
    != composition_conclusion
    for step in final_steps
  )


def test_phase82_3_invalid_catalog_is_rejected():
  data = build_phase82_3_data()

  with pytest.raises(
    TypeError,
    match=(
      "catalog must be an "
      "InferenceRuleCatalog"
    ),
  ):
    find_premise_producer_rules(
      object(),
      data[
        "missing_pattern"
      ],
    )


def test_phase82_3_invalid_premise_pattern_is_rejected():
  data = build_phase82_3_data()

  with pytest.raises(
    TypeError,
    match=(
      "premise_pattern must be a "
      "PremisePattern"
    ),
  ):
    find_premise_producer_rules(
      data[
        "catalog"
      ],
      object(),
    )



from functools import lru_cache

import pytest

from repository_inference import (
  MissingPremiseProducerLookup,
  detect_missing_premises,
  find_missing_premise_producer_lookups,
)
from rule_catalog import (
  InferenceRuleCatalog,
  InferenceRuleCatalogEntry,
)
from test_phase77_applicability_provenance import (
  build_phase77_6_data,
)
from toda_rules import (
  Toda36Lemma516BracketSumContainmentStatement,
  TodaLemma516ScaledCompositionBridgeStatement,
)


def _register_rule(
  catalog,
  key,
  rule,
  conclusion_type,
):
  catalog.register(
    InferenceRuleCatalogEntry(
      key=key,
      rule=rule,
      conclusion_type=conclusion_type,
      fixed_point_safe=True,
    )
  )


@lru_cache(maxsize=1)
def build_phase83_2_data():
  phase77 = build_phase77_6_data()

  final_rule = (
    phase77[
      "data"
    ][
      "final_rule"
    ]
  )

  bracket_sum_rule = (
    phase77[
      "bracket_sum_step"
    ].inference_rule
  )

  composition_rule = (
    phase77[
      "composition_step"
    ].inference_rule
  )

  assert bracket_sum_rule is not None
  assert composition_rule is not None

  availability = detect_missing_premises(
    final_rule,
    (),
  )

  catalog = InferenceRuleCatalog()

  _register_rule(
    catalog,
    "phase83.final",
    final_rule,
    type(
      phase77[
        "final_step"
      ].conclusion
    ),
  )

  _register_rule(
    catalog,
    "phase83.bracket-sum-producer",
    bracket_sum_rule,
    Toda36Lemma516BracketSumContainmentStatement,
  )

  _register_rule(
    catalog,
    "phase83.composition-producer",
    composition_rule,
    TodaLemma516ScaledCompositionBridgeStatement,
  )

  lookups = (
    find_missing_premise_producer_lookups(
      availability,
      catalog,
    )
  )

  return {
    "phase77": phase77,
    "final_rule": final_rule,
    "bracket_sum_rule": bracket_sum_rule,
    "composition_rule": composition_rule,
    "availability": availability,
    "catalog": catalog,
    "lookups": lookups,
  }


def test_phase83_2_detects_two_missing_premises():
  data = build_phase83_2_data()

  assert (
    data[
      "availability"
    ].missing_indices
    == (
      0,
      1,
    )
  )


def test_phase83_2_returns_one_lookup_per_missing_premise():
  data = build_phase83_2_data()

  assert len(
    data[
      "lookups"
    ]
  ) == 2

  assert all(
    isinstance(
      lookup,
      MissingPremiseProducerLookup,
    )
    for lookup in data[
      "lookups"
    ]
  )


def test_phase83_2_preserves_missing_premise_order_and_indices():
  data = build_phase83_2_data()

  assert tuple(
    lookup.premise_index
    for lookup in data[
      "lookups"
    ]
  ) == (
    0,
    1,
  )


def test_phase83_2_preserves_exact_final_rule_and_patterns():
  data = build_phase83_2_data()

  for lookup in data[
    "lookups"
  ]:
    assert (
      lookup.inference_rule
      is data[
        "final_rule"
      ]
    )

    assert (
      lookup.premise_pattern
      is data[
        "final_rule"
      ].premise_patterns[
        lookup.premise_index
      ]
    )


def test_phase83_2_finds_bracket_sum_producer_for_first_missing_premise():
  data = build_phase83_2_data()

  assert (
    data[
      "lookups"
    ][
      0
    ].producer_rules
    == (
      data[
        "bracket_sum_rule"
      ],
    )
  )


def test_phase83_2_finds_composition_producer_for_second_missing_premise():
  data = build_phase83_2_data()

  assert (
    data[
      "lookups"
    ][
      1
    ].producer_rules
    == (
      data[
        "composition_rule"
      ],
    )
  )


def test_phase83_2_lookup_does_not_execute_producers():
  data = build_phase83_2_data()

  assert (
    data[
      "availability"
    ].matched_steps
    == (
      None,
      None,
    )
  )

  assert all(
    lookup.producer_rules
    for lookup in data[
      "lookups"
    ]
  )


def test_phase83_2_complete_availability_returns_no_lookups():
  data = build_phase83_2_data()

  phase77 = data[
    "phase77"
  ]

  availability = detect_missing_premises(
    data[
      "final_rule"
    ],
    (
      phase77[
        "bracket_sum_step"
      ],
      phase77[
        "composition_step"
      ],
    ),
  )

  assert (
    find_missing_premise_producer_lookups(
      availability,
      data[
        "catalog"
      ],
    )
    == ()
  )


def test_phase83_2_missing_producer_is_represented_by_empty_tuple():
  data = build_phase83_2_data()

  catalog = InferenceRuleCatalog()

  lookups = (
    find_missing_premise_producer_lookups(
      data[
        "availability"
      ],
      catalog,
    )
  )

  assert tuple(
    lookup.producer_rules
    for lookup in lookups
  ) == (
    (),
    (),
  )


def test_phase83_2_invalid_availability_is_rejected():
  data = build_phase83_2_data()

  with pytest.raises(
    TypeError,
    match=(
      "availability must be a "
      "PremiseAvailability"
    ),
  ):
    find_missing_premise_producer_lookups(
      object(),
      data[
        "catalog"
      ],
    )


def test_phase83_2_invalid_rule_catalog_is_rejected():
  data = build_phase83_2_data()

  with pytest.raises(
    TypeError,
    match=(
      "rule_catalog must be an "
      "InferenceRuleCatalog"
    ),
  ):
    find_missing_premise_producer_lookups(
      data[
        "availability"
      ],
      object(),
    )

from copy import copy
from functools import lru_cache

import pytest

from repository_inference import (
  all_missing_premises_uniquely_producible,
  find_missing_premise_producer_lookups,
)
from rule_catalog import (
  InferenceRuleCatalog,
  InferenceRuleCatalogEntry,
)
from test_phase83_missing_premise_producer_lookup import (
  build_phase83_2_data,
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


def _build_catalog(
  data,
  *,
  include_bracket_sum=True,
  include_composition=True,
  ambiguous_composition=False,
  composition_alias=False,
):
  catalog = InferenceRuleCatalog()

  if include_bracket_sum:
    _register_rule(
      catalog,
      "phase83.unique.bracket-sum",
      data[
        "bracket_sum_rule"
      ],
      Toda36Lemma516BracketSumContainmentStatement,
    )

  if include_composition:
    _register_rule(
      catalog,
      "phase83.unique.composition",
      data[
        "composition_rule"
      ],
      TodaLemma516ScaledCompositionBridgeStatement,
    )

  if ambiguous_composition:
    _register_rule(
      catalog,
      "phase83.unique.composition-second",
      copy(
        data[
          "composition_rule"
        ]
      ),
      TodaLemma516ScaledCompositionBridgeStatement,
    )

  if composition_alias:
    _register_rule(
      catalog,
      "phase83.unique.composition-alias",
      data[
        "composition_rule"
      ],
      TodaLemma516ScaledCompositionBridgeStatement,
    )

  return catalog


@lru_cache(maxsize=1)
def build_phase83_3_data():
  phase83_2 = build_phase83_2_data()

  catalog = _build_catalog(
    phase83_2
  )

  lookups = (
    find_missing_premise_producer_lookups(
      phase83_2[
        "availability"
      ],
      catalog,
    )
  )

  return {
    "phase83_2": phase83_2,
    "catalog": catalog,
    "lookups": lookups,
    "result": (
      all_missing_premises_uniquely_producible(
        lookups
      )
    ),
  }


def test_phase83_3_actual_two_missing_premises_are_uniquely_producible():
  data = build_phase83_3_data()

  assert len(
    data[
      "lookups"
    ]
  ) == 2

  assert data[
    "result"
  ]


def test_phase83_3_requires_exactly_one_producer_for_each_lookup():
  data = build_phase83_3_data()

  assert tuple(
    len(
      lookup.producer_rules
    )
    for lookup in data[
      "lookups"
    ]
  ) == (
    1,
    1,
  )


def test_phase83_3_missing_first_producer_returns_false():
  data = build_phase83_3_data()

  catalog = _build_catalog(
    data[
      "phase83_2"
    ],
    include_bracket_sum=False,
  )

  lookups = (
    find_missing_premise_producer_lookups(
      data[
        "phase83_2"
      ][
        "availability"
      ],
      catalog,
    )
  )

  assert not (
    all_missing_premises_uniquely_producible(
      lookups
    )
  )


def test_phase83_3_missing_second_producer_returns_false():
  data = build_phase83_3_data()

  catalog = _build_catalog(
    data[
      "phase83_2"
    ],
    include_composition=False,
  )

  lookups = (
    find_missing_premise_producer_lookups(
      data[
        "phase83_2"
      ][
        "availability"
      ],
      catalog,
    )
  )

  assert not (
    all_missing_premises_uniquely_producible(
      lookups
    )
  )


def test_phase83_3_ambiguous_producer_returns_false():
  data = build_phase83_3_data()

  catalog = _build_catalog(
    data[
      "phase83_2"
    ],
    ambiguous_composition=True,
  )

  lookups = (
    find_missing_premise_producer_lookups(
      data[
        "phase83_2"
      ][
        "availability"
      ],
      catalog,
    )
  )

  assert len(
    lookups[
      1
    ].producer_rules
  ) == 2

  assert not (
    all_missing_premises_uniquely_producible(
      lookups
    )
  )


def test_phase83_3_same_rule_alias_remains_unique():
  data = build_phase83_3_data()

  catalog = _build_catalog(
    data[
      "phase83_2"
    ],
    composition_alias=True,
  )

  lookups = (
    find_missing_premise_producer_lookups(
      data[
        "phase83_2"
      ][
        "availability"
      ],
      catalog,
    )
  )

  assert len(
    lookups[
      1
    ].producer_rules
  ) == 1

  assert (
    all_missing_premises_uniquely_producible(
      lookups
    )
  )


def test_phase83_3_single_unique_lookup_is_supported():
  data = build_phase83_3_data()

  assert (
    all_missing_premises_uniquely_producible(
      (
        data[
          "lookups"
        ][
          0
        ],
      )
    )
  )


def test_phase83_3_empty_lookup_collection_returns_false():
  assert not (
    all_missing_premises_uniquely_producible(
      ()
    )
  )


def test_phase83_3_list_input_is_supported():
  data = build_phase83_3_data()

  assert (
    all_missing_premises_uniquely_producible(
      list(
        data[
          "lookups"
        ]
      )
    )
  )


def test_phase83_3_invalid_lookup_collection_is_rejected():
  with pytest.raises(
    TypeError,
    match=(
      "lookups must be a tuple/list of "
      "MissingPremiseProducerLookup"
    ),
  ):
    all_missing_premises_uniquely_producible(
      object()
    )


def test_phase83_3_invalid_lookup_item_is_rejected():
  with pytest.raises(
    TypeError,
    match=(
      "lookups must contain only "
      "MissingPremiseProducerLookup objects"
    ),
  ):
    all_missing_premises_uniquely_producible(
      (
        object(),
      )
    )

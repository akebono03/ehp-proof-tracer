from collections import (
  Counter,
  defaultdict,
)

from rule_catalog import (
  RuleRelevanceCategory,
)
from standard_production_applicability_catalog import (
  _inference_rule_factory_name,
  _phase103_6d76_apply_theorem_specific_classification,
  _phase103_6d76_original_builder,
)


PHASE103_6D76_TARGET_FAMILY = (
  "Toda Proposition 5.6 nu-prime order four"
)

PHASE103_6D76_TARGET_FACTORY = (
  "toda_prop56_nu_prime_order_four_inference_rule"
)


def _build_catalog():
  return (
    _phase103_6d76_apply_theorem_specific_classification(
      _phase103_6d76_original_builder()
    )
  )


def _families(
  catalog,
):
  result = defaultdict(
    list
  )

  for entry in catalog.entries():
    result[
      entry.rule.name
    ].append(
      entry
    )

  return {
    name: tuple(
      entries
    )
    for name, entries
    in result.items()
  }


def test_phase103_6d76_classifies_prop56_nu_prime_order_four_as_theorem_specific():
  catalog = _build_catalog()
  families = _families(
    catalog
  )

  assert PHASE103_6D76_TARGET_FAMILY in families

  entries = families[
    PHASE103_6D76_TARGET_FAMILY
  ]

  assert len(
    entries
  ) == 4

  assert all(
    entry.relevance_category
    is RuleRelevanceCategory.THEOREM_SPECIFIC
    for entry in entries
  )


def test_phase103_6d76_target_factory_is_exactly_the_audited_singleton():
  catalog = _build_catalog()

  entries = tuple(
    entry
    for entry in catalog.entries()
    if (
      entry.rule.name
      == PHASE103_6D76_TARGET_FAMILY
    )
  )

  assert len(
    entries
  ) == 4

  assert {
    _inference_rule_factory_name(
      entry.rule
    )
    for entry in entries
  } == {
    PHASE103_6D76_TARGET_FACTORY
  }


def test_phase103_6d76_changes_only_target_factory_entries():
  before = (
    _phase103_6d76_original_builder()
  )
  after = (
    _build_catalog()
  )

  before_by_key = {
    entry.key: entry
    for entry in before.entries()
  }
  after_by_key = {
    entry.key: entry
    for entry in after.entries()
  }

  assert (
    before_by_key.keys()
    == after_by_key.keys()
  )

  expected_changed = {
    key
    for key, entry in before_by_key.items()
    if (
      entry.relevance_category
      is RuleRelevanceCategory.UNCLASSIFIED
      and _inference_rule_factory_name(
        entry.rule
      )
      == PHASE103_6D76_TARGET_FACTORY
    )
  }

  assert len(
    expected_changed
  ) == 4

  actual_changed = set()

  for key, before_entry in before_by_key.items():
    after_entry = after_by_key[
      key
    ]

    if (
      before_entry.relevance_category
      is not after_entry.relevance_category
    ):
      actual_changed.add(
        key
      )

      assert (
        before_entry.relevance_category
        is RuleRelevanceCategory.UNCLASSIFIED
      )

      assert (
        after_entry.relevance_category
        is RuleRelevanceCategory.THEOREM_SPECIFIC
      )

  assert actual_changed == expected_changed


def test_phase103_6d76_target_cluster_is_closed():
  catalog = _build_catalog()

  entries = tuple(
    entry
    for entry in catalog.entries()
    if (
      _inference_rule_factory_name(
        entry.rule
      )
      == PHASE103_6D76_TARGET_FACTORY
    )
  )

  assert len(
    entries
  ) == 4

  assert all(
    entry.relevance_category
    is RuleRelevanceCategory.THEOREM_SPECIFIC
    for entry in entries
  )


def test_phase103_6d76_family_coverage_changes_by_exactly_one_family():
  before = (
    _phase103_6d76_original_builder()
  )
  after = (
    _build_catalog()
  )

  before_families = _families(
    before
  )
  after_families = _families(
    after
  )

  def classified_count(
    families,
  ):
    return sum(
      1
      for entries in families.values()
      if {
        entry.relevance_category
        for entry in entries
      }
      != {
        RuleRelevanceCategory.UNCLASSIFIED
      }
    )

  assert len(
    before_families
  ) == 267

  assert len(
    after_families
  ) == 267

  assert (
    classified_count(
      before_families
    )
    == 139
  )

  assert (
    classified_count(
      after_families
    )
    == 140
  )


def test_phase103_6d76_entry_coverage_delta_matches_four_target_entries():
  before = (
    _phase103_6d76_original_builder()
  )
  after = (
    _build_catalog()
  )

  before_entries = tuple(
    before.entries()
  )
  after_entries = tuple(
    after.entries()
  )

  before_counts = Counter(
    entry.relevance_category
    for entry in before_entries
  )

  after_counts = Counter(
    entry.relevance_category
    for entry in after_entries
  )

  assert len(
    before_entries
  ) == 1188
  assert len(
    after_entries
  ) == 1188

  assert (
    after_counts[
      RuleRelevanceCategory.UNCLASSIFIED
    ]
    == before_counts[
      RuleRelevanceCategory.UNCLASSIFIED
    ] - 4
  )

  assert (
    after_counts[
      RuleRelevanceCategory.THEOREM_SPECIFIC
    ]
    == before_counts[
      RuleRelevanceCategory.THEOREM_SPECIFIC
    ] + 4
  )

  assert (
    after_counts[
      RuleRelevanceCategory.UNCLASSIFIED
    ]
    == 369
  )

  assert (
    after_counts[
      RuleRelevanceCategory.THEOREM_SPECIFIC
    ]
    == 386
  )


def test_phase103_6d76_preserves_6d73_pi14_13_eta13_closure():
  catalog = _build_catalog()

  entries = tuple(
    entry
    for entry in catalog.entries()
    if (
      entry.rule.name
      == "Toda Proposition 5.11 pi_14^13 eta_13"
    )
  )

  assert entries

  assert all(
    entry.relevance_category
    is RuleRelevanceCategory.THEOREM_SPECIFIC
    for entry in entries
  )


def test_phase103_6d76_preserves_structural_and_map_property_counts():
  catalog = _build_catalog()

  counts = Counter(
    entry.relevance_category
    for entry in catalog.entries()
  )

  assert (
    counts[
      RuleRelevanceCategory.STRUCTURAL
    ]
    == 201
  )

  assert (
    counts[
      RuleRelevanceCategory.MAP_PROPERTY
    ]
    == 49
  )


def test_phase103_6d76_catalog_size_and_fixed_point_safety_are_unchanged():
  catalog = _build_catalog()
  entries = tuple(
    catalog.entries()
  )

  assert len(
    entries
  ) == 1188

  assert all(
    entry.fixed_point_safe
    is False
    for entry in entries
  )

from collections import (
  Counter,
  defaultdict,
)

from rule_catalog import (
  RuleRelevanceCategory,
)
from standard_production_applicability_catalog import (
  _inference_rule_factory_name,
  _phase103_6d73_apply_theorem_specific_classification,
  _phase103_6d73_original_builder,
)


PHASE103_6D73_TARGET_FAMILY = (
  "Toda Proposition 5.11 pi_14^13 eta_13"
)

PHASE103_6D73_TARGET_FACTORY = (
  "toda_prop511_pi14_13_eta13_inference_rule"
)


def _build_catalog():
  return (
    _phase103_6d73_apply_theorem_specific_classification(
      _phase103_6d73_original_builder()
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


def test_phase103_6d73_classifies_pi14_13_eta13_as_theorem_specific():
  catalog = _build_catalog()
  families = _families(
    catalog
  )

  assert PHASE103_6D73_TARGET_FAMILY in families

  entries = families[
    PHASE103_6D73_TARGET_FAMILY
  ]

  assert entries

  assert all(
    entry.relevance_category
    is RuleRelevanceCategory.THEOREM_SPECIFIC
    for entry in entries
  )


def test_phase103_6d73_target_factory_is_exactly_the_audited_singleton():
  catalog = _build_catalog()

  entries = tuple(
    entry
    for entry in catalog.entries()
    if (
      entry.rule.name
      == PHASE103_6D73_TARGET_FAMILY
    )
  )

  assert entries

  assert {
    _inference_rule_factory_name(
      entry.rule
    )
    for entry in entries
  } == {
    PHASE103_6D73_TARGET_FACTORY
  }


def test_phase103_6d73_changes_only_target_factory_entries():
  before = (
    _phase103_6d73_original_builder()
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
      == PHASE103_6D73_TARGET_FACTORY
    )
  }

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

  assert expected_changed
  assert actual_changed == expected_changed


def test_phase103_6d73_target_cluster_is_closed():
  catalog = _build_catalog()

  entries = tuple(
    entry
    for entry in catalog.entries()
    if (
      _inference_rule_factory_name(
        entry.rule
      )
      == PHASE103_6D73_TARGET_FACTORY
    )
  )

  assert entries

  assert all(
    entry.relevance_category
    is RuleRelevanceCategory.THEOREM_SPECIFIC
    for entry in entries
  )


def test_phase103_6d73_family_coverage_changes_by_exactly_one_family():
  before = (
    _phase103_6d73_original_builder()
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
      after_families
    )
    == classified_count(
      before_families
    ) + 1
  )


def test_phase103_6d73_entry_coverage_delta_matches_target_entry_count():
  before = (
    _phase103_6d73_original_builder()
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

  target_count = sum(
    1
    for entry in before_entries
    if (
      entry.relevance_category
      is RuleRelevanceCategory.UNCLASSIFIED
      and _inference_rule_factory_name(
        entry.rule
      )
      == PHASE103_6D73_TARGET_FACTORY
    )
  )

  assert target_count > 0

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
    ] - target_count
  )

  assert (
    after_counts[
      RuleRelevanceCategory.THEOREM_SPECIFIC
    ]
    == before_counts[
      RuleRelevanceCategory.THEOREM_SPECIFIC
    ] + target_count
  )


def test_phase103_6d73_preserves_6d71_eta_zero_relation_closure():
  catalog = _build_catalog()

  target_families = {
    "Toda Proposition 5.1 eta_4 order-two consequence",
    "Toda Lemma 5.4 eta_6 twice zero",
    "Toda Lemma 5.10 eta_8 two iota_9 zero",
    "Toda Lemma 5.10 eta_9 two iota_10 zero",
  }

  entries = tuple(
    entry
    for entry in catalog.entries()
    if (
      entry.rule.name
      in target_families
    )
  )

  assert entries

  assert all(
    entry.relevance_category
    is RuleRelevanceCategory.THEOREM_SPECIFIC
    for entry in entries
  )


def test_phase103_6d73_preserves_6d68_stable_range_transport_closure():
  catalog = _build_catalog()

  target_families = {
    "Toda Proposition 5.3 eta_4 squared stable transport",
    "Toda Proposition 5.6 nu_5 stable transport",
    "Toda Proposition 5.11 higher six-stem nu squared transport",
  }

  entries = tuple(
    entry
    for entry in catalog.entries()
    if (
      entry.rule.name
      in target_families
    )
  )

  assert entries

  assert all(
    entry.relevance_category
    is RuleRelevanceCategory.THEOREM_SPECIFIC
    for entry in entries
  )


def test_phase103_6d73_catalog_size_and_fixed_point_safety_are_unchanged():
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
